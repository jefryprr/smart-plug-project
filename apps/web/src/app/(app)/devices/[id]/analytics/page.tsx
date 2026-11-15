"use client";

import { useMemo, useState } from "react";
import { useParams } from "next/navigation";
import { useAnalytics } from "@/lib/hooks";
import { UsageAndCost } from "@/components/UsageAndCost";
import { EnergyGraph } from "@/components/EnergyGraph";
import { ErrorPanel, Loading } from "@/components/Feedback";
import { formatDateTime, formatIdr, formatKwh } from "@/lib/format";

type RangeKey = "24h" | "7d" | "30d";

const RANGE_LABELS: Record<RangeKey, string> = {
  "24h": "24 jam",
  "7d": "7 hari",
  "30d": "30 hari"
};

export default function AnalyticsPage() {
  const params = useParams();
  const deviceId = typeof params.id === "string" ? params.id : "";
  const [rangeKey, setRangeKey] = useState<RangeKey>("7d");
  const range = useMemo(() => {
    const to = new Date();
    const hours = rangeKey === "24h" ? 24 : rangeKey === "7d" ? 24 * 7 : 24 * 30;
    const from = new Date(to.getTime() - hours * 60 * 60 * 1000);
    return { from: from.toISOString(), to: to.toISOString() };
  }, [deviceId, rangeKey]);
  const granularity = rangeKey === "24h" ? "hour" : "day";
  const analytics = useAnalytics(deviceId, range.from, range.to, granularity);

  if (analytics.loading && !analytics.data) return <Loading />;
  if (analytics.error && !analytics.data) return <ErrorPanel message={analytics.error} onRetry={() => void analytics.reload()} />;

  return (
    <div className="stack">
      <div className="range-picker" role="group" aria-label="Rentang analitik">
        {(Object.keys(RANGE_LABELS) as RangeKey[]).map((key) => (
          <button
            key={key}
            type="button"
            className={rangeKey === key ? "range-button active" : "range-button"}
            aria-pressed={rangeKey === key}
            onClick={() => setRangeKey(key)}
          >
            {RANGE_LABELS[key]}
          </button>
        ))}
      </div>
      <UsageAndCost analytics={analytics.data} />
      <EnergyGraph
        buckets={analytics.data?.buckets ?? []}
        title={`Energi ${RANGE_LABELS[rangeKey]} — bucket ${granularity}`}
      />
      <section className="panel">
        <h2>Rincian bucket</h2>
        <p className="muted">
          Bucket kosong diberi status “tidak ada data” dan nilai kosong, bukan nol. Zona waktu:{" "}
          {analytics.data?.time_zone ?? "Asia/Jakarta"}.
        </p>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th scope="col">Periode</th>
                <th scope="col">Energi</th>
                <th scope="col">Estimasi biaya</th>
                <th scope="col">Sampel</th>
                <th scope="col">Gap</th>
                <th scope="col">Status</th>
              </tr>
            </thead>
            <tbody>
              {(analytics.data?.buckets ?? []).map((bucket) => (
                <tr key={bucket.period_start}>
                  <td>{bucket.label}</td>
                  <td>{bucket.data_available ? formatKwh(bucket.energy_kwh) : "Tidak ada data"}</td>
                  <td>{bucket.cost_idr === null ? "—" : formatIdr(bucket.cost_idr)}</td>
                  <td>{bucket.sample_count}</td>
                  <td>{bucket.gap_count}</td>
                  <td>{bucket.data_available ? "Ada data" : "Kosong"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="muted small">
          Rentang query: {formatDateTime(range.from)} → {formatDateTime(range.to)}.
        </p>
      </section>
    </div>
  );
}
