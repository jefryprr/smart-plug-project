"use client";

import { useParams } from "next/navigation";
import { useAutomations, useDevice } from "@/lib/hooks";
import { ScheduleEditor } from "@/components/ScheduleEditor";
import { ErrorPanel, Loading } from "@/components/Feedback";

export default function SchedulesPage() {
  const params = useParams();
  const deviceId = typeof params.id === "string" ? params.id : "";
  const automations = useAutomations(deviceId);
  const device = useDevice(deviceId);

  if (automations.loading && !automations.data) return <Loading />;
  if (automations.error && !automations.data) return <ErrorPanel message={automations.error} onRetry={() => void automations.reload()} />;
  if (!automations.data) return <ErrorPanel message="Jadwal tidak tersedia" />;
  const timeValid = device.data ? (device.data.state.time_valid ?? device.data.state.clock_valid) : false;

  return (
    <div className="stack">
      {!timeValid ? (
        <div className="info-strip" role="alert">
          <strong>Waktu belum valid — schedule dinonaktifkan.</strong> Kontrol manual tetap boleh. Perangkat tidak
          mengeksekusi atau me-replay jadwal sampai ada sinkronisasi baru.
        </div>
      ) : (
        <div className="info-strip">
          <strong>Eksekusi lokal.</strong> Jadwal dieksekusi oleh perangkat saat waktu valid dan kondisi aman. Dashboard
          hanya menyinkronkan konfigurasi; perubahan tidak langsung menyalakan beban.
        </div>
      )}
      <fieldset disabled={!timeValid} style={{ border: 0, padding: 0, margin: 0 }}>
        <ScheduleEditor deviceId={deviceId} initial={automations.data} />
      </fieldset>
    </div>
  );
}
