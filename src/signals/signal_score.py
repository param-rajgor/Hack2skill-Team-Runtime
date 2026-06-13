from __future__ import annotations

from typing import Any, Dict


def _signals(candidate: Dict[str, Any]) -> Dict[str, Any]:
    return candidate.get("redrob_signals", {}) or {}


def _profile(candidate: Dict[str, Any]) -> Dict[str, Any]:
    return candidate.get("profile", {}) or {}


def _num(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return float(default)
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _normalize(value: Any, max_value: float) -> float:
    if max_value <= 0:
        return 0.0
    return _clamp((_num(value) / max_value) * 100.0)


def behavior_score(candidate: Dict[str, Any]) -> float:
    """
    Output:
        0.0 -> 1.0
    """

    s = _signals(candidate)

    score = 0.0

    # 1. High Importance (60% total weight)
    # Profile Completeness Score (15%)
    score += _normalize(
        s.get("profile_completeness_score", 0),
        100.0
    ) * 0.15

    # GitHub Activity Score (15%) - Handle -1 as 0
    github_val = s.get("github_activity_score", 0)
    if github_val == -1:
        github_val = 0.0
    score += _normalize(
        github_val,
        100.0
    ) * 0.15

    # Interview Completion Rate (15%)
    score += _normalize(
        s.get("interview_completion_rate", 0),
        1.0
    ) * 0.15

    # Skill Assessment Scores (15%) - Impute with 52.92 if missing
    sa_scores = s.get("skill_assessment_scores", {})
    if not sa_scores:
        avg_assess = 52.92
    else:
        avg_assess = sum(sa_scores.values()) / len(sa_scores)
    score += _normalize(
        avg_assess,
        100.0
    ) * 0.15

    # 2. Medium Importance (25% total weight)
    # Offer Acceptance Rate (8%) - Impute -1 with 0.47
    offer_acc = s.get("offer_acceptance_rate", -1)
    if offer_acc == -1:
        offer_acc = 0.47
    score += _normalize(
        offer_acc,
        1.0
    ) * 0.08

    # Recruiter Response Rate (9%)
    score += _normalize(
        s.get("recruiter_response_rate", 0),
        1.0
    ) * 0.09

    # Saved by Recruiters (30d) (8%) - Normalized by 20.0
    score += _normalize(
        s.get("saved_by_recruiters_30d", 0),
        20.0
    ) * 0.08

    # 3. Low Importance (10% total weight)
    # Open to Work Flag (3%)
    if s.get("open_to_work_flag", False):
        score += 3.0

    # Search Appearance (30d) (4%) - Normalized by 300.0
    score += _normalize(
        s.get("search_appearance_30d", 0),
        300.0
    ) * 0.04

    # Profile Views (30d) (3%) - Normalized by 150.0
    score += _normalize(
        s.get("profile_views_received_30d", 0),
        150.0
    ) * 0.03

    # 4. Very Low Importance (5% total weight)
    # Verified Email (2%)
    if s.get("verified_email", False):
        score += 2.0

    # Verified Phone (2%)
    if s.get("verified_phone", False):
        score += 2.0

    # LinkedIn Connected (1%)
    if s.get("linkedin_connected", False):
        score += 1.0

    return round(_clamp(score) / 100.0, 4)


def logistics_score(candidate: Dict[str, Any]) -> float:
    """
    Output:
        0.0 -> 1.0
    """

    s = _signals(candidate)
    p = _profile(candidate)

    score = 100.0

    notice = _num(
        s.get("notice_period_days", 0)
    )

    if notice > 180:
        score -= 25.0
    elif notice > 120:
        score -= 18.0
    elif notice > 90:
        score -= 12.0
    elif notice > 60:
        score -= 6.0
    elif notice > 30:
        score -= 2.0

    # Relocation & Location Matching
    location = str(p.get("location", "") or "").strip().lower()
    country = str(p.get("country", "") or "").strip().lower()

    is_in_preferred_city = "noida" in location or "pune" in location
    is_in_india = "india" in country or "india" in location

    willing_to_relocate = s.get("willing_to_relocate", False)

    if is_in_preferred_city:
        score += 10.0
    elif is_in_india:
        if willing_to_relocate:
            score += 5.0
        else:
            score -= 10.0
    else:
        # Outside India
        if willing_to_relocate:
            score += 2.0
        else:
            score -= 20.0

    # Work mode preference
    work_mode = str(
        s.get("preferred_work_mode", "") or ""
    ).strip().lower()

    if work_mode in {"onsite", "hybrid"}:
        score += 2.0

    elif work_mode == "remote":
        score -= 2.0

    salary_range = (
        s.get("expected_salary_range_inr_lpa", {})
        or {}
    )

    min_salary = _num(
        salary_range.get("min", 0)
    )

    if 0 < min_salary <= 10:
        score += 1.0

    elif min_salary >= 50:
        score -= 2.0

    return round(_clamp(score) / 100.0, 4)


def signal_score(candidate: Dict[str, Any]) -> Dict[str, float]:
    """
    Returns normalized scores.

    Output:
        0.0 -> 1.0
    """

    behavior = behavior_score(candidate)
    logistics = logistics_score(candidate)

    blended = round(
        (0.8 * behavior) +
        (0.2 * logistics), 4
    )

    return {
        "behavior_score": behavior,
        "logistics_score": logistics,
        "signal_score": blended,
    }