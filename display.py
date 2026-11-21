"""display.py - All formatted output (tables and the summary report)."""


def show_expenses(expenses, title="Expenses"):
    """FR3: aligned table, or a clear message when empty."""
    if not expenses:
        print("\n  No expenses to show.")
        return
    print(f"\n{title} ({len(expenses)})")
    line = "-" * 72
    print(line)
    print(f"{'ID':<5}{'Date':<12}{'Category':<15}{'Description':<30}{'Amount':>10}")
    print(line)
    for e in expenses:
        desc = e.description if len(e.description) <= 28 else e.description[:25] + "..."
        cat = e.category if len(e.category) <= 13 else e.category[:12] + "."
        print(f"{e.expense_id:<5}{e.date:<12}{cat:<15}{desc:<30}{e.amount:>10.2f}")
    print(line)


def show_summary(summary):
    """FR8: print the summary report values."""
    print("\n===== SUMMARY REPORT =====")
    if summary["count"] == 0:
        print("  No expenses recorded yet.")
        return
    print(f"  Number of expenses : {summary['count']}")
    print(f"  Total spent        : ${summary['total']:.2f}")
    print(f"  Average expense    : ${summary['average']:.2f}")
    big = summary["largest"]
    print(f"  Largest expense    : ${big.amount:.2f} "
          f"({big.description}, {big.category}, {big.date})")
    print("  Total per category :")
    for category in sorted(summary["per_category"]):
        print(f"    {category:<15} ${summary['per_category'][category]:>10.2f}")
