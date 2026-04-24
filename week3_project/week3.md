# Week 3

This folder holds the scripts and sample CSVs for the assignment. The main script is `week3_analysis_buggy.py` and the messy survey data is `week3_survey_messy.csv`. Running it writes a cleaned copy to `week3_survey_cleaned.csv`. There is also `clean_responses.py` for cleaning `responses.csv` and `count_roles.py` for counting roles.

Example:

```bash
python3 week3_analysis_buggy.py
```

---

## Competency claim

**C3 — Data cleaning and file handling**

I load real data from CSV with Python (not hardcoded values). The messy file has bad values in more than one place, so I had to find and fix two separate issues.

**1. `experience_years` (non-numeric text).** The column is supposed to be whole years, but at least one row has a word instead of an integer. That broke `int(...)` and Python raised a `ValueError`. I used the traceback to see which line failed, then wrapped parsing in `try`/`except`, skipped non-numeric rows, and printed `response_id` and the raw value for each skip so the cleaning is auditable.

**2. `satisfaction_score` (“top 5” list was the wrong end of the sort).** The script is supposed to print the **five highest** satisfaction scores, but the list was sorted **ascending** (low scores first), so taking the first five after the sort actually returned the **five lowest** scores. I found it by re-reading the sort-and-slice logic and by checking that the printed “top” numbers did not match the largest values in the data. The fix is to sort in **descending** order on the score (`reverse=True` on the sort key), then take the first five names and scores. That way “top 5” matches the highest values.

Rows with no participant name and no role are dropped before stats. The script runs to completion on messy input and produces repeatable output.
