from features import *


def gap_score(candidate):

    gap = get_claim_evidence_gap(candidate)

    if gap <= 0:
        return 1.0

    elif gap <= 3:
        return 0.7

    elif gap <= 6:
        return 0.4

    else:
        return 0.1


def duration_score(candidate):

    avg_duration = get_avg_advanced_skill_duration(
        candidate
    )

    if avg_duration >= 36:
        return 1.0

    elif avg_duration >= 24:
        return 0.8

    elif avg_duration >= 12:
        return 0.5

    else:
        return 0.2


def assessment_score(candidate):

    avg_score = get_avg_assessment_score(
        candidate
    )

    if avg_score is None:
        return 0.5

    if avg_score >= 70:
        return 1.0

    elif avg_score >= 50:
        return 0.8

    elif avg_score >= 30:
        return 0.5

    else:
        return 0.2


def consistency_score(candidate):

    gap = gap_score(candidate)

    duration = duration_score(candidate)

    assessment = assessment_score(candidate)

    score = (
        0.60 * gap
        + 0.25 * assessment
        + 0.15 * duration
    )

    return round(score, 3)

if __name__ == "__main__":

    import json

    results = []

    with open("data/candidates.jsonl", "r") as f:

        for line in f:

            candidate = json.loads(line)

            score = consistency_score(candidate)

            results.append(
                (score, candidate)
            )

    results.sort(
        key=lambda x: x[0]
    )

    for score, candidate in results[:10]:

        print("\n====================")

        print(
            candidate["candidate_id"]
        )

        print(
            candidate["profile"][
                "current_title"
            ]
        )

        print(
            "Consistency:",
            score
        )

        print(
            extract_consistency_features(
                candidate
            )
        )