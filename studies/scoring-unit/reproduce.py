"""Compare two units of credit on exactly the same converter outputs."""

import json
from fractions import Fraction
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent


def reduce_pair(numerator, denominator):
    divisor = gcd(numerator, denominator)
    return [numerator // divisor, denominator // divisor]


def reduce_signed(numerator, denominator):
    n, d = reduce_pair(numerator, denominator)
    return [-n, -d] if d < 0 else [n, d]


def as_fraction(numerator, denominator):
    value = Fraction(numerator, denominator)
    return [value.numerator, value.denominator]


def grade(expected, output):
    """IDs identify rows. Missing records stay in both denominators."""
    if not expected or output.keys() - expected.keys():
        raise ValueError("expected a nonempty catalog and only known record IDs")
    matched = []
    for key, pair in output.items():
        if (isinstance(pair, list) and len(pair) == 2
                and all(type(value) is int for value in pair) and pair == expected[key]):
            matched.append(key)
    size = len(expected)
    return {
        "correct_records": sorted(matched),
        "field_score": (len(output) + len(matched)) / (2 * size),
        "record_score": len(matched) / size,
    }


def reproduce():
    rows = json.loads((HERE / "rates.json").read_text(encoding="utf-8"))
    expected = {key: row["expected"] for key, row in rows.items()}
    inputs = {key: row["input"] for key, row in rows.items()}
    candidates = {"empty": {}, "copy": inputs}
    for name, converter in (("unsigned_reduction", reduce_pair),
                            ("signed_reduction", reduce_signed),
                            ("fraction_library", as_fraction)):
        candidates[name] = {key: converter(*pair) for key, pair in inputs.items()}
    return {name: grade(expected, output) for name, output in candidates.items()}


if __name__ == "__main__":
    result = reproduce()
    saved = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    if result != saved:
        raise SystemExit("observed results differ from results.json")
    print(json.dumps(result, indent=2, sort_keys=True))
