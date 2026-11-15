"use client";

import Link from "next/link";
import { useDevices } from "@/lib/hooks";
import { ErrorPanel, Loading } from "@/components/Feedback";

export default function TariffsSettingsPage() {
  const { data, loading, error, reload } = useDevices();

  if (loading) return <Loading />;
  if (error) return <ErrorPanel message={error} onRetry={() => void reload()} />;

  return (
    <div className="stack">
      <header className="page-head">
        <div>
          <p className="eyebrow">Pengaturan</p>
          <h1>Tarif listrik</h1>
          <p className="muted">
            Tarif disimpan per perangkat dengan histori efektif. Perubahan tarif tidak mengubah biaya historis tanpa
            perhitungan ulang eksplisit.
          </p>
        </div>
      </header>
      <section className="panel">
        <h2>Pilih perangkat</h2>
        {(data ?? []).length === 0 ? (
          <p className="muted">Belum ada perangkat.</p>
        ) : (
          <ul className="compact-list">
            {(data ?? []).map((device) => (
              <li key={device.device_id}>
                <div>
                  <strong>{device.name}</strong>
                  <div className="muted small">{device.room ?? "Tanpa ruangan"}</div>
                </div>
                <Link href={`/devices/${device.device_id}/settings`} className="button button-small button-secondary">
                  Atur tarif
                </Link>
              </li>
            ))}
          </ul>
        )}
      </section>
      <div className="info-strip">
        <strong>Bukan tagihan resmi.</strong> Estimasi memakai tarif efektif per interval dan hanya energi tervalidasi.
        Pajak, biaya administrasi, tarif blok, dan daya abonemen tidak termasuk.
      </div>
    </div>
  );
}
