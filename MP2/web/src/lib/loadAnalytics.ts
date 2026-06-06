import type { Analytics } from "../types";

const LIVE_TIMEOUT_MS = 25_000;

async function fetchWithTimeout(url: string, ms: number): Promise<Response> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), ms);
  try {
    return await fetch(url, { cache: "no-store", signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}

async function loadStatic(): Promise<Analytics> {
  const staticRes = await fetch("/data/analytics.json");
  if (!staticRes.ok) {
    throw new Error("Failed to load bundled analytics snapshot");
  }
  return staticRes.json() as Promise<Analytics>;
}

export async function loadAnalytics(): Promise<{
  data: Analytics;
  source: "live" | "static";
}> {
  try {
    const liveRes = await fetchWithTimeout("/api/analytics", LIVE_TIMEOUT_MS);
    if (liveRes.ok) {
      const data = (await liveRes.json()) as Analytics;
      return { data, source: "live" };
    }
  } catch {
    // timeout, cold start, or offline — use bundled JSON
  }

  const data = await loadStatic();
  return { data, source: "static" };
}
