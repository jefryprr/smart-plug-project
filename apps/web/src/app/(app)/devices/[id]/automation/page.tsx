"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useAutomations, useEvents } from "@/lib/hooks";
import { EventList } from "@/components/EventList";
import { ErrorPanel, Loading } from "@/components/Feedback";
import { StatusBadge } from "@/components/StatusBadge";

const RULES = [
  {
    id: "high_power",
    name: "Daya tinggi",
    description: "Event WARNING saat daya aktif melewati ambang dan durasi; throttle mencegah spam.",
    status: "Backend rule",
    tone: "ok" as const
  },
  {
    id: "budget_crossing",
    name: "Anggaran terlampaui",
    description: "Event saat pemakaian periode melewati batas kWh/IDR; tidak berulang setiap refresh.",
    status: "Backend rule",
    tone: "ok" as const
  },
  {
    id: "standby_waste",
    name: "Standby waste",
    description: "Memerlukan baseline dan durasi; belum diaktifkan secara default.",
    status: "Belum aktif",
    tone: "warn" as const
  },
  {
    id: "temperature_rising",
    name: "Suhu naik",
    description: "Firmware menangani proteksi lokal; backend hanya menerima event. Uji fisik belum ada.",
    status: "Firmware / BLOCKED",
    tone: "warn" as const
  },
  {
    id: "sensor_stale",
    name: "Sensor basi",
    description: "Sensor timeout/CRC invalid harus menghasilkan state invalid, bukan angka lama sebagai live.",
    status: "Firmware / BLOCKED",
    tone: "warn" as const
  }
];

export default function AutomationPage() {
  const params = useParams();
  const deviceId = typeof params.id === "string" ? params.id : "";
  const automations = useAutomations(deviceId);
  const events = useEvents(deviceId, 20);

  if (automations.loading && !automations.data) return <Loading />;
  if (automations.error && !automations.data) return <ErrorPanel message={automations.error} onRetry={() => void automations.reload()} />;

  return (
    <div className="stack">
      <section className="panel">
        <div className="panel-head">
          <div>
            <h2>Aturan dan otomasi</h2>
            <p className="muted">
              Aturan keselamatan listrik tetap berada di firmware dan proteksi independen. Analitik backend bukan proteksi.
            </p>
          </div>
          <Link href={`/devices/${deviceId}/schedules`} className="button button-secondary">
            Kelola jadwal
          </Link>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th scope="col">Rule</th>
                <th scope="col">Perilaku</th>
                <th scope="col">Status</th>
              </tr>
            </thead>
            <tbody>
              {RULES.map((rule) => (
                <tr key={rule.id}>
                  <td><strong>{rule.name}</strong><br /><span className="mono small">{rule.id}</span></td>
                  <td>{rule.description}</td>
                  <td><StatusBadge label={rule.status} tone={rule.tone} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
      <section className="panel">
        <h2>Jadwal saat ini</h2>
        {(automations.data?.schedules ?? []).length === 0 ? (
          <p className="muted">Belum ada jadwal.</p>
        ) : (
          <ul className="compact-list">
            {(automations.data?.schedules ?? []).map((schedule) => (
              <li key={schedule.schedule_id}>
                <strong>{schedule.action} · {schedule.start_time} · {schedule.duration_minutes} menit</strong>
                <span className="muted small">
                  Hari: {schedule.days.join(", ")} · {schedule.enabled ? "aktif" : "nonaktif"} · {schedule.time_zone}
                </span>
              </li>
            ))}
          </ul>
        )}
      </section>
      <EventList events={events.data?.events ?? []} title="Event otomasi dan fault" />
    </div>
  );
}
