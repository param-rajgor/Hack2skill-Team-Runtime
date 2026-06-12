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

    candidate_skills = (
        normalize_skills(
            candidate["skills"]
        )
    )

    required_matches = []

    for skill in required_skills:

        if skill.lower() in candidate_skills:

            required_matches.append(
                skill
            )

    preferred_matches = []

    for skill in preferred_skills:

        if skill.lower() in candidate_skills:

            preferred_matches.append(
                skill
            )

    required_score = (

        len(required_matches)

        /

        len(required_skills)

    )

    preferred_score = (

        len(preferred_matches)

        /

        len(preferred_skills)

    )

    final_score = (

        0.8 * required_score

        +

        0.2 * preferred_score

    ) * 100

    return {

        "score":
        round(
            final_score,
            2
        ),

        "required_matches":
        required_matches,

        "preferred_matches":
        preferred_matches

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