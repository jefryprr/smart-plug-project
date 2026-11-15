export type StatusTone = "ok" | "warn" | "danger" | "neutral" | "info";

export function StatusBadge({ label, tone = "neutral" }: { label: string; tone?: StatusTone }) {
  return (
    <span className={`status-badge status-${tone}`}>
      <span className="status-dot" aria-hidden="true" />
      {label}
    </span>
  );
}

export function availabilityBadge(status: string): { label: string; tone: StatusTone } {
  switch (status) {
    case "ONLINE":
      return { label: "Online", tone: "ok" };
    case "STALE":
      return { label: "Data basi", tone: "warn" };
    case "OFFLINE":
      return { label: "Offline", tone: "danger" };
    case "NEVER_SEEN":
      return { label: "Belum terhubung", tone: "neutral" };
    default:
      return { label: status, tone: "neutral" };
  }
}

export function outputBadge(output: "ON" | "OFF", commanded = true): { label: string; tone: StatusTone } {
  if (output === "ON") {
    return { label: commanded ? "ON (commanded)" : "ON (teramati)", tone: "ok" };
  }
  return { label: commanded ? "OFF (commanded)" : "OFF (teramati)", tone: "neutral" };
}
