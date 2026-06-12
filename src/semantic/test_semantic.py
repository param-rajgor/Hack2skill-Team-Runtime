import json

from src.semantic.semantic_score import semantic_score


def load_first_candidate():
    with open("data/candidates.jsonl", "r", encoding="utf-8") as f:
        return json.loads(next(f))


def main():

    candidate = load_first_candidate()

    print("\nCandidate ID:")
    print(candidate["candidate_id"])

    print("\nSemantic Score:")
    print(semantic_score(candidate))


if __name__ == "__main__":
    main()