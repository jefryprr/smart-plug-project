import type { TelemetryListResponse } from "@smartplug/api-contract";
import { ageLabel, formatDateTime, formatNumber } from "@/lib/format";
import { EmptyState } from "./Feedback";
import { StatusBadge } from "./StatusBadge";

export function ElectricalReadings({ telemetry }: { telemetry: TelemetryListResponse | null }) {
  const sample = telemetry?.samples[0] ?? null;
  if (!sample) {
    return (
      <section className="panel" aria-labelledby="readings-title">
        <h2 id="readings-title">Pembacaan listrik</h2>
        <EmptyState title="Belum ada telemetry">
          Perangkat belum mengirim sampel. Nilai tidak ditampilkan sebagai nol karena data tidak tersedia.
        </EmptyState>
      </section>
    );
  }

  const invalid = sample.quality === "INVALID";
  const value = (input: number | null, digits: number, unit: string): string =>
    invalid || input === null ? "—" : `${formatNumber(input, digits)} ${unit}`;

  return (
    <section className="panel" aria-labelledby="readings-title">
      <div className="panel-head">
        <div>
          <h2 id="readings-title">Pembacaan listrik</h2>
          <p className="muted">
            Sampel {formatDateTime(sample.sampled_at)} · {ageLabel(sample.sampled_at)}
          </p>
        </div>
        <StatusBadge
          label={invalid ? "Data tidak valid" : sample.quality === "STALE" ? "Data basi" : "Valid"}
          tone={invalid ? "danger" : sample.quality === "STALE" ? "warn" : "ok"}
        />
      </div>
      {invalid ? (
        <div className="inline-alert danger" role="alert">
          Meter melaporkan data tidak valid. Angka tidak ditampilkan sebagai pembacaan live dan tidak dipakai untuk
          perhitungan biaya.
        </div>
      ) : null}
      <dl className="reading-grid">
        <div>
          <dt>Tegangan</dt>
          <dd>{value(sample.voltage_v, 1, "V")}</dd>
          <span className="muted small">RMS, sesuai register meter</span>
        </div>
        <div>
          <dt>Arus</dt>
          <dd>{value(sample.current_a, 3, "A")}</dd>
          <span className="muted small">Bukan rating izin arus</span>
        </div>
        <div>
          <dt>Daya aktif</dt>
          <dd>{value(sample.active_power_w, 1, "W")}</dd>
          <span className="muted small">Bukan apparent power</span>
        </div>
        <div>
          <dt>Faktor daya</dt>
          <dd>{sample.power_factor === null ? "—" : formatNumber(sample.power_factor, 2)}</dd>
          <span className="muted small">0–1 bila tersedia</span>
        </div>
        <div>
          <dt>Frekuensi</dt>
          <dd>{sample.frequency_hz === null ? "—" : formatNumber(sample.frequency_hz, 1) + " Hz"}</dd>
          <span className="muted small">Bila didukung meter</span>
        </div>
        <div>
          <dt>Energi kumulatif</dt>
          <dd>{sample.energy_kwh_total === null ? "—" : `${formatNumber(sample.energy_kwh_total, 3)} kWh`}</dd>
          <span className="muted small">Counter meter, bukan delta harian</span>
        </div>
      </dl>
    </section>
  );
}
