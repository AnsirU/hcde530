/**
 * Vercel serverless: fetch latest Fremont Bridge counter rows from Seattle Open Data,
 * aggregate in-memory, return dashboard JSON. CORS-enabled for the static app.
 */

const SOCRATA = "https://data.seattle.gov/resource/65db-xm6k.json";
const PAGE = 50000;
const DAY_ORDER = [
  "Sunday",
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
];

function parseRow(row) {
  const ts = new Date(row.date);
  if (Number.isNaN(ts.getTime())) return null;
  const total = Number(row.fremont_bridge);
  const west = Number(row.fremont_bridge_nb);
  const east = Number(row.fremont_bridge_sb);
  if (Number.isNaN(total)) return null;
  return {
    ts,
    total,
    west: Number.isNaN(west) ? null : west,
    east: Number.isNaN(east) ? null : east,
    hour: ts.getHours(),
    weekday: DAY_ORDER[ts.getDay()],
    isWeekend: ts.getDay() === 0 || ts.getDay() === 6,
    yearMonth: `${ts.getFullYear()}-${String(ts.getMonth() + 1).padStart(2, "0")}`,
  };
}

async function fetchAllRows() {
  const rows = [];
  let offset = 0;
  let lastModified = null;

  while (true) {
    const url = `${SOCRATA}?$limit=${PAGE}&$offset=${offset}&$order=date`;
    const res = await fetch(url, {
      headers: { Accept: "application/json" },
    });
    if (!res.ok) {
      throw new Error(`Seattle API ${res.status}: ${await res.text()}`);
    }
    lastModified = res.headers.get("last-modified") || lastModified;
    const batch = await res.json();
    if (!Array.isArray(batch) || batch.length === 0) break;
    rows.push(...batch);
    if (batch.length < PAGE) break;
    offset += PAGE;
  }

  return { rows, lastModified };
}

function aggregate(parsed) {
  const valid = parsed.filter(Boolean);
  const n = valid.length;
  if (n === 0) throw new Error("No valid rows after parsing");

  const heatmap = Object.fromEntries(
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].map(
      (d) => [d, Array(24).fill(0)],
    ),
  );
  const heatCounts = Object.fromEntries(
    Object.keys(heatmap).map((d) => [d, Array(24).fill(0)]),
  );

  const hourlySum = Array(24).fill(0);
  const hourlyCount = Array(24).fill(0);
  let weekdaySum = 0;
  let weekdayN = 0;
  let weekendSum = 0;
  let weekendN = 0;
  let westShareSum = 0;
  let westShareN = 0;
  let westDominant = 0;

  const monthlyMap = new Map();

  let minTs = valid[0].ts;
  let maxTs = valid[0].ts;

  for (const r of valid) {
    if (r.ts < minTs) minTs = r.ts;
    if (r.ts > maxTs) maxTs = r.ts;

    hourlySum[r.hour] += r.total;
    hourlyCount[r.hour] += 1;

    heatmap[r.weekday][r.hour] += r.total;
    heatCounts[r.weekday][r.hour] += 1;

    if (r.isWeekend) {
      weekendSum += r.total;
      weekendN += 1;
    } else {
      weekdaySum += r.total;
      weekdayN += 1;
    }

    if (r.total > 0 && r.west != null) {
      const share = r.west / r.total;
      westShareSum += share;
      westShareN += 1;
      if (share > 0.5) westDominant += 1;
    }

    const m = monthlyMap.get(r.yearMonth) || {
      total: 0,
      n: 0,
      west: 0,
      east: 0,
      westN: 0,
      eastN: 0,
    };
    m.total += r.total;
    m.n += 1;
    if (r.west != null) {
      m.west += r.west;
      m.westN += 1;
    }
    if (r.east != null) {
      m.east += r.east;
      m.eastN += 1;
    }
    monthlyMap.set(r.yearMonth, m);
  }

  const hourly_avg = hourlySum.map((s, hour) => ({
    hour,
    avg: hourlyCount[hour] ? Math.round((s / hourlyCount[hour]) * 100) / 100 : 0,
  }));

  for (const day of Object.keys(heatmap)) {
    for (let h = 0; h < 24; h++) {
      if (heatCounts[day][h]) {
        heatmap[day][h] = Math.round((heatmap[day][h] / heatCounts[day][h]) * 100) / 100;
      }
    }
  }

  const sortedHourly = [...hourly_avg].sort((a, b) => b.avg - a.avg);
  const peak_hours = sortedHourly.slice(0, 3).map((r) => `${String(r.hour).padStart(2, "0")}:00`);
  const quiet_hours = sortedHourly
    .slice(-3)
    .sort((a, b) => a.hour - b.hour)
    .map((r) => `${String(r.hour).padStart(2, "0")}:00`);

  const monthlyKeys = [...monthlyMap.keys()].sort();
  const monthlyRecent = monthlyKeys.slice(-36);
  const monthly = monthlyRecent.map((month) => {
    const m = monthlyMap.get(month);
    return { month, avg: Math.round((m.total / m.n) * 100) / 100 };
  });
  const direction_monthly = monthlyRecent.map((month) => {
    const m = monthlyMap.get(month);
    return {
      month,
      west: m.westN ? Math.round((m.west / m.westN) * 100) / 100 : 0,
      east: m.eastN ? Math.round((m.east / m.eastN) * 100) / 100 : 0,
    };
  });

  return {
    meta: {
      records: n,
      start: minTs.toISOString().slice(0, 10),
      end: maxTs.toISOString().slice(0, 10),
      live: true,
      source: "Seattle Open Data API (65db-xm6k)",
    },
    summary: {
      weekday_avg: weekdayN ? Math.round((weekdaySum / weekdayN) * 10) / 10 : 0,
      weekend_avg: weekendN ? Math.round((weekendSum / weekendN) * 10) / 10 : 0,
      west_share_pct: westShareN
        ? Math.round((westShareSum / westShareN) * 1000) / 10
        : 0,
      west_dominant_pct: westShareN
        ? Math.round((westDominant / westShareN) * 1000) / 10
        : 0,
      peak_hours,
      quiet_hours,
    },
    hourly_avg,
    heatmap,
    monthly,
    direction_monthly,
  };
}

module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") {
    return res.status(204).end();
  }

  if (req.method !== "GET") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const { rows, lastModified } = await fetchAllRows();
    const parsed = rows.map(parseRow);
    const payload = aggregate(parsed);
    payload.meta.portalLastModified = lastModified;
    payload.meta.fetchedAt = new Date().toISOString();
    payload.meta.note =
      "Counts refresh when you load this page. Seattle publishes updates periodically (not live per-second sensor data).";

    res.setHeader(
      "Cache-Control",
      "public, s-maxage=900, stale-while-revalidate=3600",
    );
    return res.status(200).json(payload);
  } catch (err) {
    console.error(err);
    return res.status(502).json({
      error: "Failed to load live Seattle data",
      detail: String(err.message || err),
    });
  }
}
