# Evaluation protocol and model roles

The outcome is a defensible claim about software engineering behavior. Start by
identifying what evidence would support or refute that claim. Select a small
testable problem, write down the expected outcome, and preserve the result when
the experiment contradicts the prediction.

## Checks from task design to analysis

| Stage | Question it answers | Evidence to record |
| --- | --- | --- |
| Problem selection | Is the outcome useful and tied to a real engineering decision? | Primary source, correctness property, simplest plausible solution, and a discriminating case. |
| Package validation | Can a clean environment build and run the intended artifact? | Bundle hash, manifest, image identity, inputs, and commands. |
| Similarity review | Does the task measure substantially distinct work? | Comparison of objectives, interfaces, source area, solution and tests against the available corpus. |
| Quality review | Do the instructions, verifier and reference agree? | Public requirements, assertions, tolerance rationale, valid alternatives, and reproduced review findings. |
| Oracle and no-op | Does a reference implementation reach the intended score, and what does the untouched starting state earn? | Completed repeated controls, raw rewards, and verifier evidence for the exact package. |
| Negative and alternative controls | Does the evaluator reject specific incorrect behavior and accept equivalent correct behavior? | Expected outcome for each control, observed result, and why the case distinguishes the two. |
| Adversarial evaluation | Can an attempt earn credit without satisfying the contract? | Score, trajectory, observed behavior, and its relation to the specified outcome. |
| Difficulty evaluation | How much can the target configuration solve? | Per-attempt score, eligibility, budget, configuration, exclusions, and scoring rule. |
| Trajectory review | Which mechanism explains the result? | The consequential decision or event, competing explanations, and a replay or controlled comparison when possible. |

For containerized tasks, test the exact packed artifact and the handoff into a
fresh verifier. Confirm that reference and no-op outcomes are valid completed
runs. Diagnose infrastructure errors from the underlying logs before interpreting
a score. Version the eligibility rules, thresholds and normalization for each
study because they determine the meaning of the reported result.

## Why models have different roles

| Role | Observed configuration | Why the role exists |
| --- | --- | --- |
| Strong coding agent | Claude Opus 5.5 at `xhigh` | Measures achievable credit for a capable software engineering agent under a fixed harness and budget. Repeated attempts characterize variability. |
| Quality reviewer | `kimi-k3.1-pro`, effort unrecorded | Reads the contract and evaluator together and flags discrepancies to investigate with executable witnesses or source review. |
| Adversarial agent | Configuration unrecorded in this public account | Looks for ways to earn credit through a behavior the evaluator may accept erroneously. The trajectory determines the interpretation. |
| Deterministic checker | Python standard library | Recalculates report totals from public case records so anyone can reproduce the first study. |

The model names are configuration labels reported by the maintainer on
2026-11-25. The evidence identifies the assignments. The original model
selection rationale, exact provider snapshots and comparable head-to-head runs
are unavailable. These role descriptions explain what a configuration measures.

For future model selection, choose the target capability first. Start with an
agent that can use the required tools and complete a known-positive control.
Choose effort and budget before measurement. For a reviewer, compare findings
with independently labeled valid and defective examples. To assess a proposed
model change, use the same task bytes, scorer, tools, resource budget and
attempt policy across configurations. Retain failures and report the sampled
population explicitly.

## How the repository follows established work

| Research repository | Practice applied here |
| --- | --- |
| [SWE-bench](https://github.com/SWE-bench/SWE-bench) | Give the reader the engineering question and a runnable reference check up front. Its codebase-and-issue tasks motivate checking software behavior through execution. |
| [Inspect](https://github.com/UKGovernmentBEIS/inspect_ai) | Document inputs, solver, environment and scoring so model choice and grader behavior can be tested independently. Its user guide describes these task components and model roles. |
| [METR's evaluation analysis](https://github.com/METR/eval-analysis-public) | Keep versioned run data with analysis and regeneration commands. Its time-horizon analysis also motivates recording task population and uncertainty. |

A public study in this repository records a question, prediction, smallest
discriminating experiment, inputs, command, observed result and limits. A second
reader should be able to recompute the result and describe what would change the
conclusion. See the [measurement guide](measurement-and-evidence.md) for the
record fields and [research references](../references/sources.bib) for the
underlying papers and software.
