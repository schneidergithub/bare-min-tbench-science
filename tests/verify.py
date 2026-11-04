"""Minimal CSV verifier. Standard library only."""
import csv
import math
import sys

COLUMNS = ["doi", "task", "n_mdd", "mean_mdd", "sd_mdd",
           "n_control", "mean_control", "sd_control", "d"]
REFERENCE_COLUMNS = ["classification", "record_id", *COLUMNS,
                     "rule", "reason", "coding_sheet_row", "source_reference"]
INTEGERS = ("n_mdd", "n_control")
NUMBERS = ("mean_mdd", "sd_mdd", "mean_control", "sd_control", "d")
ACCEPTED = {"required", "optional"}
CLASSIFICATIONS = ACCEPTED | {"excluded_outcome"}


def load(path, reference=False):
    with open(path, newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        columns = REFERENCE_COLUMNS if reference else COLUMNS
        if reader.fieldnames != columns:
            raise ValueError(f"{path}: incorrect CSV header")
        records = {}
        for line, row in enumerate(reader, start=2):
            if None in row or any(v is None for v in row.values()):
                raise ValueError(f"{path}:{line}: malformed row")
            classification = row["classification"] if reference else "submission"
            if reference and classification not in CLASSIFICATIONS:
                raise ValueError(f"{path}:{line}: unknown classification")
            key = (row["doi"].strip(), row["task"].strip())
            if not all(key) or key in records:
                raise ValueError(f"{path}:{line}: empty or duplicate identity {key}")
            if classification == "excluded_outcome":
                if any(row[field].strip() for field in INTEGERS + NUMBERS):
                    raise ValueError(f"{path}:{line}: excluded statistics must be blank")
                records[key] = row
                continue
            for field in INTEGERS:
                raw = row[field].strip()
                if not raw.isdecimal() or int(raw) <= 0:
                    raise ValueError(f"{path}:{line}: invalid {field}")
                row[field] = int(raw)
            for field in NUMBERS:
                row[field] = float(row[field])
                if not math.isfinite(row[field]):
                    raise ValueError(f"{path}:{line}: non-finite {field}")
            if row["sd_mdd"] < 0 or row["sd_control"] < 0:
                raise ValueError(f"{path}:{line}: negative SD")
            records[key] = row
    if reference and not any(row["classification"] == "required"
                             for row in records.values()):
        raise ValueError(f"{path}: no required outcomes")
    return records


def verify(submission, reference):
    errors = []
    accepted = {key: row for key, row in reference.items()
                if row["classification"] in ACCEPTED}
    required = {key for key, row in accepted.items()
                if row["classification"] == "required"}
    for key in sorted(required - submission.keys()):
        errors.append(f"missing: {key}")
    for key in sorted(submission.keys() - accepted.keys()):
        if key in reference:
            errors.append(f"excluded outcome: {key}")
        else:
            errors.append(f"unexpected: {key}")
    for key in sorted(submission.keys() & accepted.keys()):
        got, want = submission[key], accepted[key]
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
        print("Usage: python3 verify.py study_effects.csv reference.csv")
        return 1
    try:
        reference = load(sys.argv[2], reference=True)
        errors = verify(load(sys.argv[1]), reference)
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
