import csv
from pathlib import Path

# Load the survey data from a CSV file next to this script (reads real data, not hardcoded rows).
BASE = Path(__file__).resolve().parent
filename = BASE / "week3_survey_messy.csv"
rows = []

with open(filename, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

loaded_count = len(rows)

# Remove rows missing both participant_name and role (e.g. response R005): they are not valid survey
# participants for role or experience summaries, only stray text responses.
rows = [
    r
    for r in rows
    if (r.get("participant_name") or "").strip()
    or (r.get("role") or "").strip()
]

print(f"Dropped {loaded_count - len(rows)} row(s) with no participant name and no role.")

# Count responses by role
# Normalize role names so "ux researcher" and "UX Researcher" are counted together
role_counts = {}

for row in rows:
    role = (row.get("role") or "").strip().title()
    if not role:
        continue
    if role in role_counts:
        role_counts[role] += 1
    else:
        role_counts[role] = 1

print("Responses by role:")
for role, count in sorted(role_counts.items()):
    print(f"  {role}: {count}")

# Calculate the average years of experience
total_experience = 0
for row in rows:
    total_experience += int(row["experience_years"])

avg_experience = total_experience / len(rows)
print(f"\nAverage years of experience: {avg_experience:.1f}")

# Find the top 5 highest satisfaction scores
scored_rows = []
for row in rows:
    ss = (row.get("satisfaction_score") or "").strip()
    if ss:
        scored_rows.append((row["participant_name"], int(ss)))

scored_rows.sort(key=lambda x: x[1], reverse=True)
top5 = scored_rows[:5]

print("\nTop 5 satisfaction scores:")
for name, score in top5:
    print(f"  {name}: {score}")
