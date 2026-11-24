# Measurement and evidence

A result needs both a calculation and an account of how its inputs were
obtained. Reproducing arithmetic from saved records supports that calculation;
it does not establish that a historical run occurred as described.

## Name the evidence scope

| Evidence | What a reader can check | Limit |
| --- | --- | --- |
| Independent demonstration | Public inputs, code, controls and saved expected output | Does not measure a client task or a deployed model |
| Local repetition | A recorded command and environment executed the experiment again | Applies to that revision and environment |
| Platform-reported observation | A receipt reports a particular outcome for an identified artifact | Public verification depends on access to the receipt and its provenance |
| Saved-result re-analysis | A specified calculation produces a result from preserved inputs | Does not rerun the original model or service |
| Hypothesis | A prediction and proposed discriminating test | Has not yet been established by that test |

These labels describe different evidence, rather than levels that automatically
imply one another. [ACM's artifact criteria](https://www.acm.org/publications/policies/artifact-review-and-badging-current)
likewise distinguish availability, artifact evaluation and results validation.

## Make the calculation auditable

Identify the unit being scored and the complete expected case set. Record each
case outcome exactly once, check workload membership, and reject missing,
duplicate or unexpected cases. Specify how case weights and workload sizes
affect the aggregate. A mean of workload means can differ from a mean across
all cases when workload sizes differ.

Bind a report to the exact input bytes using content hashes. Reconstruct totals
from the case records, then compare the report's counts and score using a
declared numerical tolerance. Test a deliberately inconsistent report. Hashes
detect changes to bytes; they do not establish authorship or truth of the data.

For model experiments, state sample size, eligible attempts, exclusions,
cancellations, model and harness versions, budgets, scoring rule and uncertainty.
Retain individual results so readers can inspect sensitivity to aggregation or
exclusions. Never invent an unrecorded model setting or turn an infrastructure
failure into a capability finding.

## Preserve an evidence record

For each study, keep the question, dated prediction, alternatives, source
references, expected controls, observations, disagreements and next decision.
For each run, retain:

- An experiment ID, schema version, source commit and hashes of inputs, evaluated
  artifacts and saved outputs.
- Commands, exit codes, OS, CPU architecture, runtime and dependency versions,
  image digests when used, resource limits, seeds and nondeterministic settings.
- Raw case outcomes, the raw-to-result calculation, exclusion reasons and any
  justified numerical or semantic tolerance.
- Model and provider identifiers and observation date when applicable. Identify
  the source of known settings and explicitly record unknown settings.
- Authorship, source and data licenses, third-party notices, access requirements
  and the publication decision for each artifact.

The [FAIR4RS principles](https://www.nature.com/articles/s41597-022-01710-x) and
[software citation principles](https://peerj.com/articles/cs-86/) inform these
metadata and versioning practices. They do not validate an experiment's design.

## Keep public and restricted evidence separate

Only independently owned or specifically cleared material may enter a public
release. Removing names does not clear task text, distinctive examples, hidden
cases, solutions, internal criteria or transcripts for publication. Generated
summaries and derived tables can reproduce the same restricted information.

Prepare an explicit file allowlist for each release. Review the staged files,
the complete history being published, generated outputs, archives, CI logs and
attachments. Scan for secrets and private paths, then manually inspect content
for task fingerprints and unsupported claims. A clean text scan is insufficient
to establish disclosure rights. Start public history from cleared files rather
than importing a private repository's history.

When evidence must remain restricted, state that limitation and narrow the
public claim. This project's independent demonstrations are not proxies for
unpublished scores, task acceptance or client outcomes.

## Plan for restoration

Preserve exact versions, source, licensed dependencies, environment records,
data hashes, seeds and saved outputs. Keep a checksummed release archive and a
separate backup, and periodically test retrieval and restoration. Public model
APIs may change or disappear; preserved outputs can still support re-analysis.
An environment lock or container does not guarantee future execution.

An actual archived source can be identified with a
[Software Heritage identifier](https://www.swhid.org/faq/). A cleared release may
be deposited through [Zenodo's software workflow](https://help.zenodo.org/docs/github/archive-software/github-upload/).
Do not claim an archive, DOI or release exists before checking it. Zenodo's
[policies](https://about.zenodo.org/policies/) do not guarantee future usability.

## Use literature tools as aids

Search tools, including PaperOrchestra, can suggest sources and help draft from
an approved evidence set. Open the primary source, check the relevant section,
verify bibliographic metadata and record conflicting findings before relying
on a generated claim. The [PaperOrchestra source](https://github.com/google-research/paper-orchestra)
is a reference, not a dependency of this repository. No complete generated
literature review or live provider-backed synthesis is claimed here.
