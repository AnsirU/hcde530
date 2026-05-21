# Mini Project 1 (HCDE 530) — standalone package

Open **`mini_project_1.ipynb`** from this folder and run **Kernel → Restart & Run All** so the working directory resolves `data/` and `figures/` correctly.

## Data

Bundled CSV: **`data/chatgpt_reviews_sample.csv`** — **`n = 70,000` rows** sampled with **`random_state=42`** from the full Kaggle file so rating proportions (~heavy 5★) match the live feed at smaller size (~ 9 MiB, suitable for GitHub).

Full corpus: [ChatGPT reviews (daily updated) on Kaggle](https://www.kaggle.com/datasets/ashishkumarak/chatgpt-reviews-daily-updated) (`ashishkumarak/chatgpt-reviews-daily-updated`). Swap `DATA_PATH` in the notebook to your local **`chatgpt_reviews.csv`** to rerun on **all** rows (expect ~ 130 MiB disk + more RAM).

## Deliverables committed here

- `mini_project_1.ipynb` — four required sections (+ optional §5 process), setup cell as specified  
- `data/chatgpt_reviews_sample.csv` — source table for rerun  
- `figures/*.png` — Plotly + Kaleido static exports mirrored in Analysis  

Repository root competency write-up: **`../mp1.md`**
