import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from swe_eval_integrity.reward import canonical_sha256, load_json, reconstruct, validate_report


class RewardTests(unittest.TestCase):
    def setUp(self):
        inputs = ROOT / "studies" / "reward-reconstruction" / "inputs"
        self.catalog = load_json(inputs / "catalog.json")
        self.outcomes = load_json(inputs / "outcomes.json")
        self.report = load_json(inputs / "report.json")

    def test_independent_five_case_calculation(self):
        result = validate_report(self.catalog, self.outcomes, self.report)
        self.assertEqual((result["passed_count"], result["case_count"]), (3, 5))
        self.assertEqual(result["score"], 3 / 5)
        self.assertEqual(result["workloads"]["sorting"]["score"], 2 / 3)
        self.assertEqual(result["workloads"]["lookup"]["score"], 1 / 2)

    def test_wrong_count_report_is_rejected(self):
        self.report["case_count"] = 6
        with self.assertRaisesRegex(ValueError, "case_count disagrees"):
            validate_report(self.catalog, self.outcomes, self.report)

    def test_wrong_workload_count_or_score_is_rejected(self):
        for field, value in (("case_count", 4), ("passed_count", 3), ("score", 1.0)):
            with self.subTest(field=field):
                report = copy.deepcopy(self.report)
                report["workloads"]["sorting"][field] = value
                with self.assertRaises(ValueError):
                    validate_report(self.catalog, self.outcomes, report)

    def test_wrong_overall_passes_or_score_is_rejected(self):
        for field, value in (("passed_count", 4), ("score", 0.7)):
            with self.subTest(field=field):
                report = copy.deepcopy(self.report)
                report[field] = value
                with self.assertRaises(ValueError):
                    validate_report(self.catalog, self.outcomes, report)

    def test_missing_duplicate_and_unknown_outcomes_are_rejected(self):
        variants = [self.outcomes["outcomes"][:-1],
                    self.outcomes["outcomes"] + [self.outcomes["outcomes"][0]],
                    self.outcomes["outcomes"] + [{"case_id": "unknown", "score": 1}]]
        for rows in variants:
            with self.subTest(rows=rows):
                outcomes = dict(self.outcomes, outcomes=rows)
                with self.assertRaises(ValueError):
                    reconstruct(self.catalog, outcomes)

    def test_duplicate_catalog_case_and_inconsistent_fixed_counts_are_rejected(self):
        self.catalog["cases"].append(copy.deepcopy(self.catalog["cases"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate catalog case"):
            reconstruct(self.catalog, self.outcomes)
        self.catalog["cases"].pop()
        self.catalog["workload_counts"]["lookup"] = 3
        with self.assertRaisesRegex(ValueError, "fixed workload_counts"):
            reconstruct(self.catalog, self.outcomes)

    def test_changed_catalog_invalidates_outcomes(self):
        self.catalog["cases"][0]["case_id"] = "renamed-case"
        with self.assertRaisesRegex(ValueError, "catalog_sha256"):
            reconstruct(self.catalog, self.outcomes)

    def test_stale_report_rejected_even_when_totals_stay_the_same(self):
        rows = self.outcomes["outcomes"]
        rows[0]["score"], rows[2]["score"] = rows[2]["score"], rows[0]["score"]
        with self.assertRaisesRegex(ValueError, "outcomes_sha256"):
            validate_report(self.catalog, self.outcomes, self.report)

    def test_invalid_binary_outcome_scores_are_rejected(self):
        for value in (True, False, 0.0, -1, 2, "1", None, float("nan"), float("inf")):
            with self.subTest(value=value):
                self.outcomes["outcomes"][0]["score"] = value
                with self.assertRaises(ValueError):
                    reconstruct(self.catalog, self.outcomes)

    def test_boolean_and_nonfinite_report_numbers_are_rejected(self):
        for field in ("schema_version", "case_count", "passed_count", "score"):
            for value in (True, False, float("nan"), float("inf"), -float("inf")):
                with self.subTest(field=field, value=value):
                    report = copy.deepcopy(self.report)
                    report[field] = value
                    with self.assertRaises(ValueError):
                        validate_report(self.catalog, self.outcomes, report)
        self.report["workloads"]["lookup"]["passed_count"] = True
        with self.assertRaises(ValueError):
            validate_report(self.catalog, self.outcomes, self.report)

    def test_boolean_catalog_counts_and_versions_are_rejected(self):
        self.catalog["workload_counts"]["lookup"] = True
        with self.assertRaises(ValueError):
            reconstruct(self.catalog, self.outcomes)
        self.catalog["workload_counts"]["lookup"] = 2
        self.catalog["schema_version"] = True
        with self.assertRaises(ValueError):
            reconstruct(self.catalog, self.outcomes)

    def test_missing_extra_and_malformed_fields_are_rejected(self):
        for value in (None, [], {}, dict(self.report, ignored=True)):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_report(self.catalog, self.outcomes, value)
        self.report["workloads"].pop("lookup")
        with self.assertRaises(ValueError):
            validate_report(self.catalog, self.outcomes, self.report)

    def test_canonical_hash_ignores_object_order_but_preserves_array_order(self):
        first = {"b": [2, 1], "a": "oak"}
        second = {"a": "oak", "b": [2, 1]}
        expected = hashlib.sha256(b'{"a":"oak","b":[2,1]}').hexdigest()
        self.assertEqual(canonical_sha256(first), expected)
        self.assertEqual(canonical_sha256(second), expected)
        self.assertNotEqual(canonical_sha256({"a": "oak", "b": [1, 2]}), expected)

    def test_json_duplicate_keys_and_nonfinite_constants_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            for text in ('{"score":0,"score":1}', '{"score":NaN}', '{"score":Infinity}'):
                with self.subTest(text=text):
                    path.write_text(text, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        load_json(path)

    def test_cli_success_invalid_report_missing_file_and_bad_usage(self):
        inputs = ROOT / "studies" / "reward-reconstruction" / "inputs"
        env = dict(os.environ, PYTHONPATH=str(ROOT / "src"))
        for args, code, valid in (
            ([inputs / "catalog.json", inputs / "outcomes.json", inputs / "report.json"], 0, True),
            ([inputs / "catalog.json", inputs / "outcomes.json", inputs / "wrong-count-report.json"], 1, False),
            ([inputs / "missing.json"] * 3, 1, False),
            ([], 2, False),
        ):
            with self.subTest(args=args):
                result = subprocess.run([sys.executable, "-m", "swe_eval_integrity", *map(str, args)],
                                        env=env, capture_output=True, text=True, check=False)
                self.assertEqual(result.returncode, code, result.stderr)
                self.assertIs(json.loads(result.stdout)["valid"], valid)

    def test_cli_rejects_concrete_invalid_json_variants(self):
        env = dict(os.environ, PYTHONPATH=str(ROOT / "src"))
        with tempfile.TemporaryDirectory() as directory:
            paths = [Path(directory) / f"{name}.json" for name in ("catalog", "outcomes", "report")]
            for path, value in zip(paths, (self.catalog, self.outcomes, self.report)):
                path.write_text(json.dumps(value), encoding="utf-8")
            variants = ["{malformed", '{"score":0,"score":1}',
                        json.dumps(dict(self.report, score=float("nan"))),
                        json.dumps(dict(self.report, score=float("inf"))),
                        json.dumps(dict(self.report, score=True)),
                        json.dumps(dict(self.report, outcomes_sha256="stale"))]
            for text in variants:
                with self.subTest(text=text):
                    paths[2].write_text(text, encoding="utf-8")
                    result = subprocess.run([sys.executable, "-m", "swe_eval_integrity", *map(str, paths)],
                                            env=env, capture_output=True, text=True, check=False)
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertIs(json.loads(result.stdout)["valid"], False)

    def test_saved_study_replays_without_modifying_results(self):
        study = ROOT / "studies" / "reward-reconstruction"
        before = (study / "results.json").read_bytes()
        result = subprocess.run([sys.executable, str(study / "reproduce.py")],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), json.loads(before))
        self.assertEqual((study / "results.json").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
