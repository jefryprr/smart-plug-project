import type { AnalyticsResponse } from "@smartplug/api-contract";
import { formatIdr, formatKwh } from "@/lib/format";
import { EmptyState } from "./Feedback";

export function UsageAndCost({ analytics }: { analytics: AnalyticsResponse | null }) {
  if (!analytics) {
    return (
      <section className="panel">
        <h2>Pemakaian dan biaya</h2>
        <EmptyState title="Analitik belum tersedia">Data akan muncul setelah telemetry terkumpul.</EmptyState>
      </section>
    );
  }

  if (!analytics.data_available) {
    return (
      <section className="panel">
        <h2>Pemakaian dan biaya</h2>
        <EmptyState title="Tidak ada data pada rentang ini">
          Grafik tidak menampilkan nol karena tidak ada sampel, bukan karena konsumsi nol.
        </EmptyState>
      </section>
    );
  }

  return (
    <section className="panel" aria-labelledby="usage-title">
      <div className="panel-head">
        <div>
          <h2 id="usage-title">Pemakaian dan biaya</h2>
          <p className="muted">Estimasi energi, bukan tagihan resmi PLN.</p>
        </div>
      </div>
      <dl className="stat-row">
        <div>
          <dt>Energi periode</dt>
          <dd>{formatKwh(analytics.total_energy_kwh)}</dd>
        </div>
        <div>
          <dt>Estimasi biaya</dt>
          <dd>{formatIdr(analytics.total_cost_idr)}</dd>
        </div>
        <div>
          <dt>Zona waktu</dt>
          <dd>{analytics.time_zone}</dd>
        </div>
      </dl>
      {analytics.missing_tariff_buckets > 0 ? (
        <div className="inline-alert warn" role="status">
          {analytics.missing_tariff_buckets} periode tidak memiliki tarif efektif. Biaya yang ditampilkan parsial;
          periode tersebut tidak dianggap Rp0.
        </div>
      ) : null}
      <p className="muted small">
        Biaya dihitung dari delta energi tervalidasi × tarif efektif. Pajak, biaya administrasi, tarif blok, dan
        daya abonemen tidak termasuk kecuali dimodelkan eksplisit.
      </p>
    </section>
  );
}
