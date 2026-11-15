import type { DataSource } from "@smartplug/api-contract";

export function DemoBanner({ dataSource }: { dataSource: DataSource }) {
  if (dataSource !== "SYNTHETIC_DEMO") return null;
  return (
    <div className="demo-banner" role="status">
      <strong>Mode demo.</strong> Telemetry di bawah adalah data sintetik yang dihasilkan seed,
      bukan pengukuran perangkat nyata. Jangan gunakan untuk klaim akurasi atau keselamatan.
    </div>
  );
}
