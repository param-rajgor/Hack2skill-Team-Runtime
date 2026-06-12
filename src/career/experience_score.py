# src/career/experience_score.py

def calculate_experience_score(candidate):
    """
    Returns a score between 0 and 1 based on how closely
    a candidate's experience aligns with the ideal JD range.

    Ideal range:
    5–9 years

    Peak score = 1.0 inside the ideal range.
    Score gradually decreases as we move away.
    """

    years = candidate["profile"]["years_of_experience"]

    # Ideal range
    if 5 <= years <= 9:
        return 1.0

    # Less experienced candidates
    elif years < 5:

        gap = 5 - years

        score = 1.0 - (gap * 0.15)

        return max(score, 0.2)

    # More experienced candidates
    else:

        gap = years - 9

        score = 1.0 - (gap * 0.05)

        return max(score, 0.5)