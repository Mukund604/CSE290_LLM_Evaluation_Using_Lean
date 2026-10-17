-- Problem: mathd_numbertheory_81
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: E. Number theory tactic stress
-- Why this problem: 71 mod 3 = 2 — decide/norm_num territory.
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
--   Determine the remainder of 71 (mod 3). Show that it is 2.

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem mathd_numbertheory_81 : 71 % 3 = 2 := by
  sorry
