"use client";

import { useAuth } from "@/lib/auth";
import { Loading } from "@/components/Feedback";

export default function SecuritySettingsPage() {
  const { user, loading, logout } = useAuth();
  if (loading) return <Loading />;
  if (!user) return null;

  return (
    <div className="stack">
      <header className="page-head">
        <div>
          <p className="eyebrow">Pengaturan</p>
          <h1>Keamanan sesi</h1>
          <p className="muted">Token akses disimpan di sessionStorage dan tidak ditulis ke URL atau log.</p>
        </div>
      </header>
      <section className="panel">
        <h2>Kontrol saat ini</h2>
        <ul className="check-list">
          <li>Access token berumur pendek; refresh token dirotasi dan disimpan sebagai hash di backend.</li>
          <li>Login dibatasi rate limit; pesan gagal tidak membocorkan apakah email terdaftar.</li>
          <li>Setiap endpoint perangkat memakai object-level authorization dan tenant scoping.</li>
          <li>Perintah ON/OFF memakai idempotency key, TTL, replay check, dan safety lockout.</li>
          <li>Secret provider (Telegram/token) tidak boleh masuk repo, log, atau payload telemetry.</li>
        </ul>
      </section>
      <section className="panel">
        <h2>Belum tersedia</h2>
        <p className="muted">
          Endpoint revoke-all-sessions belum diimplementasikan. Logout hanya mencabut sesi saat ini. Untuk insiden,
          gunakan logout di semua perangkat dan rotasi kredensial backend.
        </p>
        <button type="button" className="button button-danger" onClick={() => void logout()}>
          Logout sesi ini
        </button>
      </section>
    </div>
  );
}
