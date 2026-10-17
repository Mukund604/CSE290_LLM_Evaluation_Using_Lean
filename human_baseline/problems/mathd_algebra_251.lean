-- Problem: mathd_algebra_251
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: A. Easy algebra sanity floor
-- Why this problem: Smallest non-trivial algebra step (division by x).
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
--   Three plus the reciprocal of a number equals 7 divided by that number.
--   What is the number? Show that it is 2.

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem mathd_algebra_251 (x : ℝ) (h₁ : 3 + 1 / x = 7 / x) : x = 2 := by
  sorry
