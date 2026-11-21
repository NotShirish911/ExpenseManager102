"""storage.py - CSV load/save (FR9). Creates the file if it does not exist."""
import csv
import os

from expense import Expense

FIELDS = ["expense_id", "date", "category", "description", "amount"]


def load_expenses(path):
    """Load expenses from CSV. If missing, create an empty file with a header."""
    if not os.path.exists(path):
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        save_expenses(path, [])
        print(f"No data file found - created new file: {path}")
        return []

    expenses = []
    skipped = 0
    try:
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:
                    expenses.append(Expense.from_row(row))
                except (KeyError, ValueError, TypeError, AttributeError):
                    skipped += 1
    except (OSError, csv.Error) as err:
        print(f"Warning: could not read {path} ({err}). Starting empty.")
        return []
    if skipped:
        print(f"Warning: skipped {skipped} invalid row(s) in {path}.")
    return expenses


def save_expenses(path, expenses):
    """Write all expenses to CSV. Returns True on success."""
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(FIELDS)
            for e in expenses:
                writer.writerow(e.to_row())
        return True
    except OSError as err:
        print(f"Error: could not save to {path} ({err}).")
        return False
