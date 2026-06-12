import json
import sys
import os
from collections import defaultdict

sys.path.append(os.path.abspath("src"))
sys.path.append(os.path.abspath("src/jd"))

from jd_loader import load_jd
from jd_parser import parse_jd
from skill_mapper import SKILL_MAP


# -----------------------------
# WEIGHTED SKILL IMPORTANCE
# -----------------------------

SKILL_WEIGHTS = {

    # Core Retrieval / Ranking (VERY HIGH SIGNAL)
    "retrieval": 3.0,
    "ranking": 3.0,
    "semantic search": 2.8,
    "recommendation systems": 2.8,
    "vector search": 2.5,

    # LLM / NLP layer (HIGH but secondary)
    "nlp": 2.0,
    "llm": 2.0,
    "embeddings": 2.2,

    # Fine tuning (medium relevance)
    "fine-tuning": 1.6,

    # Evaluation (medium-low but important)
    "evaluation": 1.4,

    # Backend / infra (supporting signal)
    "backend": 1.0,
    "feature engineering": 1.0,
    "cloud": 0.8,
}


def load_candidates():
    candidates = []
    with open("data/candidates.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            candidates.append(json.loads(line))
    return candidates


def normalize_skills(skills):
    normalized = set()

    for skill in skills:
        name = skill["name"].lower().strip()
        normalized.add(name)

        if name in SKILL_MAP:
            normalized.add(SKILL_MAP[name])

    return normalized


def get_skill_weight(skill: str) -> float:
    return SKILL_WEIGHTS.get(skill.lower(), 0.5)


def calculate_score(candidate, required_skills, preferred_skills):

    candidate_skills = normalize_skills(candidate["skills"])

    # -----------------------------
    # REQUIRED SKILL SCORE
    # -----------------------------
    required_score = 0.0
    required_total_weight = 0.0

    for skill in required_skills:

        s = skill.lower().strip()
        weight = get_skill_weight(s)
        required_total_weight += weight

        if s in candidate_skills:
            required_score += weight

    required_ratio = (
        required_score / required_total_weight
        if required_total_weight > 0 else 0
    )

    # -----------------------------
    # PREFERRED SKILL SCORE
    # -----------------------------
    preferred_score = 0.0
    preferred_total_weight = 0.0

    for skill in preferred_skills:

        s = skill.lower().strip()
        weight = get_skill_weight(s) * 0.6  # preferred reduced impact
        preferred_total_weight += weight

        if s in candidate_skills:
            preferred_score += weight

    preferred_ratio = (
        preferred_score / preferred_total_weight
        if preferred_total_weight > 0 else 0
    )

    # -----------------------------
    # FINAL SCORE (0 → 1)
    # -----------------------------
    final_score = (
        0.75 * required_ratio +
        0.25 * preferred_ratio
    )

    return {
        "score": round(final_score, 4),
        "required_score": round(required_ratio, 4),
        "preferred_score": round(preferred_ratio, 4),
        "matched_skills": list(candidate_skills)
    }


# -----------------------------
# TEST RUN
# -----------------------------
if __name__ == "__main__":

    jd = load_jd("data/job_description.docx")
    parsed = parse_jd(jd)
    candidates = load_candidates()

    print("\nTOP 10 CANDIDATES (JD MATCH)\n")

    for c in candidates[:10]:

        result = calculate_score(
            c,
            parsed["required_skills"],
            parsed["preferred_skills"]
        )

        print("\nCandidate:", c["candidate_id"])
        print("Score:", result["score"])
        print("Required:", result["required_score"])
        print("Preferred:", result["preferred_score"])