# Reward reconstruction

Can a report with a plausible score conceal an inconsistent case count? This
independent artificial example checks the recorded outcomes against a fixed case
catalog before accepting the report. It contains no model run or performance claim.

Prediction, recorded before implementation on 2026-11-25: the five outcomes yield
3/5 overall. A report claiming six cases must fail even when its score remains 0.6.

| Workload | Recorded outcomes | Passed / cases | Score |
| --- | --- | --- | --- |
| sorting | maple-01: 1, maple-02: 1, maple-03: 0 | 2 / 3 | 0.6666666666666666 |
| lookup | birch-01: 1, birch-02: 0 | 1 / 2 | 0.5 |
| Overall | All five cases | 3 / 5 | 0.6 |

The overall score counts cases equally. Averaging the two workload scores would
give 7/12 and is a different calculation. `reproduce.py` checks an independent
`fractions.Fraction(3, 5)` calculation and both workload fractions against the
implementation. The records are constructed examples, not observations of an agent.

From the repository root, with Python 3.11 or newer:

```console
python studies/reward-reconstruction/reproduce.py
python -m unittest discover -s tests -v
```

The script reads the four files in `inputs/`, validates the correct report, rejects
`wrong-count-report.json`, compares the output with `results.json`, and prints JSON.
It writes no files and needs no installation, network, model, or third-party package.

The CLI accepts the same three inputs. Set `PYTHONPATH=src` in your shell first:

```console
python -m swe_eval_integrity studies/reward-reconstruction/inputs/catalog.json studies/reward-reconstruction/inputs/outcomes.json studies/reward-reconstruction/inputs/report.json
```

Replace the last filename with `wrong-count-report.json` to exercise rejection.
Success exits 0 and prints `valid: true`. Invalid data exits 1 and prints
`valid: false` with an error; incorrect argument count exits 2.

The catalog fixes the workload counts and unique case identities. Outcomes must
contain exactly one integer score, either 0 or 1, for every catalog case. The
outcomes bind the catalog hash, and the report binds both input hashes. The report
must reproduce every count and score, including each workload. Unknown fields,
missing or duplicate cases, duplicate JSON keys, boolean numbers, and nonfinite
numbers are rejected. Supported schema version is integer 1.

Hashes use SHA-256 over compact JSON encoded as UTF-8, with object keys sorted,
`ensure_ascii=False`, and nonfinite constants forbidden. Array order remains
significant. Formatting and object-key order do not change identity. Reports use
exact Python division results serialized as JSON numbers; rounded approximations
are rejected. Hashes detect disagreement, not authenticity: someone who controls
all inputs can replace all hashes too.

On 2026-11-25, the first permissive validator failed the wrong-count regression:
`AssertionError: ValueError not raised`. A second baseline probe used the full
valid catalog and outcomes, reconstructed their valid identities, then deliberately
ignored the supplied report; the isolated wrong-count regression again failed.
The implemented validator passed all 17 tests. The replay produced:

```json
{
  "expected_fraction": "3/5",
  "valid_report_accepted": true,
  "wrong_count_report_rejected": true,
  "wrong_count_error": "report case_count disagrees with reconstructed outcomes"
}
```

This excerpt comes from the actual replay; the complete deterministic output is
saved in `results.json`. Tests also exercise changed catalogs, a stale report after
outcomes change while totals stay constant, wrong workload summaries, incomplete
coverage, duplicate cases, malformed JSON, and CLI exit codes.

Counterevidence and limits: an unchanged 0.6 score alone cannot identify the wrong
case count. Canonical hashing intentionally ignores formatting changes. This study
checks consistency of recorded binary outcomes; it does not establish whether a
case passed correctly, whether the case catalog is representative, or whether an
agent is reliable. No historical evaluation results are reproduced here.
