"use client";

import { useParams } from "next/navigation";
import { useAutomations } from "@/lib/hooks";
import { ScheduleEditor } from "@/components/ScheduleEditor";
import { ErrorPanel, Loading } from "@/components/Feedback";

export default function SchedulesPage() {
  const params = useParams();
  const deviceId = typeof params.id === "string" ? params.id : "";
  const automations = useAutomations(deviceId);

  if (automations.loading && !automations.data) return <Loading />;
  if (automations.error && !automations.data) return <ErrorPanel message={automations.error} onRetry={() => void automations.reload()} />;
  if (!automations.data) return <ErrorPanel message="Jadwal tidak tersedia" />;

  return (
    <div className="stack">
      <div className="info-strip">
        <strong>Eksekusi lokal.</strong> Jadwal dieksekusi oleh perangkat saat jam valid dan kondisi aman. Dashboard hanya
        menyinkronkan konfigurasi; perubahan tidak langsung menyalakan beban.
      </div>
      <ScheduleEditor deviceId={deviceId} initial={automations.data} />
    </div>
  );
}
