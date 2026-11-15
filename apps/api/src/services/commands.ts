import { randomUUID } from "node:crypto";
import type { CommandResponse } from "@smartplug/api-contract";
import { decideOutputCommand, type DeviceSafetySnapshot } from "@smartplug/domain";
import type { CommandMessage } from "@smartplug/mqtt-contract";
import type { AppDb } from "../db/index.js";
import { conflict, downstreamUnavailable, notFound } from "../errors.js";
import { sha256 } from "../auth/password.js";
import type { DeviceAccessRow } from "./access.js";
import { parseDeviceState } from "./access.js";
import { appendAudit, appendDeviceEvent } from "./audit.js";
import type { CommandPublisher } from "../mqtt/publisher.js";

export interface CommandRow {
  command_id: string;
  device_id: string;
  actor_id: string;
  requested_output: "ON" | "OFF";
  status: CommandResponse["status"];
  source: string;
  idempotency_key: string;
  sequence: number;
  issued_at: string;
  expires_at: string;
  accepted_at: string;
  updated_at: string;
  reason_code: string | null;
  reason: string | null;
  observed_output: "ON" | "OFF" | null;
  state_version: number;
  correlation_id: string;
}

function messageForStatus(status: CommandResponse["status"]): string {
  switch (status) {
    case "PENDING":
      return "Perintah diterima; menunggu pengiriman";
    case "ACCEPTED":
      return "Perintah diterima; menunggu ACK perangkat";
    case "DELIVERED":
      return "Perintah terkirim ke broker; menunggu ACK perangkat";
    case "APPLIED":
      return "Perangkat melaporkan perintah diterapkan";
    case "REJECTED":
      return "Perangkat menolak perintah";
    case "EXPIRED":
      return "Perintah kedaluwarsa sebelum dieksekusi";
    case "TIMEOUT":
      return "Tidak ada ACK dari perangkat dalam batas waktu";
  }
}

export function toCommandResponse(row: CommandRow, idempotentReplay = false): CommandResponse {
  return {
    command_id: row.command_id,
    device_id: row.device_id,
    requested_output: row.requested_output,
    status: row.status,
    accepted_at: row.accepted_at,
    expires_at: row.expires_at,
    state_version: row.state_version,
    observed_output: row.observed_output,
    message: messageForStatus(row.status),
    idempotent_replay: idempotentReplay
  };
}

function getCommandRow(db: AppDb, commandId: string): CommandRow | null {
  const row = db.get<CommandRow>(
    `SELECT command_id, device_id, actor_id, requested_output, status, source, idempotency_key,
            sequence, issued_at, expires_at, accepted_at, updated_at, reason_code, reason,
            observed_output, state_version, correlation_id
       FROM device_commands WHERE command_id = ?`,
    commandId
  );
  return row ?? null;
}

function safetySnapshot(access: DeviceAccessRow, db: AppDb): DeviceSafetySnapshot {
  const state = parseDeviceState(access.state_json);
  const last = db.get<{ sequence: number; command_id: string }>(
    `SELECT sequence, command_id FROM device_commands WHERE device_id = ? ORDER BY sequence DESC LIMIT 1`,
    access.device_id
  );
  const mode = state.lockout || state.fault_code
    ? "FAULT_LOCKOUT"
    : !state.meter_valid || !state.temperature_valid
      ? "DEGRADED"
      : state.commanded_output === "ON"
        ? "READY_ON"
        : "READY_OFF";
  return {
    deviceId: access.device_id,
    mode,
    commandedOutput: state.commanded_output,
    observedOutput: state.observed_output,
    lockout: state.lockout,
    faultCode: state.fault_code,
    clockValid: state.clock_valid,
    meterValid: state.meter_valid,
    temperatureValid: state.temperature_valid,
    lastCommandSequence: last?.sequence ?? 0,
    lastCommandId: last?.command_id ?? null,
    stateVersion: state.state_version
  };
}

export interface CreateCommandInput {
  db: AppDb;
  publisher: CommandPublisher;
  access: DeviceAccessRow;
  userId: string;
  requestedOutput: "ON" | "OFF";
  idempotencyKey: string;
  ttlSeconds: number;
  reason: string | null;
  now: Date;
}

export async function createDeviceCommand(input: CreateCommandInput): Promise<CommandResponse> {
  const { db, publisher, access, userId, requestedOutput, idempotencyKey, ttlSeconds, reason, now } = input;
  const scope = `device-command:${userId}:${access.device_id}`;
  const requestHash = sha256(JSON.stringify({ device_id: access.device_id, requested_output: requestedOutput }));

  const existingKey = db.get<{ command_id: string; request_hash: string }>(
    `SELECT command_id, request_hash FROM idempotency_keys WHERE scope = ? AND key = ?`,
    scope,
    idempotencyKey
  );

  if (existingKey) {
    if (existingKey.request_hash !== requestHash) {
      throw conflict("IDEMPOTENCY_CONFLICT", "Idempotency key sudah dipakai untuk permintaan berbeda");
    }
    const existing = getCommandRow(db, existingKey.command_id);
    if (existing) {
      if (["PENDING", "ACCEPTED", "DELIVERED", "APPLIED"].includes(existing.status)) {
        return toCommandResponse(existing, true);
      }
      db.run(`DELETE FROM idempotency_keys WHERE scope = ? AND key = ?`, scope, idempotencyKey);
    }
  }

  const snapshot = safetySnapshot(access, db);
  const commandId = randomUUID();
  const correlationId = randomUUID();
  const sequence = snapshot.lastCommandSequence + 1;
  const issuedAt = now.toISOString();
  const expiresAt = new Date(now.getTime() + ttlSeconds * 1000).toISOString();

  const decision = decideOutputCommand(
    snapshot,
    {
      commandId,
      deviceId: access.device_id,
      requestedOutput,
      source: "cloud_api",
      issuedAt,
      expiresAt,
      sequence,
      actorId: userId,
      reason
    },
    now
  );

  if (!decision.accepted) {
    db.run(
      `INSERT INTO device_commands
        (command_id, device_id, actor_id, requested_output, status, source, idempotency_key, sequence,
         issued_at, expires_at, accepted_at, updated_at, reason_code, reason, observed_output, state_version, correlation_id)
       VALUES (?, ?, ?, ?, 'REJECTED', 'cloud_api', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      commandId,
      access.device_id,
      userId,
      requestedOutput,
      idempotencyKey,
      sequence,
      issuedAt,
      expiresAt,
      issuedAt,
      issuedAt,
      decision.reasonCode,
      decision.reason,
      snapshot.observedOutput,
      snapshot.stateVersion,
      correlationId
    );
    appendDeviceEvent(db, {
      deviceId: access.device_id,
      type: "COMMAND_REJECTED",
      severity: requestedOutput === "ON" ? "WARNING" : "INFO",
      summary: `Perintah ${requestedOutput} ditolak: ${decision.reason}`,
      source: "cloud_api",
      actorId: userId,
      correlationId: commandId,
      payload: {
        command_id: commandId,
        requested_output: requestedOutput,
        reason_code: decision.reasonCode,
        lockout: snapshot.lockout,
        fault_code: snapshot.faultCode
      },
      now
    });
    appendAudit(db, {
      actorId: userId,
      action: "command.rejected",
      objectType: "device",
      objectId: access.device_id,
      correlationId: commandId,
      metadata: { requested_output: requestedOutput, reason_code: decision.reasonCode },
      now
    });
    throw conflict("COMMAND_REJECTED", decision.reason, {
      command_id: commandId,
      reason_code: decision.reasonCode
    });
  }

  db.transaction(() => {
    db.run(
      `INSERT INTO device_commands
        (command_id, device_id, actor_id, requested_output, status, source, idempotency_key, sequence,
         issued_at, expires_at, accepted_at, updated_at, reason_code, reason, observed_output, state_version, correlation_id)
       VALUES (?, ?, ?, ?, 'PENDING', 'cloud_api', ?, ?, ?, ?, ?, ?, NULL, ?, ?, ?, ?)`,
      commandId,
      access.device_id,
      userId,
      requestedOutput,
      idempotencyKey,
      sequence,
      issuedAt,
      expiresAt,
      issuedAt,
      issuedAt,
      reason,
      snapshot.observedOutput,
      snapshot.stateVersion,
      correlationId
    );
    db.run(
      `INSERT INTO idempotency_keys (scope, key, command_id, request_hash, created_at)
       VALUES (?, ?, ?, ?, ?)`,
      scope,
      idempotencyKey,
      commandId,
      requestHash,
      issuedAt
    );
    appendDeviceEvent(db, {
      deviceId: access.device_id,
      type: "COMMAND_ACCEPTED",
      severity: "INFO",
      summary: `Perintah ${requestedOutput} diterima untuk dikirim`,
      source: "cloud_api",
      actorId: userId,
      correlationId: commandId,
      payload: {
        command_id: commandId,
        requested_output: requestedOutput,
        sequence,
        expires_at: expiresAt
      },
      now
    });
    appendAudit(db, {
      actorId: userId,
      action: "command.accepted",
      objectType: "device",
      objectId: access.device_id,
      correlationId: commandId,
      metadata: { requested_output: requestedOutput, sequence },
      now
    });
  });

  const commandMessage: CommandMessage = {
    schema_version: 1,
    command_id: commandId,
    device_id: access.device_id,
    issued_at: issuedAt,
    expires_at: expiresAt,
    actor_id: userId,
    requested_output: requestedOutput,
    source: "cloud_api",
    correlation_id: correlationId,
    sequence
  };

  try {
    await publisher.publishCommand(commandMessage);
  } catch {
    db.run(
      `UPDATE device_commands SET status = 'TIMEOUT', reason_code = 'BROKER_UNAVAILABLE', updated_at = ? WHERE command_id = ?`,
      new Date().toISOString(),
      commandId
    );
    appendDeviceEvent(db, {
      deviceId: access.device_id,
      type: "COMMAND_PUBLISH_FAILED",
      severity: "WARNING",
      summary: "Perintah gagal dipublikasikan ke broker",
      source: "backend",
      actorId: userId,
      correlationId: commandId,
      payload: { command_id: commandId },
      now: new Date()
    });
    throw downstreamUnavailable("Broker MQTT tidak tersedia; perintah tidak diklaim terkirim");
  }

  db.run(
    `UPDATE device_commands SET status = 'ACCEPTED', updated_at = ? WHERE command_id = ?`,
    new Date().toISOString(),
    commandId
  );

  const created = getCommandRow(db, commandId);
  if (!created) {
    throw new Error("COMMAND_INSERT_FAILED");
  }
  return toCommandResponse(created, false);
}

export function getDeviceCommand(db: AppDb, userId: string, deviceId: string, commandId: string): CommandResponse {
  const row = db.get<CommandRow>(
    `SELECT c.command_id, c.device_id, c.actor_id, c.requested_output, c.status, c.source, c.idempotency_key,
            c.sequence, c.issued_at, c.expires_at, c.accepted_at, c.updated_at, c.reason_code, c.reason,
            c.observed_output, c.state_version, c.correlation_id
       FROM device_commands c
       JOIN memberships m ON m.home_id = (SELECT home_id FROM devices WHERE device_id = c.device_id)
      WHERE c.command_id = ? AND c.device_id = ? AND m.user_id = ?`,
    commandId,
    deviceId,
    userId
  );
  if (!row) {
    throw notFound("Perintah tidak ditemukan");
  }
  return toCommandResponse(row);
}

export function expireStaleCommands(db: AppDb, now: Date = new Date()): number {
  const rows = db.all<CommandRow>(
    `SELECT command_id, device_id, actor_id, requested_output, status, source, idempotency_key,
            sequence, issued_at, expires_at, accepted_at, updated_at, reason_code, reason,
            observed_output, state_version, correlation_id
       FROM device_commands
      WHERE status IN ('PENDING', 'ACCEPTED', 'DELIVERED') AND expires_at < ?`,
    now.toISOString()
  );
  for (const row of rows) {
    db.run(
      `UPDATE device_commands SET status = 'EXPIRED', reason_code = 'TTL_EXPIRED', updated_at = ? WHERE command_id = ?`,
      now.toISOString(),
      row.command_id
    );
    appendDeviceEvent(db, {
      deviceId: row.device_id,
      type: "COMMAND_EXPIRED",
      severity: "WARNING",
      summary: `Perintah ${row.command_id} kedaluwarsa tanpa ACK`,
      source: "backend",
      actorId: row.actor_id,
      correlationId: row.command_id,
      payload: { requested_output: row.requested_output, expires_at: row.expires_at },
      now
    });
  }
  return rows.length;
}
