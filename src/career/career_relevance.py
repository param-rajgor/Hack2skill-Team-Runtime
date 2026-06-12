# src/career/career_relevance.py

from career_taxonomy import (
    SPECIALIST_AI_TITLES,
    HIGH_RELEVANCE_TITLES,
    MEDIUM_RELEVANCE_TITLES,
    LOW_RELEVANCE_TITLES,
    RELEVANT_DESCRIPTION_TERMS
)


def get_role_weight(index):
    """
    Recruiters care more about recent roles.

    Current Role  -> 1.0
    Previous Role -> 0.7
    Older Roles   -> 0.5
    """

    if index == 0:
        return 1.0

    elif index == 1:
        return 0.7

    return 0.5


def score_titles(career_history):

    score = 0
    max_score = 0

    for index, job in enumerate(career_history):

        weight = get_role_weight(index)

        title = job["title"].lower()

        role_score = 0

        # strongest signals

        if any(
            role in title
            for role in SPECIALIST_AI_TITLES
        ):
            role_score = 12

        # generic AI/ML roles

        elif any(
            role in title
            for role in HIGH_RELEVANCE_TITLES
        ):
            role_score = 10

        # adjacent engineering roles

        elif any(
            role in title
            for role in MEDIUM_RELEVANCE_TITLES
        ):
            role_score = 6

        # weakly related

        elif any(
            role in title
            for role in LOW_RELEVANCE_TITLES
        ):
            role_score = 3

        score += role_score * weight

        max_score += 12 * weight

    return score, max_score


def score_descriptions(career_history):

    score = 0
    max_score = 0

    for index, job in enumerate(career_history):

        weight = get_role_weight(index)

        description = job["description"].lower()

        matches = 0

        for term in RELEVANT_DESCRIPTION_TERMS:

            if term in description:
                matches += 1

        # cap to avoid extremely long descriptions
        matches = min(matches, 12)

        score += matches * weight

        max_score += 12 * weight

    return score, max_score


def calculate_career_relevance(candidate):

    career_history = candidate.get("career_history", [])

    if not career_history:
        return 0.0

    title_score, title_max = score_titles(
        career_history
    )

    description_score, description_max = (
        score_descriptions(career_history)
    )

    title_component = (
        title_score / title_max
        if title_max > 0
        else 0
    )

    description_component = (
        description_score / description_max
        if description_max > 0
        else 0
    )

    # Recruiters trust actual job titles slightly more
    # than self-written descriptions

    final_score = (

        0.65 * title_component +

        0.35 * description_component

    )

    return round(
        min(final_score, 1.0),
        4
    )