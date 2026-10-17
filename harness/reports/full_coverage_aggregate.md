# Aggregation report

- Input rows: **222**

- Distinct problems covered: **30**

- Distinct (model, condition) cells: **3**


## 1. Pool pass-rate

- **Union pass-rate** (problem solved by ≥1 model/seed/condition): **0.633**

- **Intersection pass-rate** (problem solved by every model+seed in some condition): **0.167**


## 2. Per-(model, condition) overall

| model | condition | n_rows | n_problems | n_seeds | pass_rate | seed_mean | seed_stdev |
| --- | --- | --- | --- | --- | --- | --- | --- |
| anthropic/claude-opus-4.7 | baseline | 90 | 30 | 3 | 0.533 | 0.533 | 0.033 |
| google/gemini-2.5-pro | baseline | 42 | 30 | 3 | 0.167 | 0.078 | 0.135 |
| gpt-5.4 | baseline | 90 | 30 | 3 | 0.278 | 0.278 | 0.019 |


## 3. Per-(model, condition, stratum)

| model | condition | stratum | n_problems | n_rows | pass_rate |
| --- | --- | --- | --- | --- | --- |
| anthropic/claude-opus-4.7 | baseline | A | 3 | 9 | 1 |
| anthropic/claude-opus-4.7 | baseline | B | 5 | 15 | 0.067 |
| anthropic/claude-opus-4.7 | baseline | C | 5 | 15 | 0.533 |
| anthropic/claude-opus-4.7 | baseline | D | 3 | 9 | 0.778 |
| anthropic/claude-opus-4.7 | baseline | E | 4 | 12 | 0.833 |
| anthropic/claude-opus-4.7 | baseline | F | 3 | 9 | 0.667 |
| anthropic/claude-opus-4.7 | baseline | G | 3 | 9 | 0.778 |
| anthropic/claude-opus-4.7 | baseline | H | 4 | 12 | 0 |
| google/gemini-2.5-pro | baseline | A | 3 | 3 | 0.333 |
| google/gemini-2.5-pro | baseline | B | 5 | 11 | 0 |
| google/gemini-2.5-pro | baseline | C | 5 | 5 | 0.200 |
| google/gemini-2.5-pro | baseline | D | 3 | 5 | 0.400 |
| google/gemini-2.5-pro | baseline | E | 4 | 4 | 0.750 |
| google/gemini-2.5-pro | baseline | F | 3 | 7 | 0 |
| google/gemini-2.5-pro | baseline | G | 3 | 3 | 0 |
| google/gemini-2.5-pro | baseline | H | 4 | 4 | 0 |
| gpt-5.4 | baseline | A | 3 | 9 | 0.667 |
| gpt-5.4 | baseline | B | 5 | 15 | 0 |
| gpt-5.4 | baseline | C | 5 | 15 | 0 |
| gpt-5.4 | baseline | D | 3 | 9 | 0.333 |
| gpt-5.4 | baseline | E | 4 | 12 | 0.750 |
| gpt-5.4 | baseline | F | 3 | 9 | 0.667 |
| gpt-5.4 | baseline | G | 3 | 9 | 0.111 |
| gpt-5.4 | baseline | H | 4 | 12 | 0 |


## 4. Failure-category distribution

| model | stratum | n_failures | cat_hallucinated_lemma | cat_heavy_tactic_failed | cat_other | cat_sorry_present | cat_syntax_error | cat_tactic_failed | cat_timeout | cat_type_mismatch | cat_unfocused_goals |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| anthropic/claude-opus-4.7 | B | 14 |  | 2 | 2 |  | 3 | 3 |  |  | 4 |
| anthropic/claude-opus-4.7 | C | 7 | 1 |  |  | 1 |  | 4 |  |  | 1 |
| anthropic/claude-opus-4.7 | D | 2 |  | 1 |  |  |  | 1 |  |  |  |
| anthropic/claude-opus-4.7 | E | 2 | 2 |  |  |  |  |  |  |  |  |
| anthropic/claude-opus-4.7 | F | 3 |  |  |  | 1 |  |  |  |  | 2 |
| anthropic/claude-opus-4.7 | G | 2 | 1 |  |  |  |  |  |  |  | 1 |
| anthropic/claude-opus-4.7 | H | 12 |  |  |  | 12 |  |  |  |  |  |
| google/gemini-2.5-pro | A | 2 |  |  | 1 |  |  |  |  |  | 1 |
| google/gemini-2.5-pro | B | 11 | 2 |  |  |  | 1 |  |  |  | 8 |
| google/gemini-2.5-pro | C | 4 | 2 |  |  |  |  |  |  |  | 2 |
| google/gemini-2.5-pro | D | 3 | 1 |  |  |  |  |  |  |  | 2 |
| google/gemini-2.5-pro | E | 1 | 1 |  |  |  |  |  |  |  |  |
| google/gemini-2.5-pro | F | 7 |  |  |  |  |  |  |  |  | 7 |
| google/gemini-2.5-pro | G | 3 | 1 |  | 1 |  |  |  |  |  | 1 |
| google/gemini-2.5-pro | H | 4 |  |  |  | 4 |  |  |  |  |  |
| gpt-5.4 | A | 3 |  |  |  |  |  | 2 |  |  | 1 |
| gpt-5.4 | B | 15 | 7 | 4 |  |  | 3 |  | 1 |  |  |
| gpt-5.4 | C | 15 | 7 | 3 |  |  |  |  |  | 1 | 4 |
| gpt-5.4 | D | 6 |  | 1 |  |  |  |  |  | 2 | 3 |
| gpt-5.4 | E | 3 |  | 3 |  |  |  |  |  |  |  |
| gpt-5.4 | F | 3 |  |  |  |  |  |  |  | 2 | 1 |
| gpt-5.4 | G | 8 |  | 1 |  |  |  | 2 |  | 2 | 3 |
| gpt-5.4 | H | 12 |  |  |  | 12 |  |  |  |  |  |
