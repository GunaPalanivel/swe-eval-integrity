"""Reconstruct binary rewards and reject inconsistent saved reports."""

import hashlib
import json
import math
from pathlib import Path


def _unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value):
    raise ValueError(f"nonfinite JSON number: {value}")


def load_json(path):
    """Read JSON without accepting duplicate keys or nonfinite constants."""
    return json.loads(
        Path(path).read_text(encoding="utf-8"),
        object_pairs_hook=_unique_keys,
        parse_constant=_reject_constant,
    )


def canonical_sha256(value):
    """Hash compact, sorted-key UTF-8 JSON; preserve array order."""
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _fields(value, names, label):
    if not isinstance(value, dict) or set(value) != set(names):
        raise ValueError(f"{label}: expected fields {', '.join(names)}")


def _integer(value, label, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{label}: expected integer >= {minimum}")


def _name(value, label):
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError(f"{label}: expected nonempty name without edge whitespace")


def reconstruct(catalog, outcomes):
    """Calculate counts and scores from one complete set of binary outcomes."""
    _fields(catalog, ("schema_version", "workload_counts", "cases"), "catalog")
    _integer(catalog["schema_version"], "catalog schema_version", 1)
    if catalog["schema_version"] != 1:
        raise ValueError("unsupported catalog schema_version")
    counts = catalog["workload_counts"]
    if not isinstance(counts, dict) or not counts:
        raise ValueError("workload_counts: expected nonempty object")
    for name, count in counts.items():
        _name(name, "workload")
        _integer(count, f"{name} count", 1)
    if not isinstance(catalog["cases"], list) or not catalog["cases"]:
        raise ValueError("cases: expected nonempty list")
    cases = {}
    actual_counts = dict.fromkeys(counts, 0)
    for case in catalog["cases"]:
        _fields(case, ("case_id", "workload"), "case")
        case_id, workload = case["case_id"], case["workload"]
        _name(case_id, "case_id")
        _name(workload, "case workload")
        if case_id in cases:
            raise ValueError(f"duplicate catalog case: {case_id}")
        if workload not in counts:
            raise ValueError(f"unknown workload: {workload}")
        cases[case_id] = workload
        actual_counts[workload] += 1
    if actual_counts != counts:
        raise ValueError("catalog cases disagree with fixed workload_counts")

    _fields(outcomes, ("schema_version", "catalog_sha256", "outcomes"), "outcomes")
    _integer(outcomes["schema_version"], "outcomes schema_version", 1)
    if outcomes["schema_version"] != 1:
        raise ValueError("unsupported outcomes schema_version")
    catalog_hash = canonical_sha256(catalog)
    if outcomes["catalog_sha256"] != catalog_hash:
        raise ValueError("outcomes catalog_sha256 does not match catalog")
    if not isinstance(outcomes["outcomes"], list):
        raise ValueError("outcomes: expected list")
    seen = set()
    passed = dict.fromkeys(counts, 0)
    for outcome in outcomes["outcomes"]:
        _fields(outcome, ("case_id", "score"), "outcome")
        case_id, score = outcome["case_id"], outcome["score"]
        _name(case_id, "outcome case_id")
        _integer(score, "outcome score")
        if score not in (0, 1):
            raise ValueError("outcome score: expected 0 or 1")
        if case_id not in cases:
            raise ValueError(f"unknown outcome case: {case_id}")
        if case_id in seen:
            raise ValueError(f"duplicate outcome case: {case_id}")
        seen.add(case_id)
        passed[cases[case_id]] += score
    if seen != set(cases):
        raise ValueError("missing outcomes for catalog cases")
    total_passed = sum(passed.values())
    return {
        "schema_version": 1,
        "catalog_sha256": catalog_hash,
        "outcomes_sha256": canonical_sha256(outcomes),
        "case_count": len(cases),
        "passed_count": total_passed,
        "score": total_passed / len(cases),
        "workloads": {
            name: {"case_count": counts[name], "passed_count": passed[name],
                   "score": passed[name] / counts[name]}
            for name in sorted(counts)
        },
    }


def _check_summary(actual, expected, label):
    for field in ("case_count", "passed_count"):
        _integer(actual[field], f"{label} {field}")
        if actual[field] != expected[field]:
            raise ValueError(f"{label} {field} disagrees with reconstructed outcomes")
    score = actual["score"]
    if type(score) not in (int, float) or (type(score) is float and not math.isfinite(score)):
        raise ValueError(f"{label} score: expected finite number, not boolean")
    if score != expected["score"]:
        raise ValueError(f"{label} score disagrees with reconstructed outcomes")


def validate_report(catalog, outcomes, report):
    """Return the reconstruction if every report field agrees exactly."""
    expected = reconstruct(catalog, outcomes)
    _fields(report, tuple(expected), "report")
    _integer(report["schema_version"], "report schema_version", 1)
    for field in ("schema_version", "catalog_sha256", "outcomes_sha256"):
        if report[field] != expected[field]:
            raise ValueError(f"report {field} does not match inputs")
    _check_summary(report, expected, "report")
    _fields(report["workloads"], tuple(expected["workloads"]), "report workloads")
    for name, summary in expected["workloads"].items():
        actual = report["workloads"][name]
        _fields(actual, tuple(summary), f"workload {name}")
        _check_summary(actual, summary, f"workload {name}")
    return expected
