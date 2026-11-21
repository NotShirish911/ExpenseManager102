"""main.py - Menu-driven Expense Manager (ICT102 Assessment 3, Topic C).

Run with:  python main.py
"""
import os

import display
import reports
import storage
import validation as v
from manager import ExpenseManager

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "expenses.csv")

MENU = """
========== EXPENSE MANAGER ==========
 1. Add an expense
 2. View all expenses
 3. Search expenses
 4. Update an expense
 5. Delete an expense
 6. Filter by category
 7. Filter by month
 8. Monthly total
 9. Summary report
 0. Exit (saves data)
====================================="""


def add_expense(mgr):
    print("\n--- Add expense ---")
    date = v.read_date("Date (YYYY-MM-DD): ")
    category = v.read_text("Category (e.g. Food, Transport): ")
    description = v.read_text("Description: ")
    amount = v.read_amount("Amount: $")
    e = mgr.add(date, category, description, amount)
    print(f"  Added expense with ID {e.expense_id}.")


def search_expenses(mgr):
    print("\n--- Search ---")
    print(" 1. By category\n 2. By description\n 3. By date (e.g. 2026-11 or 2026-11-05)")
    choice = v.read_choice("Search by: ", ["1", "2", "3"])
    text = v.read_text("Search text: ")
    if choice == "1":
        results = mgr.search_by_category(text)
    elif choice == "2":
        results = mgr.search_by_description(text)
    else:
        results = mgr.search_by_date(text)
    display.show_expenses(results, "Search results")


def update_expense(mgr):
    print("\n--- Update expense ---")
    display.show_expenses(mgr.expenses)
    if not mgr.expenses:
        return
    expense_id = v.read_existing_id("ID to update (or 'c' to cancel): ", mgr)
    if expense_id is None:
        print("  Update cancelled.")
        return
    print(" 1. Date\n 2. Category\n 3. Description\n 4. Amount")
    choice = v.read_choice("Field to change: ", ["1", "2", "3", "4"])
    if choice == "1":
        mgr.update(expense_id, "date", v.read_date("New date (YYYY-MM-DD): "))
    elif choice == "2":
        mgr.update(expense_id, "category", v.read_text("New category: "))
    elif choice == "3":
        mgr.update(expense_id, "description", v.read_text("New description: "))
    else:
        mgr.update(expense_id, "amount", v.read_amount("New amount: $"))
    print("  Expense updated.")


def delete_expense(mgr):
    print("\n--- Delete expense ---")
    display.show_expenses(mgr.expenses)
    if not mgr.expenses:
        return
    expense_id = v.read_existing_id("ID to delete (or 'c' to cancel): ", mgr)
    if expense_id is None:
        print("  Delete cancelled.")
        return
    if v.read_yes_no(f"Delete expense {expense_id}? (Y/N): "):
        mgr.delete(expense_id)
        print("  Expense deleted.")
    else:
        print("  Delete cancelled.")


def filter_by_category(mgr):
    category = v.read_text("\nCategory to filter by: ")
    display.show_expenses(mgr.filter_by_category(category), f"Category: {category.title()}")


def filter_by_month(mgr):
    month = v.read_month("\nMonth (YYYY-MM): ")
    display.show_expenses(mgr.filter_by_month(month), f"Month: {month}")


def monthly_total(mgr):
    month = v.read_month("\nMonth (YYYY-MM): ")
    count = len(mgr.filter_by_month(month))
    print(f"  Total for {month}: ${mgr.monthly_total(month):.2f} ({count} expense(s))")


def main():
    mgr = ExpenseManager(storage.load_expenses(DATA_FILE))
    print(f"Loaded {len(mgr.expenses)} expense(s).")
    actions = {
        "1": add_expense,
        "2": lambda m: display.show_expenses(m.expenses, "All expenses"),
        "3": search_expenses,
        "4": update_expense,
        "5": delete_expense,
        "6": filter_by_category,
        "7": filter_by_month,
        "8": monthly_total,
        "9": lambda m: display.show_summary(reports.build_summary(m.expenses)),
    }
    try:
        while True:
            print(MENU)
            choice = input("Choose an option: ").strip()
            if choice == "0":
                break
            if choice in actions:
                actions[choice](mgr)
            else:
                print("  Invalid choice - please enter a number from 0 to 9.")
    except (KeyboardInterrupt, EOFError):
        print("\nInterrupted - saving your data before closing.")
    if storage.save_expenses(DATA_FILE, mgr.expenses):
        print(f"Saved {len(mgr.expenses)} expense(s). Goodbye!")


if __name__ == "__main__":
    main()
