# Perturbation experiment summary

Stratum C+D problems, baseline vs alpha_rename vs hyp_reorder, 3 seeds per cell.

## Per-problem pass rates

| Problem | Stratum | Model | baseline | α-rename | hyp-reorder |
|---|---|---|---|---|---|
| amc12_2001_p2 | C | Claude | 0/3 | 0/3 | 0/3 |
| amc12_2001_p2 | C | GPT-5.4 | 0/3 | 0/3 | 0/3 |
| amc12a_2009_p5 | C | Claude | 3/3 | 3/3 | — |
| amc12a_2009_p5 | C | GPT-5.4 | 0/3 | **2/3** | — |
| amc12b_2004_p3 | C | Claude | 2/3 | **0/3** | 2/3 |
| amc12b_2004_p3 | C | GPT-5.4 | 0/3 | 0/3 | 0/3 |
| mathd_algebra_119 | D | Claude | 3/3 | 3/3 | 3/3 |
| mathd_algebra_119 | D | GPT-5.4 | 3/3 | 3/3 | 3/3 |
| mathd_algebra_433 | D | Claude | 3/3 | 3/3 | — |
| mathd_algebra_433 | D | GPT-5.4 | 0/3 | **3/3** | — |

## Aggregate pass rates

- alpha_rename: 17/30 (57%)
- hyp_reorder: 8/18 (44%)

## Key findings

1. **Forward contamination signal (Claude on amc12b_2004_p3):** baseline 2/3 → α-rename 0/3. The model solves the original statement intermittently but never solves the renamed-hypothesis variant.

2. **Reverse contamination signal (GPT-5.4 on mathd_algebra_433 and amc12a_2009_p5):** baseline 0/3 → α-rename 3/3 (mathd_algebra_433) and 2/3 (amc12a_2009_p5). The model fails the original but succeeds on the renamed version — suggests memorization of a non-applicable v1 form that the rename disrupts.

3. **Stratum D control behaves correctly:** mathd_algebra_119 stays 3/3 across all conditions for both models — the perturbations preserve provability and don't artificially degrade easy problems.

4. **hyp_reorder finds no signal:** Both models pass rates are unchanged for every problem under hyp_reorder. Hypothesis order is not a memorization channel.

5. **Hard problems stay hard:** amc12_2001_p2 fails 0/3 under every condition for both models — perturbation can't help if the model can't reason about it at all.
