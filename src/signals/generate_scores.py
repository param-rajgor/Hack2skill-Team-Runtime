import json
import csv
from pathlib import Path

from src.semantic.semantic_score import semantic_score
from src.signals.signal_score import (
    behavior_score,
    logistics_score,
    signal_score,
)

INPUT_FILE = "data/candidates.jsonl"
OUTPUT_FILE = "outputs/semantic_signal_scores.csv"


def main():

    Path("outputs").mkdir(exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as infile, \
         open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:

        writer = csv.writer(outfile)

        writer.writerow([
            "candidate_id",
            "semantic_score",
            "behavior_score",
            "logistics_score",
            "signal_score",
        ])

        count = 0

        for line in infile:

            candidate = json.loads(line)

            sem_score = semantic_score(candidate)

            beh_score = behavior_score(candidate)

            log_score = logistics_score(candidate)

            sig_score = signal_score(candidate)["signal_score"]

            writer.writerow([
                candidate["candidate_id"],
                sem_score,
                beh_score,
                log_score,
                sig_score,
            ])

            count += 1

            if count % 10000 == 0:
                print(f"Processed {count:,} candidates")

    print("\nFinished!")
    print(f"Total candidates processed: {count:,}")
    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()