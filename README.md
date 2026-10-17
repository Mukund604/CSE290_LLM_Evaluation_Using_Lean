# Diagnosing How Frontier LLMs Fail at Lean: a miniF2F-v2 evaluation harness

Code and data for an evaluation study of frontier LLMs on formal theorem proving in Lean 4 (paper under review, 2026). Author: Mukund Ojha, UC Santa Cruz.

Every model generated proof is checked by the Lean 4 compiler against Mathlib. Nothing is scored by string matching or by another model.

## What the study does
- Runs frontier models on a 30 problem subset of the miniF2F-v2 test split, grouped into 8 difficulty and contamination strata (see `subset.md`), across 3 seeds.
- Verifies each attempt with Lean and classifies failures from compiler output into a failure taxonomy, then hand codes a sample (`coding_sheet.csv`).
- Sweeps the verification time budget. A common 180 second timeout understated pass rates by about 3x in our runs, because correct proofs were still compiling when the checker gave up.
- Probes contamination with perturbed problem variants (alpha renaming, hypothesis reordering, restatement) and compares model proofs with a human tactic proof baseline.

## Layout
- `harness/`: verifier, generation, perturbation, aggregation, and plotting scripts (details in `harness/README.md`)
- `datasets/`: miniF2F-v2 data used by the subset
- `attempts/`: model proof attempts
- `human_baseline/`: templates for the human proof baseline
- `subset.md`: how the 30 problems and strata were chosen
- `lean-toolchain`, `lakefile.lean`, `lake-manifest.json`: pinned Lean and Mathlib versions

## Running it
See `harness/README.md`. In short: install elan, run `lake update`, copy `.env.example` to `.env` with your own API keys, then use `harness/scripts/generate.py` to collect proofs and `harness/scripts/run.py` to verify them.
