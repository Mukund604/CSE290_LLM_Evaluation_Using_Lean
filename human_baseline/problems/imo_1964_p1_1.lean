-- Problem: imo_1964_p1_1
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: B. Mid-difficulty competition
-- Why this problem: Classical: 7 ∣ 2^n − 1 ⇒ 3 ∣ n.
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
--   Let $n$ be a natural number. Show that if $7$ divides $2^n-1$, then $3$
--   divides $n$.

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem imo_1964_p1_1 (n : ℕ) (h₀ : 7 ∣ 2 ^ n - 1) : 3 ∣ n := by
  sorry
