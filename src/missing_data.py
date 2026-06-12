import json

total = 0

offer_missing = 0
interview_missing = 0
empty_skill_scores = 0

with open("data/candidates.jsonl", "r") as f:

    for line in f:

        candidate = json.loads(line)

        signals = candidate["redrob_signals"]

        total += 1

        if signals["offer_acceptance_rate"] == -1:
            offer_missing += 1

        if signals["interview_completion_rate"] == -1:
            interview_missing += 1

        if len(signals["skill_assessment_scores"]) == 0:
            empty_skill_scores += 1

print("Total:", total)

print(
    "\nOffer Acceptance Missing:",
    round(offer_missing/total*100,2),
    "%"
)

print(
    "Interview Completion Missing:",
    round(interview_missing/total*100,2),
    "%"
)

print(
    "Skill Assessment Missing:",
    round(empty_skill_scores/total*100,2),
    "%"
)