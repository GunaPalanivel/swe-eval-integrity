# SWE Eval Integrity

Can a coding agent solve a software engineering task, and can we trust the
score used to answer that question?

A plausible score can hide an incomplete test run, an incorrect grader, or an
invalid comparison across attempts. This project develops checks for those
failure modes and records what each check establishes. The research covers
task design, Harbor-based execution, verifier integrity, model measurement and
trajectory analysis.

## Run the first study

With Python 3.11 or later, run from the repository root.

```sh
python studies/reward-reconstruction/reproduce.py
python -m unittest discover -s tests -v
```

The study reconstructs a score of `3/5 = 0.6` from five artificial outcomes.
It rejects a report that claims six cases while reporting the same score. The
replay uses saved inputs and the Python standard library.

## What the research checks

| Question | Evidence |
| --- | --- |
| Does the task measure a useful capability? | A documented behavior, an independent expected outcome, and a case that distinguishes a correct solution from a plausible wrong one. |
| Can the grader tell? | A reference implementation, an untouched starting state, and targeted wrong and alternative solutions evaluated on the same artifact. |
| How difficult is the task for an agent? | Eligible attempts under a recorded model, harness, effort and budget. Retain individual scores, exceptions and exclusions. |
| Why did an attempt fail? | Identify the first consequential error and distinguish solver, specification, evaluator and environment failures. |

The [evaluation protocol](methodology/evaluation-protocol.md) describes the
stages and model roles. Observed configurations include Claude Opus 5.5 at
`xhigh` for difficulty evaluation and `kimi-k3.1-pro` for quality review.
The public study measures report consistency with artificial inputs.

- [Evaluation lifecycle](methodology/evaluation-lifecycle.md)
- [Measurement and evidence](methodology/measurement-and-evidence.md)
- [Reward reconstruction study](studies/reward-reconstruction/README.md)
- [Reproduction instructions](REPRODUCING.md)
- [Research references](references/sources.bib)

Maintained by GunaPalanivel. Cite the exact revision using [CITATION.cff](CITATION.cff).
Source and independently authored examples are available under the [MIT license](LICENSE).
