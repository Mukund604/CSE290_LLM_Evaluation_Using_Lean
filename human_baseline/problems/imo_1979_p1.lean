-- Problem: imo_1979_p1
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: B. Mid-difficulty competition
-- Why this problem: Wolstenholme-style alternating sum; 1979 ∣ p.
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
--   If $p$ and $q$ are natural numbers so that$
--   \frac{p}{q}=1-\frac{1}{2}+\frac{1}{3}-\frac{1}{4}+ \ldots
--   -\frac{1}{1318}+\frac{1}{1319}, $prove that $p$ is divisible with $1979$.

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem imo_1979_p1 (p q : ℕ) (h₀ : 0 < q)
  (h₁ : (∑ k in Finset.Icc (1 : ℕ) 1319, (-1) ^ (k + 1) * ((1 : ℝ) / k)) = p / q) : 1979 ∣ p := by
  sorry
