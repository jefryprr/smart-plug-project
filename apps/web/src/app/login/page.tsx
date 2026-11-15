"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { errorMessage } from "@/lib/hooks";

export default function LoginPage() {
  const { user, login } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState("demo@example.com");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (user) {
      router.replace("/dashboard");
    }
  }, [router, user]);

  return (
    <main id="main-content" className="login-page">
      <section className="login-card" aria-labelledby="login-title">
        <div className="brand brand-large">
          <span className="brand-mark" aria-hidden="true" />
          <span>Smart Plug</span>
        </div>
        <h1 id="login-title">Masuk ke dashboard</h1>
        <p className="muted">
          Dashboard lokal untuk monitoring dan kontrol. Perintah ON/OFF memerlukan ACK perangkat dan tidak
          mengklaim status fisik tanpa feedback.
        </p>
        <form
          onSubmit={(event) => {
            event.preventDefault();
            setBusy(true);
            setError(null);
            void login(email, password)
              .catch((caught) => setError(errorMessage(caught)))
              .finally(() => setBusy(false));
          }}
        >
          <label>
            Email
            <input
              type="email"
              autoComplete="username"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
            />
          </label>
          <label>
            Password
            <input
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              minLength={8}
              required
            />
          </label>
          {error ? <p className="form-error" role="alert">{error}</p> : null}
          <button type="submit" className="button button-primary" disabled={busy}>
            {busy ? "Memeriksa…" : "Masuk"}
          </button>
        </form>
        <div className="demo-credentials">
          <strong>Demo lokal:</strong> <code>demo@example.com</code> / <code>demo1234</code>
          <p className="muted small">
            Kredensial ini hanya untuk seed demo. Ganti sebelum staging/production.
          </p>
        </div>
      </section>
      <aside className="login-aside" aria-label="Peringatan keselamatan">
        <h2>Batas klaim</h2>
        <ul>
          <li>Status <strong>OFFLINE</strong> berarti koneksi tidak terpantau, bukan bukti outlet fisik OFF.</li>
          <li><strong>ON</strong> ditolak saat lockout, fault, sensor tidak valid, atau kondisi terdegradasi.</li>
          <li>Data demo sintetik selalu diberi label; bukan hasil pengukuran perangkat nyata.</li>
          <li>Estimasi biaya bukan tagihan resmi PLN.</li>
        </ul>
      </aside>
    </main>
  );
}
