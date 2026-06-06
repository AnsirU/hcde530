export type Analytics = {
  meta: { records: number; start: string; end: string };
  summary: {
    weekday_avg: number;
    weekend_avg: number;
    west_share_pct: number;
    west_dominant_pct: number;
    peak_hours: string[];
    quiet_hours: string[];
  };
  hourly_avg: { hour: number; avg: number }[];
  heatmap: Record<string, number[]>;
  monthly: { month: string; avg: number }[];
  direction_monthly: { month: string; west: number; east: number }[];
};
