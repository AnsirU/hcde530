#!/usr/bin/env python3
"""Regenerate public/data/analytics.json from mobility_insights.py (run before deploy)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent))

from mobility_insights import (  # noqa: E402
    COL_TOTAL,
    direction_balance,
    load_and_clean,
    low_activity_windows,
    monthly_trend,
    peak_hours,
    weekday_weekend_compare,
)

DAY_ORDER = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def main() -> None:
    csv_path = ROOT.parent / "data" / "fremont_micromobility_hourly.csv"
    df = load_and_clean(csv_path)

    heat = df.groupby(["weekday", "hour"], as_index=False)[COL_TOTAL].mean()
    heat_pivot = {d: [0.0] * 24 for d in DAY_ORDER}
    for _, row in heat.iterrows():
        heat_pivot[row["weekday"]][int(row["hour"])] = round(float(row[COL_TOTAL]), 2)

    hourly = df.groupby("hour", as_index=False)[COL_TOTAL].mean().sort_values("hour")
    peaks = peak_hours(df, top_n=8)
    ww = weekday_weekend_compare(df)
    direction = direction_balance(df)
    monthly = monthly_trend(df).tail(36)
    quiet = low_activity_windows(df)

    payload = {
        "meta": {
            "records": len(df),
            "start": str(df["timestamp"].min().date()),
            "end": str(df["timestamp"].max().date()),
        },
        "summary": {
            "weekday_avg": round(
                float(ww.loc[ww.day_type == "weekday", "avg_crossings"].iloc[0]), 1
            ),
            "weekend_avg": round(
                float(ww.loc[ww.day_type == "weekend", "avg_crossings"].iloc[0]), 1
            ),
            "west_share_pct": round(direction["mean_west_share"] * 100, 1),
            "west_dominant_pct": round(direction["hours_west_dominant_pct"], 1),
            "peak_hours": [f"{int(r.hour):02d}:00" for _, r in peaks.head(3).iterrows()],
            "quiet_hours": [f"{int(r.hour):02d}:00" for _, r in quiet.iterrows()],
        },
        "hourly_avg": [
            {"hour": int(r.hour), "avg": round(float(r[COL_TOTAL]), 2)}
            for _, r in hourly.iterrows()
        ],
        "heatmap": heat_pivot,
        "monthly": [
            {"month": r.year_month, "avg": round(float(r.avg_hourly_crossings), 2)}
            for _, r in monthly.iterrows()
        ],
        "direction_monthly": [
            {
                "month": m,
                "west": round(float(sub["crossings_west"].mean()), 2),
                "east": round(float(sub["crossings_east"].mean()), 2),
            }
            for m in monthly["year_month"]
            for sub in [df[df["year_month"] == m]]
        ],
    }

    out = ROOT / "public" / "data" / "analytics.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
