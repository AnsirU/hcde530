# Mobility Insight Kit (Mini Project 2)

> **Canvas submission:** Repo https://github.com/AnsirU/hcde530 · Live tool https://hcde530.vercel.app · Notebook https://github.com/AnsirU/hcde530/blob/main/MP2/mp2_notebook.ipynb

## What it does

**Mobility Insight Kit** helps **UX researchers, service designers, and urban mobility product teams** (including Lime/Bird-style scooter workflows) understand **when and where** shared micromobility demand peaks on a major Seattle corridor — without relying only on interviews or manual counts.

The tool ingests Seattle’s public **Fremont Bridge bicycle + scooter counter** and produces:

- Cleaned hourly tables and reusable Python analysis functions  
- Plotly charts + a plain-language insight report (notebook path)  
- A **live web dashboard** with animated metrics and refreshable charts (browser path)

Use it to time field studies, spot directional flow imbalance, and baseline seasonal demand — **not** as a replacement for qualitative friction research.

## Who it is for

| Audience | How they use it |
|----------|-----------------|
| UX researchers | Schedule intercepts during computed peak hours (e.g. 08:00, 17:00) |
| Service designers | Read west/east sidewalk skew for parking, charging, or signage placement |
| Mobility PM / city ops | Track weekday vs weekend intensity and monthly seasonality |

Written for practitioners who **did not take HCDE 530** — no course context required.

## Public URLs (use these in Canvas)

| Artifact | URL |
|----------|-----|
| **Live dashboard (primary)** | https://hcde530.vercel.app |
| **GitHub notebook** | https://github.com/AnsirU/hcde530/blob/main/MP2/mp2_notebook.ipynb |
| **Full repository** | https://github.com/AnsirU/hcde530 |

The dashboard syncs from the [Seattle Open Data API](https://data.seattle.gov/resource/65db-xm6k.json) on load or **Refresh data** (portal updates periodically; not per-second live sensors).

## How to run

### Web (no install)

Open https://hcde530.vercel.app

### Notebook

```bash
git clone https://github.com/AnsirU/hcde530.git
cd hcde530/MP2
# open mp2_notebook.ipynb → Kernel → Restart & Run All
```

First cell: `pip install jupyter pandas plotly kaleido`

### Web — local dev

```bash
cd MP2/web
npm install
npm run dev
```

### Python module only

```bash
cd MP2
python -c "from mobility_insights import load_and_clean, build_insight_report; df=load_and_clean('data/fremont_micromobility_hourly.csv'); print(build_insight_report(df))"
```

## MP2 submission checklist (this folder)

| Required item | Location |
|---------------|----------|
| Complete code | `MP2/` (notebook, module, `web/`, `api/` at repo root for Vercel) |
| Competency claims | [`mp2.md`](mp2.md) |
| Reflection (~500 words) | [`reflection.md`](reflection.md) |
| README (this file) | [`README.md`](README.md) |
| Source data | [`data/fremont_micromobility_hourly.csv`](data/fremont_micromobility_hourly.csv) |
| Static chart exports | [`figures/`](figures/) |

## Data source

[City of Seattle Open Data — Fremont Bridge / Shared Mobility Program](https://data.seattle.gov/Transportation/Shared-Mobility-Program-Data/65db-xm6k)

**Scope note:** Trip-level vendor logs are not public CSV; this tool analyzes **hourly corridor counts**. See [`reflection.md`](reflection.md).
