# src/ranking/validate_submission.py

import os
import sys
import csv
import json

def validate():
    print("Starting submission validation checks...")
    
    csv_path = "outputs/final_submission.csv"
    candidates_jsonl_path = "data/candidates.jsonl"
    
    # Check if CSV exists
    if not os.path.exists(csv_path):
        print(f"[ERROR] Submission CSV file not found at {csv_path}")
        sys.exit(1)
        
    # Check if JSONL exists
    if not os.path.exists(candidates_jsonl_path):
        print(f"[ERROR] Candidates JSONL file not found at {candidates_jsonl_path}")
        sys.exit(1)

    # Load all candidate IDs from JSONL into a set for fast lookup
    print("Loading valid candidate IDs from dataset...")
    valid_ids = set()
    with open(candidates_jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            cand = json.loads(line)
            valid_ids.add(cand.get("candidate_id"))
            
    print(f"Loaded {len(valid_ids)} valid candidate IDs.")

    # Read the CSV file
    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        
        # Verify headers
        expected_header = ["candidate_id", "rank", "score", "reasoning"]
        if header != expected_header:
            print(f"[ERROR] Invalid headers in CSV. Expected: {expected_header}, Found: {header}")
            sys.exit(1)
            
        for row in reader:
            rows.append(row)
            
    print(f"Read {len(rows)} candidate rows from CSV.")

    # Rule 1: Exactly 100 rows
    if len(rows) != 100:
        print(f"[ERROR] Row count is {len(rows)} (expected exactly 100).")
        sys.exit(1)
    print("[SUCCESS] Exactly 100 rows found.")

    # Extract columns
    candidate_ids = []
    ranks = []
    scores = []
    reasonings = []
    
    for idx, row in enumerate(rows, 1):
        if len(row) != 4:
            print(f"[ERROR] Row {idx} has invalid column count. Expected 4, got {len(row)}: {row}")
            sys.exit(1)
        
        cand_id, rank_val, score_val, reasoning = row
        candidate_ids.append(cand_id)
        ranks.append(int(rank_val))
        scores.append(float(score_val))
        reasonings.append(reasoning)

    # Rule 2: Unique ranks from 1..100
    expected_ranks = list(range(1, 101))
    if sorted(ranks) != expected_ranks:
        print(f"[ERROR] Ranks are not uniquely 1..100. Sorted ranks: {sorted(ranks)[:5]} ... {sorted(ranks)[-5:]}")
        sys.exit(1)
    print("[SUCCESS] Ranks are uniquely 1..100.")

    # Rule 3: Unique candidate IDs
    if len(set(candidate_ids)) != 100:
        duplicate_ids = [cid for cid in set(candidate_ids) if candidate_ids.count(cid) > 1]
        print(f"[ERROR] Duplicate candidate IDs found: {duplicate_ids}")
        sys.exit(1)
    print("[SUCCESS] All candidate IDs are unique.")

    # Rule 4: Descending score order
    for i in range(len(scores) - 1):
        if scores[i] < scores[i+1]:
            print(f"[ERROR] Scores are not in descending order: Row {i+1} ({scores[i]}) is less than Row {i+2} ({scores[i+1]})")
            sys.exit(1)
    print("[SUCCESS] Scores are in strict descending order.")

    # Rule 5: No empty reasoning
    empty_reasoning_count = sum(1 for r in reasonings if not r.strip())
    if empty_reasoning_count > 0:
        print("[ERROR] Found empty or blank reasoning strings.")
        sys.exit(1)
    print("[SUCCESS] No empty reasoning strings.")

    # Rule 6: Reasoning uniqueness
    unique_reasonings = set(reasonings)
    print(f"Found {len(unique_reasonings)} unique reasoning strings out of 100.")
    if len(unique_reasonings) < 100:
        print(f"[WARNING] Reasoning strings are not 100% unique. Unique count: {len(unique_reasonings)}")
        # Check if it meets a minimum threshold, say at least 95
        if len(unique_reasonings) < 95:
            print("[ERROR] High number of duplicate reasoning strings.")
            sys.exit(1)
    print("[SUCCESS] Reasoning strings show high uniqueness.")

    # Rule 7: Candidate existence in dataset
    missing_ids = [cid for cid in candidate_ids if cid not in valid_ids]
    if missing_ids:
        print(f"[ERROR] Candidate IDs not found in database: {missing_ids}")
        sys.exit(1)
    print("[SUCCESS] All candidate IDs exist in the source dataset.")

    print("\n[COMPLETE] All validation checks passed successfully!")


if __name__ == "__main__":
    validate()
