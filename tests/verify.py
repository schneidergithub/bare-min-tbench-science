"""Minimal CSV verifier. Standard library only."""
import csv
import math
import sys

COLUMNS = ["doi", "outcome", "n_mdd", "mdd_mean", "mdd_sd",
           "n_ctrl", "ctrl_mean", "ctrl_sd", "d"]
INTEGERS = ("n_mdd", "n_ctrl")
NUMBERS = ("mdd_mean", "mdd_sd", "ctrl_mean", "ctrl_sd", "d")


def load(path):
    with open(path, newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != COLUMNS:
            raise ValueError(f"{path}: incorrect CSV header")
        records = {}
        for line, row in enumerate(reader, start=2):
            if None in row or any(v is None for v in row.values()):
                raise ValueError(f"{path}:{line}: malformed row")
            key = (row["doi"].strip(), row["outcome"].strip())
            if not all(key) or key in records:
                raise ValueError(f"{path}:{line}: empty or duplicate identity {key}")
            for field in INTEGERS:
                raw = row[field].strip()
                if not raw.isdecimal() or int(raw) <= 0:
                    raise ValueError(f"{path}:{line}: invalid {field}")
                row[field] = int(raw)
            for field in NUMBERS:
                row[field] = float(row[field])
                if not math.isfinite(row[field]):
                    raise ValueError(f"{path}:{line}: non-finite {field}")
            if row["mdd_sd"] < 0 or row["ctrl_sd"] < 0:
                raise ValueError(f"{path}:{line}: negative SD")
            records[key] = row
        return records


def verify(submission, reference):
    errors = []
    for key in sorted(reference.keys() - submission.keys()):
        errors.append(f"missing: {key}")
    for key in sorted(submission.keys() - reference.keys()):
        errors.append(f"unexpected: {key}")
    for key in sorted(submission.keys() & reference.keys()):
        got, want = submission[key], reference[key]
        for field in INTEGERS:
            if got[field] != want[field]:
                errors.append(f"{key}: {field} differs")
        for field in NUMBERS:
            tolerance = 0.0001 if field == "d" else 0.000001
            if abs(got[field] - want[field]) > tolerance:
                errors.append(f"{key}: {field} differs")
    return errors


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 verify.py study_effects.csv expected_answers.csv")
        return 1
    try:
        errors = verify(load(sys.argv[1]), load(sys.argv[2]))
    except (OSError, ValueError, csv.Error) as exc:
        print(f"FAIL: {exc}")
        return 1
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
