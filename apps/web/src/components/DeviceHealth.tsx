import type { DiagnosticsResponse } from "@smartplug/api-contract";
import { ageLabel, formatDateTime, formatNumber } from "@/lib/format";
import { EmptyState } from "./Feedback";
import { StatusBadge, type StatusTone } from "./StatusBadge";

function healthTone(value: string): StatusTone {
  if (value === "OK" || value === "CONNECTED" || value === "NOT_INSTALLED") return value === "NOT_INSTALLED" ? "info" : "ok";
  if (value === "STALE" || value === "MISMATCH" || value === "PROVISIONING") return "warn";
  if (value === "INVALID" || value === "DISCONNECTED") return "danger";
  return "neutral";
}

export function DeviceHealth({ diagnostics }: { diagnostics: DiagnosticsResponse | null }) {
  if (!diagnostics) {
    return (
      <section className="panel">
        <h2>Kesehatan perangkat</h2>
        <EmptyState title="Diagnostik belum tersedia">
          Perangkat belum mengirim data diagnostik. Nilai tidak diisi dengan asumsi.
        </EmptyState>
      </section>
    );
  }

  return (
    <section className="panel" aria-labelledby="health-title">
      <div className="panel-head">
        <div>
          <h2 id="health-title">Kesehatan perangkat</h2>
          <p className="muted">Diperiksa {formatDateTime(diagnostics.checked_at)}</p>
        </div>
      </div>
      <dl className="stat-row">
        <div>
          <dt>Firmware</dt>
          <dd>{diagnostics.firmware_version ?? "Tidak diketahui"}</dd>
        </div>
        <div>
          <dt>Build SHA</dt>
          <dd className="mono">{diagnostics.build_sha ?? "—"}</dd>
        </div>
        <div>
          <dt>Uptime</dt>
          <dd>{diagnostics.uptime_seconds === null ? "—" : `${formatNumber(diagnostics.uptime_seconds, 0)} detik`}</dd>
        </div>
        <div>
          <dt>RSSI</dt>
          <dd>{diagnostics.rssi_dbm === null ? "—" : `${diagnostics.rssi_dbm} dBm`}</dd>
        </div>
        <div>
          <dt>Heap bebas</dt>
          <dd>{diagnostics.heap_free_bytes === null ? "—" : `${formatNumber(diagnostics.heap_free_bytes, 0)} B`}</dd>
        </div>
        <div>
          <dt>Terakhir diperiksa</dt>
          <dd>{ageLabel(diagnostics.checked_at)}</dd>
        </div>
      </dl>
      <div className="health-grid">
        <div>
          <span className="label">Metering</span>
          <StatusBadge label={diagnostics.sensor_health.meter} tone={healthTone(diagnostics.sensor_health.meter)} />
        </div>
        <div>
          <span className="label">Suhu</span>
          <StatusBadge
            label={diagnostics.sensor_health.temperature}
            tone={healthTone(diagnostics.sensor_health.temperature)}
          />
        </div>
        <div>
          <span className="label">Feedback relay</span>
          <StatusBadge
            label={diagnostics.sensor_health.relay_feedback}
            tone={healthTone(diagnostics.sensor_health.relay_feedback)}
          />
        </div>
        <div>
          <span className="label">Wi-Fi</span>
          <StatusBadge label={diagnostics.wifi_state} tone={healthTone(diagnostics.wifi_state)} />
        </div>
      </div>
      <dl className="stat-row">
        <div>
          <dt>Command diterima</dt>
          <dd>{diagnostics.command_counts.accepted}</dd>
        </div>
        <div>
          <dt>Command ditolak</dt>
          <dd>{diagnostics.command_counts.rejected}</dd>
        </div>
        <div>
          <dt>Command kedaluwarsa</dt>
          <dd>{diagnostics.command_counts.expired}</dd>
        </div>
      </dl>
      {diagnostics.last_error ? (
        <div className="inline-alert warn" role="status">
          <strong>Error terakhir:</strong> {diagnostics.last_error}
        </div>
      ) : (
        <p className="muted small">Tidak ada error terakhir yang dilaporkan.</p>
      )}
    </section>
  );
}
