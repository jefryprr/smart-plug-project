"use client";

import type { ReactNode } from "react";
import { useParams } from "next/navigation";
import { useDevice } from "@/lib/hooks";
import { DeviceTabs } from "@/components/DeviceTabs";
import { DemoBanner } from "@/components/DemoBanner";
import { ErrorPanel, Loading } from "@/components/Feedback";
import { StatusBadge, availabilityBadge, outputBadge } from "@/components/StatusBadge";

export default function DeviceLayout({ children }: { children: ReactNode }) {
  const params = useParams();
  const deviceId = typeof params.id === "string" ? params.id : "";
  const { data: device, loading, error, reload } = useDevice(deviceId);

  if (!deviceId) return <ErrorPanel message="Device ID tidak valid" />;
  if (loading && !device) return <Loading label="Memuat perangkat…" />;
  if (error && !device) return <ErrorPanel message={error} onRetry={() => void reload()} />;
  if (!device) return <ErrorPanel message="Perangkat tidak ditemukan atau tidak dapat diakses." />;

  const availability = availabilityBadge(device.availability);
  const output = outputBadge(device.state.commanded_output);

  return (
    <div className="stack">
      <header className="device-head">
        <div>
          <p className="eyebrow">Perangkat</p>
          <h1>{device.name}</h1>
          <p className="muted">
            {device.room ?? "Tanpa ruangan"} · <span className="mono">{device.device_id}</span> · role {device.role}
          </p>
        </div>
        <div className="device-head-badges">
          <StatusBadge label={availability.label} tone={availability.tone} />
          <StatusBadge label={output.label} tone={output.tone} />
          {device.state.lockout ? <StatusBadge label="LOCKOUT" tone="danger" /> : null}
        </div>
      </header>
      <DemoBanner dataSource={device.data_source} />
      <DeviceTabs deviceId={device.device_id} />
      {children}
    </div>
  );
}
