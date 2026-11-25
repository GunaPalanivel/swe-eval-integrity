# Can a successful batch contain a missing measurement?

## Prediction recorded November 26, 2026

An offline batch collector is configured to continue after an individual
input fails. One input is a valid zero, one is a valid positive value and one
fails to parse. The collector should exit zero after recording all three
attempts. A consumer checking only that exit code would call the batch
complete. A consumer that requires a numeric observation for each expected
attempt should identify the failed input and withhold the aggregate.

Run the same collector after correcting that input. Predict a completed
three-attempt batch including the genuine zero. The experiment isolates
completion reporting from the value of the measurement.

## Observations

| Input to the third instrument | Collector exit | Recorded values | Mean |
|---|---:|---|---|
| `unreadable` | 0 | 0, 3, parse error | Withheld |
| `6` | 0 | 0, 3, 6 | 3 |

Treating the failed reading as zero would yield 1. Dropping it would yield
1.5. Both calculations silently change what the mean represents. The consumer
requires one completed integer reading for each expected instrument, including
the instrument that genuinely returned zero.

Run `python studies/incomplete-run/reproduce.py` from the repository root.
It executes [the collector](collect.py) and compares both raw row sets, exit
codes and aggregation decisions with [the saved record](results.json).
This small collector demonstrates the failure mode. The experiment estimates
neither its frequency in other harnesses nor any agent's capability.
