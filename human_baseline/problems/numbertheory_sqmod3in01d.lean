-- Problem: numbertheory_sqmod3in01d
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: E. Number theory tactic stress
-- Why this problem: ∀ x∈ℤ, x² mod 3 ∈ {0,1} — case on x mod 3.
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
--   Show that the square of any integer is congruent to 0 or 1 modulo 3.

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem numbertheory_sqmod3in01d (a : ℤ) : a ^ 2 ≡ 0 [ZMOD 3] ∨ a ^ 2 ≡ 1 [ZMOD 3] := by
  sorry
