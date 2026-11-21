"""expense.py - The Expense record (one row of data)."""
from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"


class Expense:
    """A single expense: id, date (YYYY-MM-DD), category, description, amount."""

    def __init__(self, expense_id, date, category, description, amount):
        self.expense_id = expense_id
        self.date = date
        self.category = category
        self.description = description
        self.amount = amount

    @property
    def month(self):
        """Return the 'YYYY-MM' part of the date (used for monthly filters)."""
        return self.date[:7]

    def to_row(self):
        """Convert to a list of strings for writing to CSV."""
        return [self.expense_id, self.date, self.category,
                self.description, f"{self.amount:.2f}"]

    @classmethod
    def from_row(cls, row):
        """Build an Expense from a CSV dict row. Raises ValueError/KeyError if bad."""
        expense_id = int(row["expense_id"])
        date = row["date"].strip()
        datetime.strptime(date, DATE_FORMAT)          # validates the date
        category = row["category"].strip()
        description = row["description"].strip()
        amount = float(row["amount"])
        if expense_id <= 0 or not category or not description or amount <= 0:
            raise ValueError("invalid expense values")
        return cls(expense_id, date, category, description, amount)
