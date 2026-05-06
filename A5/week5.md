# Week 5 — Competency Claim(s)

## C5 — Data Analysis with Pandas

**Claim:** I used pandas on my Mini Project 1 dataset (ChatGPT app reviews from Kaggle) to inspect structure, summarize distributions, isolate subsets, aggregate by rating, and quantify missingness—with plain-English notes tied to each step.

**What I did (evidence in `week5_chatgpt_kaggle_five_questions.ipynb`):**

- **`head()` / `info()`:** Verified roughly one million rows and eight columns (`reviewId`, `userName`, `content`, `score`, `thumbsUpCount`, version/time fields). Confirmed dtypes and where non-null counts drop—this frames what MP1 / Week 6 can rely on without extra cleaning.
- **`value_counts()` on star rating (`score`):** Measured how skewed sentiment labels are (heavy concentration at 5 stars). That imbalance matters for any comparison across ratings or sampling strategy later.
- **Boolean filter (`df[rating_col] < 3`):** Isolated dissatisfied reviewers (~87k rows from the cached snapshot when last run). That subset is the natural pool for complaint-focused qualitative coding in MP1.
- **`groupby(score)["thumbsUpCount"].mean()`:** Compared average thumbs-up counts across ratings (community engagement signal). Any systematic gap across stars is something I’m treating as follow-up for MP1—noticing whether engagement aligns with polarity or with controversy/noise.
- **`isnull().sum()`:** Showed version-related columns (`reviewCreatedVersion`, `appVersion`) share the same missing count (~74k in that snapshot), with almost-complete text/usernames—useful for deciding which fields to drop or impute in the Week 6 notebook.

**Interpretation (beyond running cells):** The rating distribution and the low-score subset size tell me MP1 cannot assume balanced labels; missing version metadata is structured enough to handle deliberately rather than ignore; grouping thumbs-ups by star rating gives one quantitative lens before digging into review text.
