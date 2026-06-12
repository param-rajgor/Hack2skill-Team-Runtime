AI_SKILLS = [
    "llm",
    "rag",
    "embedding",
    "vector",
    "retrieval",
    "search",
    "transformer",
    "faiss",
    "pinecone",
    "recommendation",
    "nlp"
]

AI_EVIDENCE = [
    "ai",
    "ml",
    "machine learning",
    "nlp",
    "search",
    "retrieval",
    "ranking",
    "recommendation",
    "embedding",
    "llm",
    "transformer"
]


def get_claim_score(candidate):
    """
    Count AI-related skill claims.
    """

    claim_score = 0

    for skill in candidate["skills"]:

        skill_name = skill["name"].lower()

        if any(
            keyword in skill_name
            for keyword in AI_SKILLS
        ):
            claim_score += 1

    return claim_score


def get_evidence_score(candidate):
    """
    Count AI-related evidence found in
    career titles and descriptions.
    """

    evidence_score = 0

    for job in candidate["career_history"]:

        text = (
            job["title"] + " " +
            job["description"]
        ).lower()

        for keyword in AI_EVIDENCE:

            if keyword in text:
                evidence_score += 1

    return evidence_score


def get_claim_evidence_gap(candidate):
    """
    Positive gap means claims exceed evidence.
    Negative gap means evidence exceeds claims.
    """

    claim_score = get_claim_score(candidate)

    evidence_score = get_evidence_score(candidate)

    return claim_score - evidence_score


def get_advanced_skill_count(candidate):
    """
    Count advanced-level skills.
    """

    count = 0

    for skill in candidate["skills"]:

        if skill["proficiency"] == "advanced":
            count += 1

    return count


def get_avg_advanced_skill_duration(candidate):
    """
    Average duration (months)
    of advanced skills.
    """

    durations = []

    for skill in candidate["skills"]:

        if skill["proficiency"] == "advanced":

            durations.append(
                skill["duration_months"]
            )

    if len(durations) == 0:
        return 0

    return sum(durations) / len(durations)


def get_avg_assessment_score(candidate):
    """
    Average assessment score.
    Returns None if unavailable.
    """

    scores = candidate["redrob_signals"][
        "skill_assessment_scores"
    ]

    if not scores:
        return None

    return (
        sum(scores.values())
        / len(scores)
    )


def get_assessment_count(candidate):
    """
    Number of assessment scores available.
    """

    scores = candidate["redrob_signals"][
        "skill_assessment_scores"
    ]

    return len(scores)


def extract_consistency_features(candidate):
    """
    Convenience function.
    Returns all consistency features together.
    """

    return {
        "claim_score":
            get_claim_score(candidate),

        "evidence_score":
            get_evidence_score(candidate),

        "claim_evidence_gap":
            get_claim_evidence_gap(candidate),

        "advanced_skill_count":
            get_advanced_skill_count(candidate),

        "avg_advanced_skill_duration":
            get_avg_advanced_skill_duration(candidate),

        "avg_assessment_score":
            get_avg_assessment_score(candidate),

        "assessment_count":
            get_assessment_count(candidate)
    }