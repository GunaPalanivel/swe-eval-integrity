"""Run the collector twice and reconcile observations against expected instruments."""

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def mean_if_complete(expected, rows):
    if not expected:
        raise ValueError("empty instrument catalog")
    observed = {}
    for row in rows:
        key = row["instrument"]
        if key not in expected or key in observed:
            raise ValueError(f"unexpected or duplicate instrument: {key}")
        if row.get("status") != "complete" or type(row.get("value")) is not int:
            raise ValueError(f"incomplete reading: {key}")
        observed[key] = row["value"]
    if observed.keys() != expected:
        raise ValueError("missing instrument")
    return sum(observed.values()) / len(expected)


def run_batch(inputs):
    command = [sys.executable, str(HERE / "collect.py")]
    process = subprocess.run(command, input=json.dumps(inputs), capture_output=True, text=True)
    process.check_returncode()
    rows = json.loads(process.stdout)
    try:
        mean = mean_if_complete(inputs.keys(), rows)
    except ValueError as error:
        mean, reason = None, str(error)
    else:
        reason = "all readings present"
    return {"exit_code": process.returncode, "rows": rows, "mean": mean, "reason": reason}


def reproduce():
    readings = {"north": "0", "south": "3", "east": "unreadable"}
    return {"failed_reading": run_batch(readings),
            "corrected_reading": run_batch({**readings, "east": "6"})}


if __name__ == "__main__":
    observed = reproduce()
    expected = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    if observed != expected:
        raise SystemExit("observed readings differ from results.json")
    print(json.dumps(observed, indent=2, sort_keys=True))
