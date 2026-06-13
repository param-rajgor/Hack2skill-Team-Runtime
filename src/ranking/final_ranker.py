# src/ranking/final_ranker.py

import os
import sys
import json
import csv
import time

# Resolve absolute paths and append src subdirectories to sys.path
SRC_DIR = os.path.abspath("src")
sys.path.append(SRC_DIR)
sys.path.append(os.path.join(SRC_DIR, "career"))
sys.path.append(os.path.join(SRC_DIR, "consistency"))
sys.path.append(os.path.join(SRC_DIR, "jd"))
sys.path.append(os.path.join(SRC_DIR, "scoring"))
sys.path.append(os.path.join(SRC_DIR, "semantic"))
sys.path.append(os.path.join(SRC_DIR, "signals"))
sys.path.append(os.path.join(SRC_DIR, "ranking"))

# Imports from existing modules
from career.career_relevance import calculate_career_relevance
from career.experience_score import calculate_experience_score
from consistency.scorer import consistency_score
from semantic.semantic_score import semantic_score
from signals.signal_score import signal_score
from scoring.jd_match_score import calculate_score
from jd.jd_loader import load_jd
from jd.jd_parser import parse_jd

# Imports from our new modules
from recruiter_confidence import (
    calculate_role_fit,
    calculate_evidence_score,
    calculate_execution_score,
    calculate_recruiter_confidence,
    is_hidden_talent,
    is_honeypot_candidate
)
from reasoning_generator import generate_reasoning


def process_candidate(candidate, required_skills, preferred_skills, apply_filters=True):
    """
    Processes a single candidate, applying Stage 1 filters if requested.
    Returns (scored_dict, passed_filters) where passed_filters is True if candidate passed all filters.
    """
    # Reject honeypot candidates immediately under all circumstances
    if is_honeypot_candidate(candidate):
        return None, False

    # Check if candidate is a Hidden Talent (outstanding assessment score >= 80%)
    hidden_talent = is_hidden_talent(candidate)

    # Stage 1 - Candidate Filtering
    # Compute Career Relevance (fast)
    career_score = calculate_career_relevance(candidate)
    if apply_filters and not hidden_talent and career_score < 0.25:
        return None, False

    # Compute Consistency Score (fast)
    consistency_score_val = consistency_score(candidate)
    if apply_filters and consistency_score_val < 0.25:
        return None, False

    # Compute Semantic Score (moderate, string search / regex)
    semantic_score_val = semantic_score(candidate)
    if apply_filters and not hidden_talent and semantic_score_val < 0.25:
        return None, False

    # Stage 2 - Recruiter Dimensions
    # Compute the remaining scores
    jd_res = calculate_score(candidate, required_skills, preferred_skills)
    jd_score_val = jd_res["score"]
    
    experience_score_val = calculate_experience_score(candidate)
    
    sig_res = signal_score(candidate)
    signal_score_val = sig_res["signal_score"]

    # Recruiter Dimensions formulas
    role_fit = calculate_role_fit(career_score, semantic_score_val, jd_score_val)
    evidence_score_val = calculate_evidence_score(consistency_score_val)
    execution_score_val = calculate_execution_score(experience_score_val, signal_score_val)

    # Stage 3 - Recruiter Confidence Score
    confidence = calculate_recruiter_confidence(role_fit, evidence_score_val, execution_score_val, candidate)

    candidate_id = candidate.get("candidate_id")

    return {
        "candidate_id": candidate_id,
        "score": confidence,
        "candidate": candidate,
        "consistency_score": consistency_score_val,
        "career_score": career_score,
        "semantic_score": semantic_score_val,
        "jd_score": jd_score_val,
        "experience_score": experience_score_val,
        "signal_score": signal_score_val
    }, True


def run_ranking_pipeline():
    start_time = time.time()
    print("Initializing ranking pipeline...")

    # Load Job Description
    jd_path = "data/job_description.docx"
    if not os.path.exists(jd_path):
        raise FileNotFoundError(f"Job Description file not found at {jd_path}")

    jd_text = load_jd(jd_path)
    parsed_jd = parse_jd(jd_text)
    required_skills = parsed_jd["required_skills"]
    preferred_skills = parsed_jd["preferred_skills"]

    print(f"Loaded JD. Required skills: {len(required_skills)}, Preferred skills: {len(preferred_skills)}")

    candidates_path = "data/candidates.jsonl"
    if not os.path.exists(candidates_path):
        raise FileNotFoundError(f"Candidates file not found at {candidates_path}")

    passed_candidates = []
    total_processed = 0

    print("Processing candidates with lazy filters...")
    with open(candidates_path, "r", encoding="utf-8") as f:
        for line in f:
            candidate = json.loads(line)
            total_processed += 1
            
            # Apply processing and Stage 1 filtering
            res, passed = process_candidate(candidate, required_skills, preferred_skills, apply_filters=True)
            if passed:
                passed_candidates.append(res)
            
            # Print progress indicator
            if total_processed % 10000 == 0:
                print(f"Processed {total_processed} candidates... (Passed filters: {len(passed_candidates)})")

    print(f"Finished parsing. Total candidates processed: {total_processed}")
    print(f"Candidates passing Stage 1 filter: {len(passed_candidates)}")

    # Fallback Mechanism:
    # If less than 100 candidates passed the strict filters, run a relaxed check to fill the list.
    if len(passed_candidates) < 100:
        print("[WARNING] Fewer than 100 candidates passed Stage 1 filtering. Falling back to relaxed filtering...")
        passed_ids = {c["candidate_id"] for c in passed_candidates}
        
        # We process all candidates again without filtering, storing their candidate_id and score
        with open(candidates_path, "r", encoding="utf-8") as f:
            for line in f:
                candidate = json.loads(line)
                candidate_id = candidate.get("candidate_id")
                if candidate_id in passed_ids:
                    continue
                
                # Process without filter
                res, _ = process_candidate(candidate, required_skills, preferred_skills, apply_filters=False)
                passed_candidates.append(res)
                if len(passed_candidates) >= 100:
                    break

    # Sort candidates: confidence DESC, candidate_id ASC (deterministic tie-breaker)
    print("Sorting candidates and selecting Top 100...")
    passed_candidates.sort(key=lambda x: (-x["score"], x["candidate_id"]))

    top_100 = passed_candidates[:100]

    # Generate outputs directory if it does not exist
    os.makedirs("outputs", exist_ok=True)
    output_file = "outputs/final_submission.csv"

    print(f"Generating candidate reasoning and writing to {output_file}...")
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Write headers
        writer.writerow(["candidate_id", "rank", "score", "reasoning"])
        
        for rank, item in enumerate(top_100, 1):
            candidate = item["candidate"]
            candidate_id = item["candidate_id"]
            score = item["score"]
            consistency_score_val = item["consistency_score"]
            
            # Generate customized, non-template, fact-based reasoning
            reasoning = generate_reasoning(candidate, consistency_score_val)
            
            # Format score to 4 decimal places as in the submission format
            formatted_score = f"{score:.4f}"
            
            writer.writerow([candidate_id, rank, formatted_score, reasoning])

    elapsed = time.time() - start_time
    print(f"Ranking pipeline executed successfully in {elapsed:.2f} seconds.")
    print(f"Final output written to: {output_file}")


if __name__ == "__main__":
    run_ranking_pipeline()