import runpy
import unittest
from pathlib import Path

STUDY = Path(__file__).resolve().parents[1] / "studies" / "scoring-unit"
grade = runpy.run_path(str(STUDY / "reproduce.py"))["grade"]


class ScoringUnitTests(unittest.TestCase):
    def test_copy_can_be_correct_on_canonical_input(self):
        rows = {"stream": [2, 3]}
        self.assertEqual(grade(rows, rows)["record_score"], 1)

    def test_missing_rows_stay_in_denominator(self):
        expected = {"left": [1, 2], "right": [2, 3]}
        self.assertEqual(grade(expected, {"right": [2, 3]})["record_score"], 0.5)

    def test_equivalent_but_noncanonical_fraction_fails_conversion(self):
        self.assertEqual(grade({"x": [1, 2]}, {"x": [2, 4]})["record_score"], 0)

    def test_row_order_is_irrelevant(self):
        expected = {"left": [1, 2], "right": [2, 3]}
        self.assertEqual(grade(expected, dict(reversed(expected.items()))),
                         grade(expected, expected))

    def test_unknown_id_cannot_inflate_field_credit(self):
        with self.assertRaises(ValueError):
            grade({"left": [1, 2]}, {"other": [1, 2]})

    def test_booleans_do_not_equal_integer_components(self):
        self.assertEqual(grade({"left": [1, 2]}, {"left": [True, 2]})["record_score"], 0)
