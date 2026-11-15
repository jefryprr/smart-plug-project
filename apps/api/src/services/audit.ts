import { randomUUID } from "node:crypto";
import type { AppDb } from "../db/index.js";

export interface AuditInput {
  actorId: string | null;
  action: string;
  objectType: string;
  objectId: string;
  correlationId?: string | null;
  metadata?: Record<string, unknown>;
  now?: Date;
}

export function appendAudit(db: AppDb, input: AuditInput): string {
  const eventId = randomUUID();
  const now = input.now ?? new Date();
  db.run(
    `INSERT INTO audit_events (event_id, actor_id, action, object_type, object_id, correlation_id, created_at, metadata_json)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
    eventId,
    input.actorId,
    input.action,
    input.objectType,
    input.objectId,
    input.correlationId ?? null,
    now.toISOString(),
    JSON.stringify(input.metadata ?? {})
  );
  return eventId;
}

export interface DeviceEventInput {
  deviceId: string;
  type: string;
  severity: "INFO" | "WARNING" | "CRITICAL";
  summary: string;
  source: string;
  actorId?: string | null;
  correlationId?: string | null;
  payload?: Record<string, unknown>;
  now?: Date;
}

export function appendDeviceEvent(db: AppDb, input: DeviceEventInput): string {
  const eventId = randomUUID();
  const now = input.now ?? new Date();
  db.run(
    `INSERT INTO fault_events (event_id, device_id, type, severity, occurred_at, actor_id, source, correlation_id, summary, payload_json)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
    eventId,
    input.deviceId,
    input.type,
    input.severity,
    now.toISOString(),
    input.actorId ?? null,
    input.source,
    input.correlationId ?? null,
    input.summary,
    JSON.stringify(input.payload ?? {})
  );
  return eventId;
}
