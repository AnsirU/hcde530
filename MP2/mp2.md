# Mini Project 2 — Competency Claim(s)

**Author:** Zhian Hu  
**Repository:** [`AnsirU/hcde530`](https://github.com/AnsirU/hcde530)  
**Live tool:** https://hcde530.vercel.app  
**Notebook:** [`mp2_notebook.ipynb`](https://github.com/AnsirU/hcde530/blob/main/MP2/mp2_notebook.ipynb)  
**Supporting module:** `mobility_insights.py` · **Web source:** `MP2/web/`

---

## C5 — Data analysis with pandas

I built **`load_and_clean()`** and five analysis functions in `mobility_insights.py` that transform raw Seattle counter CSVs into typed datetime/numeric fields (`hour`, `weekday`, `is_weekend`, `west_share`) and answer research questions via **`groupby`**, **`quantile`**, and **`agg`** — e.g., `peak_hours()`, `weekday_weekend_compare()`, and `low_activity_windows()`. The notebook’s Data Profile cells (`head`, `info`, shape checks) document data quality before charts run. Evidence: `mp2_notebook.ipynb` §1–2 and `mobility_insights.py` lines 24–95.

## C6 — Data visualization

Four Plotly views in the notebook map question → geometry: **heatmap** (hour × weekday intensity), **line** (monthly trend), **bar** (peak-hour profile), **stacked area** (directional west/east demand). Each has a **title and axis labels** and is exported with **Kaleido** to `figures/*.png` for offline grading. I chose heatmaps for two-dimensional temporal patterns and lines for ordered monthly series rather than repeating one chart type.

## C7 — Tooling / reproducible research workflow

Mobility Insight Kit is a **standalone `MP2/` package** plus a **deployed web dashboard** at https://hcde530.vercel.app: bundled CSV, Python module (`mobility_insights.py`), executed notebook, generated `outputs/mobility_insight_report.md`, and a Vite/React front-end (`MP2/web/`) that precomputes analytics JSON and renders animated charts for researchers without a local Python environment. `build_insight_report()` turns aggregates into **plain-language findings** for non-coders.

## C8 — HCD sensemaking (research translation)

`build_insight_report()` explicitly connects metrics to **research actions** (when to run intercepts, where directional imbalance suggests parking/signage friction, which quiet hours suit maintenance studies) and states limits: counter data ≠ trip microdata. Section 4 of the notebook prints the report for workshop readouts — bridging computation and service-design decisions without claiming surveys are obsolete.
