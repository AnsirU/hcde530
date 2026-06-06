# Mini Project 2 — Reflection

**Author:** Zhian Hu · **Project:** Mobility Insight Kit · **Platform:** Cursor + Python

---

## What did you build?

I built **Mobility Insight Kit**, a Python research utility packaged in the `MP2/` folder for UX researchers and service designers working on shared micromobility. The centerpiece is a published Jupyter notebook (`mp2_notebook.ipynb`) plus a reusable module (`mobility_insights.py`). Together they ingest Seattle’s public Fremont Bridge bicycle-and-scooter counter data, clean hourly records, run standardized analyses (peak hours, weekday versus weekend volume, east–west directional balance, monthly trends, and low-activity windows), render four Plotly summaries exported as PNGs, and auto-generate a markdown insight report a researcher can paste into a readout. A collaborator outside HCDE 530 could open the GitHub notebook in a browser without installing anything, or clone the repo, run **Restart & Run All**, and reproduce every table and figure from the bundled CSV.

---

## What decisions did you make?

I stayed on the **Cursor + Python research track** because the core problem is structured behavioral data at scale, not interface prototyping in Lovable or Bolt. For data, I used the City of Seattle portal entry linked in my MP2a declaration ([Shared Mobility Program Data](https://data.seattle.gov/Transportation/Shared-Mobility-Program-Data/65db-xm6k)). That URL resolves to the **Fremont Bridge hourly counter**, not vendor trip logs with start/end/provider fields. Trip-level MDS exports are permit-bound and not published as open CSV, so I **narrowed scope** to corridor **demand intensity**—still actionable for timing field studies and ops planning—rather than faking trip rows. I committed a ~3.7 MB subset of the full history so graders have a self-contained artifact. I extracted logic into `mobility_insights.py` so the notebook reads as a workflow tool, not a one-off homework script, and added `build_insight_report()` to translate numbers into plain language for HCD audiences.

---

## What would you do differently?

First, I would add a **thin configuration layer** (`config.yaml` for date filters, corridor labels, report sections) so researchers swap datasets without editing function code—important if Seattle later publishes trip aggregates or if teams compare multiple counter locations. Second, I would integrate **one qualitative linkage step**: e.g., export peak-hour timestamps as a CSV calendar for scheduling ride-alongs, with prompt text for intercept guides. The current tool stops at quantitative patterns; bridging to study protocols would make it feel more like a deployed research instrument and less like an analysis notebook.

---

## What does this work demonstrate?

This project shows **pandas competency** in `load_and_clean()` and the `groupby`/`quantile` helpers that power every chart. It shows **visualization judgment** in matching heatmaps to hour-by-weekday questions and line charts to monthly seasonality, with labeled axes and committed PNGs. It shows **tool thinking** via a module + notebook + README + public URL pattern aligned with course delivery requirements. It also shows **HCD translation**: the generated report in `outputs/mobility_insight_report.md` ties peaks and directional skew to concrete research moves (when to observe riders, where asymmetry hints at infrastructure friction) while documenting that counter data cannot answer parking-compliance or per-provider trip questions alone. Those claims are expanded in `mp2.md` with file-level evidence.
