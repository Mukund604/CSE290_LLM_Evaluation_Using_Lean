-- Problem: mathd_algebra_22
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: A. Easy algebra sanity floor
-- Why this problem: Trivial log identity — sanity floor; failure here is a harness bug.
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
--   Evaluate $\log_{5^2}5^4$. Show that it is 2.

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem mathd_algebra_22 : Real.logb (5 ^ 2) (5 ^ 4) = 2 := by
  sorry
