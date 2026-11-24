"""Replay the independent reward-reconstruction study without writing files."""

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from swe_eval_integrity.reward import load_json, validate_report


def reproduce():
    study = Path(__file__).resolve().parent
    inputs = study / "inputs"
    catalog = load_json(inputs / "catalog.json")
    outcomes = load_json(inputs / "outcomes.json")
    report = load_json(inputs / "report.json")

    # Hand-counted from the five recorded outcomes, independently of the scorer.
    expected_workloads = {"lookup": (1, 2), "sorting": (2, 3)}
    expected_fraction = Fraction(1 + 2, 2 + 3)
    reconstructed = validate_report(catalog, outcomes, report)
    if reconstructed["score"] != float(expected_fraction):
        raise AssertionError("overall score differs from the independent calculation")
    for name, (passed, count) in expected_workloads.items():
        expected = {"case_count": count, "passed_count": passed,
                    "score": float(Fraction(passed, count))}
        if reconstructed["workloads"][name] != expected:
            raise AssertionError(f"{name} differs from the independent calculation")
    try:
        validate_report(catalog, outcomes, load_json(inputs / "wrong-count-report.json"))
    except ValueError as exc:
        wrong_report_error = str(exc)
    else:
        raise AssertionError("deliberately wrong report was accepted")
    return {
        "study": "reward-reconstruction",
        "evidence_scope": "independent artificial example; no model execution",
        "expected_fraction": str(expected_fraction),
        "valid_report_accepted": True,
        "wrong_count_report_rejected": True,
        "wrong_count_error": wrong_report_error,
        "reconstructed": reconstructed,
    }


if __name__ == "__main__":
    result = reproduce()
    if result != load_json(Path(__file__).resolve().parent / "results.json"):
        raise AssertionError("replayed result differs from saved results.json")
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
