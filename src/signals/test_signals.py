import sys
import os
import json

sys.path.append(
    os.path.abspath(".")
)

from src.signals.signal_score import (
    behavior_score,
    logistics_score,
    signal_score
)


def load_first_candidate():
    with open("data/candidates.jsonl", "r", encoding="utf-8") as f:
        return json.loads(next(f))


def main():

    with open(
        "data/candidates.jsonl",
        "r",
        encoding="utf-8"
    ) as f:

        for i, line in enumerate(f):

            candidate = json.loads(line)

            result = signal_score(candidate)

            print(
                candidate["candidate_id"],
                "|",
                result["signal_score"]
            )

            if i == 19:
                break


if __name__ == "__main__":
    main()