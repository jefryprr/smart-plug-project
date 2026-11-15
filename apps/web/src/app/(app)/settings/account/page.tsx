"use client";

import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { Loading } from "@/components/Feedback";

export default function AccountSettingsPage() {
  const { user, loading } = useAuth();
  if (loading) return <Loading />;
  if (!user) return null;

  return (
    <div className="stack">
      <header className="page-head">
        <div>
          <p className="eyebrow">Pengaturan</p>
          <h1>Akun</h1>
          <p className="muted">Profil dan peran per rumah.</p>
        </div>
      </header>
      <section className="panel">
        <h2>Profil</h2>
        <dl className="stat-row">
          <div><dt>Nama</dt><dd>{user.display_name}</dd></div>
          <div><dt>Email</dt><dd>{user.email}</dd></div>
          <div><dt>User ID</dt><dd className="mono">{user.user_id}</dd></div>
        </dl>
      </section>
      <section className="panel">
        <h2>Rumah dan peran</h2>
        <ul className="compact-list">
          {user.homes.map((home) => (
            <li key={home.home_id}>
              <div>
                <strong>{home.name}</strong>
                <div className="muted small mono">{home.home_id}</div>
              </div>
              <span className="status-badge status-info">{home.role}</span>
            </li>
          ))}
        </ul>
        <p className="muted small">
          Peran diterapkan di backend melalui membership dan object-level authorization, bukan hanya menyembunyikan
          tombol di UI.
        </p>
      </section>
      <Link href="/settings/security" className="button button-secondary">
        Keamanan sesi
      </Link>
    </div>
  );
}
