-- Problem: amc12_2001_p2
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: C. Contamination probe (edited from v1, v2c≠v2s)
-- Why this problem: Digit sum/product puzzle; edited statement.
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
--   Let $P(n)$ and $S(n)$ denote the product and the sum, respectively, of
--   the digits of the integer $n$. For example, $P(23) = 6$ and $S(23) = 5$.
--   Suppose $N$ is a two-digit number such that $N = P(N)+S(N)$. What is the
--   units digit of $N$? Prove that it is one of the following options.
--   $\text{(A)}\ 2\qquad \text{(B)}\ 3\qquad \text{(C)}\ 6\qquad \text{(D)}\
--   8\qquad \text{(E)}\ 9$

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem amc12_2001_p2
  (n : ℕ)
  (P S : ℕ → ℕ)
  (h₀ : P = fun x => (Nat.digits 10 x).prod)
  (h₁ : S = fun x => (Nat.digits 10 x).sum)
  (h₂ : (Nat.digits 10 n).length = 2)
  (h₃ : n = P n + S n) :
  n % 10 = 2 ∨ n % 10 = 3 ∨ n % 10 = 6 ∨ n % 10 = 8 ∨ n % 10 = 9 := by
  sorry
