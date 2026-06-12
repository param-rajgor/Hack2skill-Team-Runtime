import math


def role_fit_score(
    jd_score,
    career_score,
    semantic_score
):
    """
    Measures how closely the candidate
    matches the actual role.
    """

    return (

        0.40 * jd_score +

        0.35 * career_score +

        0.25 * semantic_score

    )


def execution_score(
    experience_score,
    signal_score
):
    """
    Measures practical hireability.
    """

    return (

        0.70 * experience_score +

        0.30 * signal_score

    )


def recruiter_confidence_score(
    jd_score,
    career_score,
    semantic_score,
    consistency_score,
    experience_score,
    signal_score
):
    """
    Final ranking score.

    Uses geometric weighting so weak
    dimensions are punished instead of
    being hidden by averages.
    """

    role_fit = role_fit_score(
        jd_score,
        career_score,
        semantic_score
    )

    evidence = consistency_score

    execution = execution_score(
        experience_score,
        signal_score
    )

    epsilon = 1e-6

    confidence = (

        (role_fit + epsilon) ** 0.60

        *

        (evidence + epsilon) ** 0.25

        *

        (execution + epsilon) ** 0.15

    )

    return round(
        confidence,
        6
    )


def passes_filter(
    career_score,
    semantic_score,
    consistency_score
):
    """
    Stage 1 filtering.

    Removes obvious non-fits
    and likely honeypots.
    """

    if career_score < 0.20:
        return False

    if semantic_score < 0.20:
        return False

    if consistency_score < 0.20:
        return False

    return True