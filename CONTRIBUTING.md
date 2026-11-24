# Contributing

Start with the behavior that needs testing and a small input that distinguishes a correct implementation from a plausible incorrect one. Record the expected outcome before running the experiment.

## Changes

Keep each change focused. Add a regression for the observed failure, run it before the fix, and retain the expected and observed outcomes. Explain the reason for a change in the commit body when the diff alone is insufficient.

Run the tests and each affected study using the commands in `REPRODUCING.md`. Ask another reviewer to examine the requirements and implementation. Record remaining limitations alongside the result.

## Public material

Submit independently authored examples or material explicitly cleared for publication. Check source ownership, redistribution terms and attribution before adding code or data.

Review the entire published change, including Git history, generated results, release archives and CI attachments. Automated scans help find secrets and private paths. A person must also check whether text or data reveals confidential work.

Every study needs its question, prediction, inputs, expected result, command, observed result and limitations. Identify whether a result is a demonstration, a repeated experiment or a separately reviewed finding.

## Reproduction

Keep source and saved inputs in plain formats. Record exact dependency and environment versions where they affect the result. Make it possible to rerun saved-result analysis without a model provider or a private workspace.

If external services are required for a new experiment, state their configuration, cost and availability constraints before execution. Never commit credentials.
