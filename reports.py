"""reports.py - Summary calculations written with our own loops (FR8) and recursion (FR10)."""


# ---------------- FR10: RECURSIVE FUNCTION ----------------
def recursive_total(expenses, index=0):
    """RECURSIVE: sum the amounts of a list of expenses.

    Base case     : index has passed the end of the list -> return 0.
    Recursive case: amount at this index + total of the rest (index + 1).
    """
    if index >= len(expenses):                       # base case
        return 0.0
    return expenses[index].amount + recursive_total(expenses, index + 1)  # recursive case


# ---------------- FR8: loop-based statistics ----------------
def total_spent(expenses):
    total = 0.0
    for e in expenses:
        total += e.amount
    return total


def total_per_category(expenses):
    """Return {category: total}. Categories are grouped case-insensitively."""
    totals = {}
    for e in expenses:
        key = e.category.title()
        if key in totals:
            totals[key] += e.amount
        else:
            totals[key] = e.amount
    return totals


def largest_expense(expenses):
    """Return the Expense with the biggest amount, or None if the list is empty."""
    largest = None
    for e in expenses:
        if largest is None or e.amount > largest.amount:
            largest = e
    return largest


def average_expense(expenses):
    count = 0
    total = 0.0
    for e in expenses:
        total += e.amount
        count += 1
    return total / count if count else 0.0


def build_summary(expenses):
    """Collect every value the summary report must show."""
    return {
        "count": len(expenses),
        "total": total_spent(expenses),
        "per_category": total_per_category(expenses),
        "largest": largest_expense(expenses),
        "average": average_expense(expenses),
    }
