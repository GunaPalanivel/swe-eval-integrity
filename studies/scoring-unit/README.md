# Does the unit of partial credit change what a score measures?

## Prediction recorded November 26, 2026

A file converter carries a record ID through each conversion and represents a
rate as a fraction in lowest terms with a positive denominator. Suppose we
give one point for preserving the ID and one for producing the canonical
fraction. A converter that copies its input should receive half the points
even if it converts none of the rates. If a point requires a complete usable
record, the same output should earn zero on these inputs.

Use four invented rows. The expected output is written out so a reader can
check it by hand.

| ID | Input fraction | Expected fraction |
|---|---|---|
| alder | 8/12 | 2/3 |
| birch | 15/25 | 3/5 |
| cedar | 6/-8 | -3/4 |
| elm | -10/-15 | 2/3 |

Hold the rows, contract and candidate outputs fixed. Change only the unit of
credit. Use an empty submission, an input copier, a reducer that forgets to
normalize the sign, and a correct converter. Predict whole-record scores of
0, 0, 1/2 and 1 respectively. A second correct implementation should receive
the same score. As a counterexample, copying an already canonical fraction
should earn full credit on that record. The grader observes output.

This is a deterministic study of scoring. Measuring the effect on agent
difficulty would require new attempts on each revision.

## Observations

| Candidate | Points per field | Points per complete record |
|---|---:|---:|
| Empty | 0 | 0 |
| Copy the input | 0.5 | 0 |
| Reduce by the GCD, keep the denominator sign | 0.75 | 0.5 |
| Reduce and normalize the sign | 1 | 1 |
| Python fraction library | 1 | 1 |

The two endpoint checks agree under both rules. Only the intermediate controls
expose the difference. The sign-blind reducer produces usable records for
alder and birch. Counting completed records preserves that partial credit.
If preserving record IDs were itself a capability of interest, scoring it
separately could serve a different research question.

Run `python studies/scoring-unit/reproduce.py` from the repository root.
The script checks the observed values against [the saved results](results.json).
The [control tests](../../tests/test_scoring_unit.py) also exercise already
canonical input and reordered records.
