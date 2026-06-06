import type { Analytics } from "../types";

export async function loadAnalytics(): Promise<{
  data: Analytics;
  source: "live" | "static";
}> {
  try {
    const liveRes = await fetch("/api/analytics", { cache: "no-store" });
    if (liveRes.ok) {
      const data = (await liveRes.json()) as Analytics;
      return { data, source: "live" };
    }
  } catch {
    // Vite dev or API cold start — fall back to bundled snapshot
  }

  const staticRes = await fetch("/data/analytics.json");
  if (!staticRes.ok) {
    throw new Error("Failed to load analytics (live API and static fallback)");
  }
  const data = (await staticRes.json()) as Analytics;
  return { data, source: "static" };
}
