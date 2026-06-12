import json
from collections import Counter

TARGET_TITLES = [
    "ML Engineer",
    "AI Specialist",
    "Search Engineer",
    "Recommendation Systems Engineer",
    "Data Scientist"
]

industry_counter = Counter()

with open(
    "data/candidates.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        candidate = json.loads(line)

        current_title = candidate[
            "profile"
        ][
            "current_title"
        ]

        if current_title in TARGET_TITLES:

            industry = candidate[
                "profile"
            ][
                "current_industry"
            ]

            industry_counter[
                industry
            ] += 1

print(
    "\nTop Industries Among AI Candidates\n"
)

for industry, count in industry_counter.most_common(20):

    print(
        industry,
        ":",
        count
    )