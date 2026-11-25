"""Collect all integer readings, recording a parse failure per instrument."""

import json
import sys


def collect(readings):
    rows = []
    for instrument, raw in readings.items():
        try:
            value = int(raw)
        except ValueError:
            rows.append({"instrument": instrument, "status": "parse_error"})
        else:
            rows.append({"instrument": instrument, "status": "complete", "value": value})
    return rows


if __name__ == "__main__":
    print(json.dumps(collect(json.load(sys.stdin))))
