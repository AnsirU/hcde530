# Week 3 — Competency claim

## C3 — Data Cleaning and File Handling

**What it means:** Loading messy real-world data with Python, finding what is broken, and fixing it so the script runs cleanly on any valid input. Reading error messages as diagnostic information. Writing scripts that produce consistent, repeatable output.

### What counts as evidence

- A Python script that reads from a CSV file (not hardcoded data)
- Handling of at least one real data problem: non-numeric values, inconsistent formatting, missing entries
- A traceback you read and diagnosed — explain what the error was pointing to
- Commit history that shows you found a bug, understood it, and fixed it

### Strong claim

The script crashed with `ValueError: invalid literal for int() with base 10: 'fifteen'` because one row had the word `'fifteen'` in the experience column instead of a number. I added a `try`/`except` block to catch that and skip bad rows. The output now reports how many rows were skipped and why.

*(Weak claim for contrast: “I cleaned the data and fixed the bugs.” — too vague; the strong claim ties the traceback, the root cause, the code change, and the user-visible reporting together.)*

### Traceback diagnosis (what the error pointed to)

Python raised `ValueError` at `int(row["experience_years"])`. That line assumes every value can become an integer. The message `invalid literal for int() with base 10: 'fifteen'` names the exact string that failed: the letter **word** `fifteen`, not the digits `15`. So the fix is not “try harder,” but validate or catch non-numeric text and exclude (or map) those rows before averaging.

### Incomplete rows

Some responses may omit `participant_name` and `role` entirely (e.g. response **R005** in `week3_survey_messy.csv`). Those rows are dropped before role counts and averages so anonymous fragments do not pollute participant-based statistics.
