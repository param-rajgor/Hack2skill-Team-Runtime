from __future__ import annotations

import re
from typing import Dict, Any

SEMANTIC_GROUPS = {
    "retrieval": {
        "weight": 24,
        "keywords": [
            "retrieval systems",
            "retrieval",
            "semantic search",
            "vector search",
            "information retrieval",
            "search infrastructure",
        ],
    },
    "ranking": {
        "weight": 24,
        "keywords": [
            "ranking systems",
            "ranking",
            "re-ranking",
            "reranking",
            "recommendation systems",
            "recommendation engine",
            "recommendation",
            "recommender",
            "learning to rank",
        ],
    },
    "production_ml": {
        "weight": 18,
        "keywords": [
            "production ml",
            "model serving",
            "deployed",
            "shipped",
            "launched",
            "latency",
            "monitoring",
            "scalable",
            "pipelines",
            "feature pipelines",
            "inference",
            "api",
        ],
    },
    "nlp_llm": {
        "weight": 14,
        "keywords": [
            "nlp",
            "natural language processing",
            "llm",
            "large language model",
            "transformers",
            "embeddings",
            "fine-tuning",
            "finetuning",
            "language model",
        ],
    },
    "evaluation": {
        "weight": 10,
        "keywords": [
            "evaluation",
            "ndcg",
            "mrr",
            "map",
            "ab testing",
            "a/b testing",
            "benchmark",
            "metrics",
        ],
    },
    "data_backend": {
        "weight": 10,
        "keywords": [
            "data pipelines",
            "feature engineering",
            "airflow",
            "spark",
            "kafka",
            "dbt",
            "snowflake",
            "databricks",
            "bigquery",
            "microservices",
        ],
    },
}


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).lower().strip()


def _career_text(candidate: Dict[str, Any]) -> str:
    parts = []

    profile = candidate.get("profile", {}) or {}

    for key in ("headline", "summary", "current_title"):
        value = profile.get(key)
        if value:
            parts.append(_normalize_text(value))

    for job in candidate.get("career_history", []) or []:
        for key in ("title", "description"):
            value = job.get(key)
            if value:
                parts.append(_normalize_text(value))

    return " ".join(parts)


def _skills_text(candidate: Dict[str, Any]) -> str:
    parts = []

    for skill in candidate.get("skills", []) or []:
        name = skill.get("name")
        if name:
            parts.append(_normalize_text(name))

    return " ".join(parts)


def _keyword_found(text: str, keyword: str) -> bool:
    keyword = keyword.lower().strip()

    if not keyword:
        return False

    if " " in keyword or "-" in keyword or "/" in keyword:
        return keyword in text

    return re.search(rf"\b{re.escape(keyword)}\b", text) is not None


def semantic_score(candidate: Dict[str, Any]) -> float:
    """
    Semantic relevance score.

    Career evidence = 70%
    Skill evidence = 30%

    Output:
        0.0 -> 1.0
    """

    career_text = _career_text(candidate)
    skills_text = _skills_text(candidate)

    career_score = 0.0
    skills_score = 0.0
    matched_groups = 0

    for _, spec in SEMANTIC_GROUPS.items():

        career_match = any(
            _keyword_found(career_text, kw)
            for kw in spec["keywords"]
        )

        skills_match = any(
            _keyword_found(skills_text, kw)
            for kw in spec["keywords"]
        )

        if career_match:
            career_score += spec["weight"]
            matched_groups += 1

        elif skills_match:
            skills_score += spec["weight"]

    score = (0.70 * career_score) + (0.30 * skills_score)

    if matched_groups == 2:
        score += 2.0
    elif matched_groups == 3:
        score += 4.0
    elif matched_groups == 4:
        score += 6.0
    elif matched_groups >= 5:
        score += 8.0

    score = min(score, 100.0)

    return round(score / 100.0, 4)