"""
Fetch structured book metadata from the Open Library Search API.

Run from this folder:
  pip install -r requirements.txt
  python open_library_search.py

If you switch to an API that needs a secret key, put it in a .env file
(never commit .env) and load it with os.environ.get("YOUR_KEY_NAME").
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request

# If you later use an API that needs a key, store it in .env and load it here (do not commit .env).
# pip install python-dotenv  # only needed for keyed APIs
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Example pattern for a keyed API (not needed for Open Library):
# API_KEY = os.environ.get("OPEN_LIBRARY_KEY")  # noqa: ERA001 — template for other APIs


def fetch_books(query: str, limit: int = 8) -> dict:
    """
    Call Open Library's public search endpoint and return the parsed JSON.
    """
    # Build the query string for the API URL: Open Library expects q=... and limit=...
    params = urllib.parse.urlencode({"q": query, "limit": limit})
    url = f"https://openlibrary.org/search.json?{params}"

    # This is a normal GET request; the server returns JSON text (not HTML).
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "HCDE530-Week4-Project/1.0 (course assignment)"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        raw = response.read().decode("utf-8")

    # json.loads turns the response body into nested Python dicts/lists we can loop over.
    return json.loads(raw)


def main() -> None:
    # You can change this string; it is what Open Library searches for in titles and metadata.
    search_query = "human computer interaction"

    # After this call, `data` is the whole JSON object from the API (dict with keys like "docs").
    data = fetch_books(search_query, limit=8)
    # The useful rows live in `docs`; each entry is one bibliographic "work" with many optional fields.
    docs = data.get("docs", [])

    # We only keep a small slice of fields so the output stays readable for people:
    # title — the name of the book/work (core identity for users scanning a list).
    # first_author — primary creator credit (important for trust and attribution in HCD literature).
    # first_publish_year — when the idea entered print (helps place the work in time).
    # edition_count — how many editions Open Library knows about (rough signal of spread/reprints).
    rows = []
    for doc in docs:
        title = doc.get("title", "(no title)")
        authors = doc.get("author_name") or []
        first_author = authors[0] if authors else "(unknown author)"
        year = doc.get("first_publish_year")
        editions = doc.get("edition_count")

        rows.append(
            {
                "title": title,
                "first_author": first_author,
                "first_publish_year": year,
                "edition_count": editions,
            }
        )

    # Terminal output: fixed-width columns so a reviewer can skim results without opening a file.
    print(f"Open Library search: {search_query!r}\n")
    print(f"{'Title':<45} | {'Author':<22} | Year | Editions")
    print("-" * 85)
    for r in rows:
        title = (r["title"][:42] + "…") if len(r["title"]) > 45 else r["title"]
        author = (r["first_author"][:19] + "…") if len(r["first_author"]) > 22 else r["first_author"]
        year_str = str(r["first_publish_year"]) if r["first_publish_year"] is not None else "—"
        ed_str = str(r["edition_count"]) if r["edition_count"] is not None else "—"
        print(f"{title:<45} | {author:<22} | {year_str:^4} | {ed_str}")

    # Write the same records to disk so the run is reproducible and easy to diff or import elsewhere.
    out_path = os.path.join(os.path.dirname(__file__), "open_library_sample.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"query": search_query, "results": rows}, f, indent=2)
    print(f"\nSaved {len(rows)} records to {out_path}")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as e:
        print(f"HTTP error from Open Library: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        print(f"Network error: {e.reason}")
