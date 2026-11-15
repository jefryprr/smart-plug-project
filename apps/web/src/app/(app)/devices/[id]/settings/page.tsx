"use client";

import { useParams } from "next/navigation";
import { useBudget, useDevice, useTariffs } from "@/lib/hooks";
import { DeviceSettings } from "@/components/DeviceSettings";
import { ErrorPanel, Loading } from "@/components/Feedback";

export default function SettingsPage() {
  const params = useParams();
  const deviceId = typeof params.id === "string" ? params.id : "";
  const device = useDevice(deviceId);
  const tariffs = useTariffs(deviceId);
  const budget = useBudget(deviceId);

  if ((device.loading && !device.data) || (tariffs.loading && !tariffs.data) || (budget.loading && !budget.data)) {
    return <Loading />;
  }
  if (device.error && !device.data) return <ErrorPanel message={device.error} onRetry={() => void device.reload()} />;
  if (tariffs.error && !tariffs.data) return <ErrorPanel message={tariffs.error} onRetry={() => void tariffs.reload()} />;
  if (budget.error && !budget.data) return <ErrorPanel message={budget.error} onRetry={() => void budget.reload()} />;
  if (!device.data || !tariffs.data || !budget.data) return <ErrorPanel message="Pengaturan tidak tersedia" />;

  return (
    <DeviceSettings
      device={device.data}
      tariffs={tariffs.data}
      budget={budget.data}
      onChanged={() => {
        void device.reload();
        void tariffs.reload();
        void budget.reload();
      }}
    />
  );
}
