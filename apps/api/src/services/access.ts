import type { AppDb, Row } from "../db/index.js";
import { forbidden, notFound } from "../errors.js";
import type { Role } from "@smartplug/api-contract";

export interface DeviceAccessRow extends Row {
  device_id: string;
  home_id: string;
  name: string;
  room: string | null;
  hardware_revision: string | null;
  firmware_version: string | null;
  data_source: string;
  state_json: string;
  diagnostics_json: string | null;
  last_seen_at: string | null;
  availability: string;
  created_at: string;
  role: Role;
}

export function getDeviceAccess(db: AppDb, userId: string, deviceId: string): DeviceAccessRow | null {
  const row = db.get<DeviceAccessRow>(
    `SELECT d.device_id, d.home_id, d.name, d.room, d.hardware_revision, d.firmware_version,
            d.data_source, d.state_json, d.diagnostics_json, d.last_seen_at, d.availability,
            d.created_at, m.role
       FROM devices d
       JOIN memberships m ON m.home_id = d.home_id
      WHERE d.device_id = ? AND m.user_id = ?`,
    deviceId,
    userId
  );
  return row ?? null;
}

export function requireDeviceAccess(db: AppDb, userId: string, deviceId: string): DeviceAccessRow {
  const access = getDeviceAccess(db, userId, deviceId);
  if (!access) {
    // Deliberately return 404 for a device in another tenant, not 403.
    throw notFound("Perangkat tidak ditemukan");
  }
  return access;
}

export function requireWriteRole(access: DeviceAccessRow): void {
  if (access.role !== "owner" && access.role !== "admin") {
    throw forbidden("Peran viewer tidak boleh mengubah perangkat");
  }
}

export function requireOwnerRole(access: DeviceAccessRow): void {
  if (access.role !== "owner") {
    throw forbidden("Hanya owner yang boleh melakukan tindakan ini");
  }
}

export function listDevicesForUser(db: AppDb, userId: string): DeviceAccessRow[] {
  return db.all<DeviceAccessRow>(
    `SELECT d.device_id, d.home_id, d.name, d.room, d.hardware_revision, d.firmware_version,
            d.data_source, d.state_json, d.diagnostics_json, d.last_seen_at, d.availability,
            d.created_at, m.role
       FROM devices d
       JOIN memberships m ON m.home_id = d.home_id
      WHERE m.user_id = ?
      ORDER BY d.created_at ASC`,
    userId
  );
}

export interface StoredDeviceState {
  commanded_output: "ON" | "OFF";
  observed_output: "ON" | "OFF" | null;
  lockout: boolean;
  fault_code: string | null;
  state_version: number;
  last_transition_at: string;
  clock_valid: boolean;
  meter_valid: boolean;
  temperature_valid: boolean;
  time_valid: boolean;
  time_source: "sntp" | "api" | "mqtt" | "manual" | "none";
  last_sync: string | null;
  last_known_time: string | null;
  time_age_s: number | null;
}

export function defaultDeviceState(now: Date = new Date()): StoredDeviceState {
  return {
    commanded_output: "OFF",
    observed_output: null,
    lockout: false,
    fault_code: null,
    state_version: 0,
    last_transition_at: now.toISOString(),
    clock_valid: false,
    meter_valid: false,
    temperature_valid: false,
    time_valid: false,
    time_source: "none",
    last_sync: null,
    last_known_time: null,
    time_age_s: null
  };
}

export function parseDeviceState(raw: string): StoredDeviceState {
  try {
    const parsed = JSON.parse(raw) as Partial<StoredDeviceState>;
    const base = defaultDeviceState();
    return {
      commanded_output: parsed.commanded_output === "ON" ? "ON" : "OFF",
      observed_output: parsed.observed_output === "ON" || parsed.observed_output === "OFF" ? parsed.observed_output : null,
      lockout: parsed.lockout === true,
      fault_code: typeof parsed.fault_code === "string" ? parsed.fault_code : null,
      state_version: typeof parsed.state_version === "number" && Number.isFinite(parsed.state_version) ? parsed.state_version : 0,
      last_transition_at: typeof parsed.last_transition_at === "string" ? parsed.last_transition_at : base.last_transition_at,
      clock_valid: parsed.clock_valid === true,
      meter_valid: parsed.meter_valid === true,
      temperature_valid: parsed.temperature_valid === true,
      time_valid: parsed.time_valid === true,
      time_source:
        parsed.time_source === "sntp" || parsed.time_source === "api" || parsed.time_source === "mqtt" ||
        parsed.time_source === "manual" || parsed.time_source === "none"
          ? parsed.time_source
          : "none",
      last_sync: typeof parsed.last_sync === "string" ? parsed.last_sync : null,
      last_known_time: typeof parsed.last_known_time === "string" ? parsed.last_known_time : null,
      time_age_s: typeof parsed.time_age_s === "number" && Number.isFinite(parsed.time_age_s) ? parsed.time_age_s : null
    };
  } catch {
    return defaultDeviceState();
  }
}

export function serializeDeviceState(state: StoredDeviceState): string {
  return JSON.stringify(state);
}
