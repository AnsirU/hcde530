# Mini Project 2 — Competency Claim(s)

**Author:** Zhian Hu  
**Repository:** [`AnsirU/hcde530`](https://github.com/AnsirU/hcde530)  
**Live tool (primary URL for Canvas):** https://hcde530.vercel.app  
**Notebook:** [`mp2_notebook.ipynb`](https://github.com/AnsirU/hcde530/blob/main/MP2/mp2_notebook.ipynb)  
**Supporting module:** `mobility_insights.py` · **Web app:** `MP2/web/` · **Live API:** `api/analytics.js`

---

## C5 — Data analysis with pandas

I built **`load_and_clean()`** and five analysis functions in `mobility_insights.py` that transform raw Seattle counter CSVs into typed datetime/numeric fields (`hour`, `weekday`, `is_weekend`, `west_share`) and answer research questions via **`groupby`**, **`quantile`**, and **`agg`** — e.g., `peak_hours()`, `weekday_weekend_compare()`, and `low_activity_windows()`. The same aggregation logic is mirrored in `api/analytics.js` for live portal sync. Evidence: `mp2_notebook.ipynb` §1–2, `mobility_insights.py` lines 26–101, and report output in `outputs/mobility_insight_report.md` (peak hours 17:00/08:00/16:00; weekday 122.5 vs weekend 69.7 avg crossings).

## C6 — Data visualization

Four Plotly views in the notebook map question → geometry: **heatmap** (hour × weekday), **line** (monthly trend), **bar** (peak-hour profile), **stacked area** (directional demand) — each exported to `figures/*.png` with Kaleido. The deployed dashboard (`MP2/web/`) adds Recharts bar/area charts with **animated count-up metrics** and weekday tabs. Chart types match data structure (2D temporal heatmap vs ordered monthly line) rather than repeating one geometry.

## C7 — Tooling / reproducible research workflow

Mobility Insight Kit ships as a **standalone `MP2/` package** plus **public deployment**: bundled `data/fremont_micromobility_hourly.csv`, executed notebook, `mobility_insights.py`, generated reports, and https://hcde530.vercel.app. The `/api/analytics` endpoint fetches the latest Seattle Open Data snapshot on page load or refresh (15-minute cache). README documents notebook, web, and CLI entry points for graders who were not in the course.

## C8 — HCD sensemaking (research translation)

`build_insight_report()` and the dashboard **Research readout** connect metrics to **research actions** — when to run intercepts, which quiet hours suit maintenance studies, how west/east skew informs parking placement — while explicitly limiting claims: hourly counter data ≠ trip-level vendor logs. Section 4 of `mp2_notebook.ipynb` and the live UI translate numbers into workshop-ready language without replacing qualitative methods.
