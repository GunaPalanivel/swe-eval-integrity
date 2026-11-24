# From a problem to an evaluation

An evaluation should answer a stated question with observable evidence. A useful
question is narrow enough that one controlled experiment could disprove its
prediction. This is a working method for this project, not an operator's
submission policy or a statement that a task passed external review.

## 1. Select a problem

Start with a public incident, a reproducible defect, or an independently created
engineering scenario. Record the source, publication rights and what was
actually observed. A source report suggests a mechanism; reproduce that
mechanism before claiming it is present in a new environment.

Write the correctness property and a concrete counterexample. Ask whether the
task measures a useful capability and whether an existing task already measures
the same outcome. Keep rejected candidates and contradictory evidence. A more
complicated setup is not evidence of a more meaningful task.

## 2. Freeze the question and scope

Define the allowed inputs, tools, environment, completion condition, resource
budget and scoring rule before measurement. Separate a successful outcome from
one preferred implementation. List valid alternatives and boundary cases.

Record a prediction, the comparison that could refute it and any planned
exclusions. Identify the exact source and input revision. A change to the
problem, evaluator or environment creates a new revision; it must not silently
inherit earlier results.

## 3. Construct the task and evaluator

Build the smallest environment that produces the intended fault and exposes
enough information to solve it. Verify the underlying scientific or engineering
assumptions using primary sources and direct execution where possible.

An evaluator checks the requested state or behavior. It should accept correct
alternatives, reject plausible wrong results and report errors separately from
task failure. Reconstruct aggregate reward from case-level outcomes and declared
workload sizes. A report file is a claim to check against those records.

Document trust boundaries: what the agent may change, what the evaluator reads,
and which records establish completion. Test whether empty, partial, stale or
malformed outputs can receive credit. The control must exercise the same
artifact and evaluator as the measured run.

## 4. Check the measurement before using it

Run a known correct solution, a no-op and a plausible wrong solution. Add
counterexamples for the particular mechanism, including valid alternatives.
Where a grader trusts a generated report, deliberately alter its counts or
input identity and check that reconciliation rejects it.

These controls answer different questions. A correct solution shows at least
one achievable path. A no-op tests accidental credit. A wrong solution tests a
known false pass. None proves the absence of other defects. Retain failures and
have a separate reviewer inspect the consequential claims.

## 5. Measure a fixed revision

Capture the exact evaluated artifact, harness, model identifier, configuration,
budgets, environment and scoring rule. Record each eligible attempt, its outcome
and any exclusion or cancellation reason. Keep infrastructure errors distinct
from unsuccessful agent behavior.

Report counts and denominators before percentages. State whether observations
come from local execution, a platform receipt or re-analysis of saved outputs.
Repeated attempts can share dependencies and are not automatically independent
samples. Explain the sampling design and uncertainty before generalizing.

## 6. Investigate trajectories

Begin with a research question and inspect a sample of trajectories before
defining labels. Write observable signals for each category, preserve ambiguous
cases and check labels against source material. Validate automated scanners on
examples outside their development set and report disagreements.

Compare a predicted failure mechanism with what actually occurred. Distinguish
the first consequential error from later symptoms. Use a controlled change to
test the proposed cause. A fluent explanation of a transcript is a hypothesis
until evidence distinguishes it from alternatives. The [AISI transcript
workflow](https://www.aisi.gov.uk/blog/a-pipeline-for-transcript-analysis-using-inspect-scout)
is a primary reference for question-led inspection and scanner validation.

## 7. Deliver a bounded finding

Connect the claim to exact inputs, commands, outputs and limitations. Publish
the independent reproduction when rights permit. Describe inaccessible evidence
and the resulting limit on public verification. Local controls do not establish
platform acceptance, a general model capability gap or a productivity benefit.

If the result contradicts the prediction, retain it and revise the hypothesis.
If a repair changes the evaluated bytes, rerun the relevant controls and report
the new revision. The useful output is an auditable finding, including a finding
that a promising task or explanation did not survive testing.
