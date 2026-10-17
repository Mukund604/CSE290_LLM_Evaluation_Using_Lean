# Human tactic-proof baseline — contributor guide

Thanks for helping with this. This directory is the contributor-facing
package for the human baseline of the CSE 290Q project
*Diagnosing How Frontier LLMs Fail at Lean (revised)*.

## What you're contributing

One Lean 4 **tactic-mode** proof for one (or more) of the 30 problems in
`problems/`. The proofs are used as:

1. A tractability check (confirm each problem is humanly provable in the
   pinned toolchain).
2. A taxonomy validation reference (if humans reach for the same "misused"
   heavy tactic as a model, the failure category needs sharpening).
3. A shape comparison anchor (model vs. human proof length, tactic mix,
   lemma vocabulary).

## How to set up

```bash
cd human_baseline
# elan / lake should already be installed; see https://leanprover.github.io/
lake update           # pulls Mathlib at the pinned version
lake build            # confirms the toolchain works on your machine
```

The `lean-toolchain` and `lakefile.lean` are pinned to match the miniF2F-v2
release. **Do not change them in your PR.**

## How to write a proof

1. Open a file in `problems/`, e.g. `mathd_algebra_22.lean`. The header,
   imports, and `theorem ... := by` line are filled in for you; only edit
   below the `by`.
2. Replace the `sorry` placeholder with your tactic proof.
3. Add your name (or preferred handle) to the `-- Author:` line at the top.
4. Run `lake build` and confirm the file compiles with no `sorry` warnings.
5. Submit (see below).

## Rules

These exist so the proofs are useful as a baseline — they're not arbitrary.

- **Tactic mode only.** No term-mode proofs (`exact ⟨..., by ...⟩` is fine
  in passing; the top-level proof must be `by ...`).
- **No bare one-liner closers** as the entire proof. A single `decide`,
  `nlinarith`, `polyrith`, `omega`, or `aesop` does not count, even if it
  works. Use heavy tactics *inside* a structured proof. The few problems
  where `decide` is the natural full proof are noted in the file header.
- **Don't change the `theorem ... := by` line.** It is the v2c statement
  verbatim. Changing it invalidates the baseline.
- **Soft length cap: 50 lines.** Prefer `have` / `calc` / `induction` over
  one mega-tactic chain. Readability is part of the baseline.
- **Compile clean.** No `sorry`, no `admit`, no `set_option ... in` hacks
  to silence errors.

## How to submit — Zulip DM only

DM Mukund the completed `.lean` file on Zulip with subject
`[CSE290Q baseline] <problem name>`. He'll verify it compiles and confirm
receipt.

**Please do not open a pull request.** Submissions are kept private during
collection so no student sees another's proof before submitting their own.
The full proof set is published in the final report appendix at the end of
the project, with contributor attribution.

## Credit

Every accepted contribution lands in `CONTRIBUTORS.md` (public, name only
— no proof contents) and in the project report's appendix and
acknowledgments. Tell us if you prefer a different display name or want to
stay anonymous.

## Available problems

See `problems/` for the full list. Strata and rationales are documented in
the project-root `subset.md`.

| Stratum | Easy → hard (rough) |
|---|---|
| A. Easy algebra sanity | `mathd_algebra_22`, `mathd_algebra_10`, `mathd_algebra_251` |
| D. Memorization-friendly control | `mathd_algebra_119`, `mathd_algebra_433`, `algebra_amgm_faxinrrp2msqrt2geq2mxm1div2x` |
| E. Number theory | `mathd_numbertheory_81`, `mathd_numbertheory_132`, `mathd_numbertheory_252`, `numbertheory_sqmod3in01d` |
| G. Induction | `induction_sum2kp1npqsqm1`, `induction_divisibility_3divnto3m2n`, `induction_ineq_nsqlefactn` |
| F. Inequalities | `algebra_sqineq_2unitcircatblt1`, `algebra_apb4leq8ta4pb4`, `algebra_amgm_prod1toneq1_sum1tongeqn` |
| B. Mid-difficulty competition | `imo_1964_p1_1`, `imo_1979_p1`, `aime_1988_p3`, `aime_1991_p1`, `aime_1996_p5` |
| C. Contamination probe | `amc12a_2008_p4`, `amc12a_2009_p5`, `amc12_2001_p2`, `amc12b_2004_p3`, `imo_1984_p2` |
| H. Hard (specialist-failure proxy) | `imo_1961_p1`, `imo_1966_p5`, `imo_1977_p5`, `imo_2006_p3` |

If a problem already has a submitted proof, the file's `-- Author:` line
will be filled in. Pick an unclaimed one or message the channel.
