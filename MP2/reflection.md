# Mini Project 2 — Reflection

**Author:** Zhian Hu · **Project:** Mobility Insight Kit · **Platform:** Cursor + Python + Vercel

---

## What did you build?

I built **Mobility Insight Kit** — a research tool for UX and service-design teams studying shared micromobility. The deliverable is a self-contained `MP2/` folder with three surfaces collaborators can actually use. First, a published Jupyter notebook (`mp2_notebook.ipynb`) and Python module (`mobility_insights.py`) that clean Seattle’s Fremont Bridge counter CSV, compute peak hours, weekday/weekend splits, directional balance, and monthly trends, then export Plotly figures and a plain-language markdown report. Second, a **live web dashboard** at https://hcde530.vercel.app built with Vite, React, and Recharts — animated summary cards, interactive charts, and a one-click **Refresh data** control. Third, a Vercel serverless endpoint (`/api/analytics`) that pulls the latest ~120k rows from the Seattle Open Data API on demand, aggregates them server-side, and feeds the dashboard so reviewers see current portal data without cloning Python. Someone outside HCDE 530 can use the site immediately, open the notebook on GitHub, or reproduce everything locally from the bundled CSV.

---

## What decisions did you make?

I stayed on the **Cursor + Python research track** rather than Lovable/Bolt because the core work is structured behavioral analysis at scale. My MP2a proposal assumed trip-level scooter logs; the declared Seattle URL actually hosts an **hourly bridge counter**, not vendor MDS exports. I narrowed scope to **corridor demand intensity** — still useful for timing intercepts and ops windows — instead of fabricating trip rows. I packaged analysis logic in `mobility_insights.py` so the notebook stays readable and the web layer can share the same semantics. For distribution I added a **Vercel deployment** alongside the GitHub notebook: graders get a public URL (course requirement) plus native notebook rendering. The live API caches results for fifteen minutes and falls back to bundled JSON if the API fails — a pragmatic split between “always fresh when possible” and “always works offline.” I later added Lime-inspired visual tokens to the dashboard so the interface signals the micromobility product context my audience (Lime/Bird-adjacent teams) actually works in.

---

## What would you do differently?

I would add a **study-protocol export**: when peak hours are computed, automatically download a CSV calendar with suggested intercept windows and draft discussion-guide bullets — bridging quant output to qualitative fieldwork in one click. I would also **abstract data sources** behind a small config file so swapping the Fremont feed for another city’s Socrata dataset does not require editing aggregation code in both Python and the serverless handler; right now the column rename map is duplicated across `mobility_insights.py` and `api/analytics.js`.

---

## What does this work demonstrate?

**Pandas analysis (C5):** `load_and_clean()`, `groupby`, and `quantile` in `mobility_insights.py` — evidenced by concrete outputs like weekday average 122.5 vs weekend 69.7 crossings/hour in `outputs/mobility_insight_report.md`. **Visualization (C6):** notebook Plotly exports in `figures/` plus Recharts heatmaps and bar/area charts in `MP2/web/src/App.tsx`, each titled and axis-labeled for a specific question. **Tooling (C7):** standalone folder with CSV, notebook, module, committed PNGs, README, live URL, and `/api/analytics` live sync. **HCD translation (C8):** `build_insight_report()` and the dashboard “Research readout” section tie metrics to actions (when to observe riders, where directional skew hints at infrastructure friction) while stating that counter data cannot replace trip-level friction interviews. Claims with file paths are in `mp2.md`.
