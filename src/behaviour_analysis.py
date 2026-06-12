import json

verified_acceptance = []
unverified_acceptance = []

with open("data/candidates.jsonl", "r") as f:

    for line in f:

        candidate = json.loads(line)

        signals = candidate["redrob_signals"]

        acceptance = signals["offer_acceptance_rate"]

        if acceptance == -1:
            continue

        fully_verified = (
            signals["verified_email"]
            and
            signals["verified_phone"]
        )

        if fully_verified:
            verified_acceptance.append(acceptance)
        else:
            unverified_acceptance.append(acceptance)

print(
    "Verified Avg Acceptance:",
    round(sum(verified_acceptance)/len(verified_acceptance),4)
)

print(
    "Unverified Avg Acceptance:",
    round(sum(unverified_acceptance)/len(unverified_acceptance),4)
)