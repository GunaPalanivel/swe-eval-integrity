# Reproducing the independent demonstration

Run commands from the repository root with Python 3.11 or later. The tests and
demonstration use only the Python standard library. They need no model service,
credentials, network access or private workspace. Use `python3` or `py -3` in
place of `python` if that is how your system selects the intended interpreter.

## Run the checks

```text
python --version
python -m unittest discover -s tests -v
python studies/reward-reconstruction/reproduce.py
```

The first command records the interpreter. The second runs the regression
suite. The third compares a reconstruction with the study's saved expected
output and exercises the deliberate wrong-count report. It prints JSON and
must exit zero on agreement. It does not rewrite inputs or saved results.

The expected independent calculation is `3 / 5 = 0.6`. The two workloads contain
three and two cases. The consistent report should be accepted and the report
with altered counts should be rejected. Read the
[study](studies/reward-reconstruction/README.md) for the prediction, exact inputs,
controls and limits. These are expected outcomes, not a declaration that this
revision has already passed execution. Record actual command output before
claiming a successful repetition.

## Use the report checker

The module takes three positional paths: the case catalog, case outcomes and a
report to validate. With the repository's `src` directory on `PYTHONPATH`:

PowerShell:

```powershell
$env:PYTHONPATH = 'src'
python -m swe_eval_integrity catalog.json outcomes.json report.json
```

Bash:

```bash
PYTHONPATH=src python -m swe_eval_integrity catalog.json outcomes.json report.json
```

Replace these three filenames with your actual inputs. A matching report emits
JSON with `valid: true` and the reconstruction, and exits zero. Invalid data or
an inconsistent report emits `valid: false` and exits one. Incorrect argument
count exits two. Rejecting a deliberately invalid report is the expected
behavior, so that command's nonzero exit is not a failed control.

The checker hashes compact, sorted-key UTF-8 JSON, preserving array order.
Whitespace and object-key order do not affect these hashes. They identify the
canonical JSON representation, not original file bytes. Scores must match the
reconstruction exactly; this binary-reward demonstration does not use a floating
point tolerance. It checks consistency of supplied records, not whether those
records describe a genuine external run.

## Continuous integration and packaging

The workflow targets Python 3.11 and 3.13 on Ubuntu and Windows. It runs the same
unit-test and demonstration commands with `PYTHONPATH=src`. The matrix describes
the intended checks; consult the actual workflow result for a particular
commit before claiming coverage.

No installation is required for those checks. If a `pyproject.toml` is present,
an optional `python -m pip install --no-deps .` makes the module available
without setting `PYTHONPATH`. Building a package may fetch its build backend;
it is separate from the dependency-free source execution above. For a fully
offline package build, preserve the declared backend and its dependencies in
advance and document their versions and hashes.

## Repeat later

Record the Git commit, OS, architecture, exact Python version, commands, exit
codes and output. Preserve source, study inputs and saved results together.
This deterministic study has no random seed or external model. If a later
study introduces either, preserve the seed, model identity, provider date,
configuration and the limits of replay.

For a release, archive the cleared source and outputs with file checksums,
store a separate backup and test restoration into a fresh checkout. A saved
result supports future re-analysis even when an original service is absent.
Neither an archive nor a locked environment guarantees execution on future
hardware. See [measurement and evidence](methodology/measurement-and-evidence.md)
for the evidence and disclosure records that must accompany a result.
