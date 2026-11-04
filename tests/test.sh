#!/bin/sh
# Harbor executes this in the verifier context, with /tests mounted.
set -u
mkdir -p /logs/verifier
if python3 /tests/verify.py /app/study_effects.csv /tests/expected_answers.csv; then
  printf '1.0\n' > /logs/verifier/reward.txt
else
  printf '0.0\n' > /logs/verifier/reward.txt
fi
