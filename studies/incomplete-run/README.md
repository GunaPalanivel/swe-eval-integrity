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
