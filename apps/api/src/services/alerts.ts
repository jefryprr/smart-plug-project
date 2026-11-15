import type { TelemetryMessage } from "@smartplug/mqtt-contract";
import type { AppDb } from "../db/index.js";
import { appendDeviceEvent } from "./audit.js";
import { addDaysToDateKey, dateKeyInTimeZone, weekStartDateKey } from "./energy.js";

export interface AlertContext {
  timeZone: string;
  highPowerThresholdW?: number;
  highPowerSamples?: number;
  cooldownMs?: number;
}

const DEFAULT_HIGH_POWER_W = 2300;
const DEFAULT_SAMPLES = 3;
const DEFAULT_COOLDOWN_MS = 10 * 60 * 1000;

interface RecentPowerRow {
  active_power_w: number | null;
}

interface LastEventRow {
  occurred_at: string;
  payload_json: string;
}

function lastEvent(db: AppDb, deviceId: string, type: string): LastEventRow | null {
  return (
    db.get<LastEventRow>(
      `SELECT occurred_at, payload_json FROM fault_events
        WHERE device_id = ? AND type = ?
        ORDER BY occurred_at DESC LIMIT 1`,
      deviceId,
      type
    ) ?? null
  );
}

function canFire(last: LastEventRow | null, now: Date, cooldownMs: number): boolean {
  if (!last) return true;
  return now.getTime() - new Date(last.occurred_at).getTime() >= cooldownMs;
}

function periodBounds(period: "daily" | "weekly" | "monthly", now: Date, timeZone: string): {
  key: string;
  start: string;
  end: string;
} {
  const today = dateKeyInTimeZone(now.toISOString(), timeZone);
  if (period === "daily") {
    return {
      key: today,
      start: `${today}T00:00:00.000Z`,
      end: `${addDaysToDateKey(today, 1)}T00:00:00.000Z`
    };
  }
  if (period === "weekly") {
    const start = weekStartDateKey(today);
    return {
      key: start,
      start: `${start}T00:00:00.000Z`,
      end: `${addDaysToDateKey(start, 7)}T00:00:00.000Z`
    };
  }
  const month = today.slice(0, 7);
  const [yearText, monthText] = month.split("-");
  const nextMonth = new Date(Date.UTC(Number(yearText), Number(monthText), 1)).toISOString().slice(0, 7);
  return {
    key: month,
    start: `${month}-01T00:00:00.000Z`,
    end: `${nextMonth}-01T00:00:00.000Z`
  };
}

/**
 * Explainable, stateful rule evaluation. Alerts are advisory events; they are
 * not electrical protection and never bypass firmware safety interlocks.
 */
export function evaluateTelemetryAlerts(
  db: AppDb,
  deviceId: string,
  message: TelemetryMessage,
  now: Date,
  context: AlertContext
): string[] {
  const fired: string[] = [];
  const cooldownMs = context.cooldownMs ?? DEFAULT_COOLDOWN_MS;
  const threshold = context.highPowerThresholdW ?? DEFAULT_HIGH_POWER_W;
  const requiredSamples = context.highPowerSamples ?? DEFAULT_SAMPLES;

  if (message.quality === "INVALID") {
    const last = lastEvent(db, deviceId, "SENSOR_INVALID_ALERT");
    if (canFire(last, now, cooldownMs)) {
      appendDeviceEvent(db, {
        deviceId,
        type: "SENSOR_INVALID_ALERT",
        severity: "WARNING",
        summary: "Meter melaporkan data tidak valid; pembacaan tidak boleh ditampilkan sebagai live",
        source: "backend_rule",
        payload: { rule: "sensor_invalid", quality: message.quality },
        now
      });
      fired.push("sensor_invalid");
    }
  }

  if (message.state.fault === "OVERTEMP") {
    const last = lastEvent(db, deviceId, "HIGH_TEMPERATURE_ALERT");
    if (canFire(last, now, cooldownMs)) {
      appendDeviceEvent(db, {
        deviceId,
        type: "HIGH_TEMPERATURE_ALERT",
        severity: "CRITICAL",
        summary: "Firmware melaporkan OVERTEMP; proteksi lokal harus menangani pemutusan",
        source: "backend_rule",
        payload: { rule: "high_temperature", fault: message.state.fault, lockout: message.state.lockout },
        now
      });
      fired.push("high_temperature");
    }
  }

  const recent = db.all<RecentPowerRow>(
    `SELECT active_power_w FROM telemetry_samples
      WHERE device_id = ? AND quality = 'VALID'
      ORDER BY sequence DESC LIMIT ?`,
    deviceId,
    requiredSamples
  );
  if (
    recent.length >= requiredSamples &&
    recent.every((row) => row.active_power_w !== null && row.active_power_w > threshold)
  ) {
    const last = lastEvent(db, deviceId, "HIGH_POWER_ALERT");
    if (canFire(last, now, cooldownMs)) {
      appendDeviceEvent(db, {
        deviceId,
        type: "HIGH_POWER_ALERT",
        severity: "WARNING",
        summary: `Daya tinggi: ${message.measurements.active_power_w?.toFixed(1) ?? "?"} W melewati ambang ${threshold} W selama ${requiredSamples} sampel`,
        source: "backend_rule",
        payload: {
          rule: "high_power",
          threshold_w: threshold,
          required_samples: requiredSamples,
          observed_w: message.measurements.active_power_w
        },
        now
      });
      fired.push("high_power");
    }
  }

  const budget = db.get<{
    period: "daily" | "weekly" | "monthly";
    kwh_limit: number | null;
    idr_limit: number | null;
    enabled: number;
  }>(`SELECT period, kwh_limit, idr_limit, enabled FROM energy_budgets WHERE device_id = ?`, deviceId);

  if (budget && budget.enabled === 1) {
    const bounds = periodBounds(budget.period, now, context.timeZone);
    const totals = db.get<{ energy_kwh: number; cost_idr: number | null }>(
      `SELECT COALESCE(SUM(energy_kwh), 0) AS energy_kwh,
              CASE WHEN SUM(CASE WHEN cost_idr IS NULL THEN 1 ELSE 0 END) > 0 THEN NULL
                   ELSE COALESCE(SUM(cost_idr), 0) END AS cost_idr
         FROM daily_energy_aggregates
        WHERE device_id = ? AND day >= ? AND day < ?`,
      deviceId,
      bounds.start.slice(0, 10),
      bounds.end.slice(0, 10)
    );
    const kwhCrossed = budget.kwh_limit !== null && (totals?.energy_kwh ?? 0) >= budget.kwh_limit;
    const idrCrossed = budget.idr_limit !== null && totals?.cost_idr !== null && (totals?.cost_idr ?? 0) >= budget.idr_limit;
    if (kwhCrossed || idrCrossed) {
      const last = lastEvent(db, deviceId, "BUDGET_ALERT");
      const samePeriod = last
        ? (last.payload_json.includes(`"period_key":"${bounds.key}"`) && last.occurred_at >= bounds.start)
        : false;
      if (!samePeriod) {
        appendDeviceEvent(db, {
          deviceId,
          type: "BUDGET_ALERT",
          severity: "WARNING",
          summary: `Anggaran ${budget.period} terlampaui (${totals?.energy_kwh.toFixed(3) ?? "?"} kWh, biaya ${totals?.cost_idr === null ? "parsial" : `Rp${Math.round(totals?.cost_idr ?? 0)}`})`,
          source: "backend_rule",
          payload: {
            rule: "budget_crossing",
            period: budget.period,
            period_key: bounds.key,
            energy_kwh: totals?.energy_kwh ?? null,
            cost_idr: totals?.cost_idr ?? null,
            kwh_limit: budget.kwh_limit,
            idr_limit: budget.idr_limit,
            kwh_crossed: kwhCrossed,
            idr_crossed: idrCrossed
          },
          now
        });
        fired.push("budget_crossing");
      }
    }
  }

  return fired;
}
