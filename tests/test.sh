#!/bin/sh
# Harbor executes this in the verifier context, with /tests mounted.
set -u
mkdir -p /logs/verifier
if python3 /tests/verify.py /app/results/study_effects.csv /tests/reference.csv; then
  printf '1.0\n' > /logs/verifier/reward.txt
else
  printf '0.0\n' > /logs/verifier/reward.txt
fi
