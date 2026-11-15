import { randomUUID } from "node:crypto";
import type { AppDb, Row } from "../db/index.js";
import type { AckMessage, AvailabilityMessage, EventMessage, StateMessage, TelemetryMessage } from "@smartplug/mqtt-contract";
import { computeEnergyDelta } from "@smartplug/domain";
import { applyIntervalToDailyAggregate } from "./energy.js";
import { appendDeviceEvent } from "./audit.js";
import { parseDeviceState, serializeDeviceState, type StoredDeviceState } from "./access.js";
import { evaluateTelemetryAlerts } from "./alerts.js";
import type { DeviceState } from "@smartplug/api-contract";

export interface TelemetryIngestResult {
  inserted: boolean;
  duplicate: boolean;
  gap: boolean;
  reasonCode: string;
  sampleId: string | null;
  alertsFired: string[];
}

export interface TelemetryRow extends Row {
  sample_id: string;
  device_id: string;
  sequence: number;
  sampled_at: string;
  received_at: string;
  quality: "VALID" | "STALE" | "INVALID";
  voltage_v: number | null;
  current_a: number | null;
  active_power_w: number | null;
  energy_kwh_total: number | null;
  power_factor: number | null;
  frequency_hz: number | null;
  state_json: string;
}

function stateFromMqtt(state: TelemetryMessage["state"], previous: StoredDeviceState, receivedAt: string): StoredDeviceState {
  const changed =
    previous.commanded_output !== state.commanded_output ||
    previous.fault_code !== state.fault ||
    previous.lockout !== state.lockout;
  return {
    commanded_output: state.commanded_output,
    observed_output: state.observed_output,
    lockout: state.lockout,
    fault_code: state.fault,
    state_version: state.state_version,
    last_transition_at: changed ? receivedAt : previous.last_transition_at,
    clock_valid: state.clock_valid,
    meter_valid: state.meter_valid,
    temperature_valid: state.temperature_valid
  };
}

export function ingestTelemetry(
  db: AppDb,
  deviceId: string,
  message: TelemetryMessage,
  receivedAt: string,
  timeZone: string
): TelemetryIngestResult {
  if (message.device_id !== deviceId) {
    throw new Error("TELEMETRY_DEVICE_MISMATCH");
  }
  const device = db.get<{ state_json: string; data_source: string }>(
    `SELECT state_json, data_source FROM devices WHERE device_id = ?`,
    deviceId
  );
  if (!device) {
    throw new Error("DEVICE_NOT_FOUND");
  }

  const previous = db.get<TelemetryRow>(
    `SELECT * FROM telemetry_samples
      WHERE device_id = ? AND sequence < ?
      ORDER BY sequence DESC LIMIT 1`,
    deviceId,
    message.sequence
  );

  const previousState = parseDeviceState(device.state_json);
  const nextState = stateFromMqtt(message.state, previousState, receivedAt);
  const sampleId = randomUUID();

  try {
    db.transaction(() => {
      db.run(
        `INSERT INTO telemetry_samples
          (sample_id, device_id, sequence, sampled_at, received_at, quality, voltage_v, current_a,
           active_power_w, energy_kwh_total, power_factor, frequency_hz, state_json)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
        sampleId,
        deviceId,
        message.sequence,
        message.sampled_at,
        receivedAt,
        message.quality,
        message.measurements.voltage_v,
        message.measurements.current_a,
        message.measurements.active_power_w,
        message.measurements.energy_kwh_total,
        message.measurements.power_factor,
        message.measurements.frequency_hz,
        JSON.stringify(nextState)
      );

      db.run(
        `UPDATE devices
            SET state_json = ?, last_seen_at = ?, availability = 'ONLINE',
                data_source = CASE WHEN data_source = 'UNKNOWN' THEN 'DEVICE' ELSE data_source END
          WHERE device_id = ?`,
        serializeDeviceState(nextState),
        receivedAt,
        deviceId
      );

      if (previous && previous.energy_kwh_total !== null && message.measurements.energy_kwh_total !== null) {
        const delta = computeEnergyDelta(
          {
            energyKwhTotal: previous.energy_kwh_total,
            sampledAt: previous.sampled_at,
            meterId: deviceId,
            sequence: previous.sequence,
            quality: previous.quality
          },
          {
            energyKwhTotal: message.measurements.energy_kwh_total,
            sampledAt: message.sampled_at,
            meterId: deviceId,
            sequence: message.sequence,
            quality: message.quality
          }
        );
        db.run(
          `INSERT INTO energy_intervals (interval_id, device_id, start_at, end_at, delta_kwh, gap, reason_code, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
          randomUUID(),
          deviceId,
          previous.sampled_at,
          message.sampled_at,
          delta.deltaKwh,
          delta.gap ? 1 : 0,
          delta.reasonCode,
          receivedAt
        );
        applyIntervalToDailyAggregate(
          db,
          deviceId,
          previous.sampled_at,
          delta.deltaKwh,
          delta.gap,
          1,
          new Date(receivedAt),
          timeZone
        );
        if (delta.gap) {
          appendDeviceEvent(db, {
            deviceId,
            type: "ENERGY_GAP",
            severity: "WARNING",
            summary: `Data energi tidak dihitung: ${delta.reasonCode}`,
            source: "backend",
            payload: {
              reason_code: delta.reasonCode,
              previous_sequence: previous.sequence,
              current_sequence: message.sequence,
              previous_sampled_at: previous.sampled_at,
              current_sampled_at: message.sampled_at
            },
            now: new Date(receivedAt)
          });
        }
      } else {
        applyIntervalToDailyAggregate(
          db,
          deviceId,
          message.sampled_at,
          0,
          false,
          1,
          new Date(receivedAt),
          timeZone
        );
      }
    });
  } catch (error) {
    if (error instanceof Error && /UNIQUE|constraint/i.test(error.message)) {
      return {
        inserted: false,
        duplicate: true,
        gap: false,
        reasonCode: "DUPLICATE_SEQUENCE",
        sampleId: null,
        alertsFired: []
      };
    }
    throw error;
  }

  const alertsFired = evaluateTelemetryAlerts(db, deviceId, message, new Date(receivedAt), { timeZone });

  return {
    inserted: true,
    duplicate: false,
    gap: false,
    reasonCode: "OK",
    sampleId,
    alertsFired
  };
}

export function ingestState(
  db: AppDb,
  deviceId: string,
  message: StateMessage,
  receivedAt: string
): void {
  if (message.device_id !== deviceId) {
    throw new Error("STATE_DEVICE_MISMATCH");
  }
  const device = db.get<{ state_json: string }>(`SELECT state_json FROM devices WHERE device_id = ?`, deviceId);
  if (!device) {
    throw new Error("DEVICE_NOT_FOUND");
  }
  const previous = parseDeviceState(device.state_json);
  const next = stateFromMqtt(message.state, previous, receivedAt);
  db.run(
    `UPDATE devices SET state_json = ?, last_seen_at = ?, availability = 'ONLINE' WHERE device_id = ?`,
    serializeDeviceState(next),
    receivedAt,
    deviceId
  );
}

export function ingestAck(
  db: AppDb,
  deviceId: string,
  message: AckMessage,
  receivedAt: string
): void {
  if (message.device_id !== deviceId) {
    throw new Error("ACK_DEVICE_MISMATCH");
  }
  const command = db.get<{
    command_id: string;
    device_id: string;
    actor_id: string;
    requested_output: string;
    status: string;
    reason_code: string | null;
    observed_output: string | null;
    state_version: number;
  }>(
    `SELECT command_id, device_id, actor_id, requested_output, status, reason_code, observed_output, state_version
       FROM device_commands WHERE command_id = ?`,
    message.command_id
  );
  if (!command) {
    return;
  }
  if (command.device_id !== deviceId) {
    return;
  }
  db.run(
    `UPDATE device_commands
        SET status = ?, reason_code = ?, observed_output = ?, state_version = ?, updated_at = ?
      WHERE command_id = ?`,
    message.status,
    message.reason_code,
    message.observed_output,
    message.state_version,
    receivedAt,
    message.command_id
  );
  if (message.observed_output !== null) {
    const device = db.get<{ state_json: string }>(`SELECT state_json FROM devices WHERE device_id = ?`, deviceId);
    if (device) {
      const state = parseDeviceState(device.state_json);
      state.observed_output = message.observed_output;
      state.state_version = message.state_version;
      db.run(`UPDATE devices SET state_json = ? WHERE device_id = ?`, serializeDeviceState(state), deviceId);
    }
  }
  appendDeviceEvent(db, {
    deviceId,
    type: "COMMAND_ACK",
    severity: message.status === "APPLIED" ? "INFO" : "WARNING",
    summary: `Perintah ${message.command_id}: ${message.status} (${message.reason_code})`,
    source: "device",
    actorId: command.actor_id,
    correlationId: message.command_id,
    payload: {
      command_id: message.command_id,
      status: message.status,
      reason_code: message.reason_code,
      observed_output: message.observed_output,
      state_version: message.state_version
    },
    now: new Date(receivedAt)
  });
}

export function ingestAvailability(
  db: AppDb,
  deviceId: string,
  message: AvailabilityMessage,
  receivedAt: string
): void {
  if (message.device_id !== deviceId) {
    throw new Error("AVAILABILITY_DEVICE_MISMATCH");
  }
  db.run(
    `UPDATE devices SET availability = ?, last_seen_at = ? WHERE device_id = ?`,
    message.status === "online" ? "ONLINE" : "OFFLINE",
    receivedAt,
    deviceId
  );
  appendDeviceEvent(db, {
    deviceId,
    type: "AVAILABILITY_CHANGED",
    severity: message.status === "online" ? "INFO" : "WARNING",
    summary: `Perangkat ${message.status}${message.last_will ? " (last will)" : ""}`,
    source: "device",
    payload: { status: message.status, last_will: message.last_will },
    now: new Date(receivedAt)
  });
}

export function ingestDeviceEvent(
  db: AppDb,
  deviceId: string,
  message: EventMessage,
  receivedAt: string
): void {
  if (message.device_id !== deviceId) {
    throw new Error("EVENT_DEVICE_MISMATCH");
  }
  appendDeviceEvent(db, {
    deviceId,
    type: message.type,
    severity: message.severity,
    summary: message.summary,
    source: "device",
    correlationId: message.event_id,
    payload: message.payload,
    now: new Date(receivedAt)
  });
}

export function storeDiagnostics(db: AppDb, deviceId: string, payload: Record<string, unknown>, now: Date): void {
  db.run(
    `UPDATE devices SET diagnostics_json = ?, last_seen_at = ? WHERE device_id = ?`,
    JSON.stringify(payload),
    now.toISOString(),
    deviceId
  );
}

export function toTelemetrySample(row: TelemetryRow): {
  sample_id: string;
  device_id: string;
  sequence: number;
  sampled_at: string;
  received_at: string;
  quality: "VALID" | "STALE" | "INVALID";
  voltage_v: number | null;
  current_a: number | null;
  active_power_w: number | null;
  energy_kwh_total: number | null;
  power_factor: number | null;
  frequency_hz: number | null;
  state: DeviceState;
} {
  const state = parseDeviceState(row.state_json);
  return {
    sample_id: row.sample_id,
    device_id: row.device_id,
    sequence: row.sequence,
    sampled_at: row.sampled_at,
    received_at: row.received_at,
    quality: row.quality,
    voltage_v: row.voltage_v,
    current_a: row.current_a,
    active_power_w: row.active_power_w,
    energy_kwh_total: row.energy_kwh_total,
    power_factor: row.power_factor,
    frequency_hz: row.frequency_hz,
    state: {
      commanded_output: state.commanded_output,
      observed_output: state.observed_output,
      lockout: state.lockout,
      fault_code: state.fault_code,
      state_version: state.state_version,
      last_transition_at: state.last_transition_at,
      clock_valid: state.clock_valid,
      meter_valid: state.meter_valid,
      temperature_valid: state.temperature_valid
    }
  };
}
