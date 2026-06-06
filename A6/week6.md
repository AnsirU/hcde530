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

---

## Chart justifications

Each chart answers one MP1 analytical question. The geometry is chosen for how readers should compare values—not because it is the default in a tutorial.

### Chart 1 — Rating distribution (donut pie)

| | |
|---|---|
| **Question** | How concentrated are star ratings at each level—is sentiment dominated by 5★ reviews? |
| **Why this chart type** | Ratings are **five exhaustive categories that sum to 100%** of reviews. A donut pie (`go.Pie`, `hole≈0.45`) encodes **share-of-whole** as wedge angle, which is the direct read for polarity skew. Bars would work, but wedges make “how much of the corpus is 5★?” the headline comparison. |
| **Design choices** | Percentages render **inside** wedges (not outside labels that overlapped the title on small slices like 2★). A right-side **legend** lists every star level with hover counts. Title asks the research question plainly: *How are ChatGPT Play Store ratings distributed?* |
| **Takeaway** | ~**77%** of reviews are 5★; 1–3★ combined are a thin minority. Any theme sampling or subgroup comparison must **stratify or normalize**—raw counts will over-represent praise. |

### Chart 2 — Mean thumbs-ups by rating (line + markers)

| | |
|---|---|
| **Question** | Do lower-star reviews draw more thumbs-ups on average (amplified complaints), or does engagement track positivity? |
| **Why this chart type** | Star ratings form an **ordinal 1–5 scale**. `go.Scatter` in `lines+markers` mode links category means so viewers judge **direction**—rising, falling, or flat—while markers preserve exact y-values. A bar chart would show the same numbers but under-emphasize whether engagement **systematically** changes across the scale. |
| **Design choices** | Linear x-axis with `dtick=1` treats stars as ordered categories. Axis titles name the units (*mean thumbs-up count per review*). |
| **Takeaway** | Means sit in a **narrow, relatively flat band** across stars. Thumbs-ups are **not** a loud signal separating complaints from praise in this corpus—qualitative reading still matters. A flat line is a **finding**, not filler. |

### Chart 3 — Missing values by column (horizontal bar)

| | |
|---|---|
| **Question** | Which columns are unreliable because of systematic missing values—especially version metadata needed for rollout studies? |
| **Why this chart type** | Missingness is compared across **eight column names** where **severity differs by orders of magnitude** (`reviewCreatedVersion` / `appVersion` ≈ 77k gaps vs. near-zero on `score`). A horizontal bar chart lists **every column on the y-axis** so readers compare absolute missing counts in one scan. A treemap with only two non-zero fields collapsed into two equal tiles and failed to show the contrast with complete columns. |
| **Design choices** | Title states the **decision intent**: *Which columns are too incomplete for version-based analysis?* Subtitle explains that long orange/red bars flag fields to exclude or bucket as “unknown.” Bar-end labels show count + percent; color encodes **% of rows missing**. |
| **Takeaway** | `reviewCreatedVersion` and `appVersion` share the same missing count (~7.2% of rows)—structured gaps, not random noise. Version-aware analyses need explicit exclusions or an **“unknown version”** bucket before drawing rollout conclusions. |

---

### Strong competency claim

I used three **different Plotly representations** tied to MP1 questions (not three identical bar charts): a **donut pie** for rating **composition**, a **line + markers** scatter for **ordinal engagement trend**, and a **horizontal bar chart** for **comparing missing-cell severity across every column**.

Notebook + exports: reproducible loaders and `write_image(...)` wiring live in **`A6/mp1b_analysis.ipynb`** with Markdown cells documenting chart-type rationale beside each plot.

**Weak claim (avoid):** “I made charts in my notebook.” — Too vague; avoids linking question → geometry → takeaway.
