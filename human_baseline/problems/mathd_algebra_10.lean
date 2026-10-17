-- Problem: mathd_algebra_10
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: A. Easy algebra sanity floor
-- Why this problem: Pure arithmetic; end-to-end pipeline test.
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
--   What is the positive difference between $120\%$ of 30 and $130\%$ of 20?
--   Show that it is 10.

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem mathd_algebra_10 : abs ((120 : ℝ) / 100 * 30 - 130 / 100 * 20) = 10 := by
  sorry
