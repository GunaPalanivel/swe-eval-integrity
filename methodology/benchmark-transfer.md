# What evidence survives a benchmark port?

A published benchmark can supply a useful engineering problem, an executable
reference and a measured baseline. Each supports a different claim. When
selecting a source, identify the claim the next experiment needs.

| Question | What to inspect | What to do when it changes |
|---|---|---|
| Was the source evaluated? | Source revision, evaluator, run record, and the decision actually recorded for that revision. | Describe a published task with no comparable decision as a precedent. |
| Does the port award credit for the same work? | Candidate-visible inputs, observable deliverable, unit of credit, case weights and accepted alternatives. | Replay the same outputs through both rules where possible. Identify which cases gain or lose credit. |
| Does a completed run support the reported number? | Expected trial identities, terminal states, exceptions, actual verifier outputs and artifact identity. | Preserve an errored or missing trial as such. A successful wrapper exit can coexist with a missing measurement. |
| Did a model find the new version difficult? | Model, effort, harness, tools, budget, eligibility policy and per-attempt results on the new revision. | Run a matched comparison, or report the original result with its original configuration. |

A green reference and an empty starting state establish two endpoints. Between
them, try an output assembled entirely from the request and a plausible
implementation that completes only part of the job. If the task admits a
successful empty or infeasible outcome, exercise that branch with both a
justified answer and a guess. A simple method that satisfies the published
contract deserves the credit it earns.

Review the engineering question separately from the executable. Name the
person who uses the output, the decision they make, and the evidence needed
to make it. Confirm that the public contract states what is graded. A correct
test executable cannot establish whether another engineer could have inferred
an unstated requirement.

Keep a record for each submitted revision. A queue status shows progress, a
stage verdict identifies what was checked, and a final decision belongs to
the evaluated artifact. Group results by source and revision before counting
failures. An unresolved attempt has no measured outcome yet.
