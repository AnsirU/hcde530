# Mini Project 1 — Competency Claim(s)

**Author:** Zhian Hu  
**Repository:** [`AnsirU/hcde530`](https://github.com/AnsirU/hcde530)  
**Mini Project artifact:** **`MP1/mini_project_1.ipynb`** (standalone folder with **`data/`** + **`figures/`**) — [notebook on GitHub](https://github.com/AnsirU/hcde530/blob/main/MP1/mini_project_1.ipynb)

---

## C5 — Analysis with pandas

My MP1 **`Section 2 — Data Profile`** runs the mandated pandas inspections (`df.head()`, `df.info()`, `df.describe()`, `df.isnull().sum()`) with a concise interpretation tied to **each output**, showing I can relate dtypes, descriptive stats, and **structured missing pairs** (`reviewCreatedVersion` / `appVersion`) back to plausible analytic limits (version-level studies). Supporting exploratory work appears in Weeks 5–6 notebooks (e.g. **`A5/week5_chatgpt_kaggle_five_questions.ipynb`**).

## C6 — Data visualization

Three Plotly views in **`Section 3 — Analysis`** each answer **one analytical question**, use **labeled titles / axes where applicable**, and diversify geometry (donut composition for polarity share, **`lines+markers`** across ordinal ratings for average thumbs-ups, **treemap** for missing-cell magnitudes). Every figure is reproducibly scripted and exported with **Kaleido** alongside committed PNGs under **`MP1/figures/`** so reviewers see outputs even offline.

## Reproducible workflow statement

Mini Project 1 submits as **`MP1/`** with **`!pip install jupyter plotly kaleido pandas`** in the first setup cell plus bundled **`data/chatgpt_reviews_sample.csv`** (seeded proportional random subset for GitHub size limits — see **`README.md`**). **`Section 5`** narrates tooling surprises (notebook MIME dependencies) and pragmatic sampling choices so competency evidence includes **process transparency**, not only charts.
