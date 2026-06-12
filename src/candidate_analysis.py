import json

# Load all candidates
candidates = []

with open("data/candidates.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        candidates.append(json.loads(line))

print("Total Candidates:", len(candidates))

# Analyze first 5 candidates
for i in range(5):
    c = candidates[i]

    print("\n" + "=" * 50)
    print("Candidate ID:", c["candidate_id"])

    print("\nPROFILE")
    print("Current Title:",
          c["profile"]["current_title"])

    print("Experience:",
          c["profile"]["years_of_experience"])

    print("Current Company:",
          c["profile"]["current_company"])

    print("Country:",
          c["profile"]["country"])

    print("Open To Work:",
          c["redrob_signals"]["open_to_work_flag"])

    print("\nCAREER HISTORY")

    for job in c["career_history"]:
        print(f"- {job['title']} ({job['company']})")

    print("\nTOP SKILLS")

    for skill in c["skills"][:10]:
        print("-", skill["name"])

    print("\nASSESSMENT SCORES")

    scores = c["redrob_signals"].get(
        "skill_assessment_scores", {}
    )

    if scores:
        for skill, score in scores.items():
            print(f"{skill}: {score}")
    else:
        print("No assessment scores available")

    print("\nEDUCATION")

    for edu in c["education"]:
        print(
            f"{edu['degree']} in "
            f"{edu['field_of_study']} "
            f"({edu['institution']})"
        )