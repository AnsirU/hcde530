import { motion } from "framer-motion";
import { useEffect, useMemo, useState } from "react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useCountUp } from "./hooks/useCountUp";
import { loadAnalytics } from "./lib/loadAnalytics";
import type { Analytics } from "./types";
import "./App.css";

const fade = {
  hidden: { opacity: 0, y: 16 },
  show: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.08, duration: 0.45, ease: [0.23, 1, 0.32, 1] },
  }),
};

function StatCard({
  label,
  value,
  suffix = "",
  detail,
  index,
  animKey,
}: {
  label: string;
  value: number;
  suffix?: string;
  detail?: string;
  index: number;
  animKey: number;
}) {
  const animated = useCountUp(value, 1000, true);
  void animKey;
  const display =
    suffix === "%"
      ? animated.toFixed(1)
      : suffix === "k"
        ? (animated / 1000).toFixed(1)
        : Math.round(animated).toString();

  return (
    <motion.article
      className="stat-card"
      variants={fade}
      custom={index}
      initial="hidden"
      animate="show"
    >
      <p className="stat-label">{label}</p>
      <p className="stat-value">
        {display}
        {suffix && <span className="stat-suffix">{suffix}</span>}
      </p>
      {detail && <p className="stat-detail">{detail}</p>}
    </motion.article>
  );
}

export default function App() {
  const [data, setData] = useState<Analytics | null>(null);
  const [heatDay, setHeatDay] = useState("Monday");
  const [error, setError] = useState("");
  const [source, setSource] = useState<"live" | "static" | null>(null);
  const [refreshing, setRefreshing] = useState(false);
  const [animKey, setAnimKey] = useState(0);

  const refresh = async () => {
    setRefreshing(true);
    setError("");
    try {
      const result = await loadAnalytics();
      setData(result.data);
      setSource(result.source);
      setAnimKey((k) => k + 1);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Refresh failed");
    } finally {
      setRefreshing(false);
    }
  };

  useEffect(() => {
    void refresh();
  }, []);

  const heatSeries = useMemo(() => {
    if (!data) return [];
    return (data.heatmap[heatDay] ?? []).map((avg, hour) => ({
      hour: `${hour.toString().padStart(2, "0")}:00`,
      avg,
    }));
  }, [data, heatDay]);

  if (error) {
    return (
      <main className="shell">
        <p className="error">Could not load data: {error}</p>
      </main>
    );
  }

  if (!data && refreshing) {
    return (
      <main className="shell loading">
        <motion.div
          className="loader"
          animate={{ opacity: [0.4, 1, 0.4] }}
          transition={{ duration: 1.2, repeat: Infinity, ease: "easeInOut" }}
        >
          {refreshing ? "Syncing from Seattle Open Data…" : "Loading corridor data…"}
        </motion.div>
      </main>
    );
  }

  const { summary, meta } = data;

  const chartLime = "#00DD00";
  const chartBlack = "#111111";
  const chartCoral = "#FF5A3C";

  return (
    <div className="page">
      <div className="lime-bar">
        <div className="lime-logo">
          <span className="lime-dot" aria-hidden />
          Mobility Insight Kit
        </div>
        <span className="lime-bar-tag">Seattle micromobility research</span>
      </div>
      <header className="hero">
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
          <p className="eyebrow">HCDE 530 · Mini Project 2</p>
          <h1>Mobility Insight Kit</h1>
          <p className="lede">
            Demand-pattern dashboard for UX researchers and service designers studying shared
            micromobility on Seattle&apos;s Fremont Bridge corridor.
          </p>
          <p className="meta-line">
            {meta.records.toLocaleString()} hourly records · {meta.start} → {meta.end}
          </p>
          <div className="hero-actions">
            <span className={`live-badge ${source === "live" ? "on" : ""}`}>
              {source === "live" ? "Live from Seattle API" : "Offline snapshot"}
            </span>
            <button
              type="button"
              className="refresh-btn"
              onClick={() => void refresh()}
              disabled={refreshing}
            >
              {refreshing ? "Refreshing…" : "Refresh data"}
            </button>
          </div>
          {meta.portalLastModified && (
            <p className="sync-line">
              Portal last updated: {new Date(meta.portalLastModified).toLocaleString()}
              {meta.fetchedAt && (
                <> · Fetched: {new Date(meta.fetchedAt).toLocaleString()}</>
              )}
            </p>
          )}
          {meta.note && <p className="sync-note">{meta.note}</p>}
        </motion.div>
      </header>

      <section className="stats-grid">
        <StatCard
          key={`wd-${animKey}`}
          label="Weekday avg crossings / hour"
          value={summary.weekday_avg}
          detail="Commute-heavy pattern"
          index={0}
          animKey={animKey}
        />
        <StatCard
          key={`we-${animKey}`}
          label="Weekend avg crossings / hour"
          value={summary.weekend_avg}
          detail="Lower leisure baseline"
          index={1}
          animKey={animKey}
        />
        <StatCard
          key={`ws-${animKey}`}
          label="West sidewalk share"
          value={summary.west_share_pct}
          suffix="%"
          detail={`West-dominant ${summary.west_dominant_pct}% of hours`}
          index={2}
          animKey={animKey}
        />
        <StatCard
          key={`rc-${animKey}`}
          label="Records analyzed"
          value={meta.records}
          suffix="k"
          detail={`Peaks: ${summary.peak_hours.join(", ")}`}
          index={3}
          animKey={animKey}
        />
      </section>

      <section className="panel">
        <div className="panel-head">
          <h2>Peak hours profile</h2>
          <p>When to schedule intercept studies or field observation.</p>
        </div>
        <div className="chart-wrap">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={data.hourly_avg} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(26,31,46,0.06)" />
              <XAxis dataKey="hour" tickFormatter={(h) => `${h}h`} tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} width={36} />
              <Tooltip
                formatter={(v: number) => [`${v.toFixed(1)} crossings`, "Avg / hour"]}
                labelFormatter={(h) => `Hour ${h}:00`}
              />
              <Bar
                dataKey="avg"
                fill={chartLime}
                stroke={chartBlack}
                strokeWidth={0}
                radius={[4, 4, 0, 0]}
                animationDuration={900}
                animationEasing="ease-out"
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section className="panel">
        <div className="panel-head">
          <h2>Day-of-week intensity</h2>
          <p>Select a weekday to animate hourly demand for that day.</p>
        </div>
        <div className="day-tabs" role="tablist">
          {Object.keys(data.heatmap).map((day) => (
            <button
              key={day}
              type="button"
              role="tab"
              aria-selected={heatDay === day}
              className={heatDay === day ? "day-tab active" : "day-tab"}
              onClick={() => setHeatDay(day)}
            >
              {day.slice(0, 3)}
            </button>
          ))}
        </div>
        <div className="chart-wrap">
          <ResponsiveContainer width="100%" height={260}>
            <AreaChart data={heatSeries} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="heatFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor={chartLime} stopOpacity={0.45} />
                  <stop offset="100%" stopColor={chartLime} stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(26,31,46,0.06)" />
              <XAxis dataKey="hour" tick={{ fontSize: 10 }} interval={2} />
              <YAxis tick={{ fontSize: 11 }} width={36} />
              <Tooltip formatter={(v: number) => [`${v.toFixed(1)}`, "Avg crossings"]} />
              <Area
                type="monotone"
                dataKey="avg"
                stroke={chartBlack}
                fill="url(#heatFill)"
                strokeWidth={2}
                animationDuration={700}
                animationEasing="ease-out"
                isAnimationActive
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section className="panel two-col">
        <div>
          <div className="panel-head">
            <h2>Monthly trend</h2>
            <p>Recent seasonal baseline (36 months).</p>
          </div>
          <div className="chart-wrap short">
            <ResponsiveContainer width="100%" height={220}>
              <AreaChart data={data.monthly}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(26,31,46,0.06)" />
                <XAxis dataKey="month" tick={{ fontSize: 9 }} interval={5} angle={-35} textAnchor="end" height={50} />
                <YAxis tick={{ fontSize: 10 }} width={32} />
                <Tooltip />
                <Area
                  type="monotone"
                  dataKey="avg"
                  stroke={chartBlack}
                  fill={chartLime}
                  fillOpacity={0.25}
                  animationDuration={800}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div>
          <div className="panel-head">
            <h2>Directional flow</h2>
            <p>West vs east sidewalk averages.</p>
          </div>
          <div className="chart-wrap short">
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={data.direction_monthly.slice(-12)}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(26,31,46,0.06)" />
                <XAxis dataKey="month" tick={{ fontSize: 9 }} interval={2} angle={-25} textAnchor="end" height={44} />
                <YAxis tick={{ fontSize: 10 }} width={32} />
                <Tooltip />
                <Legend />
                <Bar dataKey="west" stackId="a" fill={chartLime} animationDuration={700} />
                <Bar dataKey="east" stackId="a" fill={chartBlack} animationDuration={700} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>

      <section className="insight panel">
        <h2>Research readout</h2>
        <ul>
          <li>
            <strong>Peak windows:</strong> {summary.peak_hours.join(", ")} — align intercepts when
            corridor activity is highest.
          </li>
          <li>
            <strong>Quiet hours:</strong> {summary.quiet_hours.join(", ")} — useful for maintenance
            scheduling or low-noise observation.
          </li>
          <li>
            <strong>Data note:</strong> Hourly bridge counts (bikes + scooters), not trip-level vendor
            logs. Pair with qualitative work for friction narratives.
          </li>
        </ul>
        <p className="footer-links">
          <a href="https://github.com/AnsirU/hcde530/tree/main/MP2">Source on GitHub</a>
          {" · "}
          <a href="https://data.seattle.gov/Transportation/Shared-Mobility-Program-Data/65db-xm6k">
            Seattle Open Data
          </a>
        </p>
      </section>
    </div>
  );
}
