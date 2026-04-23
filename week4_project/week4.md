# Week 4 — API data pull

This folder contains `open_library_search.py`, which calls the **Open Library Search API** (not the class weather demo), parses **JSON**, and extracts multiple fields per record. Running the script prints a readable table and writes `open_library_sample.json`.

## How to run

```bash
cd week4_project
pip install -r requirements.txt   # optional unless you use python-dotenv for a keyed API
python open_library_search.py
```

---

## C4 — Competency claim (APIs and Data Acquisition)

I read the **Open Library Search API** documentation and implemented a **GET** request to `https://openlibrary.org/search.json`. **This endpoint does not require an API key**, so there is no secret in my code or repo; I still use the **environment-variable / `.env` pattern** documented in the script and in `.env.example`, and the **repository `.gitignore` ignores `.env`** so a keyed API would not get committed by mistake.

**What the endpoint returns:** JSON with search metadata (for example how many hits exist) and a **`docs` array**. Each item in `docs` is one bibliographic *work* with many optional fields.

**What I did with that response:** I capped the number of results with the API’s **`limit`** parameter, **walked `docs` in Python**, **pulled four fields** (`title`, first entry of `author_name`, `first_publish_year`, `edition_count`), **handled missing authors safely**, **printed a column-aligned summary**, and **saved the same structured rows to `open_library_sample.json`** for review or later analysis.

The paragraphs below explain **why I chose this dataset for HCD work** and **how the response is structured in practice**.

---

## Endpoint, parameters, and response shape (short)

| Piece | Detail |
|--------|--------|
| **Endpoint** | `GET https://openlibrary.org/search.json` |
| **Parameters I used** | `q` — search string (I use `human computer interaction`); `limit` — max number of `docs` rows to return |
| **Top-level JSON** | Includes keys such as `numFound` (total matches) and **`docs`** (the list I iterate) |
| **Each `docs[i]` object** | Can include `title`, `author_name` (list), `first_publish_year`, `edition_count`, and many other optional keys depending on the work |

Official reference (for reviewers): [Open Library Search API documentation](https://openlibrary.org/dev/docs/api/search) (`/search.json`).

---

## HCD reflection — why this dataset and response matter

Human-centered design often starts from **secondary data** already stored in institutional systems. A search API turns that catalog into **structured, machine-readable JSON**, which makes it possible to **sample what the collection surfaces** for a topic (here, HCI-related books), **see who is credited**, **when works entered the discourse**, and **how many editions appear in the catalog** — all decisions shaped by **information architecture** and curation.

Understanding **`docs` as a list of heterogeneous objects** (some fields missing) is also good practice for real APIs: the script has to **defend against empty author lists** and absent years instead of assuming a perfect table. That mirrors how teams consume analytics or survey exports that also arrive as nested JSON.
