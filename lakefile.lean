import Lake
open Lake DSL

package miniF2FEval where
  -- One Mathlib pin for both the harness and the human baseline.
  -- After cloning, run `lake update` once to materialize lake-manifest.json,
  -- then commit the manifest so all collaborators build against the same hash.

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "master"

@[default_target]
lean_lib MiniF2FEval where
  -- Top-level library that just imports Mathlib so the first `lake build`
  -- primes the Mathlib build cache. Per-problem files live under
  -- `harness/problems/` and are verified individually via `lake env lean`.
  roots := #[`MiniF2FEval]
