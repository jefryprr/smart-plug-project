"use client";

import { useEffect, useState } from "react";
import type { AutomationsResponse, Schedule } from "@smartplug/api-contract";
import { api } from "@/lib/api";
import { errorMessage } from "@/lib/hooks";

const DAY_LABELS = ["Min", "Sen", "Sel", "Rab", "Kam", "Jum", "Sab"];

function newSchedule(): Schedule {
  return {
    schedule_id: crypto.randomUUID(),
    days: [1, 2, 3, 4, 5],
    start_time: "18:00",
    duration_minutes: 60,
    action: "ON",
    time_zone: "Asia/Jakarta",
    enabled: false
  };
}

export function ScheduleEditor({
  deviceId,
  initial
}: {
  deviceId: string;
  initial: AutomationsResponse;
}) {
  const [schedules, setSchedules] = useState<Schedule[]>(initial.schedules);
  const [version, setVersion] = useState(initial.version);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    setSchedules(initial.schedules);
    setVersion(initial.version);
  }, [initial]);

  const update = (scheduleId: string, patch: Partial<Schedule>): void => {
    setSchedules((current) =>
      current.map((schedule) => (schedule.schedule_id === scheduleId ? { ...schedule, ...patch } : schedule))
    );
  };

  const toggleDay = (schedule: Schedule, day: number): void => {
    const days = schedule.days.includes(day)
      ? schedule.days.filter((value) => value !== day)
      : [...schedule.days, day].sort((a, b) => a - b);
    update(schedule.schedule_id, { days });
  };

  const save = async (): Promise<void> => {
    setSaving(true);
    setError(null);
    setMessage(null);
    try {
      const saved = await api.saveAutomations(deviceId, { schedules, version });
      setSchedules(saved.schedules);
      setVersion(saved.version);
      setMessage("Jadwal tersimpan. Perangkat akan mengeksekusi hanya saat jam valid dan kondisi aman.");
    } catch (caught) {
      setError(errorMessage(caught));
    } finally {
      setSaving(false);
    }
  };

  return (
    <section className="panel" aria-labelledby="schedule-title">
      <div className="panel-head">
        <div>
          <h2 id="schedule-title">Jadwal mingguan</h2>
          <p className="muted">
            Jadwal disimpan sebagai konfigurasi. ON otomatis ditolak bila jam tidak valid atau lockout aktif.
          </p>
        </div>
        <button type="button" className="button button-secondary" onClick={() => setSchedules((current) => [...current, newSchedule()])}>
          Tambah jadwal
        </button>
      </div>

      {schedules.length === 0 ? (
        <p className="muted">Belum ada jadwal. Tambahkan satu untuk mulai.</p>
      ) : (
        <ul className="schedule-list">
          {schedules.map((schedule) => (
            <li key={schedule.schedule_id} className="schedule-card">
              <div className="schedule-row">
                <label>
                  Hari
                  <span className="day-picker">
                    {DAY_LABELS.map((label, day) => (
                      <button
                        key={label}
                        type="button"
                        className={schedule.days.includes(day) ? "day-chip active" : "day-chip"}
                        aria-pressed={schedule.days.includes(day)}
                        onClick={() => toggleDay(schedule, day)}
                      >
                        {label}
                      </button>
                    ))}
                  </span>
                </label>
              </div>
              <div className="schedule-row">
                <label>
                  Jam mulai
                  <input
                    type="time"
                    value={schedule.start_time}
                    onChange={(event) => update(schedule.schedule_id, { start_time: event.target.value })}
                  />
                </label>
                <label>
                  Durasi (menit)
                  <input
                    type="number"
                    min={1}
                    max={1440}
                    value={schedule.duration_minutes}
                    onChange={(event) =>
                      update(schedule.schedule_id, { duration_minutes: Number(event.target.value) })
                    }
                  />
                </label>
                <label>
                  Aksi
                  <select
                    value={schedule.action}
                    onChange={(event) => update(schedule.schedule_id, { action: event.target.value as "ON" | "OFF" })}
                  >
                    <option value="ON">ON</option>
                    <option value="OFF">OFF</option>
                  </select>
                </label>
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={schedule.enabled}
                    onChange={(event) => update(schedule.schedule_id, { enabled: event.target.checked })}
                  />
                  Aktif
                </label>
              </div>
              <div className="schedule-row">
                <span className="muted small">Zona waktu: {schedule.time_zone}</span>
                <button
                  type="button"
                  className="button button-small button-danger"
                  onClick={() =>
                    setSchedules((current) => current.filter((item) => item.schedule_id !== schedule.schedule_id))
                  }
                >
                  Hapus
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}

      <div className="button-row">
        <button type="button" className="button button-primary" disabled={saving} onClick={() => void save()}>
          {saving ? "Menyimpan…" : "Simpan jadwal"}
        </button>
        <span className="muted small">Versi konfigurasi: {version}</span>
      </div>
      {message ? <p className="form-success" role="status">{message}</p> : null}
      {error ? <p className="form-error" role="alert">{error}</p> : null}
    </section>
  );
}
