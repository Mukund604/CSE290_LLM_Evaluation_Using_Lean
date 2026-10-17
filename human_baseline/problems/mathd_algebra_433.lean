-- Problem: mathd_algebra_433
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: D. Unchanged from v1 (memorization-friendly control)
-- Why this problem: Evaluate f(8) for f(x) = 3√(2x−7) − 8.
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
--   Let $f(x) = 3\sqrt{2x - 7} - 8$.  Find $f(8)$. Show that it is 1.

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem mathd_algebra_433 (f : ℝ → ℝ) (h₀ : ∀ x, f x = 3 * Real.sqrt (2 * x - 7) - 8) : f 8 = 1 := by
  sorry
