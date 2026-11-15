"use client";

import { useState } from "react";
import type { Budget, DeviceDetail, Tariff } from "@smartplug/api-contract";
import { api } from "@/lib/api";
import { errorMessage } from "@/lib/hooks";
import { formatDateTime, formatIdr, toLocalInputValue } from "@/lib/format";

export function DeviceSettings({
  device,
  tariffs,
  budget,
  onChanged
}: {
  device: DeviceDetail;
  tariffs: Tariff[];
  budget: Budget;
  onChanged: () => void | Promise<void>;
}) {
  const [name, setName] = useState(device.name);
  const [room, setRoom] = useState(device.room ?? "");
  const [tariffValue, setTariffValue] = useState("1500");
  const [tariffFrom, setTariffFrom] = useState(toLocalInputValue(new Date(Date.now() + 60_000)));
  const [budgetPeriod, setBudgetPeriod] = useState(budget.period);
  const [kwhLimit, setKwhLimit] = useState(budget.kwh_limit?.toString() ?? "");
  const [idrLimit, setIdrLimit] = useState(budget.idr_limit?.toString() ?? "");
  const [budgetEnabled, setBudgetEnabled] = useState(budget.enabled);
  const [releaseId, setReleaseId] = useState("fw-0.2.0-rc1");
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

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
    <div className="settings-grid">
      <section className="panel">
        <h2>Identitas perangkat</h2>
        <form
          onSubmit={(event) => {
            event.preventDefault();
            void run(async () => {
              await api.renameDevice(device.device_id, name.trim(), room.trim() ? room.trim() : null);
            }, "Nama dan ruangan disimpan.");
          }}
        >
          <label>
            Nama
            <input value={name} maxLength={80} onChange={(event) => setName(event.target.value)} required />
          </label>
          <label>
            Ruangan
            <input value={room} maxLength={80} onChange={(event) => setRoom(event.target.value)} />
          </label>
          <button type="submit" className="button button-primary" disabled={busy}>
            Simpan identitas
          </button>
        </form>
      </section>

      <section className="panel">
        <h2>Notifikasi</h2>
        <p className="muted">
          Tombol ini mengirim satu notifikasi test ke provider yang dikonfigurasi. Tanpa token Telegram, backend memakai
          mock provider dan menandainya sebagai mock.
        </p>
        <button
          type="button"
          className="button button-secondary"
          disabled={busy}
          onClick={() =>
            void run(async () => {
              const result = await api.testNotification(device.device_id);
              setMessage(`Notifikasi ${result.status} melalui ${result.provider}.`);
            }, "")
          }
        >
          Kirim notifikasi test
        </button>
      </section>

      <section className="panel">
        <h2>Tarif listrik</h2>
        <p className="muted">
          Tarif baru hanya berlaku untuk periode setelah <code>effective_from</code>. Biaya historis tidak dihitung ulang
          diam-diam.
        </p>
        <ul className="compact-list">
          {tariffs.map((tariff) => (
            <li key={tariff.tariff_id}>
              <strong>{formatIdr(tariff.idr_per_kwh)}/kWh</strong>
              <span className="muted small">
                {formatDateTime(tariff.effective_from)} → {tariff.effective_to ? formatDateTime(tariff.effective_to) : "sekarang"}
              </span>
            </li>
          ))}
        </ul>
        <form
          onSubmit={(event) => {
            event.preventDefault();
            void run(async () => {
              const idr = Number(tariffValue);
              if (!Number.isFinite(idr) || idr <= 0) throw new Error("Tarif harus berupa angka > 0");
              const effective = new Date(tariffFrom);
              if (Number.isNaN(effective.getTime())) throw new Error("Waktu efektif tidak valid");
              await api.addTariff(device.device_id, idr, effective.toISOString());
            }, "Tarif baru ditambahkan.");
          }}
        >
          <label>
            Tarif (Rp/kWh)
            <input
              type="number"
              min={1}
              max={100000}
              value={tariffValue}
              onChange={(event) => setTariffValue(event.target.value)}
              required
            />
          </label>
          <label>
            Efektif mulai
            <input
              type="datetime-local"
              value={tariffFrom}
              onChange={(event) => setTariffFrom(event.target.value)}
              required
            />
          </label>
          <button type="submit" className="button button-primary" disabled={busy}>
            Tambah tarif
          </button>
        </form>
      </section>

      <section className="panel">
        <h2>Anggaran energi</h2>
        <form
          onSubmit={(event) => {
            event.preventDefault();
            void run(async () => {
              await api.saveBudget(device.device_id, {
                period: budgetPeriod,
                kwh_limit: kwhLimit ? Number(kwhLimit) : null,
                idr_limit: idrLimit ? Number(idrLimit) : null,
                enabled: budgetEnabled
              });
            }, "Anggaran disimpan.");
          }}
        >
          <label>
            Periode
            <select value={budgetPeriod} onChange={(event) => setBudgetPeriod(event.target.value as typeof budgetPeriod)}>
              <option value="daily">Harian</option>
              <option value="weekly">Mingguan</option>
              <option value="monthly">Bulanan</option>
            </select>
          </label>
          <label>
            Batas kWh (opsional)
            <input type="number" min={0} step="0.1" value={kwhLimit} onChange={(event) => setKwhLimit(event.target.value)} />
          </label>
          <label>
            Batas IDR (opsional)
            <input type="number" min={0} step="100" value={idrLimit} onChange={(event) => setIdrLimit(event.target.value)} />
          </label>
          <label className="checkbox-label">
            <input type="checkbox" checked={budgetEnabled} onChange={(event) => setBudgetEnabled(event.target.checked)} />
            Aktifkan peringatan anggaran
          </label>
          <button type="submit" className="button button-primary" disabled={busy}>
            Simpan anggaran
          </button>
        </form>
      </section>

      <section className="panel">
        <h2>OTA firmware</h2>
        <p className="muted">
          Permintaan OTA dicatat sebagai event dan tidak langsung dikirim ke perangkat. Firmware harus memverifikasi
          rilis, integritas, dan rollback; output tetap mengikuti kebijakan fail-safe.
        </p>
        <form
          onSubmit={(event) => {
            event.preventDefault();
            if (!window.confirm(`Minta OTA untuk rilis ${releaseId}? Ini belum mengirim firmware.`)) return;
            void run(async () => {
              const result = await api.requestOta(device.device_id, releaseId);
              setMessage(`Permintaan OTA dicatat: ${result.command_id} (${result.status}).`);
            }, "");
          }}
        >
          <label>
            Release ID
            <input value={releaseId} maxLength={80} onChange={(event) => setReleaseId(event.target.value)} required />
          </label>
          <button type="submit" className="button button-secondary" disabled={busy}>
            Minta OTA
          </button>
        </form>
      </section>

      <section className="panel danger-zone">
        <h2>Cabut akses perangkat</h2>
        <p className="muted">
          Mencabut kredensial dan pairing. Tindakan ini tidak memperbaiki kerusakan fisik dan tidak mereset lockout.
        </p>
        <button
          type="button"
          className="button button-danger"
          disabled={busy}
          onClick={() => {
            if (!window.confirm("Cabut akses perangkat ini? Tindakan ini memerlukan konfirmasi kedua.")) return;
            if (!window.confirm("Konfirmasi terakhir: cabut ownership dan kredensial perangkat?")) return;
            void run(async () => {
              await api.revoke(device.device_id);
              window.location.href = "/dashboard";
            }, "");
          }}
        >
          Cabut akses
        </button>
      </section>

      {message ? <p className="form-success" role="status">{message}</p> : null}
      {error ? <p className="form-error" role="alert">{error}</p> : null}
    </div>
  );
}
