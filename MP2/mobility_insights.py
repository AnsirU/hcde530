"""
Mobility Insight Kit — reusable analysis helpers for Seattle micromobility counter data.

Designed for UX researchers / service designers who need quantitative demand patterns
without running ad-hoc pandas snippets for every question.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

# Canonical column names after load_and_clean()
COL_TS = "timestamp"
COL_TOTAL = "crossings_total"
COL_WEST = "crossings_west"
COL_EAST = "crossings_east"

RAW_DATE = "Date"
RAW_TOTAL = "Fremont Bridge Sidewalks, south of N 34th St Total"
RAW_WEST = "Fremont Bridge Sidewalks, south of N 34th St Cyclist West Sidewalk"
RAW_EAST = "Fremont Bridge Sidewalks, south of N 34th St Cyclist East Sidewalk"


def load_and_clean(csv_path: str | Path) -> pd.DataFrame:
    """Load hourly Fremont Bridge counter CSV and return analysis-ready frame."""
    path = Path(csv_path)
    df = pd.read_csv(path)
    df = df.rename(
        columns={
            RAW_DATE: COL_TS,
            RAW_TOTAL: COL_TOTAL,
            RAW_WEST: COL_WEST,
            RAW_EAST: COL_EAST,
        }
    )
    df[COL_TS] = pd.to_datetime(df[COL_TS], errors="coerce")
    for c in (COL_TOTAL, COL_WEST, COL_EAST):
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna(subset=[COL_TS, COL_TOTAL]).copy()
    df["hour"] = df[COL_TS].dt.hour
    df["weekday"] = df[COL_TS].dt.day_name()
    df["is_weekend"] = df[COL_TS].dt.dayofweek >= 5
    df["year_month"] = df[COL_TS].dt.to_period("M").astype(str)
    df["west_share"] = df[COL_WEST] / df[COL_TOTAL].replace(0, pd.NA)
    return df.sort_values(COL_TS).reset_index(drop=True)


def peak_hours(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """Average hourly crossings by clock hour (0–23), sorted descending."""
    out = (
        df.groupby("hour", as_index=False)[COL_TOTAL]
        .mean()
        .rename(columns={COL_TOTAL: "avg_crossings"})
        .sort_values("avg_crossings", ascending=False)
    )
    return out.head(top_n)


def weekday_weekend_compare(df: pd.DataFrame) -> pd.DataFrame:
    """Compare mean hourly volume on weekdays vs weekends."""
    out = (
        df.groupby("is_weekend")[COL_TOTAL]
        .agg(["mean", "median"])
        .reset_index()
        .rename(columns={"mean": "avg_crossings", "median": "median_crossings"})
    )
    out["day_type"] = out["is_weekend"].map({False: "weekday", True: "weekend"})
    return out


def direction_balance(df: pd.DataFrame) -> dict:
    """Summarize east vs west sidewalk share (directional demand proxy)."""
    valid = df.dropna(subset=["west_share"])
    return {
        "mean_west_share": float(valid["west_share"].mean()),
        "mean_east_share": float(1 - valid["west_share"].mean()),
        "hours_west_dominant_pct": float((valid["west_share"] > 0.5).mean() * 100),
    }


def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Monthly average hourly crossings — operational / seasonal view."""
    return (
        df.groupby("year_month", as_index=False)[COL_TOTAL]
        .mean()
        .rename(columns={COL_TOTAL: "avg_hourly_crossings"})
        .sort_values("year_month")
    )


def low_activity_windows(df: pd.DataFrame, percentile: float = 10) -> pd.DataFrame:
    """
    Hours where average crossings fall in the bottom percentile — proxy for
    'quiet' windows (rebalancing, maintenance, or access-friction study periods).
    """
    by_hour = df.groupby("hour", as_index=False)[COL_TOTAL].mean()
    threshold = by_hour[COL_TOTAL].quantile(percentile / 100)
    return by_hour[by_hour[COL_TOTAL] <= threshold].sort_values(COL_TOTAL)


def build_insight_report(df: pd.DataFrame) -> str:
    """Plain-language summary for researchers (not code commentary)."""
    peaks = peak_hours(df, top_n=3)
    ww = weekday_weekend_compare(df)
    direction = direction_balance(df)
    quiet = low_activity_windows(df)

    weekday_avg = ww.loc[ww["day_type"] == "weekday", "avg_crossings"].iloc[0]
    weekend_avg = ww.loc[ww["day_type"] == "weekend", "avg_crossings"].iloc[0]
    peak_list = ", ".join(f"{int(r.hour):02d}:00" for _, r in peaks.iterrows())

    lines = [
        "# Mobility Insight Report — Fremont Bridge corridor",
        "",
        f"**Records analyzed:** {len(df):,} hourly observations "
        f"({df[COL_TS].min().date()} → {df[COL_TS].max().date()}).",
        "",
        "## Peak demand",
        f"Typical **peak hours** (highest average crossings): **{peak_list}**. "
        "Service teams can align field research, intercept surveys, or ops staffing "
        "with these windows when live rider behavior is most visible on this corridor.",
        "",
        "## Weekday vs weekend",
        f"Weekday average hourly crossings: **{weekday_avg:.1f}**; "
        f"weekend: **{weekend_avg:.1f}**. "
        + (
            "Weekends run hotter — leisure/rec errand patterns may dominate."
            if weekend_avg > weekday_avg
            else "Weekdays run hotter — commute-linked micromobility use likely dominates."
        ),
        "",
        "## Directional balance",
        f"West sidewalk accounts for **{direction['mean_west_share']*100:.1f}%** of crossings on average; "
        f"west-dominant hours occur **{direction['hours_west_dominant_pct']:.1f}%** of the time. "
        "Asymmetric flow can inform placement of parking zones, charging hubs, or signage on one approach.",
        "",
        "## Quiet windows (bottom decile by hour-of-day average)",
        "Low-activity clock hours: "
        + ", ".join(f"{int(r.hour):02d}:00" for _, r in quiet.iterrows())
        + ". Useful for maintenance scheduling or studying barrier effects without peak-traffic noise.",
        "",
        "## Research note",
        "This feed is **hourly corridor counts** (bicycles + scooters combined), not trip-level MDS logs. "
        "Use it for **temporal demand and access-intensity** questions; pair with interviews for friction narratives.",
    ]
    return "\n".join(lines)
