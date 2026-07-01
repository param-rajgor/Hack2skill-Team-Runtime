# Intelligent Candidate Retrieval & Ranking at Scale
A recruiter-inspired candidate ranking system that moves beyond traditional ATS keyword matching by evaluating candidates across multiple independent hiring dimensions.

## Overview
This project processes **100,000 candidate profiles** by parsing a job description, filtering low-confidence profiles, and ranking candidates using a **Recruiter Confidence Score**. Instead of relying solely on keyword overlap, the system combines **JD Match, Career Relevance, Semantic Relevance, Experience Fit, Behavioral Signals, and Resume Consistency** to produce explainable and deterministic rankings.

## Features
- Job Description Parsing
- Multi-stage Candidate Filtering
- Modular Scoring Pipeline
- Resume Consistency & Fraud Detection
- Explainable Candidate Ranking
- Streaming Processing for 100K+ Candidates

## Pipeline
Job Description
      ↓
JD Parsing
      ↓
Candidate Filtering
      ↓
Parallel Scoring Modules
      ↓
Recruiter Confidence Score
      ↓
Top 100 Ranked Candidates

## Tech Stack
- Python
- JSONL Processing
- Rule-Based NLP
- Modular Scoring Framework

## Run
```bash
pip install -r requirements.txt
python src/ranking/generate_submission.py
```
Output:
```text
outputs/submission.csv

Team Runtime | Redrob Hackathon 2026
