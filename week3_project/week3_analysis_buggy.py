import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent
INPUT_CSV = BASE / "week3_survey_messy.csv"
OUTPUT_CSV = BASE / "week3_survey_cleaned.csv"


def load_survey_rows(csv_path: Path) -> tuple[list[dict[str, str]], list[str]]:
    """Read a survey CSV file and return all rows plus the header column names."""
    rows: list[dict[str, str]] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        for row in reader:
            rows.append({k: (v if v is not None else "") for k, v in row.items()})
    return rows, fieldnames


def drop_rows_without_participant_identity(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], int]:
    """
    Remove rows that have no participant name and no role.

    Those rows are anonymous fragments and should not affect role or experience stats.
    """
    kept: list[dict[str, str]] = []
    for r in rows:
        has_name = bool((r.get("participant_name") or "").strip())
        has_role = bool((r.get("role") or "").strip())
        if has_name or has_role:
            kept.append(r)
    dropped = len(rows) - len(kept)
    return kept, dropped


def write_cleaned_survey_csv(
    csv_path: Path,
    fieldnames: list[str],
    rows: list[dict[str, str]],
) -> None:
    """Write cleaned survey rows to a new CSV file (UTF-8, same columns as the source)."""
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def summarize_data(rows: list[dict[str, str]]) -> str:
    """
    Build a plain-language summary of cleaned survey data.

    Includes row count, unique roles, and how many rows have an empty name field.
    (Name is read from ``participant_name``, the column used in this dataset.)
    """
    n = len(rows)
    roles = {(r.get("role") or "").strip().title() for r in rows}
    roles.discard("")
    unique_roles = sorted(roles, key=str.lower)
    empty_name = sum(1 for r in rows if not (r.get("participant_name") or "").strip())

    lines = [
        f"There are {n} rows in the cleaned data.",
        f"Unique values in the role column ({len(unique_roles)}): {', '.join(unique_roles)}."
        if unique_roles
        else "There are no non-empty role values.",
        f"Rows with an empty name field (participant_name): {empty_name}.",
    ]
    return "\n".join(lines)


def main() -> None:
    rows, fieldnames = load_survey_rows(INPUT_CSV)
    loaded_count = len(rows)

    rows, dropped = drop_rows_without_participant_identity(rows)
    print(f"Dropped {dropped} row(s) with no participant name and no role.")

    write_cleaned_survey_csv(OUTPUT_CSV, fieldnames, rows)
    print(f"Wrote cleaned data to {OUTPUT_CSV.name}")

    print("\nSummary:")
    print(summarize_data(rows))

    # Count responses by role
    role_counts: dict[str, int] = {}
    for row in rows:
        role = (row.get("role") or "").strip().title()
        if not role:
            continue
        role_counts[role] = role_counts.get(role, 0) + 1

    print("\nResponses by role:")
    for role, count in sorted(role_counts.items()):
        print(f"  {role}: {count}")

    # Average years of experience (only rows where experience_years parses as an integer)
    total_experience = 0
    experience_count = 0
    skipped_experience: list[tuple[str, str]] = []

    for row in rows:
        raw = (row.get("experience_years") or "").strip()
        try:
            total_experience += int(raw)
            experience_count += 1
        except ValueError:
            skipped_experience.append((row.get("response_id", "?"), raw))

    if skipped_experience:
        print(
            f"\nSkipped {len(skipped_experience)} row(s) with non-numeric experience_years "
            "(cannot convert to int — e.g. words instead of digits)."
        )
        for rid, raw in skipped_experience:
            print(f"  {rid}: {raw!r}")

    if experience_count:
        avg_experience = total_experience / experience_count
        print(f"\nAverage years of experience: {avg_experience:.1f} (from {experience_count} valid rows)")
    else:
        print("\nAverage years of experience: n/a (no numeric experience values)")

    # Top 5 highest satisfaction scores
    scored_rows: list[tuple[str, int]] = []
    for row in rows:
        ss = (row.get("satisfaction_score") or "").strip()
        if ss:
            scored_rows.append((row["participant_name"], int(ss)))

    # Descending: highest scores first (ascending sort would make [:5] the five *lowest*).
    scored_rows.sort(key=lambda x: x[1], reverse=True)
    top5 = scored_rows[:5]

    print("\nTop 5 satisfaction scores:")
    for name, score in top5:
        print(f"  {name}: {score}")


if __name__ == "__main__":
    main()
