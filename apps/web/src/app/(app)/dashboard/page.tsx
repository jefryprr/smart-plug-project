"use client";

import Link from "next/link";
import { useDevices } from "@/lib/hooks";
import { useAuth } from "@/lib/auth";
import { DeviceSummaryCard } from "@/components/DeviceSummaryCard";
import { EmptyState, ErrorPanel, Loading } from "@/components/Feedback";
import { StatusBadge } from "@/components/StatusBadge";

export default function DashboardPage() {
  const { user } = useAuth();
  const { data, loading, error, reload } = useDevices();

  if (loading) return <Loading />;
  if (error) return <ErrorPanel message={error} onRetry={() => void reload()} />;

  const devices = data ?? [];
  const online = devices.filter((device) => device.availability === "ONLINE").length;
  const faults = devices.filter((device) => device.state.lockout || device.state.fault_code).length;
  const synthetic = devices.filter((device) => device.data_source === "SYNTHETIC_DEMO").length;

  return (
    <div className="stack">
      <header className="page-head">
        <div>
          <p className="eyebrow">Dashboard</p>
          <h1>Halo, {user?.display_name ?? "Pengguna"}</h1>
          <p className="muted">
            Ringkasan perangkat dan status terakhir. Status koneksi tidak sama dengan status fisik outlet.
          </p>
        </div>
        <Link href="/onboarding/pair-device" className="button button-primary">
          Tambah perangkat
        </Link>
      </header>

      <div className="summary-grid">
        <div className="summary-card">
          <span className="label">Total perangkat</span>
          <strong>{devices.length}</strong>
        </div>
        <div className="summary-card">
          <span className="label">Online</span>
          <strong>{online}</strong>
        </div>
        <div className="summary-card">
          <span className="label">Fault / lockout</span>
          <strong>{faults}</strong>
        </div>
        <div className="summary-card">
          <span className="label">Data demo</span>
          <strong>{synthetic}</strong>
        </div>
      </div>

      {synthetic > 0 ? (
        <div className="demo-banner" role="status">
          <strong>{synthetic} perangkat memakai data demo sintetik.</strong> Label ini wajib dipertahankan; data
          sintetik tidak boleh dipakai sebagai bukti pengukuran atau keselamatan.
        </div>
      ) : null}

      {devices.length === 0 ? (
        <EmptyState title="Belum ada perangkat">
          <p>Klaim perangkat dengan kode pairing, atau jalankan device simulator untuk demo lokal.</p>
          <Link href="/onboarding/pair-device" className="button button-secondary">
            Buka pairing
          </Link>
        </EmptyState>
      ) : (
        <section aria-labelledby="devices-title">
          <div className="section-head">
            <h2 id="devices-title">Perangkat</h2>
            <StatusBadge label={`${devices.length} terdaftar`} tone="info" />
          </div>
          <div className="device-grid">
            {devices.map((device) => (
              <DeviceSummaryCard key={device.device_id} device={device} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
