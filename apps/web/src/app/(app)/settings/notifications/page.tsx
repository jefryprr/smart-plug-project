"use client";

import { useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { errorMessage, useDevices } from "@/lib/hooks";
import { ErrorPanel, Loading } from "@/components/Feedback";

export default function NotificationsSettingsPage() {
  const { data, loading, error, reload } = useDevices();
  const [status, setStatus] = useState<string | null>(null);
  const [failure, setFailure] = useState<string | null>(null);
  const [busyId, setBusyId] = useState<string | null>(null);

  if (loading) return <Loading />;
  if (error) return <ErrorPanel message={error} onRetry={() => void reload()} />;

  return (
    <div className="stack">
      <header className="page-head">
        <div>
          <p className="eyebrow">Pengaturan</p>
          <h1>Notifikasi</h1>
          <p className="muted">
            Notifikasi test memakai provider yang dikonfigurasi. Tanpa token Telegram, backend memakai mock dan tidak
            mengklaim pengiriman eksternal.
          </p>
        </div>
      </header>
      <section className="panel">
        <h2>Test per perangkat</h2>
        {(data ?? []).length === 0 ? (
          <p className="muted">Belum ada perangkat.</p>
        ) : (
          <ul className="compact-list">
            {(data ?? []).map((device) => (
              <li key={device.device_id}>
                <div>
                  <strong>{device.name}</strong>
                  <div className="muted small">{device.device_id}</div>
                </div>
                <button
                  type="button"
                  className="button button-small button-secondary"
                  disabled={busyId !== null}
                  onClick={() => {
                    setBusyId(device.device_id);
                    setStatus(null);
                    setFailure(null);
                    void api
                      .testNotification(device.device_id)
                      .then((result) => setStatus(`${result.status} via ${result.provider}`))
                      .catch((caught) => setFailure(errorMessage(caught)))
                      .finally(() => setBusyId(null));
                  }}
                >
                  {busyId === device.device_id ? "Mengirim…" : "Kirim test"}
                </button>
              </li>
            ))}
          </ul>
        )}
        {status ? <p className="form-success" role="status">{status}</p> : null}
        {failure ? <p className="form-error" role="alert">{failure}</p> : null}
      </section>
      <section className="panel">
        <h2>Kanal</h2>
        <p className="muted">
          Telegram adalah kanal MVP. Android push direncanakan tetapi memerlukan Firebase/Expo credentials dan belum
          diaktifkan. Notifikasi tidak boleh menyalakan perangkat tanpa autentikasi.
        </p>
        <Link href="/settings/account" className="button button-secondary">
          Lihat akun
        </Link>
      </section>
    </div>
  );
}
