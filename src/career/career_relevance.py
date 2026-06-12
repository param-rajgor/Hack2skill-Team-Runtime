# src/career/career_relevance.py

from career_taxonomy import *

def score_titles(career_history):

    score = 0

    for job in career_history:

        title = job["title"].lower()

        if any(role in title for role in HIGH_RELEVANCE_TITLES):
            score += 10

        elif any(role in title for role in MEDIUM_RELEVANCE_TITLES):
            score += 6

        elif any(role in title for role in LOW_RELEVANCE_TITLES):
            score += 3

    return score

def score_descriptions(career_history):

    score = 0

    for job in career_history:

        description = job["description"].lower()

        for term in RELEVANT_DESCRIPTION_TERMS:

            if term in description:
                score += 1

    return score

def current_role_bonus(candidate):

    current_title = candidate["profile"]["current_title"].lower()

    if any(
        role in current_title
        for role in HIGH_RELEVANCE_TITLES
    ):
        return 5

    elif any(
        role in current_title
        for role in MEDIUM_RELEVANCE_TITLES
    ):
        return 3

    return 0

def calculate_career_relevance(candidate):

    career_history = candidate["career_history"]

    title_score = score_titles(career_history)

    description_score = score_descriptions(career_history)

    current_bonus = current_role_bonus(candidate)

    raw_score = (

        0.50 * title_score +

        0.30 * description_score +

        0.20 * current_bonus

    )

    max_possible = 25

    normalized = min(raw_score / max_possible, 1.0)

    return round(normalized, 4)