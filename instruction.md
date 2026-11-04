# Task: Executive-function study effects (minimal POC)

This is an illustrative three-outcome subset inspired by
https://github.com/harbor-framework/terminal-bench-science/pull/1513

Source article: DOI 10.1016/j.jad.2008.10.028 (Gohier et al.).
The article is not bundled in this minimal POC. Obtain and consult the
source before attempting the task.

Create `/app/study_effects.csv` with exactly these outcomes:

- Stroop incongruent (colour-word) time (s)
- Stroop incongruent errors (accuracy)
- TMT-B time (s)

Do not include TMT error counts or any other outcomes.

CSV columns in this exact order:

doi,outcome,n_mdd,mdd_mean,mdd_sd,n_ctrl,ctrl_mean,ctrl_sd,d

For each outcome, report the MDD and control group sample sizes, means,
sample standard deviations, and signed small-sample-corrected effect size:

N = n_mdd + n_ctrl
SD_pooled = sqrt(((n_mdd-1)*mdd_sd^2 + (n_ctrl-1)*ctrl_sd^2)/(N-2))
d = (mdd_mean - ctrl_mean)/SD_pooled * (1 - 3/(4*N - 9))

Preserve the sign. Do not reverse accuracy outcomes.

Grading: row order is irrelevant; each of the three outcomes is required
exactly once. No extra or duplicate rows. Sample sizes must match exactly.
Means and standard deviations must match the trusted reference within
absolute tolerance 0.000001; d within 0.0001. Nonfinite values fail.
All checks pass => reward 1.0; otherwise reward 0.0.
