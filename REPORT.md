# ICT102 Assessment 3 - Expense Manager Report
**Student:** [Shirish Shrestha] **Student ID:** [SM20253812]

## 1. Program overview and design choices
The Expense Manager is a menu-driven console program (Topic C). I split it into modules with one responsibility each, so logic is separate from input/output:

- `main.py` - menu loop only (calls everything else)
- `manager.py` - `ExpenseManager` class (add, search, update, delete, filter, monthly total); contains no `input()`/`print()`, so it is easy to test
- `expense.py` - `Expense` class (one record)
- `reports.py` - summary statistics (own loops) and the recursive function
- `storage.py` - CSV load/save with the `csv` module
- `validation.py` - every input is re-prompted in a loop until valid
- `display.py` - aligned tables and report layout

**Data structure:** a list of `Expense` objects; categories are stored in Title Case so "food" and "FOOD" group together.
**Unique IDs:** highest existing ID + 1, so IDs are never reused after a delete.
**Recursion (FR10):** `recursive_total(expenses, index)` - base case: index past the end returns 0; recursive case: current amount + total of the rest. It is used for the monthly total.
**Loops (FR8):** total, per-category totals, largest and average are all calculated with explicit loops.

### Pseudocode - recursive_total
```
FUNCTION recursive_total(list, index)
    IF index >= length(list) THEN RETURN 0          // base case
    RETURN list[index].amount + recursive_total(list, index + 1)   // recursive case
```

## 2. Test cases and results
Automated tests: `python -m unittest discover -s tests -v` -> **26 tests, all passed.**

| # | Type | Test | Expected | Result |
|---|------|------|----------|--------|
| 1 | Normal | Add valid expense | Saved with next ID | Pass |
| 2 | Boundary | Add to empty list | ID = 1 | Pass |
| 3 | Boundary | Delete middle record, then add | ID not reused | Pass |
| 4 | Normal | Search category "fOOd" | Case-insensitive match | Pass |
| 5 | Boundary | Search with no matches | Empty result, message shown | Pass |
| 6 | Normal | Update amount | New amount stored | Pass |
| 7 | Error | Update/delete unknown ID | Rejected, no crash | Pass |
| 8 | Normal | Monthly total 2026-10 | Correct sum | Pass |
| 9 | Boundary | Monthly total for month with no data | 0.00 | Pass |
| 10 | Normal | Recursive total | Equals loop total | Pass |
| 11 | Boundary | Recursive total of empty list (base case) | 0 | Pass |
| 12 | Error | Amount: empty, abc, -5, 0, nan, inf, 9999999 | Re-prompt each time | Pass |
| 13 | Boundary | Amount 1,000,000 accepted; 1,000,000.01 rejected | As stated | Pass |
| 14 | Error | Dates: empty, 05/11/2026, 2026-13-01, 2026-02-30 | Re-prompt | Pass |
| 15 | Error | Month: 2026-13, "Nov" | Re-prompt | Pass |
| 16 | Error | Delete confirmation: "maybe" | Re-prompt until Y/N | Pass |
| 17 | Error | Menu: "abc", "99" | "Invalid choice", menu again | Pass |
| 18 | Normal | CSV round-trip with comma in description | Text preserved | Pass |
| 19 | Error | CSV with bad rows | Bad rows skipped, warning | Pass |
| 20 | Boundary | First run, no CSV file | File created, no crash | Pass |
| 21 | Normal | Exit | Data saved, goodbye message | Pass |

**Defect found and fixed:** my own test wrongly treated `12.345` as invalid; the program correctly rounds it to 12.35, so I corrected the test.

*(Add screenshots here: the menu, a summary report, an error being re-prompted, and the passing test run.)*

## 3. Reflection (about 330 words)
**Overview.** I built an Expense Manager that lets a user add, view, search, update and delete expenses, filter them by category or month, and see a summary report. Records are loaded from a CSV file when the program starts and saved when it exits.

**Design choices.** I used several small modules rather than one long script, because it made each part easier to understand and test. The `ExpenseManager` class holds the logic and has no input or output, which meant I could write automated tests without typing into the console. I used the `csv` module so descriptions containing commas are stored safely. For validation I wrote one helper per data type that loops until the input is valid, which stopped crashes from empty, non-numeric, negative or unknown values.

**Recursion and algorithms.** The recursive function adds up expense amounts one item at a time, with a base case for the end of the list. I used it for the monthly total. For the summary report I used plain loops for the total, average, largest expense and category totals, as required. Recursion is elegant for a short list like this, but a loop would be safer for thousands of records because Python limits recursion depth.

**Testing.** I wrote 26 automated tests covering normal, boundary and error cases, and all pass. Testing showed me that a boundary I thought was invalid (12.345) was actually handled correctly by rounding, which taught me to check both the code and the test.

**Improvements.** Next time I would add a spending budget per category, export to a report file, and a graphical interface. I could also replace the recursion with a loop for large data sets.

**Professional practice and acknowledgement.** I used Git and GitHub with regular commits. I used an AI tool (Claude, by Anthropic) to help generate the initial code structure and tests. I then [ran the program, read and understood each file, and tested it myself - EDIT to describe what you really did]. [Describe anything you changed yourself.]

## 4. References
Python Software Foundation. (2026). *csv - CSV file reading and writing*. https://docs.python.org/3/library/csv.html
Python Software Foundation. (2026). *unittest - Unit testing framework*. https://docs.python.org/3/library/unittest.html
Anthropic. (2026). *Claude* [Large language model]. https://claude.ai
