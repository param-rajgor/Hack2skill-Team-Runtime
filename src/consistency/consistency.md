# Consistency Analysis
Goal:
Check whether a candidate's profile is actually supported by evidence instead of just trusting listed skills.

## Things We Tested

### 1. Experience vs Career History
Compared claimed experience with experience calculated from career history.

Result:
- Average difference = 0.1 years
- Maximum difference = 0.33 years

Conclusion:
Not useful. Dataset is already very consistent.

---

### 2. Advanced Skill with Low Duration
Checked candidates claiming advanced skills with less than 6 months of usage.

Result:
Many legitimate candidates had recently learned newer technologies like LLMs, RAG, etc.

Conclusion:
Weak signal. Rejected.

---

### 3. Number of Advanced Skills
Average advanced skills per candidate = 1.14

Some candidates had 8-11 advanced AI skills.

Conclusion:
Skill count alone is not enough, but becomes useful when combined with career evidence.

---

## Useful Findings

### Claim vs Career Evidence Gap

Found multiple candidates claiming skills such as:

- RAG
- FAISS
- Embeddings
- Vector Search
- Information Retrieval

while having career histories in:

- Marketing
- Sales
- Operations
- Customer Support

Conclusion:
Large gap between claims and career evidence is a strong consistency signal.

---

### Assessment Support

Assessment scores provide independent evidence for claimed skills.

Example:
Candidates with strong claims and strong assessment scores appear more credible than candidates with no supporting evidence.

Conclusion:
Useful signal.

---

### Skill Duration Support

Technical profiles generally had much longer usage duration for advanced skills.

Examples:

- Backend Engineer → ~35 months
- Data Engineer → ~42 months
- ML Engineer → ~39 months

Non-technical profiles often showed:

- 8–16 months

Conclusion:
Longer skill duration increases confidence in claimed expertise.

---

## Final Takeaways

Most useful signals:

1. Claim vs Career Evidence Gap
2. Assessment Support
3. Skill Duration Support

Rejected signals:

1. Experience vs Career History
2. Advanced Skill < 6 Months
3. Seniority vs Experience