-- Problem: algebra_apb4leq8ta4pb4
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: F. Inequalities (polyrith/nlinarith stress)
-- Why this problem: (a+b)^4 ≤ 8(a^4+b^4) — boundary of nlinarith reach.
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
--   Show that for any positive real numbers $a$ and $b$, $(a+b)^4 \leq 8(a^4
--   + b^4)$.

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem algebra_apb4leq8ta4pb4 (a b : ℝ) (h₀ : 0 < a ∧ 0 < b) : (a + b) ^ 4 ≤ 8 * (a ^ 4 + b ^ 4) := by
  sorry
