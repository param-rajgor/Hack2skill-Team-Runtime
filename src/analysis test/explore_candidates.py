import json
import pprint

with open("data/candidates.jsonl", "r") as f:
    first_candidate = json.loads(next(f))

print("\nPROFILE")
pprint.pp(first_candidate["profile"])

print("\nSKILLS")
pprint.pp(first_candidate["skills"][:5])

print("\nREDROB SIGNALS")
pprint.pp(first_candidate["redrob_signals"])