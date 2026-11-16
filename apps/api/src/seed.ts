import { randomUUID } from "node:crypto";
import type { AppDb } from "./db/index.js";
import { hashPassword, sha256 } from "./auth/password.js";
import { appendDeviceEvent } from "./services/audit.js";
import { ingestTelemetry } from "./services/telemetry.js";

export interface SeedResult {
  userId: string;
  homeId: string;
  deviceId: string;
  pairingCode: string;
}

export interface SeedOptions {
  withSyntheticTelemetry?: boolean;
  demoEmail?: string;
  demoPassword?: string;
}

function hourIso(base: Date, offsetHours: number): string {
  return new Date(base.getTime() + offsetHours * 60 * 60 * 1000).toISOString();
}

/**
 * Deterministic demo seed. All telemetry is explicitly synthetic and marked
 * data_source=SYNTHETIC_DEMO. It must never be presented as a real measurement.
 */
export function seedDemo(db: AppDb, now: Date, options: SeedOptions = {}): SeedResult {
  const email = options.demoEmail ?? "demo@example.com";
  const password = options.demoPassword ?? "demo1234";
  const userId = "user-demo";
  const homeId = "home-demo";
  const deviceId = "dev-sim-001";
  const pairingCode = "123456";
  const nowIso = now.toISOString();

  const existing = db.get<{ user_id: string }>(`SELECT user_id FROM users WHERE email = ?`, email);
  if (existing) {
    const device = db.get<{ device_id: string }>(`SELECT device_id FROM devices WHERE device_id = ?`, deviceId);
    return { userId: existing.user_id, homeId, deviceId: device?.device_id ?? deviceId, pairingCode };
  }

  db.transaction(() => {
    db.run(
      `INSERT INTO users (user_id, email, password_hash, display_name, created_at) VALUES (?, ?, ?, ?, ?)`,
      userId,
      email,
      hashPassword(password),
      "Demo User",
      nowIso
    );
    db.run(`INSERT INTO homes (home_id, name, created_at) VALUES (?, ?, ?)`, homeId, "Rumah Demo", nowIso);
    db.run(
      `INSERT INTO memberships (home_id, user_id, role, created_at) VALUES (?, ?, 'owner', ?)`,
      homeId,
      userId,
      nowIso
    );

    const state = {
      commanded_output: "OFF",
      observed_output: null,
      lockout: false,
      fault_code: null,
      state_version: 4,
      last_transition_at: hourIso(now, -12),
      clock_valid: true,
      meter_valid: true,
      temperature_valid: true
    };
    db.run(
      `INSERT INTO devices
        (device_id, home_id, name, room, hardware_revision, firmware_version, data_source, state_json,
         diagnostics_json, last_seen_at, availability, created_at)
       VALUES (?, ?, ?, ?, ?, ?, 'SYNTHETIC_DEMO', ?, ?, ?, 'ONLINE', ?)`,
      deviceId,
      homeId,
      "Smart Plug Demo",
      "Ruang Tamu",
      "REV_C_PSU_BOARD",
      "0.1.0-demo",
      JSON.stringify(state),
      JSON.stringify({
        firmware_version: "0.1.0-demo",
        build_sha: "synthetic-demo",
        uptime_seconds: 3600,
        rssi_dbm: -52,
        heap_free_bytes: 180000,
        last_error: null,
        sensor_health: { meter: "OK", temperature: "OK", relay_feedback: "NOT_INSTALLED" },
        wifi_state: "CONNECTED",
        command_counts: { accepted: 0, rejected: 0, expired: 0 }
      }),
      nowIso,
      nowIso
    );

    db.run(
      `INSERT INTO device_claims (claim_id, device_id, pairing_code_hash, expires_at, claimed_at, claimed_by)
       VALUES (?, ?, ?, ?, NULL, NULL)`,
      randomUUID(),
      deviceId,
      sha256(pairingCode),
      hourIso(now, 24 * 30)
    );

    db.run(
      `INSERT INTO electricity_tariffs (tariff_id, device_id, currency, idr_per_kwh, effective_from, effective_to, created_at)
       VALUES (?, ?, 'IDR', 1500, '2026-01-01T00:00:00.000Z', NULL, ?)`,
      "tariff-demo",
      deviceId,
      nowIso
    );

    db.run(
      `INSERT INTO energy_budgets (budget_id, device_id, period, kwh_limit, idr_limit, enabled, updated_at)
       VALUES (?, ?, 'monthly', 30, 50000, 1, ?)`,
      "budget-demo",
      deviceId,
      nowIso
    );

    db.run(
      `INSERT INTO automation_rules (device_id, version, schedules_json, updated_at) VALUES (?, 0, ?, ?)`,
      deviceId,
      JSON.stringify([
        {
          schedule_id: "schedule-demo-1",
          days: [1, 2, 3, 4, 5],
          start_time: "18:00",
          duration_minutes: 120,
          action: "ON",
          time_zone: "Asia/Jakarta",
          enabled: false
        }
      ]),
      nowIso
    );
  });

  if (options.withSyntheticTelemetry !== false) {
    let energy = 12;
    for (let index = 0; index < 48; index += 1) {
      const sampledAt = hourIso(now, index - 47);
      const on = index >= 36;
      const activePower = on ? 120 + Math.round(60 * Math.sin(index / 3)) : 0.4;
      const voltage = 230 + 1.2 * Math.sin(index / 4);
      const powerFactor = 0.9;
      const current = activePower / (voltage * powerFactor);
      energy += activePower / 1000;
      ingestTelemetry(
        db,
        deviceId,
        {
          schema_version: 1,
          device_id: deviceId,
          message_id: `seed-telemetry-${index}`,
          sequence: 100 + index,
          sampled_at: sampledAt,
          quality: "VALID",
          measurements: {
            voltage_v: Number(voltage.toFixed(2)),
            current_a: Number(current.toFixed(3)),
            active_power_w: Number(activePower.toFixed(2)),
            energy_kwh_total: Number(energy.toFixed(4)),
            power_factor: powerFactor,
            frequency_hz: 50
          },
          state: {
            commanded_output: on ? "ON" : "OFF",
            observed_output: null,
            fault: null,
            lockout: false,
            state_version: 4 + index,
            clock_valid: true,
            meter_valid: true,
            temperature_valid: true
          }
        },
        nowIso,
        "Asia/Jakarta"
      );
    }

    appendDeviceEvent(db, {
      deviceId,
      type: "DEMO_DATA_SEEDED",
      severity: "INFO",
      summary: "Data demo sintetik dimuat; bukan hasil pengukuran perangkat nyata",
      source: "seed",
      payload: { samples: 48, data_source: "SYNTHETIC_DEMO" },
      now
    });
  }

  return { userId, homeId, deviceId, pairingCode };
}
