"use client";

import { useState } from "react";
import type { DeviceDetail } from "@smartplug/api-contract";
import { api } from "@/lib/api";
import { errorMessage } from "@/lib/hooks";
import { formatDateTime } from "@/lib/format";

export function TimeStatusPanel({
  device,
  onChanged
}: {
  device: DeviceDetail;
  onChanged: () => void | Promise<void>;
}) {
  const [manualUtc, setManualUtc] = useState("");
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const timeValid = device.state.time_valid ?? device.state.clock_valid;
  const source = device.state.time_source ?? (timeValid ? "sntp" : "none");
  const lastSync = device.state.last_sync ?? null;
  const lastKnown = device.state.last_known_time ?? null;
  const age = device.state.time_age_s ?? null;
  const canWrite = device.role === "owner" || device.role === "admin";

  const run = async (operation: () => Promise<void>, success: string): Promise<void> => {
    setBusy(true);
    setError(null);
    setMessage(null);
    try {
      await operation();
      setMessage(success);
      await onChanged();
    } catch (caught) {
      setError(errorMessage(caught));
    } finally {
      setBusy(false);
    }
  };

  return (
    <section className="panel" aria-labelledby="time-title">
      <div className="panel-head">
        <div>
          <h2 id="time-title">Waktu perangkat</h2>
          <p className="muted">
            UTC internal, tampilan Asia/Jakarta. Schedule hanya berjalan bila sinkronisasi masih valid.
          </p>
        </div>
      </div>

      {!timeValid ? (
        <div className="info-strip" role="alert">
          <strong>Waktu belum valid — schedule dinonaktifkan.</strong> Kontrol manual lewat tombol, web, atau API tetap
          boleh. Waktu yang terlewat tidak di-replay.
        </div>
      ) : null}

      <dl className="kv">
        <dt>Status</dt>
        <dd>{timeValid ? "VALID" : "INVALID"}</dd>
        <dt>Sumber</dt>
        <dd>{source}</dd>
        <dt>Sinkron terakhir</dt>
        <dd>{formatDateTime(lastSync)}</dd>
        <dt>Last known (display saja)</dt>
        <dd>{formatDateTime(lastKnown)}</dd>
        <dt>Umur sinkronisasi</dt>
        <dd>{age === null ? "—" : `${age} detik`}</dd>
      </dl>

      {canWrite ? (
        <div className="stack">
          <div className="button-row">
            <button
              type="button"
              className="button button-secondary"
              disabled={busy}
              onClick={() =>
                void run(async () => {
                  const server = await api.timeStatus();
                  await api.setDeviceTime(device.device_id, server.server_time, server.timezone);
                }, "Waktu perangkat disinkronkan dari server.")
              }
            >
              Sync now
            </button>
          </div>
          <form
            className="form-row"
            onSubmit={(event) => {
              event.preventDefault();
              void run(async () => {
                const iso = new Date(`${manualUtc}:00+07:00`).toISOString();
                await api.setDeviceTime(device.device_id, iso, "Asia/Jakarta");
              }, "Waktu manual disimpan dan diaudit.");
            }}
          >
            <label>
              Set manual (Asia/Jakarta)
              <input
                type="datetime-local"
                value={manualUtc}
                onChange={(event) => setManualUtc(event.target.value)}
                required
                disabled={busy}
              />
            </label>
            <button type="submit" className="button button-primary" disabled={busy || manualUtc.length === 0}>
              Simpan waktu
            </button>
          </form>
        </div>
      ) : (
        <p className="muted">Hanya owner/admin yang dapat mengubah waktu.</p>
      )}

      {message ? <p className="success">{message}</p> : null}
      {error ? <p className="error">{error}</p> : null}
    </section>
  );
}
