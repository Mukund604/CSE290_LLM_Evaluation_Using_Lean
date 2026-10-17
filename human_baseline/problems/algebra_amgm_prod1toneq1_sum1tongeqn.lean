-- Problem: algebra_amgm_prod1toneq1_sum1tongeqn
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: F. Inequalities (polyrith/nlinarith stress)
-- Why this problem: AMGM product form — beyond nlinarith.
--
-- Author: (your name here)
--
-- Rules (see ../README.md):
--   * Tactic mode only.
--   * No bare one-liner closer as the entire proof (decide / nlinarith /
--     polyrith / omega / aesop alone is not a valid submission unless this
--     header explicitly says otherwise).
--   * Do NOT modify the `theorem ... := by` line below — it is the v2c
--     statement verbatim. Only replace the `sorry` with your proof.
--
-- Informal statement:
--   Show that for any real-valued function $a$ on the natural numbers such
--   that $\forall i \in \mathbb{N}, a_i \geq 0$, if $prod_{i=0}^{n-1} a_i =
--   1$, then $sum_{i=0}^{n-1} a_i \geq n$.

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem algebra_amgm_prod1toneq1_sum1tongeqn (a : ℕ → ℝ) (n : ℕ)
  (h₀: ∀ x:ℕ, 0 ≤ a x)
  (h₀ : Finset.prod (Finset.range n) a = 1) : Finset.sum (Finset.range n) a ≥ n := by
  sorry
