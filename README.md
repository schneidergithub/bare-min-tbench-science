# bare-min-tbench-science

A minimal science-benchmark proof of concept: an agent reconstructs study-level
statistics from articles, writes a CSV, and a Python verifier compares the answer
with one reference file.

## One grading reference

`tests/reference.csv` is the source of truth for outcome grading. It combines
the previous PR1513 expected-answer and excluded-outcome tables. The grader
uses each row's classification and expected statistics; it has no study-level
exclusion list. Retained rows keep their classifications, reasons, source
references, and numeric precision.

| Classification | Records | Grading behavior |
| --- | ---: | --- |
| `required` | 34 | Must appear exactly once and match the reference. |
| `optional` | 35 | May be omitted; must match the reference if submitted. |
| `excluded_outcome` | 16 | Must not be submitted. |

The reference has 85 outcome records across eight of the nine DOIs in the
instructions. Seven studies have required outcomes. `10.1037/a0017206` has
17 optional outcomes. `10.1007/s00406-010-0165-3` has no reference outcomes;
any submission for it follows the same unknown-outcome rule as any other
unlisted comparison.

The required-only table duplicated rows in the larger expected-answer table.
The old three-row `expected_answers.csv` also duplicated three of its outcomes;
the consolidated reference keeps the larger table's labels and precision.

The reference retains `record_id`, `rule`, `reason`, `coding_sheet_row`, and
`source_reference` for review. These metadata columns belong only in the
reference, not in the agent's submission. Every reference row identifies an
outcome by DOI and task name. Excluded-outcome rows have no expected statistics.

## Submission and grading

Write `/app/results/study_effects.csv` with these columns in this order:

```csv
doi,task,n_mdd,mean_mdd,sd_mdd,n_control,mean_control,sd_control,d
```

`tests/test.sh` passes the submission and `/tests/reference.csv` to the
standard-library verifier. It writes `1.0` to `/logs/verifier/reward.txt` when
all checks pass, or `0.0` otherwise.

Rows are identified by DOI and task name, ignoring surrounding whitespace.
Sample sizes must match exactly. Means and standard deviations use an absolute
tolerance of `0.000001`; `d` uses `0.0001`. Duplicate or unexpected rows,
malformed data, and nonfinite numbers fail.

## Remaining MVP decisions

The reference preserves the imported outcome classifications and values; this
refactor does not independently revalidate them against the source articles.

The task also needs a clear convention for outcome names and the effect-size
calculation. Its stated eight-hour allowance currently differs from the
ten-minute agent limit in `task.toml`. Execution validation remains outstanding.
