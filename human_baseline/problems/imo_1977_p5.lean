-- Problem: imo_1977_p5
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: H. Hard / specialist-prover failure proxy
-- Why this problem: q²+r=1977 from dividing a²+b² by a+b.
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
--   Let $a,b$ be two natural numbers. When we divide $a^2+b^2$ by $a+b$, we
--   the the remainder $r$ and the quotient $q.$ Determine all pairs $(a, b)$
--   for which $q^2 + r = 1977.$

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

abbrev imo_1977_p5_solution : Finset (ℕ × ℕ) := sorry

theorem imo_1977_p5
  (a b q r : ℕ)
  (hp: 0 < a ∧ 0 < b)
  (h₀ : r = (a ^ 2 + b ^ 2) % (a + b))
  (h₁ : q = (a ^ 2 + b ^ 2) / (a + b)) :
  q ^ 2 + r = 1977 ↔ (a , b) ∈ imo_1977_p5_solution := by
  sorry
