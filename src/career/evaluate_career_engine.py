import json
import pandas as pd

from career_relevance import calculate_career_relevance
from experience_score import calculate_experience_score

results = []

count = 0

with open("data/candidates.jsonl", "r", encoding="utf-8") as f:

    for line in f:

        candidate = json.loads(line)

        candidate_id = candidate["candidate_id"]

        career_score = calculate_career_relevance(candidate)

        experience_score = calculate_experience_score(candidate)

        results.append({
            "candidate_id": candidate_id,
            "career_relevance_score": career_score,
            "experience_score": experience_score
        })

        count += 1

        if count % 10000 == 0:
            print(f"Processed {count} candidates")

df = pd.DataFrame(results)

df.to_csv(
    "outputs/career_engine_results.csv",
    index=False
)

print()
print("Finished")
print("Candidates Processed:", len(df))

print()
print("Career Score Statistics")
print(df["career_relevance_score"].describe())

print()
print("Experience Score Statistics")
print(df["experience_score"].describe())