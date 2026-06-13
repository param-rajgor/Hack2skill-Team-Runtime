# src/ranking/recruiter_confidence.py

import os
import sys

# Resolve absolute paths and append src subdirectories to sys.path
SRC_DIR = os.path.abspath("src")
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)


def calculate_role_fit(career_score: float, semantic_score: float, jd_score: float) -> float:
    """
    Measures: Can this candidate actually do retrieval/search/ranking/recommendation work?
    Formula: 0.40 * career_score + 0.35 * semantic_score + 0.25 * jd_score
    """
    return 0.40 * career_score + 0.35 * semantic_score + 0.25 * jd_score


def calculate_evidence_score(consistency_score: float) -> float:
    """
    Measures: Do I believe this profile?
    Formula: consistency_score
    """
    return consistency_score


def calculate_execution_score(experience_score: float, signal_score: float) -> float:
    """
    Measures: Can we realistically hire and onboard this candidate?
    Formula: 0.85 * experience_score + 0.15 * signal_score
    """
    return 0.85 * experience_score + 0.15 * signal_score


def is_suspicious_candidate(candidate: dict) -> bool:
    """
    Flags candidates who claim advanced AI/ML skills with zero evidence,
    or have extremely low assessments, or claim many advanced skills with short durations.
    """
    from consistency.features import (
        get_claim_score, get_evidence_score, get_avg_assessment_score,
        get_avg_advanced_skill_duration, get_advanced_skill_count
    )
    claims = get_claim_score(candidate)
    evidence = get_evidence_score(candidate)
    avg_assess = get_avg_assessment_score(candidate)
    avg_dur = get_avg_advanced_skill_duration(candidate)
    adv_count = get_advanced_skill_count(candidate)
    
    # 1. Claims AI skills but has no career history evidence
    if claims >= 3 and evidence == 0:
        return True
        
    # 2. Claims advanced skills but has low average assessment score
    if avg_assess is not None and avg_assess < 45.0 and adv_count >= 1:
        return True
        
    # 3. Claims many advanced skills with short average duration
    if adv_count >= 4 and 0 < avg_dur < 12.0:
        return True
        
    return False


def is_authentic_candidate(candidate: dict) -> bool:
    """
    Flags candidates whose career history aligns well with claims and have high assessments.
    """
    from consistency.features import get_claim_evidence_gap, get_avg_assessment_score
    gap = get_claim_evidence_gap(candidate)
    avg_assess = get_avg_assessment_score(candidate)
    
    if gap <= 0 and avg_assess is not None and avg_assess >= 75.0:
        return True
    return False


def is_hidden_talent(candidate: dict) -> bool:
    """
    Flags candidates with exceptional assessment scores (top tier),
    even if their career background is unconventional.
    """
    from consistency.features import get_avg_assessment_score
    avg_assess = get_avg_assessment_score(candidate)
    if avg_assess is not None and avg_assess >= 80.0:
        return True
    return False


def is_service_only_career(candidate: dict) -> bool:
    """
    Flags candidates who have worked solely in service-based consulting companies
    with no product exposure.
    """
    career_history = candidate.get("career_history", []) or []
    if not career_history:
        return False
        
    service_only = True
    for job in career_history:
        company = str(job.get("company", "")).strip().lower()
        industry = str(job.get("industry", "")).strip().lower()
        
        is_service_company = any(s in company for s in [
            "tcs", "tata consultancy", "infosys", "wipro", "cognizant", 
            "capgemini", "accenture", "hcl", "tech mahindra", "mindtree", 
            "l&t", "ltts", "lti", "hexaware", "mphasis", "ust global"
        ])
        is_service_industry = any(ind in industry for ind in [
            "it services", "consulting", "services", "system integration"
        ])
        
        if not (is_service_company or is_service_industry):
            service_only = False
            break
            
    return service_only


def calculate_recruiter_confidence(role_fit: float, evidence_score: float, execution_score: float, candidate: dict = None) -> float:
    """
    Measures overall candidate confidence using a weighted geometric mean with pattern modifiers.
    Formula: role_fit ** 0.60 * evidence_score ** 0.25 * execution_score ** 0.15
    """
    # Clip values to be non-negative to avoid complex math errors
    rf = max(0.0, role_fit)
    ev = max(0.0, evidence_score)
    ex = max(0.0, execution_score)
    
    # Apply pattern modifiers
    if candidate is not None:
        if is_authentic_candidate(candidate):
            rf = min(1.0, rf + 0.05)
            ev = min(1.0, ev + 0.05)
            
        if is_hidden_talent(candidate):
            ex = min(1.0, ex + 0.10)

    confidence = (rf ** 0.60) * (ev ** 0.25) * (ex ** 0.15)
    
    if candidate is not None:
        if is_suspicious_candidate(candidate):
            confidence *= 0.6
            
        if is_service_only_career(candidate):
            confidence *= 0.8
            
    return round(confidence, 4)


def is_honeypot_candidate(candidate: dict) -> bool:
    """
    Scans candidate profile for logical impossibilities.
    Returns True if the profile is a honeypot candidate.
    """
    from datetime import datetime
    
    profile = candidate.get("profile", {}) or {}
    years_exp = profile.get("years_of_experience", 0)
    career = candidate.get("career_history", []) or []
    skills = candidate.get("skills", []) or []
    education = candidate.get("education", []) or []
    
    # Check 1: expert proficiency in 10 skills with 0 duration (allowing 8 as a threshold)
    expert_zero_dur = sum(
        1 for s in skills 
        if s.get("proficiency") == "expert" and s.get("duration_months", 0) == 0
    )
    if expert_zero_dur >= 8:
        return True

    # Check 2: Total years of experience is less than a single job duration
    for job in career:
        dur_months = job.get("duration_months", 0)
        dur_years = dur_months / 12.0
        if dur_years > years_exp + 0.1:
            return True

    # Check 3: Job end date is before start date
    for job in career:
        start_str = job.get("start_date")
        end_str = job.get("end_date")
        if start_str and end_str:
            try:
                start = datetime.strptime(start_str, "%Y-%m-%d")
                end = datetime.strptime(end_str, "%Y-%m-%d")
                if end < start:
                    return True
            except:
                pass

    # Check 4: Job duration exceeds date span by a lot (more than 12 months)
    for job in career:
        start_str = job.get("start_date")
        end_str = job.get("end_date")
        dur = job.get("duration_months", 0)
        if start_str and end_str and dur:
            try:
                start = datetime.strptime(start_str, "%Y-%m-%d")
                end = datetime.strptime(end_str, "%Y-%m-%d")
                span_months = (end.year - start.year) * 12 + (end.month - start.month)
                if dur > span_months + 12:
                    return True
            except:
                pass

    # Check 5: Experience exceeds years since earliest school
    if education:
        start_years = [e.get("start_year") for e in education if e.get("start_year")]
        if start_years:
            earliest_school = min(start_years)
            years_since_school = 2026 - earliest_school
            if years_exp > years_since_school + 3 and earliest_school > 2000:
                return True

    # Check 6: Sum of job durations has a massive discrepancy with years_of_experience
    total_job_months = sum(job.get("duration_months", 0) for job in career)
    total_job_years = total_job_months / 12.0
    if abs(years_exp - total_job_years) > 10.0:
        return True

    return False
