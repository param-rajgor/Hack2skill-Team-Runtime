import sys
import os
import json

# Add project folders temporarily

sys.path.append(os.path.abspath("src"))
sys.path.append(os.path.abspath("src/career"))
sys.path.append(os.path.abspath("src/semantic"))
sys.path.append(os.path.abspath("src/signals"))
sys.path.append(os.path.abspath("src/consistency"))

from career_relevance import calculate_career_relevance
from experience_score import calculate_experience_score

from semantic_score import semantic_score

from signal_score import signal_score

from scorer import consistency_score


with open(
    "data/candidates.jsonl",
    "r",
    encoding="utf-8"
) as f:

    candidate = json.loads(next(f))

print("\nCandidate:")
print(candidate["candidate_id"])

print("\nCareer:")
print(
    calculate_career_relevance(candidate)
)

print("\nExperience:")
print(
    calculate_experience_score(candidate)
)

print("\nSemantic:")
print(
    semantic_score(candidate)
)

print("\nSignals:")
print(
    signal_score(candidate)
)

print("\nConsistency:")
print(
    consistency_score(candidate)
)