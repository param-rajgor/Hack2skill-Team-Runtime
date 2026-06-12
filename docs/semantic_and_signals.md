# Semantic and Signals Engine

## Purpose
This module evaluates candidate relevance and hireability beyond keyword matching.

It produces three scores:

* Semantic Score
* Behavior Score
* Logistics Score

## Semantic Score
Measures whether a candidate's profile and career history resemble the target role.

Signals:

* Retrieval Systems
* Ranking Systems
* Recommendation Systems
* Production ML
* NLP / LLM Experience
* Evaluation Metrics

Output:

0–100

## Behavior Score
Measures candidate engagement and recruiter attractiveness.

Signals:

* Profile Completeness
* GitHub Activity
* Interview Completion Rate
* Recruiter Response Rate
* Open To Work Status

Output:

0–100

## Logistics Score
Measures hiring feasibility.

Signals:

* Notice Period
* Relocation Willingness
* Work Mode Preference
* Location

Output:

0–100

## Files
Semantic Engine:

* src/semantic/semantic_score.py

Signals Engine:

* src/signals/signal_score.py

Test Files:

* src/semantic/test_semantic.py
* src/signals/test_signals.py
