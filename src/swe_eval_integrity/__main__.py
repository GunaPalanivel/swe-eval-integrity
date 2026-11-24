"""Validate a saved report against its catalog and outcomes."""

import json
import sys

from .reward import load_json, validate_report


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 3:
        print(json.dumps({"valid": False, "error":
                          "usage: python -m swe_eval_integrity <catalog.json> <outcomes.json> <report.json>"}))
        return 2
    try:
        report = validate_report(*(load_json(path) for path in args))
    except (OSError, ValueError, OverflowError, RecursionError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, sort_keys=True))
        return 1
    print(json.dumps({"valid": True, "reconstructed": report}, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
