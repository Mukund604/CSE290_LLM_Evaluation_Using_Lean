-- Problem: imo_2006_p3
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: H. Hard / specialist-prover failure proxy
-- Why this problem: Classic ab(a²−b²)+… ≤ M(a²+b²+c²)² inequality.
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
--   Determine the least real number $M$ such that the inequality  $(ab(a^2 -
--   b^2)) + (bc(b^2 - c^2)) + (ca(c^2 - a^2)) \leq M (a^2 + b^2 + c^2)^2$
--   holds for all real numbers a, b and c.

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

abbrev imo_2006_p3_solution : ℝ := sorry

theorem imo_2006_p3
  (a b c : ℝ)
  (S : Set ℝ)
  (hS : S = {M | a * b * (a ^ 2 - b ^ 2) + b * c * (b ^ 2 - c ^ 2) + c * a * (c ^ 2 - a ^ 2) ≤ M * (a ^ 2 + b ^ 2 + c ^ 2) ^ 2}) :
  IsLeast S imo_2006_p3_solution := by
  sorry
