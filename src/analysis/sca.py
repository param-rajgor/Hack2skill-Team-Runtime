import json

TARGET_TITLES = [
    "Search Engineer",
    "Recommendation Systems Engineer",
    "NLP Engineer"
]

count = 0

with open(
    "data/candidates.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        candidate = json.loads(line)

        title = candidate[
            "profile"
        ][
            "current_title"
        ]

        if title in TARGET_TITLES:

            count += 1

            print("\n" + "=" * 50)

            print(
                "Candidate:",
                candidate["candidate_id"]
            )

            print(
                "Title:",
                title
            )

            print(
                "Experience:",
                candidate["profile"][
                    "years_of_experience"
                ]
            )

            print(
                "Industry:",
                candidate["profile"][
                    "current_industry"
                ]
            )

            print("\nTop Skills:")

            for skill in candidate[
                "skills"
            ][:10]:

                print(
                    "-",
                    skill["name"]
                )

            if count == 20:
                break