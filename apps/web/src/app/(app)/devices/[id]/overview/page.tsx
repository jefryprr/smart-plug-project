"use client";

import { useMemo } from "react";
import { useParams } from "next/navigation";
import { useAnalytics, useDevice, useDiagnostics, useEvents, useTelemetry } from "@/lib/hooks";
import { PowerControl } from "@/components/PowerControl";
import { ElectricalReadings } from "@/components/ElectricalReadings";
import { UsageAndCost } from "@/components/UsageAndCost";
import { EnergyGraph } from "@/components/EnergyGraph";
import { EventList } from "@/components/EventList";
import { DeviceHealth } from "@/components/DeviceHealth";
import { TimeStatusPanel } from "@/components/TimeStatusPanel";
import { ErrorPanel, Loading } from "@/components/Feedback";

export default function OverviewPage() {
  const params = useParams();
  const deviceId = typeof params.id === "string" ? params.id : "";
  const device = useDevice(deviceId);
  const telemetry = useTelemetry(deviceId, 60);
  const events = useEvents(deviceId, 12);
  const diagnostics = useDiagnostics(deviceId);
  const range = useMemo(() => {
    const to = new Date();
    const from = new Date(to.getTime() - 24 * 60 * 60 * 1000);
    return { from: from.toISOString(), to: to.toISOString() };
  }, [deviceId]);
  const analytics = useAnalytics(deviceId, range.from, range.to, "hour");

  if (device.loading && !device.data) return <Loading />;
  if (device.error && !device.data) return <ErrorPanel message={device.error} onRetry={() => void device.reload()} />;
  if (!device.data) return <ErrorPanel message="Perangkat tidak ditemukan" />;

  const refresh = (): void => {
    void device.reload();
    void telemetry.reload();
    void events.reload();
    void analytics.reload();
    void diagnostics.reload();
  };

  return (
    <div className="overview-grid">
      <div className="span-2">
        <PowerControl device={device.data} onChanged={refresh} />
      </div>
      <div className="span-2">
        <TimeStatusPanel device={device.data} onChanged={refresh} />
      </div>
      <ElectricalReadings telemetry={telemetry.data} />
      <UsageAndCost analytics={analytics.data} />
      <div className="span-2">
        <EnergyGraph buckets={analytics.data?.buckets ?? []} title="Energi 24 jam terakhir" />
      </div>
      <EventList events={events.data?.events ?? []} />
      <DeviceHealth diagnostics={diagnostics.data} />
    </div>
  );
}
