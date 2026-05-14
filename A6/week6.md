# Week 6 — Competency Claim (A6)

**Repository:** https://github.com/AnsirU/hcde530  
**Analysis notebook:** [A6/mp1b_analysis.ipynb](https://github.com/AnsirU/hcde530/blob/main/A6/mp1b_analysis.ipynb)  
**Static chart files (committed):**

- [`chart1_rating_distribution.png`](https://github.com/AnsirU/hcde530/blob/main/A6/chart1_rating_distribution.png) — Question 1 (distribution / composition of ratings).
- [`chart2_mean_thumbs_by_rating.png`](https://github.com/AnsirU/hcde530/blob/main/A6/chart2_mean_thumbs_by_rating.png) — Question 2 (engagement by rating).
- [`chart3_missing_values_by_column.png`](https://github.com/AnsirU/hcde530/blob/main/A6/chart3_missing_values_by_column.png) — Question 3 (data completeness).

---

## C6 — Data Visualization

**What it means:** Building charts that make a specific argument clearly. Choosing a chart type that fits the data structure and the question. Publishing the analysis as a Jupyter notebook on GitHub so someone else can read it and follow the reasoning.

### Strong competency claim

I used three **different Plotly representations** tied to MP1 questions (not repeating bar charts): a **donut pie (`go.Pie`, `hole≈0.45`)** for rating composition so **percentage-of-whole** is the headline read (skew toward 5★ is framed as proportional share), **`go.Scatter` in `lines+markers` mode** for mean thumbs-ups across the **ordinal 1–5 scale** so viewers judge **direction/flat trend** alongside exact means, and a **`plotly.express.treemap`** tiling missing-cell totals so dominant data-quality defects read as **area** comparisons across column names (`reviewCreatedVersion` / `appVersion` vs. scattered text gaps).

The line chart still shows **a relatively flat mean-thumbs trajectory** (`chart2_mean_thumbs_by_rating.png`) — I treat that as a **finding**, not filler: polarity and “helpful” engagement are loosely coupled here.

Notebook + exports: reproducible loaders and `write_image(...)` wiring live in **`A6/mp1b_analysis.ipynb`** with Markdown cells documenting chart-type rationale beside each plot.

**Weak claim (avoid):** “I made charts in my notebook.” — Too vague; avoids linking question → geometry → takeaway.
