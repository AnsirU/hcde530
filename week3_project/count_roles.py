"""Count how many times each role appears in responses.csv (same folder as this script)."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

INPUT_NAME = "responses.csv"
ROLE_COLUMN = "role"


def _normalize_keys(row: dict[str, str | None]) -> dict[str, str]:
    out: dict[str, str] = {}
    for key, val in row.items():
        if key is None:
            continue
        clean_key = key.lstrip("\ufeff")
        out[clean_key] = "" if val is None else val
    return out


def main() -> None:
    base = Path(__file__).resolve().parent
    path = base / INPUT_NAME

    counts: Counter[str] = Counter()
    skipped_empty = 0

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"No header row in {path}")
        for row in reader:
            row = _normalize_keys(row)
            role = (row.get(ROLE_COLUMN) or "").strip()
            if not role:
                skipped_empty += 1
                continue
            counts[role] += 1

    # Highest count first, then alphabetical by role name
    ordered = sorted(counts.items(), key=lambda x: (-x[1], x[0].lower()))

    print(f"Role counts ({path.name}, rows with non-empty role): {sum(counts.values())}")
    if skipped_empty:
        print(f"Skipped rows with empty role: {skipped_empty}")
    print()
    print(f"{'role':<30} {'count':>5}")
    print("-" * 38)
    for role, n in ordered:
        print(f"{role:<30} {n:>5}")


if __name__ == "__main__":
    main()
