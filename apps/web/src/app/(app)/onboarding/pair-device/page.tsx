"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { errorMessage } from "@/lib/hooks";

export default function PairDevicePage() {
  const router = useRouter();
  const [code, setCode] = useState("");
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  return (
    <div className="stack">
      <header className="page-head">
        <div>
          <p className="eyebrow">Onboarding</p>
          <h1>Klaim perangkat</h1>
          <p className="muted">
            Pairing memerlukan kode sekali pakai yang membuktikan kepemilikan fisik. Kode kedaluwarsa dan tidak dapat
            dipakai ulang.
          </p>
        </div>
      </header>
      <section className="panel narrow-panel">
        <form
          onSubmit={(event) => {
            event.preventDefault();
            setBusy(true);
            setError(null);
            setMessage(null);
            void api
              .claim(code.trim(), name.trim() || undefined)
              .then((result) => {
                setMessage(`Perangkat ${result.device_id} berhasil diklaim.`);
                router.push(`/devices/${result.device_id}/overview`);
              })
              .catch((caught) => setError(errorMessage(caught)))
              .finally(() => setBusy(false));
          }}
        >
          <label>
            Kode pairing
            <input
              inputMode="numeric"
              pattern="[0-9]{6,10}"
              value={code}
              onChange={(event) => setCode(event.target.value)}
              placeholder="123456"
              required
            />
          </label>
          <label>
            Nama perangkat (opsional)
            <input value={name} maxLength={80} onChange={(event) => setName(event.target.value)} placeholder="Plug Dapur" />
          </label>
          {error ? <p className="form-error" role="alert">{error}</p> : null}
          {message ? <p className="form-success" role="status">{message}</p> : null}
          <button type="submit" className="button button-primary" disabled={busy}>
            {busy ? "Mengklaim…" : "Klaim perangkat"}
          </button>
        </form>
        <p className="muted small">
          Demo lokal memakai kode <code>123456</code>. Kode ini hanya untuk seed demo dan harus diganti pada perangkat
          nyata. Jangan menulis kode pairing ke log publik.
        </p>
      </section>
    </div>
  );
}
