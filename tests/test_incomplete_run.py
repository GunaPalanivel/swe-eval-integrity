import runpy
import unittest
from pathlib import Path

study = Path(__file__).resolve().parents[1] / "studies/incomplete-run/reproduce.py"
mean_if_complete = runpy.run_path(str(study))["mean_if_complete"]


class BatchTests(unittest.TestCase):
    def test_genuine_zero_is_a_measurement(self):
        self.assertEqual(mean_if_complete({"a"}, [{"instrument": "a", "status": "complete", "value": 0}]), 0)

    def test_zero_cannot_rescue_an_errored_reading(self):
        with self.assertRaisesRegex(ValueError, "incomplete reading"):
            mean_if_complete({"a"}, [{"instrument": "a", "status": "parse_error", "value": 0}])

    def test_expected_instruments_must_appear_exactly_once(self):
        good = {"instrument": "a", "status": "complete", "value": 3}
        for rows in ([], [good, good], [{**good, "instrument": "b"}]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                mean_if_complete({"a"}, rows)
