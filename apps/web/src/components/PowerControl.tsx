"use client";

import { useEffect, useRef, useState } from "react";
import type { CommandResponse, DeviceDetail } from "@smartplug/api-contract";
import { api } from "@/lib/api";
import { errorMessage } from "@/lib/hooks";
import { formatTime } from "@/lib/format";

const TERMINAL = new Set(["APPLIED", "REJECTED", "EXPIRED", "TIMEOUT"]);

export function PowerControl({ device, onChanged }: { device: DeviceDetail; onChanged: () => void }) {
  const [busy, setBusy] = useState(false);
  const [pending, setPending] = useState<CommandResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const mounted = useRef(true);

  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
    };
  }, []);

  const offline = device.availability === "OFFLINE" || device.availability === "NEVER_SEEN";
  const locked = device.state.lockout || device.state.fault_code !== null;
  const onBlocked = offline || locked || !device.state.meter_valid || !device.state.temperature_valid;

  const send = async (requested: "ON" | "OFF"): Promise<void> => {
    if (requested === "ON" && onBlocked) {
      setError(
        locked
          ? "ON diblokir: lockout/fault aktif. Periksa penyebab dan reset secara otoritatif."
          : offline
            ? "ON diblokir: perangkat offline. Perintah tidak akan diklaim berhasil."
            : "ON diblokir: sensor metering/suhu tidak valid."
      );
      return;
    }
    setBusy(true);
    setError(null);
    setPending(null);
    try {
      const command = await api.command(device.device_id, requested, crypto.randomUUID());
      if (mounted.current) setPending(command);
      let latest = command;
      const deadline = Date.now() + 35_000;
      while (mounted.current && !TERMINAL.has(latest.status) && Date.now() < deadline) {
        await new Promise((resolve) => setTimeout(resolve, 1000));
        latest = await api.commandStatus(device.device_id, command.command_id);
        if (mounted.current) setPending(latest);
      }
      if (latest.status === "TIMEOUT" || (!TERMINAL.has(latest.status) && Date.now() >= deadline)) {
        setError("Tidak ada ACK final dari perangkat. Status fisik tidak dapat dipastikan.");
      }
      onChanged();
    } catch (caught) {
      setError(errorMessage(caught));
    } finally {
      if (mounted.current) setBusy(false);
    }
  };

  return (
    <section className="panel" aria-labelledby="power-control-title">
      <div className="panel-head">
        <div>
          <h2 id="power-control-title">Kontrol daya</h2>
          <p className="muted">Perintah ON/OFF memerlukan ACK perangkat; broker saja bukan bukti output berubah.</p>
        </div>
      </div>

      {offline ? (
        <div className="inline-alert warn" role="status">
          Perangkat <strong>{device.availability === "NEVER_SEEN" ? "belum pernah terhubung" : "offline"}</strong>.
          Status outlet fisik tidak dapat diklaim dari dashboard. Tombol ON dinonaktifkan.
        </div>
      ) : null}
      {locked ? (
        <div className="inline-alert danger" role="alert">
          <strong>Lockout aktif{device.state.fault_code ? `: ${device.state.fault_code}` : ""}.</strong> ON ditolak
          sampai penyebab diselesaikan dan reset otoritatif dilakukan.
        </div>
      ) : null}

      <dl className="stat-row">
        <div>
          <dt>Commanded</dt>
          <dd>{device.state.commanded_output}</dd>
        </div>
        <div>
          <dt>Teramati (feedback)</dt>
          <dd>{device.state.observed_output ?? "Tidak tersedia"}</dd>
        </div>
        <div>
          <dt>State version</dt>
          <dd>{device.state.state_version}</dd>
        </div>
      </dl>
      {device.state.observed_output === null ? (
        <p className="muted small">
          Perangkat ini tidak memiliki sensor feedback kontak. Dashboard tidak dapat membuktikan outlet fisik OFF;
          hanya status <em>commanded</em> dan ACK firmware yang tersedia.
        </p>
      ) : null}

      <div className="button-row">
        <button
          type="button"
          className="button button-on"
          disabled={busy || onBlocked || device.state.commanded_output === "ON"}
          onClick={() => void send("ON")}
        >
          Nyalakan
        </button>
        <button
          type="button"
          className="button button-off"
          disabled={busy || device.state.commanded_output === "OFF"}
          onClick={() => void send("OFF")}
        >
          Matikan
        </button>
        <button
          type="button"
          className="button button-danger"
          disabled={busy}
          onClick={() => void send("OFF")}
        >
          Emergency OFF
        </button>
      </div>

      <div className="command-status" aria-live="polite">
        {busy && !pending ? <p>Mengirim perintah…</p> : null}
        {pending ? (
          <p>
            <strong>{pending.status}</strong> — {pending.message}{" "}
            <span className="muted">({formatTime(pending.accepted_at)})</span>
          </p>
        ) : null}
        {error ? <p className="form-error" role="alert">{error}</p> : null}
      </div>
    </section>
  );
}
