# Aggregation report

- Input rows: **78**

- Distinct problems covered: **10**

- Distinct (model, condition) cells: **3**


## 1. Pool pass-rate

- **Union pass-rate** (problem solved by ≥1 model/seed/condition): **0.400**

- **Intersection pass-rate** (problem solved by every model+seed in some condition): **0.100**


## 2. Per-(model, condition) overall

| model | condition | n_rows | n_problems | n_seeds | pass_rate | seed_mean | seed_stdev |
| --- | --- | --- | --- | --- | --- | --- | --- |
| anthropic/claude-opus-4.7 | baseline | 30 | 10 | 3 | 0.333 | 0.333 | 0.058 |
| google/gemini-2.5-pro | baseline | 18 | 6 | 3 | 0 | 0 | 0.000 |
| gpt-5.4 | baseline | 30 | 10 | 3 | 0.200 | 0.200 | 0.000 |


## 3. Per-(model, condition, stratum)

| model | condition | stratum | n_problems | n_rows | pass_rate |
| --- | --- | --- | --- | --- | --- |
| anthropic/claude-opus-4.7 | baseline | B | 3 | 9 | 0 |
| anthropic/claude-opus-4.7 | baseline | C | 3 | 9 | 0.333 |
| anthropic/claude-opus-4.7 | baseline | D | 1 | 3 | 0.333 |
| anthropic/claude-opus-4.7 | baseline | F | 3 | 9 | 0.667 |
| google/gemini-2.5-pro | baseline | B | 3 | 9 | 0 |
| google/gemini-2.5-pro | baseline | D | 1 | 3 | 0 |
| google/gemini-2.5-pro | baseline | F | 2 | 6 | 0 |
| gpt-5.4 | baseline | B | 3 | 9 | 0 |
| gpt-5.4 | baseline | C | 3 | 9 | 0 |
| gpt-5.4 | baseline | D | 1 | 3 | 0 |
| gpt-5.4 | baseline | F | 3 | 9 | 0.667 |


## 4. Failure-category distribution

| model | stratum | n_failures | cat_hallucinated_lemma | cat_heavy_tactic_failed | cat_other | cat_sorry_present | cat_tactic_failed | cat_timeout | cat_type_mismatch | cat_unfocused_goals |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| anthropic/claude-opus-4.7 | B | 9 |  | 2 | 1 |  | 3 |  |  | 3 |
| anthropic/claude-opus-4.7 | C | 6 |  |  |  | 1 | 4 |  |  | 1 |
| anthropic/claude-opus-4.7 | D | 2 |  | 1 |  |  | 1 |  |  |  |
| anthropic/claude-opus-4.7 | F | 3 |  |  |  | 1 |  |  |  | 2 |
| google/gemini-2.5-pro | B | 9 | 1 |  |  |  |  |  |  | 8 |
| google/gemini-2.5-pro | D | 3 | 1 |  |  |  |  |  |  | 2 |
| google/gemini-2.5-pro | F | 6 |  |  |  |  |  |  |  | 6 |
| gpt-5.4 | B | 9 | 4 | 4 |  |  |  | 1 |  |  |
| gpt-5.4 | C | 9 | 6 | 3 |  |  |  |  |  |  |
| gpt-5.4 | D | 3 |  | 1 |  |  |  |  | 2 |  |
| gpt-5.4 | F | 3 |  |  |  |  |  |  | 2 | 1 |
