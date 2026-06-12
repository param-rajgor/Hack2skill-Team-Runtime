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


def _collect_candidate_text(candidate: Dict[str, Any]) -> str:
    parts = []

    profile = candidate.get("profile", {}) or {}
    for key in ("headline", "summary", "current_title", "current_company", "current_industry"):
        value = profile.get(key)
        if value:
            parts.append(_normalize_text(value))

    for job in candidate.get("career_history", []) or []:
        for key in ("title", "company", "industry", "description"):
            value = job.get(key)
            if value:
                parts.append(_normalize_text(value))

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
    Measures whether the candidate's actual career history
    resembles the target JD, even if the exact wording differs.

    Output:
        0.0 to 100.0
    """
    text = _collect_candidate_text(candidate)

    matched_groups = 0
    score = 0.0

    for _, spec in SEMANTIC_GROUPS.items():
        if any(_keyword_found(text, keyword) for keyword in spec["keywords"]):
            matched_groups += 1
            score += spec["weight"]

    # Small bonus for breadth: candidates matching more distinct semantic areas
    # are slightly better than candidates matching only one.
    if matched_groups == 2:
        score += 2.0
    elif matched_groups == 3:
        score += 4.0
    elif matched_groups == 4:
        score += 6.0
    elif matched_groups >= 5:
        score += 8.0

    return round(min(score, 100.0), 2)