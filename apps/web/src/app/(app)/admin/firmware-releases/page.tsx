"use client";

import { useAuth } from "@/lib/auth";
import { Loading } from "@/components/Feedback";

export default function FirmwareReleasesPage() {
  const { user, loading } = useAuth();
  if (loading) return <Loading />;
  if (!user) return null;
  const canManage = user.homes.some((home) => home.role === "owner" || home.role === "admin");

  return (
    <div className="stack">
      <header className="page-head">
        <div>
          <p className="eyebrow">Admin</p>
          <h1>Rilis firmware</h1>
          <p className="muted">Halaman ini tidak menampilkan rilis palsu. Backend belum memiliki endpoint release management.</p>
        </div>
      </header>
      {!canManage ? (
        <div className="inline-alert danger" role="alert">
          Peran Anda tidak memiliki akses admin. Halaman tetap dapat dibaca sebagai dokumentasi status.
        </div>
      ) : null}
      <section className="panel">
        <h2>Status implementasi</h2>
        <ul className="check-list">
          <li>Permintaan OTA per perangkat dicatat sebagai event melalui halaman pengaturan perangkat.</li>
          <li>Belum ada endpoint publikasi rilis, signing, atau distribusi image.</li>
          <li>Firmware harus memverifikasi versi, hash/signature, partisi dual-bank, dan rollback.</li>
          <li>OTA tidak boleh menyalakan beban otomatis dan tetap tunduk lockout.</li>
        </ul>
        <p className="muted small">
          Status: <code>BLOCKED: RELEASE_MANAGEMENT_NOT_IMPLEMENTED</code>. Jangan menganggap unggahan APK atau ZIP
          firmware sebagai rilis yang ditandatangani.
        </p>
      </section>
    </div>
  );
}
