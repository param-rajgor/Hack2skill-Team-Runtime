import json
import sys
import os

sys.path.append(
    os.path.abspath("src")
)

sys.path.append(
    os.path.abspath("src/jd")
)

from jd_loader import load_jd
from jd_parser import parse_jd
from skill_mapper import SKILL_MAP


def load_candidates():

    candidates = []

    with open(
        "data/candidates.jsonl",
        "r",
        encoding="utf-8"
    ) as f:

        for line in f:

            candidates.append(
                json.loads(line)
            )

    return candidates


def normalize_skills(skills):

    normalized = set()

    for skill in skills:

        skill_name = (
            skill["name"]
            .lower()
            .strip()
        )

        normalized.add(
            skill_name
        )

        if skill_name in SKILL_MAP:

            normalized.add(
                SKILL_MAP[
                    skill_name
                ]
            )

    return normalized

def calculate_score(
    candidate,
    required_skills,
    preferred_skills
):

    candidate_skills = normalize_skills(
        candidate["skills"]
    )

    required_matches = []
    preferred_matches = []

    SKILL_WEIGHTS = {

    "retrieval": 4,

    "ranking": 4,

    "vector database": 4,

    "evaluation": 4,

    "python": 2,

    "backend": 2,

    "cloud": 2,

    "llm": 1,

    "fine-tuning": 1,

    "rag": 1
}

    required_match_weight = 0
    total_required_weight = 0

    for skill in required_skills:

        weight = SKILL_WEIGHTS.get(
            skill.lower(),
            1
        )

        total_required_weight += weight

        if skill.lower() in candidate_skills:

            required_matches.append(
                skill
            )

            required_match_weight += weight

    preferred_match_weight = 0
    total_preferred_weight = 0

    for skill in preferred_skills:

        weight = SKILL_WEIGHTS.get(
            skill.lower(),
            1
        )

        total_preferred_weight += weight

        if skill.lower() in candidate_skills:

            preferred_matches.append(
                skill
            )

            preferred_match_weight += weight

    required_score = 0

    if total_required_weight > 0:

        required_score = (

            required_match_weight

            /

            total_required_weight

        )

    preferred_score = 0

    if total_preferred_weight > 0:

        preferred_score = (

            preferred_match_weight

            /

            total_preferred_weight

        )

    final_score = (

        0.8 * required_score

        +

        0.2 * preferred_score

    )

    return {

    "score": round(final_score, 4),

    "required_matches": required_matches,

    "preferred_matches": preferred_matches,

    "required_match_count": len(required_matches),

    "preferred_match_count": len(preferred_matches),

    "required_score": round(required_score, 4),

    "preferred_score": round(preferred_score, 4)
}


if __name__ == "__main__":

    jd = load_jd(
        "data/job_description.docx"
    )

    parsed = parse_jd(jd)

    candidates = (
        load_candidates()
    )

    print(
        "\nTOP 10 CANDIDATES\n"
    )

    for candidate in candidates[:10]:

        result = calculate_score(

            candidate,

            parsed[
                "required_skills"
            ],

            parsed[
                "preferred_skills"
            ]

        )

        print(
            "\nCandidate:",
            candidate[
                "candidate_id"
            ]
        )

        print(
            "Score:",
            result[
                "score"
            ]
        )

        print(
            "Required Matches:",
            result[
                "required_matches"
            ]
        )

        print(
            "Preferred Matches:",
            result[
                "preferred_matches"
            ]
        )