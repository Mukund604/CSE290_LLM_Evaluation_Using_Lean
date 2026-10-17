-- Problem: amc12a_2008_p4
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: C. Contamination probe (edited from v1, v2c≠v2s)
-- Why this problem: Telescoping product; competition form retained.
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
--   What is the numerical value of the [[product]] $\frac{8}{4}\cdot\frac{12}
--   {8}\cdot\frac{16}{12}\cdot\cdots\cdot\frac{4n+4}{4n}\cdot\cdots\cdot\frac
--   {2008}{2004}?$ Prove that it is one of the following options.
--   $\textbf{(A)}\ 251\qquad\textbf{(B)}\ 502\qquad\textbf{(C)}\
--   1004\qquad\textbf{(D)}\ 2008\qquad\textbf{(E)}\ 4016$

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem amc12a_2008_p4
  (X : ℝ)
  (hX : X = ∏ k ∈ Finset.Icc (1 : ℕ) 501, ((4 : ℝ) * k + 4) / (4 * k)) :
  X = 251 ∨ X = 502 ∨ X = 1004 ∨ X = 2008 ∨ X = 4016 := by
  sorry
