# Behavioral Signals Analysis

## Signals Found

- profile_completeness_score
- signup_date
- last_active_date
- open_to_work_flag
- profile_views_received_30d
- applications_submitted_30d
- recruiter_response_rate
- avg_response_time_hours
- skill_assessment_scores
- connection_count
- endorsements_received
- notice_period_days
- expected_salary_range_inr_lpa
- preferred_work_mode
- willing_to_relocate
- github_activity_score
- search_appearance_30d
- saved_by_recruiters_30d
- interview_completion_rate
- offer_acceptance_rate
- verified_email
- verified_phone
- linkedin_connected


## Signal Categories

### Availability Signals

- open_to_work_flag
- avg_response_time_hours
- notice_period_days
- willing_to_relocate


Purpose:
Can this candidate be hired quickly?

### Recruiter Interest Signals

- profile_views_received_30d
- search_appearance_30d
- saved_by_recruiters_30d

Purpose:
Do recruiters already find this candidate attractive?

### Technical Activity Signals

- github_activity_score
- skill_assessment_scores

Purpose:
Is the candidate actively building and learning?

### Reliability Signals

- interview_completion_rate
- offer_acceptance_rate


Purpose:
Does the candidate follow through on opportunities?

### Trust Signals

- verified_email
- verified_phone
- linkedin_connected
- avg_response_time_hours

Purpose:
Can we trust this profile?

## Findings

- Open to work = 35.34%

- Open-to-work candidates and non-open-to-work candidates exhibited nearly identical recruiter response rates, indicating that open-to-work status alone is not a strong predictor of responsiveness. OPEN TO WORK (0.4425) and NOT OPEN TO WORK (0.4333)

- The offer_acceptance_rate field contains many -1 values, which likely represent missing or unavailable historical offer data. These records should be excluded or imputed before using the feature in scoring.

- Candidates with stronger technical assessment performance showed moderately higher offer acceptance rates(0.522) compared to lower-skilled candidates( 0.4833), suggesting a weak positive relationship between technical competence and hiring success.

- Candidates with higher recruiter response rates showed only a marginally higher interview completion rate, suggesting that recruiter responsiveness alone is not a strong predictor of interview engagement. (0.633 vs 0.6137)

- Candidates frequently saved by recruiters demonstrated slightly higher technical assessment scores, suggesting that recruiter interest aligns weakly with measured technical competence.
High Saved Candidates: 51.80
Low Saved Candidates: 49.41

- Candidates with high GitHub activity achieved significantly higher technical assessment scores than candidates with low GitHub activity, indicating a strong positive relationship between practical technical engagement and demonstrated technical competence.
High GitHub Avg Skill: 62.32
Low GitHub Avg Skill: 50.47

- Profile completeness strongly correlates with offer acceptance rates, while LinkedIn connectivity has negligible impact, indicating that profile quality is a more meaningful hiring signal than external profile linkage.
LinkedIn Avg Acceptance: 0.4798
No LinkedIn Avg Acceptance: 0.4714
High Profile Avg Acceptance: 0.5813
Low Profile Avg Acceptance: 0.4708

- Profile verification exhibits a negligible relationship with offer acceptance rates, suggesting that verification status functions primarily as a trust and authenticity signal rather than a predictor of hiring outcomes.
Verified Avg Acceptance: 0.4785
Unverified Avg Acceptance: 0.4713