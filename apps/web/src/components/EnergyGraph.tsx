import type { AnalyticsBucket } from "@smartplug/api-contract";
import { formatKwh } from "@/lib/format";
import { EmptyState } from "./Feedback";

export function EnergyGraph({
  buckets,
  title = "Energi per periode"
}: {
  buckets: AnalyticsBucket[];
  title?: string;
}) {
  const available = buckets.filter((bucket) => bucket.data_available);
  if (available.length === 0) {
    return (
      <section className="panel" aria-labelledby="graph-title">
        <h2 id="graph-title">{title}</h2>
        <EmptyState title="Belum ada data energi">
          Bucket kosong ditampilkan sebagai “tidak ada data”, bukan konsumsi nol.
        </EmptyState>
      </section>
    );
  }

  const max = Math.max(...available.map((bucket) => bucket.energy_kwh ?? 0), 0.001);
  const width = 760;
  const height = 280;
  const paddingLeft = 52;
  const paddingRight = 16;
  const paddingTop = 24;
  const paddingBottom = 64;
  const chartWidth = width - paddingLeft - paddingRight;
  const chartHeight = height - paddingTop - paddingBottom;
  const slot = chartWidth / Math.max(buckets.length, 1);
  const barWidth = Math.max(6, Math.min(34, slot * 0.62));

  return (
    <section className="panel" aria-labelledby="graph-title">
      <div className="panel-head">
        <div>
          <h2 id="graph-title">{title}</h2>
          <p className="muted">Satuan: kWh. Klik/tahan batang untuk melihat tooltip browser.</p>
        </div>
        <div className="legend">
          <span><span className="legend-swatch energy" /> Ada data</span>
          <span><span className="legend-swatch missing" /> Tidak ada data</span>
        </div>
      </div>
      <div className="chart-wrap">
        <svg viewBox={`0 0 ${width} ${height}`} role="img" aria-label={`Grafik ${title}`}>
          <line
            x1={paddingLeft}
            y1={paddingTop + chartHeight}
            x2={width - paddingRight}
            y2={paddingTop + chartHeight}
            className="chart-axis"
          />
          {[0, 0.5, 1].map((fraction) => {
            const y = paddingTop + chartHeight - chartHeight * fraction;
            return (
              <g key={fraction}>
                <line x1={paddingLeft} y1={y} x2={width - paddingRight} y2={y} className="chart-grid" />
                <text x={paddingLeft - 8} y={y + 4} textAnchor="end" className="chart-label">
                  {(max * fraction).toFixed(2)}
                </text>
              </g>
            );
          })}
          {buckets.map((bucket, index) => {
            const x = paddingLeft + index * slot + (slot - barWidth) / 2;
            const value = bucket.energy_kwh ?? 0;
            const barHeight = bucket.data_available ? Math.max(2, (value / max) * chartHeight) : 6;
            const y = paddingTop + chartHeight - barHeight;
            const label = bucket.label.length > 10 ? bucket.label.slice(5) : bucket.label;
            return (
              <g key={`${bucket.period_start}-${index}`}>
                <rect
                  x={x}
                  y={y}
                  width={barWidth}
                  height={barHeight}
                  className={bucket.data_available ? "chart-bar" : "chart-bar-missing"}
                >
                  <title>
                    {bucket.label}: {bucket.data_available ? formatKwh(bucket.energy_kwh) : "tidak ada data"}
                  </title>
                </rect>
                {index % Math.ceil(buckets.length / 8) === 0 ? (
                  <text
                    x={x + barWidth / 2}
                    y={paddingTop + chartHeight + 18}
                    textAnchor="end"
                    transform={`rotate(-35 ${x + barWidth / 2} ${paddingTop + chartHeight + 18})`}
                    className="chart-label"
                  >
                    {label}
                  </text>
                ) : null}
              </g>
            );
          })}
          <text x={paddingLeft} y={16} className="chart-label">
            kWh
          </text>
        </svg>
      </div>
    </section>
  );
}
