import json
from collections import Counter

AI_INDUSTRIES = [
    "AI/ML",
    "HealthTech AI",
    "Conversational AI",
    "AI Services"
]

title_counter = Counter()

with open(
    "data/candidates.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        candidate = json.loads(line)

        industry = candidate[
            "profile"
        ][
            "current_industry"
        ]

        if industry in AI_INDUSTRIES:

            title = candidate[
                "profile"
            ][
                "current_title"
            ]

            title_counter[
                title
            ] += 1

print(
    "\nTop Titles In AI Industries\n"
)

for title, count in title_counter.most_common(30):

    print(
        title,
        ":",
        count
    )