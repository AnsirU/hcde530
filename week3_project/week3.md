# Week 3

This folder holds the scripts and sample CSVs for the assignment. The main script is `week3_analysis_buggy.py` and the messy survey data is `week3_survey_messy.csv`. There is also `clean_responses.py` for cleaning `responses.csv` and `count_roles.py` for counting roles.

Example:

```bash
python3 week3_analysis_buggy.py
```

---

## Competency claim

**C3 — Data cleaning and file handling**

I load real data from CSV with Python (not hardcoded values). The file has missing fields and bad values—for example, `experience_years` sometimes contains a word instead of an integer. I used the traceback to find the bad value, added `try`/`except` around parsing, skipped rows that cannot convert to integers, and printed which rows were skipped. Rows with no participant name and no role are dropped before stats. The script runs to completion on messy input and produces repeatable output.
