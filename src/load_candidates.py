import json
import pprint

candidates = []

with open("data/candidates.jsonl", "r") as f:
    for line in f:
        candidates.append(json.loads(line))

pprint.pp(candidates[0])