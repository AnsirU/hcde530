"""Read responses.csv next to this script, filter rows, title-case role, write responses_cleaned.csv."""

from __future__ import annotations

import csv
from pathlib import Path

INPUT_NAME = "responses.csv"
OUTPUT_NAME = "responses_cleaned.csv"

# Rows are kept if any of these columns is non-empty after stripping (CSV may use
# "name" or "participant_id" instead of a literal "name" column).
_ID_COLUMNS = ("name", "participant_id")


def _normalize_keys(row: dict[str, str | None]) -> dict[str, str]:
    """Strip UTF-8 BOM from first column name if present."""
    out: dict[str, str] = {}
    for key, val in row.items():
        if key is None:
            continue
        clean_key = key.lstrip("\ufeff")
        out[clean_key] = "" if val is None else val
    return out


def _row_has_identity(row: dict[str, str]) -> bool:
    for col in _ID_COLUMNS:
        if (row.get(col) or "").strip():
            return True
    return False


def main() -> None:
    base = Path(__file__).resolve().parent
    in_path = base / INPUT_NAME
    out_path = base / OUTPUT_NAME

    with in_path.open(newline="", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in)
        raw_fieldnames = reader.fieldnames
        if not raw_fieldnames:
            raise ValueError(f"No header row in {in_path}")

        fieldnames = [k.lstrip("\ufeff") if k else k for k in raw_fieldnames]

        rows_out: list[dict[str, str]] = []
        for row in reader:
            row = _normalize_keys(row)
            if not _row_has_identity(row):
                continue
            out = dict(row)
            role_raw = out.get("role", "") or ""
            out["role"] = str(role_raw).strip().title()
            rows_out.append(out)

    with out_path.open("w", newline="", encoding="utf-8") as f_out:
        writer = csv.DictWriter(
            f_out,
            fieldnames=fieldnames,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows_out)


if __name__ == "__main__":
    main()
