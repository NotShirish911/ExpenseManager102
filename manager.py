"""manager.py - ExpenseManager: holds the records and does add/search/update/delete/filter."""
from expense import Expense
import reports


class ExpenseManager:
    """Owns the list of Expense objects. No input()/print() here - logic only."""

    def __init__(self, expenses=None):
        self.expenses = expenses if expenses is not None else []

    # ---- FR2 add ----
    def next_id(self):
        """Unique ID = highest existing ID + 1 (loop, no built-in max)."""
        highest = 0
        for e in self.expenses:
            if e.expense_id > highest:
                highest = e.expense_id
        return highest + 1

    def add(self, date, category, description, amount):
        expense = Expense(self.next_id(), date, category.strip().title(),
                          description.strip(), float(amount))
        self.expenses.append(expense)
        return expense

    # ---- lookup ----
    def get(self, expense_id):
        for e in self.expenses:
            if e.expense_id == expense_id:
                return e
        return None

    # ---- FR4 search (case-insensitive, may return many) ----
    def search_by_category(self, text):
        text = text.lower()
        return [e for e in self.expenses if text in e.category.lower()]

    def search_by_description(self, text):
        text = text.lower()
        return [e for e in self.expenses if text in e.description.lower()]

    def search_by_date(self, text):
        return [e for e in self.expenses if text in e.date]

    # ---- FR5 update ----
    def update(self, expense_id, field, value):
        """Change one field. Value must already be validated. Returns True if updated."""
        e = self.get(expense_id)
        if e is None:
            return False
        if field == "date":
            e.date = value
        elif field == "category":
            e.category = value.strip().title()
        elif field == "description":
            e.description = value.strip()
        elif field == "amount":
            e.amount = float(value)
        else:
            return False
        return True

    # ---- FR6 delete ----
    def delete(self, expense_id):
        e = self.get(expense_id)
        if e is None:
            return False
        self.expenses.remove(e)
        return True

    # ---- FR7 topic-specific: filter + monthly total ----
    def filter_by_category(self, category):
        category = category.strip().lower()
        return [e for e in self.expenses if e.category.lower() == category]

    def filter_by_month(self, month):
        return [e for e in self.expenses if e.month == month]

    def monthly_total(self, month):
        """Total for a month using the recursive function (FR10)."""
        return reports.recursive_total(self.filter_by_month(month))
