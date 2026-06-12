import json

from career_relevance import calculate_career_relevance

from experience_score import calculate_experience_score

with open("data/candidates.jsonl", "r", encoding="utf-8") as f:

    first_candidate = json.loads(next(f))


print()

print("Candidate ID:")
print(first_candidate["candidate_id"])

print()

print("Career Relevance Score:")
print(calculate_career_relevance(first_candidate))

print()

print("Experience Score:")
print(calculate_experience_score(first_candidate))