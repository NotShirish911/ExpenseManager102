"""Automated tests (normal / boundary / error). Run:  python -m unittest discover -s tests -v"""
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import reports
import storage
import validation as v
from expense import Expense
from manager import ExpenseManager


def sample():
    return ExpenseManager([
        Expense(1, "2026-10-02", "Food", "Groceries", 50.0),
        Expense(2, "2026-10-09", "Transport", "Train", 20.0),
        Expense(3, "2026-11-01", "Food", "Lunch", 30.0),
    ])


class TestManager(unittest.TestCase):
    def test_add_unique_id(self):                      # normal
        m = sample()
        self.assertEqual(m.add("2026-11-02", "rent", "Rent", 100).expense_id, 4)

    def test_add_to_empty_gets_id_1(self):             # boundary
        self.assertEqual(ExpenseManager().add("2026-11-02", "Food", "x", 5).expense_id, 1)

    def test_id_not_reused_after_delete_middle(self):  # boundary
        m = sample(); m.delete(2)
        self.assertEqual(m.next_id(), 4)

    def test_search_case_insensitive(self):            # normal
        self.assertEqual(len(sample().search_by_category("fOOd")), 2)

    def test_search_description_and_none(self):        # normal + boundary
        m = sample()
        self.assertEqual(len(m.search_by_description("TRA")), 1)
        self.assertEqual(m.search_by_description("zzz"), [])

    def test_update_amount(self):                      # normal
        m = sample(); self.assertTrue(m.update(1, "amount", 75))
        self.assertEqual(m.get(1).amount, 75.0)

    def test_update_unknown_id(self):                  # error
        self.assertFalse(sample().update(99, "amount", 5))

    def test_delete(self):                             # normal + error
        m = sample()
        self.assertTrue(m.delete(1)); self.assertIsNone(m.get(1))
        self.assertFalse(m.delete(1))

    def test_filter_category_and_month(self):          # normal
        m = sample()
        self.assertEqual(len(m.filter_by_category("food")), 2)
        self.assertEqual(len(m.filter_by_month("2026-10")), 2)

    def test_monthly_total(self):                      # normal + boundary
        m = sample()
        self.assertAlmostEqual(m.monthly_total("2026-10"), 70.0)
        self.assertEqual(m.monthly_total("2020-01"), 0.0)


class TestReports(unittest.TestCase):
    def test_recursive_total(self):
        self.assertAlmostEqual(reports.recursive_total(sample().expenses), 100.0)

    def test_recursive_total_empty_base_case(self):
        self.assertEqual(reports.recursive_total([]), 0.0)

    def test_summary_values(self):
        s = reports.build_summary(sample().expenses)
        self.assertEqual(s["count"], 3)
        self.assertAlmostEqual(s["total"], 100.0)
        self.assertAlmostEqual(s["average"], 100 / 3)
        self.assertEqual(s["largest"].expense_id, 1)
        self.assertAlmostEqual(s["per_category"]["Food"], 80.0)

    def test_summary_empty(self):
        s = reports.build_summary([])
        self.assertEqual((s["total"], s["average"], s["largest"]), (0.0, 0.0, None))


class TestStorage(unittest.TestCase):
    def test_creates_missing_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "data", "new.csv")
            self.assertEqual(storage.load_expenses(path), [])
            self.assertTrue(os.path.exists(path))

    def test_round_trip_with_comma_in_text(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "e.csv")
            storage.save_expenses(path, [Expense(1, "2026-11-01", "Food", "Milk, eggs", 9.5)])
            loaded = storage.load_expenses(path)
            self.assertEqual(loaded[0].description, "Milk, eggs")

    def test_bad_rows_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "e.csv")
            with open(path, "w") as f:
                f.write("expense_id,date,category,description,amount\n"
                        "1,2026-11-01,Food,ok,5\n"
                        "x,bad-date,Food,bad,abc\n"
                        "2,2026-11-02,Food,negative,-5\n")
            self.assertEqual(len(storage.load_expenses(path)), 1)

    def test_sample_csv_has_8_plus_records(self):
        path = os.path.join(os.path.dirname(__file__), "..", "data", "expenses.csv")
        self.assertGreaterEqual(len(storage.load_expenses(path)), 8)


class TestValidation(unittest.TestCase):
    def run_with(self, func, inputs, *args):
        with patch("builtins.input", side_effect=inputs), patch("builtins.print"):
            return func("p: ", *args)

    def test_amount_rejects_bad_then_accepts(self):
        bad = ["", "abc", "-5", "0", "nan", "inf", "9999999"]
        self.assertEqual(self.run_with(v.read_amount, bad + ["$12.50"]), 12.5)

    def test_amount_rounds_to_cents(self):
        self.assertEqual(self.run_with(v.read_amount, ["12.345"]), 12.35)

    def test_amount_upper_boundary(self):
        self.assertEqual(self.run_with(v.read_amount, ["1000000.01", "1000000"]), 1000000.0)

    def test_text_rejects_empty(self):
        self.assertEqual(self.run_with(v.read_text, ["", "   ", "Food"]), "Food")

    def test_date_rejects_invalid(self):
        self.assertEqual(
            self.run_with(v.read_date, ["", "05/11/2026", "2026-13-01", "2026-02-30", "2026-11-05"]),
            "2026-11-05")

    def test_month_rejects_invalid(self):
        self.assertEqual(self.run_with(v.read_month, ["2026-13", "Nov", "2026-11"]), "2026-11")

    def test_yes_no(self):
        self.assertTrue(self.run_with(v.read_yes_no, ["maybe", "Y"]))
        self.assertFalse(self.run_with(v.read_yes_no, ["", "n"]))

    def test_existing_id(self):
        m = sample()
        self.assertEqual(self.run_with(v.read_existing_id, ["", "abc", "-1", "99", "2"], m), 2)
        self.assertIsNone(self.run_with(v.read_existing_id, ["C"], m))


if __name__ == "__main__":
    unittest.main()
