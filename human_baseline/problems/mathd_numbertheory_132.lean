-- Problem: mathd_numbertheory_132
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: E. Number theory tactic stress
-- Why this problem: 2004 mod 12 = 0 — consistency check vs. NT-81.
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
--   What is the remainder of 2004 divided by 12? Show that it is 0.

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem mathd_numbertheory_132 : 2004 % 12 = 0 := by
  sorry
