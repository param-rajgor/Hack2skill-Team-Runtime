# src/career/experience_score.py

def calculate_experience_score(candidate):

    years = candidate["profile"]["years_of_experience"]

    if 5 <= years <= 9:
        return 1.0

    elif 3 <= years < 5:
        return 0.75

    elif 9 < years <= 12:
        return 0.80

    elif years < 3:
        return 0.30

    else:
        return 0.60