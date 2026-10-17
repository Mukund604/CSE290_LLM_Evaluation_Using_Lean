-- Problem: induction_divisibility_3divnto3m2n
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: G. Induction
-- Why this problem: 3 ∣ n³+2n by induction.
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
--   Show that for any natural number $n \in \mathbb{N}$, $3 \mid n^3 + 2n$ .

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem induction_divisibility_3divnto3m2n (n : ℕ) : 3 ∣ n ^ 3 + 2 * n := by
  sorry
