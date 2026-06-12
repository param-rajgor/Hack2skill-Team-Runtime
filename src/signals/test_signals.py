import json

from src.signals.signal_score import (
    behavior_score,
    logistics_score,
    signal_score
)


def load_first_candidate():
    with open("data/candidates.jsonl", "r", encoding="utf-8") as f:
        return json.loads(next(f))


def main():

    candidate = load_first_candidate()

    print("\nCandidate ID:")
    print(candidate["candidate_id"])

    print("\nBehavior Score:")
    print(behavior_score(candidate))

    print("\nLogistics Score:")
    print(logistics_score(candidate))

    print("\nCombined Signal Score:")
    print(signal_score(candidate))


if __name__ == "__main__":
    main()