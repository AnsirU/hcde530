# Week 6 — Competency Claim (A6)

**Repository:** https://github.com/AnsirU/hcde530  
**Analysis notebook:** [A6/mp1b_analysis.ipynb](https://github.com/AnsirU/hcde530/blob/main/A6/mp1b_analysis.ipynb)  
**Static chart files (committed):**

- [`chart1_rating_distribution.png`](https://github.com/AnsirU/hcde530/blob/main/A6/chart1_rating_distribution.png) — Question 1 (distribution of ratings).
- [`chart2_mean_thumbs_by_rating.png`](https://github.com/AnsirU/hcde530/blob/main/A6/chart2_mean_thumbs_by_rating.png) — Question 2 (engagement by rating).
- [`chart3_missing_values_by_column.png`](https://github.com/AnsirU/hcde530/blob/main/A6/chart3_missing_values_by_column.png) — Question 3 (data completeness).

---

## C6 — Data Visualization

**What it means:** Building charts that make a specific argument clearly. Choosing a chart type that fits the data structure and the question. Publishing the analysis as a Jupyter notebook on GitHub so someone else can read it and follow the reasoning.

### Strong competency claim

I used **vertical bar charts** for star-rating counts and for mean thumbs-up counts by rating because star ratings are a **small ordered discrete scale (1–5)** and bars make exact comparisons between levels easy—the audience can read magnitude at a glance without implying a continuous trend between unrelated stars.

I used a **horizontal bar chart** for missing-value counts **per column** because column names are long technical strings (`reviewCreatedVersion`, `appVersion`): horizontal orientation keeps labels readable without crowding or rotation.

Mean thumbs-up averages differ only slightly across star levels in this snapshot (**a relatively flat pattern**—see `chart2_mean_thumbs_by_rating.png`). I still treat that as a **finding**: the platform’s “helpful” signal does not strongly separate polarity here, which matters if I hoped engagement as a proxy for “visibility of complaints.”

All three figures were generated in Plotly from the same reproducible pandas pipeline documented in **`A6/mp1b_analysis.ipynb`**, and exported to `.png` with Kaleido (`fig.write_image(...)`) so the visuals are reviewable outside the notebook.

**Weak claim (avoid):** “I made charts in my notebook.” — This does not tie chart choice to structure, cite paths, or state what each figure argues.
