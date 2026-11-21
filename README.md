# Expense Manager (ICT102 Assessment 3 - Topic C)

A modular, menu-driven Python console application for recording and analysing personal expenses.

## Requirements
- Python 3.8 or newer (standard library only - no installs needed)

## How to run
```
cd expense_manager
python main.py        (use `python3 main.py` on macOS/Linux)
```
Data is loaded from `data/expenses.csv` at start-up and saved when you choose **0. Exit**.
If the file is missing, it is created automatically.

## How to run the tests
```
python -m unittest discover -s tests -v
```

## Project structure
| File | Responsibility |
|------|----------------|
| `main.py` | Menu loop and user interaction |
| `manager.py` | `ExpenseManager` - add, search, update, delete, filter, monthly total |
| `expense.py` | `Expense` record class |
| `reports.py` | Loop-based statistics (FR8) and the **recursive** `recursive_total` (FR10) |
| `storage.py` | CSV load/save (FR9) |
| `validation.py` | Re-prompting input validation (FR11) |
| `display.py` | Table and summary formatting |
| `tests/test_expenses.py` | 26 automated tests |
| `data/expenses.csv` | Sample data (10 records) |

## Menu
1 Add - 2 View - 3 Search (category / description / date) - 4 Update - 5 Delete (Y/N confirm) -
6 Filter by category - 7 Filter by month - 8 Monthly total - 9 Summary report - 0 Exit

## Acknowledgement of assistance
This project was developed with assistance from an AI tool (Claude, by Anthropic). See REPORT.md.
