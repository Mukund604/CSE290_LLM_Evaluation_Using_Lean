# miniF2F-v2 evaluation subset (30 problems)

All problems are from the **test** split of miniF2F-v2 (Ospanov et al., 2025;
[github.com/roozbeh-yz/miniF2F_v2](https://github.com/roozbeh-yz/miniF2F_v2)).
By default we use the **v2c (competition)** form; we fall back to the v2s
(simplified) form only on problems that fail uniformly across the pool, and
record the swap.

Test split totals: 244 problems. Topic distribution: `mathd_algebra` 70,
`mathd_numbertheory` 60, `amc*` 45, `imo_*` 20, `algebra_*` 18, `aime*` 15,
`induction_*` 8, `numbertheory_*` 8.

Cross-version analysis used to derive strata C and D:

- **243 of 244** v2c-test problems also appear (by name) in v1 (test ∪ valid).
- Of those, **211 had their formal statement edited** between v1 and v2.
- **53 problems** are both edited-from-v1 *and* have a v2c form that differs
  from v2s (i.e., the competition form was retained). These are the strongest
  contamination-probe candidates.
- **32 problems** are unchanged between v1 and v2 — the "memorization-friendly"
  candidates for stratum D.

## Stratum-level rationale

| # | Stratum | Count | Purpose |
|---|---|---|---|
| A | Easy algebra sanity floor | 3 | Uniform success expected. Failures here indicate harness/prompt issues, not model issues. |
| B | Mid-difficulty competition (IMO/AIME) | 5 | Real reasoning required; expect partial pool success and rich failure modes. |
| C | Strongest contamination probe (edited from v1, v2c ≠ v2s) | 5 | Direct memorization test. A model trained on v1 should produce a confidently wrong proof of the v2c-form statement. |
| D | Unchanged from v1 (memorization-friendly) | 3 | Control for stratum C. If pass rates spike here vs. stratum C, that gap is evidence of contamination. |
| E | Number theory tactic stress | 4 | Stresses `omega`, `decide`, `norm_num` tactic-choice behavior. |
| F | Inequalities | 3 | Stresses `polyrith` / `nlinarith` behavior, including overreach and timeouts. |
| G | Induction | 3 | Tests structural reasoning and `induction` tactic discipline. |
| H | Hard / specialist-prover failure proxy | 4 | Frontier of difficulty; anchors what the frontier general-purpose pool *cannot* yet do. |

Total: **30**.

> Proxy note on stratum H: per-problem specialist-prover failure lists are
> not published in the v2 release. We use longest-statement IMO problems as
> a proxy for difficulty; if per-problem specialist-prover outputs become
> available, we will swap to a direct failure list.

## Per-problem selections

### A. Easy algebra sanity floor (3)

| Name | Why this specific problem |
|---|---|
| `mathd_algebra_22` | One-line goal: `log_{5^2}(5^4) = 2`. Trivially closed by `norm_num` / `simp` — failure here is a harness bug. |
| `mathd_algebra_10` | `120% of 30 − 130% of 20 = 10`. Pure arithmetic; tests that the prompt template and numeric literal handling work end-to-end. |
| `mathd_algebra_251` | Solve `3 + 1/x = 7/x`. Smallest non-trivial algebra step — division by `x` — catches models that skip the `x ≠ 0` side condition. |

### B. Mid-difficulty competition (5)

| Name | Why this specific problem |
|---|---|
| `imo_1964_p1_1` | Short, classical: `7 ∣ 2^n − 1 ⇒ 3 ∣ n`. Number-theoretic case analysis on `n mod 3`. Expected partial success across the pool. |
| `imo_1979_p1` | Wolstenholme-style alternating sum `p/q = Σ ±1/k` for `k = 1..1319`; show `1979 ∣ p`. Reasoning-heavy; expected near-uniform failure. |
| `aime_1988_p3` | Logarithm-substitution puzzle, single numerical answer. Tests whether models can do change-of-base symbolic manipulation. |
| `aime_1991_p1` | Symmetric-system integer puzzle (`xy + x + y = 71`, `x²y + xy² = 880`). Tests integer reasoning over algebraic manipulation. |
| `aime_1996_p5` | Roots-of-cubic identity using elementary symmetric polynomials. Tests whether the pool can use Vieta-style structure. |

### C. Strongest contamination probe — edited from v1, v2c ≠ v2s (5)

| Name | Why this specific problem |
|---|---|
| `amc12a_2008_p4` | Telescoping product `(8/4)(12/8)…(2008/2004)`. The v1 form pre-simplified the answer; v2c keeps the original multiple-choice form. |
| `amc12a_2009_p5` | Cube-with-perturbed-dimensions volume problem. v2c keeps original answer-choice framing. |
| `amc12_2001_p2` | `P(n) = S(n) + ...` digit-sum/product puzzle. Edited statement; tests memorization of the v1 form. |
| `amc12b_2004_p3` | `2^x · 3^y = 1296`. Multiple-choice form retained in v2c. Short and clean — easy to read errors. |
| `imo_1984_p2` | Exhibit `(a,b)` with `7 ∤ ab(a+b)` and `7^7 ∣ (a+b)^7 − a^7 − b^7`. The v2c statement is an existence claim; v1 was differently phrased. |

### D. Unchanged from v1 — memorization-friendly control (3)

| Name | Why this specific problem |
|---|---|
| `algebra_amgm_faxinrrp2msqrt2geq2mxm1div2x` | Classic AMGM consequence `2 − √2 ≥ 2 − x − 1/(2x)`. Identical to v1 — likely in pre-training. |
| `mathd_algebra_119` | Two-equation linear system over integers. Trivial human proof; ideal control: if models fail here but pass stratum C, contamination is unlikely. |
| `mathd_algebra_433` | Evaluate `f(8)` for `f(x) = 3√(2x−7) − 8`. Identical to v1; simple closed form. |

### E. Number theory tactic stress (4)

| Name | Why this specific problem |
|---|---|
| `mathd_numbertheory_81` | `71 mod 3 = 2`. Pure `decide` / `norm_num` territory — observes whether models reach for the right closer. |
| `mathd_numbertheory_132` | `2004 mod 12 = 0`. Same family as 81, but a different divisor — checks consistency of tactic choice. |
| `mathd_numbertheory_252` | `7! mod 23`. Forces a factorial expansion + modular reduction. Tests `omega` overreach vs. structured `Nat.factorial` reasoning. |
| `numbertheory_sqmod3in01d` | `∀ x : ℤ, x² mod 3 ∈ {0, 1}`. Universally quantified; pushes models toward `decide`/`omega` vs. case-on-`x mod 3`. |

### F. Inequalities — polyrith/nlinarith stress (3)

| Name | Why this specific problem |
|---|---|
| `algebra_sqineq_2unitcircatblt1` | `a² + b² = 2 ⇒ ab ≤ 1`. One-line `nlinarith` candidate; tests whether the pool reaches for it. |
| `algebra_apb4leq8ta4pb4` | `(a+b)^4 ≤ 8(a^4 + b^4)`. Right at the boundary of what `nlinarith`/`polyrith` close automatically; useful for diagnosing overreach. |
| `algebra_amgm_prod1toneq1_sum1tongeqn` | AMGM in product form. Beyond `nlinarith`'s reach — exposes how models fail when the heavy closers don't work. |

### G. Induction (3)

| Name | Why this specific problem |
|---|---|
| `induction_sum2kp1npqsqm1` | `Σ_{k=0}^{n-1} (2k+3) = (n+1)² − 1`. Tests basic `Finset.sum_range_succ` discipline. |
| `induction_divisibility_3divnto3m2n` | `3 ∣ n³ + 2n`. Combines `induction` with a modular-arithmetic step in the inductive case. |
| `induction_ineq_nsqlefactn` | `n² ≤ n!` for `n ≥ 4`. Has a non-trivial base case threshold — exposes off-by-one induction mistakes. |

### H. Hard / specialist-prover failure proxy (4)

| Name | Why this specific problem |
|---|---|
| `imo_1961_p1` | Solve the system `x + y + z = a`, `x² + y² + z² = b²`, `xy = z²`. Multi-equation, mixed-variable elimination. |
| `imo_1966_p5` | Linear system over `\|a_i − a_j\|` coefficients. Case analysis on the order of `a_1..a_4`; long even for humans. |
| `imo_1977_p5` | Characterize `(a,b)` for which `q² + r = 1977`, where `q,r` come from dividing `a²+b²` by `a+b`. Combines number theory with case enumeration. |
| `imo_2006_p3` | The classic `ab(a²−b²) + bc(b²−c²) + ca(c²−a²) ≤ M(a²+b²+c²)²` problem. Famous, hard, and a strong test of whether the pool can produce *any* coherent attempt. |

## Notes for the human-baseline pipeline

- Strata A, D, E, G are highest-yield for the Zulip recruitment (humans
  finish in minutes).
- Stratum H is the lowest-yield; I will write at least 2 of the 4 myself and
  treat any Zulip contributions as bonus coverage.
- Stratum C problems must be human-verified against the **v2c** statement
  specifically (not v1); the recruitment template will paste the v2c
  `formal_statement` verbatim so contributors don't accidentally prove the
  v1 form.
