"""validation.py - Input helpers. Every function loops until the input is valid (FR11)."""
import math
from datetime import datetime

MAX_AMOUNT = 1_000_000


def read_text(prompt):
    """Re-prompt until the user enters non-empty text."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  Error: this field cannot be empty.")


def read_date(prompt):
    """Re-prompt until a real calendar date in YYYY-MM-DD format is entered."""
    while True:
        value = input(prompt).strip()
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("  Error: enter a valid date as YYYY-MM-DD (e.g. 2026-11-05).")


def read_month(prompt):
    """Re-prompt until a month in YYYY-MM format is entered."""
    while True:
        value = input(prompt).strip()
        try:
            datetime.strptime(value, "%Y-%m")
            return value
        except ValueError:
            print("  Error: enter a valid month as YYYY-MM (e.g. 2026-11).")


def read_amount(prompt):
    """Re-prompt until a positive number (not NaN/inf, within limit) is entered."""
    while True:
        value = input(prompt).strip().replace("$", "")
        try:
            amount = float(value)
        except ValueError:
            print("  Error: amount must be a number (e.g. 12.50).")
            continue
        if not math.isfinite(amount) or amount <= 0:
            print("  Error: amount must be greater than 0.")
        elif amount > MAX_AMOUNT:
            print(f"  Error: amount cannot exceed {MAX_AMOUNT:,}.")
        else:
            return round(amount, 2)


def read_yes_no(prompt):
    """Return True for Y, False for N. Re-prompt on anything else."""
    while True:
        value = input(prompt).strip().lower()
        if value in ("y", "yes"):
            return True
        if value in ("n", "no"):
            return False
        print("  Error: please answer Y or N.")


def read_choice(prompt, valid_choices):
    """Re-prompt until the entry is one of valid_choices (list of strings)."""
    while True:
        value = input(prompt).strip()
        if value in valid_choices:
            return value
        print(f"  Error: choose one of {', '.join(valid_choices)}.")


def read_existing_id(prompt, manager):
    """Re-prompt until the ID exists. Returns the ID, or None if the user types 'c'."""
    while True:
        value = input(prompt).strip().lower()
        if value == "c":
            return None
        if not value.isdigit():
            print("  Error: ID must be a whole number (or 'c' to cancel).")
            continue
        if manager.get(int(value)) is None:
            print(f"  Error: no expense with ID {value} (or 'c' to cancel).")
            continue
        return int(value)
