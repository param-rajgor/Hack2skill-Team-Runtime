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
    Recruitability / engagement score.

    Strong signals:
    - profile completeness
    - GitHub activity
    - interview completion
    - recruiter response rate

    Weak signals:
    - verified email
    - verified phone
    - LinkedIn connected
    """
    s = _signals(candidate)

    score = 0.0

    score += _normalize(s.get("profile_completeness_score", 0), 100.0) * 0.30
    score += _normalize(s.get("github_activity_score", 0), 10.0) * 0.25
    score += _normalize(s.get("interview_completion_rate", 0), 1.0) * 0.25
    score += _normalize(s.get("recruiter_response_rate", 0), 1.0) * 0.12
    score += _normalize(s.get("saved_by_recruiters_30d", 0), 10.0) * 0.05
    score += _normalize(s.get("profile_views_received_30d", 0), 250.0) * 0.02

    if s.get("open_to_work_flag", False):
        score += 3.0

    if s.get("verified_email", False):
        score += 1.0

    if s.get("verified_phone", False):
        score += 1.0

    if s.get("linkedin_connected", False):
        score += 0.5

    applications = _num(s.get("applications_submitted_30d", 0))
    if applications > 0:
        score += min(applications, 10.0) * 0.1

    return round(_clamp(score), 2)


def logistics_score(candidate: Dict[str, Any]) -> float:
    """
    Hireability / logistics score.

    Focuses on:
    - notice period
    - willingness to relocate
    - location fit
    - preferred work mode
    """
    s = _signals(candidate)
    p = _profile(candidate)

    score = 100.0

    notice = _num(s.get("notice_period_days", 0))
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

    if s.get("willing_to_relocate", False):
        score += 8.0
    else:
        score -= 6.0

    country = str(p.get("country", "") or "").strip().lower()
    if country == "india":
        score += 3.0

    work_mode = str(s.get("preferred_work_mode", "") or "").strip().lower()
    if work_mode in {"onsite", "hybrid"}:
        score += 2.0
    elif work_mode == "remote":
        score -= 2.0

    salary_range = s.get("expected_salary_range_inr_lpa", {}) or {}
    min_salary = _num(salary_range.get("min", 0))
    if 0 < min_salary <= 10:
        score += 1.0
    elif min_salary >= 50:
        score -= 2.0

    return round(_clamp(score), 2)


def signal_score(candidate: Dict[str, Any]) -> Dict[str, float]:
    """
    Convenience wrapper for downstream integration.
    Returns both sub-scores plus a blended helper score.
    """
    behavior = behavior_score(candidate)
    logistics = logistics_score(candidate)

    blended = round(0.75 * behavior + 0.25 * logistics, 2)

    return {
        "behavior_score": behavior,
        "logistics_score": logistics,
        "signal_score": blended,
    }