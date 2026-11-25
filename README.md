# SWE Eval Integrity

SWE Eval Integrity tests whether a coding-agent score is supported by the work
the agent completed. It gives benchmark authors and harness maintainers three
offline experiments they can run when reviewing a grader, porting a benchmark
or interpreting a batch of trials.

## What can go wrong with a score?

| Question | Experiment | Observed result |
|---|---|---|
| Can an incomplete implementation earn credit just by copying inputs? | [Change the unit of credit](studies/scoring-unit/README.md). Grade the same fraction converters by field and by completed record. | The copier earns 0.5 by field and 0 by record. Both correct converters earn 1 under either rule. |
| Can a successful process leave a measurement missing? | [Inspect a batch after it exits](studies/incomplete-run/README.md). Change one instrument reading and rerun the same collector. | Both processes exit zero. Only the batch with three numeric observations has a mean. |
| Can a report give the right score and still have the wrong denominator? | [Reconstruct the reward](studies/reward-reconstruction/README.md) from a fixed catalog and per-case outcomes. | Three of five cases passed. A report claiming six cases with the same score is rejected. |

These results come from independently authored inputs and deterministic Python
programs. Each study includes its prediction, controls and saved result.
With Python 3.11 or later, run these commands from the repository root:

```sh
python studies/scoring-unit/reproduce.py
python studies/incomplete-run/reproduce.py
python studies/reward-reconstruction/reproduce.py
python -m unittest discover -s tests -v
```

## Applying the results to agent evaluations

**Before reusing a benchmark**, identify the evaluated revision, what counted
as a success, and which information the agent received. A change to partial
credit can change the interpretation of a result even if the reference still
earns full marks. [Benchmark transfer](methodology/benchmark-transfer.md)

**When diagnosing a failed run**, locate the first stage with contrary evidence.
Package construction, quality review, reference controls, adversarial attempts
and difficulty trials answer different questions. Record the raw outcome and
the exact evaluated artifact at that stage. [Evaluation lifecycle](methodology/evaluation-lifecycle.md)

**When reporting model performance**, identify who attempted the task and who
judged it. Observed configurations include Claude Opus 5.5 at `xhigh` for
difficulty trials and `kimi-k3.1-pro` for quality review. The public replays
require no model or credentials. [Model roles and protocol](methodology/evaluation-protocol.md)

[Reproduce the studies](REPRODUCING.md) · [Evidence and preservation](methodology/measurement-and-evidence.md) · [Research references](references/sources.bib) · [Cite the repository](CITATION.cff)
