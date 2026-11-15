"use client";

import Link from "next/link";
import { useDevices } from "@/lib/hooks";
import { DeviceSummaryCard } from "@/components/DeviceSummaryCard";
import { EmptyState, ErrorPanel, Loading } from "@/components/Feedback";

export default function DevicesPage() {
  const { data, loading, error, reload } = useDevices();

  if (loading) return <Loading />;
  if (error) return <ErrorPanel message={error} onRetry={() => void reload()} />;

  return (
    <div className="stack">
      <header className="page-head">
        <div>
          <p className="eyebrow">Perangkat</p>
          <h1>Semua perangkat</h1>
          <p className="muted">Setiap kartu menunjukkan availability dan output commanded, bukan klaim fisik.</p>
        </div>
        <Link href="/onboarding/pair-device" className="button button-primary">
          Tambah perangkat
        </Link>
      </header>
      {(data ?? []).length === 0 ? (
        <EmptyState title="Belum ada perangkat" />
      ) : (
        <div className="device-grid">
          {(data ?? []).map((device) => (
            <DeviceSummaryCard key={device.device_id} device={device} />
          ))}
        </div>
      )}
    </div>
  );
}
