# Mobility Insight Kit (Mini Project 2)

## What it does

**Mobility Insight Kit** is a Python research tool for **UX researchers, service designers, and urban mobility product teams** (e.g., Lime/Bird-adjacent workflows, city ops partners). It turns Seattle’s public **Fremont Bridge bicycle + scooter counter** feed into:

- Cleaned, analysis-ready hourly tables  
- Reusable functions (`peak_hours`, weekday/weekend compare, directional balance, monthly trend, quiet windows)  
- Plotly visual summaries (heatmap, trends, peak-hour profile, directional stack)  
- An auto-generated **plain-language insight report** (`outputs/mobility_insight_report.md`)

Use it when you need **quantitative demand patterns** before or alongside interviews and field observation — not as a substitute for qualitative work.

## Who it is for

| Audience | How they use it |
|----------|-----------------|
| UX researchers | Time intercept studies to peak corridors/hours |
| Service designers | Spot asymmetric flow and quiet maintenance windows |
| Mobility PM / ops | Seasonal intensity baselines for fleet or parking policy |

## Public URL (live artifact — no server)

**Published notebook (GitHub renders natively):**  
https://github.com/AnsirU/hcde530/blob/main/MP2/mp2_notebook.ipynb

**Repository:** https://github.com/AnsirU/hcde530

## How to run

### Option A — Notebook (recommended)

1. Clone the repo and `cd MP2`  
2. Create/activate a Python 3.9+ environment  
3. Open `mp2_notebook.ipynb`  
4. **Kernel → Restart & Run All** (first cell installs `jupyter`, `pandas`, `plotly`, `kaleido`)

Bundled data: `data/fremont_micromobility_hourly.csv` (~120k hourly rows, ~3.7 MB).

### Option B — Script / module

```bash
cd MP2
python -c "from mobility_insights import load_and_clean, build_insight_report; df=load_and_clean('data/fremont_micromobility_hourly.csv'); print(build_insight_report(df))"
```

Supporting code: `mobility_insights.py`

## Data source

[City of Seattle Open Data — Shared Mobility Program / Fremont Bridge counter](https://data.seattle.gov/Transportation/Shared-Mobility-Program-Data/65db-xm6k)  
Columns: timestamp, total crossings, west sidewalk, east sidewalk (hourly).

**Scope note:** Vendor trip-level logs (start/end/provider/geo per trip) are **not** published as open CSV on this portal. This tool analyzes the **public counter feed** at your MP2a program URL and frames findings as **corridor demand intensity** — see [`reflection.md`](reflection.md) for the MP2a pivot.

## Outputs committed in this folder

| Path | Purpose |
|------|---------|
| `mp2_notebook.ipynb` | Main tool |
| `mobility_insights.py` | Reusable analysis functions |
| `data/fremont_micromobility_hourly.csv` | Source data |
| `figures/*.png` | Static chart exports |
| `outputs/mobility_insight_report.md` | Generated after notebook run |
| `mp2.md` | Competency claims |
| `reflection.md` | 500-word process reflection |
