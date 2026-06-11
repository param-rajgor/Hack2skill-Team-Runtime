import json
from collections import Counter

# LOAD DATASET
def load_candidates():
    candidates = []

    with open("data/candidates.jsonl", "r") as f:
        for line in f:
            candidates.append(json.loads(line))

    return candidates

# TOP TITLES
def top_titles(candidates):

    title_counter = Counter()

    for candidate in candidates:
        title = candidate["profile"]["current_title"]
        title_counter[title] += 1

    print("\nTOP 20 TITLES\n")

    for title, count in title_counter.most_common(20):
        print(f"{title}: {count}")

# TOP SKILLS
def top_skills(candidates):

    skill_counter = Counter()

    for candidate in candidates:

        for skill in candidate["skills"]:
            skill_counter[skill["name"]] += 1

    print("\nTOP 50 SKILLS\n")

    for skill, count in skill_counter.most_common(50):
        print(f"{skill}: {count}")

# EXPERIENCE DISTRIBUTION
def experience_distribution(candidates):

    buckets = {
        "0-2": 0,
        "2-5": 0,
        "5-8": 0,
        "8-12": 0,
        "12+": 0
    }

    for candidate in candidates:

        exp = candidate["profile"]["years_of_experience"]

        if exp < 2:
            buckets["0-2"] += 1

        elif exp < 5:
            buckets["2-5"] += 1

        elif exp < 8:
            buckets["5-8"] += 1

        elif exp < 12:
            buckets["8-12"] += 1

        else:
            buckets["12+"] += 1

    print("\nEXPERIENCE DISTRIBUTION\n")

    for bucket, count in buckets.items():
        print(f"{bucket}: {count}")

# COUNTRY DISTRIBUTION
def country_distribution(candidates):

    country_counter = Counter()

    for candidate in candidates:

        country = candidate["profile"]["country"]
        country_counter[country] += 1

    print("\nTOP COUNTRIES\n")

    for country, count in country_counter.most_common(20):
        print(f"{country}: {count}")

# INDUSTRY DISTRIBUTION
def industry_distribution(candidates):

    industry_counter = Counter()

    for candidate in candidates:

        industry = candidate["profile"]["current_industry"]
        industry_counter[industry] += 1

    print("\nTOP INDUSTRIES\n")

    for industry, count in industry_counter.most_common(20):
        print(f"{industry}: {count}")


# MAIN
if __name__ == "__main__":

    candidates = load_candidates()

    print(f"\nTotal Candidates: {len(candidates)}")

    # Uncomment whichever analysis you want

    top_titles(candidates)

    # top_skills(candidates)

    # experience_distribution(candidates)

    # country_distribution(candidates)

    # industry_distribution(candidates)