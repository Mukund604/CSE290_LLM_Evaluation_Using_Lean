-- Problem: induction_sum2kp1npqsqm1
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: G. Induction
-- Why this problem: Σ_{k=0}^{n−1}(2k+3) = (n+1)²−1.
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
--   Show that for positive integer n, $\sum_{k=0}^{n-1} (2k + 3) = (n + 1)^2
--   - 1$.

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem induction_sum2kp1npqsqm1 (n : ℕ) (hn₀: 0 < n) :
  ∑ k ∈ Finset.range n, (2 * k + 3) = (n + 1) ^ 2 - 1 := by
  sorry
