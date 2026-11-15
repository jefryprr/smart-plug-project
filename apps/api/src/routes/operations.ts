import type { FastifyInstance } from "fastify";
import { z } from "zod";
import type { DiagnosticsResponse, EventItem, EventsResponse } from "@smartplug/api-contract";
import { requireAuthUser } from "../auth/middleware.js";
import { appendAudit, appendDeviceEvent } from "../services/audit.js";
import { parseDeviceState, requireDeviceAccess, requireOwnerRole, requireWriteRole } from "../services/access.js";
import { sendTestNotification } from "../services/notifications.js";
import { parseBody, parseQuery, type RouteDeps } from "./helpers.js";

const EventsQuerySchema = z
  .object({
    limit: z.coerce.number().int().min(1).max(200).default(50),
    cursor: z.string().datetime().optional()
  })
  .strict();

const OtaRequestSchema = z.object({ release_id: z.string().min(1).max(80) }).strict();

interface EventRow {
  event_id: string;
  device_id: string;
  type: string;
  severity: "INFO" | "WARNING" | "CRITICAL";
  occurred_at: string;
  actor_id: string | null;
  source: string;
  correlation_id: string | null;
  summary: string;
  payload_json: string;
}

export function registerOperationsRoutes(app: FastifyInstance, deps: RouteDeps): void {
  const { db, authenticate } = deps;

  app.get<{ Params: { deviceId: string } }>(
    "/api/v1/devices/:deviceId/events",
    { preHandler: authenticate },
    async (request) => {
      const user = requireAuthUser(request);
      const access = requireDeviceAccess(db, user.userId, request.params.deviceId);
      const query = parseQuery(EventsQuerySchema, request.query);
      let sql = `SELECT event_id, device_id, type, severity, occurred_at, actor_id, source, correlation_id, summary, payload_json
                   FROM fault_events WHERE device_id = ?`;
      const params: Array<string | number> = [access.device_id];
      if (query.cursor) {
        sql += ` AND occurred_at < ?`;
        params.push(query.cursor);
      }
      sql += ` ORDER BY occurred_at DESC LIMIT ?`;
      params.push(query.limit + 1);
      const rows = db.all<EventRow>(sql, ...params);
      const hasMore = rows.length > query.limit;
      const page = hasMore ? rows.slice(0, query.limit) : rows;
      const events: EventItem[] = page.map((row) => ({
        event_id: row.event_id,
        device_id: row.device_id,
        type: row.type,
        severity: row.severity,
        occurred_at: row.occurred_at,
        actor_id: row.actor_id,
        source: row.source,
        correlation_id: row.correlation_id,
        summary: row.summary,
        payload: JSON.parse(row.payload_json) as Record<string, unknown>
      }));
      const response: EventsResponse = {
        device_id: access.device_id,
        events,
        next_cursor: hasMore && page.length > 0 ? (page[page.length - 1]?.occurred_at ?? null) : null
      };
      return response;
    }
  );

  app.get<{ Params: { deviceId: string } }>(
    "/api/v1/devices/:deviceId/diagnostics",
    { preHandler: authenticate },
    async (request) => {
      const user = requireAuthUser(request);
      const access = requireDeviceAccess(db, user.userId, request.params.deviceId);
      if (access.role === "viewer") {
        requireWriteRole(access); // throws a consistent 403
      }
      const state = parseDeviceState(access.state_json);
      let stored: Record<string, unknown> = {};
      if (access.diagnostics_json) {
        try {
          const parsed: unknown = JSON.parse(access.diagnostics_json);
          if (typeof parsed === "object" && parsed !== null) {
            stored = parsed as Record<string, unknown>;
          }
        } catch {
          stored = {};
        }
      }
      const sensorHealth = (stored.sensor_health ?? {}) as Record<string, unknown>;
      const commandCounts = (stored.command_counts ?? {}) as Record<string, unknown>;
      const response: DiagnosticsResponse = {
        device_id: access.device_id,
        firmware_version: access.firmware_version ?? (typeof stored.firmware_version === "string" ? stored.firmware_version : null),
        build_sha: typeof stored.build_sha === "string" ? stored.build_sha : null,
        uptime_seconds: typeof stored.uptime_seconds === "number" ? stored.uptime_seconds : null,
        rssi_dbm: typeof stored.rssi_dbm === "number" ? stored.rssi_dbm : null,
        heap_free_bytes: typeof stored.heap_free_bytes === "number" ? stored.heap_free_bytes : null,
        last_error: typeof stored.last_error === "string" ? stored.last_error : null,
        sensor_health: {
          meter:
            sensorHealth.meter === "OK" || sensorHealth.meter === "STALE" || sensorHealth.meter === "INVALID"
              ? sensorHealth.meter
              : state.meter_valid
                ? "OK"
                : "UNKNOWN",
          temperature:
            sensorHealth.temperature === "OK" || sensorHealth.temperature === "STALE" || sensorHealth.temperature === "INVALID"
              ? sensorHealth.temperature
              : state.temperature_valid
                ? "OK"
                : "UNKNOWN",
          relay_feedback:
            sensorHealth.relay_feedback === "OK" || sensorHealth.relay_feedback === "MISMATCH"
              ? sensorHealth.relay_feedback
              : "NOT_INSTALLED"
        },
        wifi_state:
          stored.wifi_state === "CONNECTED" || stored.wifi_state === "DISCONNECTED" || stored.wifi_state === "PROVISIONING"
            ? stored.wifi_state
            : "UNKNOWN",
        command_counts: {
          accepted: typeof commandCounts.accepted === "number" ? commandCounts.accepted : 0,
          rejected: typeof commandCounts.rejected === "number" ? commandCounts.rejected : 0,
          expired: typeof commandCounts.expired === "number" ? commandCounts.expired : 0
        },
        checked_at: deps.now().toISOString()
      };
      return response;
    }
  );

  app.post<{ Params: { deviceId: string } }>(
    "/api/v1/devices/:deviceId/notifications/test",
    {
      preHandler: authenticate,
      config: deps.config.rateLimitEnabled ? { rateLimit: { max: 2, timeWindow: "1 minute" } } : {}
    },
    async (request, reply) => {
      const user = requireAuthUser(request);
      const access = requireDeviceAccess(db, user.userId, request.params.deviceId);
      requireWriteRole(access);
      const result = await sendTestNotification(db, deps.config, user.userId, access.device_id, deps.now());
      return reply.status(202).send(result);
    }
  );

  app.post<{ Params: { deviceId: string } }>(
    "/api/v1/devices/:deviceId/ota",
    { preHandler: authenticate },
    async (request, reply) => {
      const user = requireAuthUser(request);
      const access = requireDeviceAccess(db, user.userId, request.params.deviceId);
      requireWriteRole(access);
      const body = parseBody(OtaRequestSchema, request.body);
      const eventId = appendDeviceEvent(db, {
        deviceId: access.device_id,
        type: "OTA_REQUESTED",
        severity: "INFO",
        summary: `Permintaan OTA untuk rilis ${body.release_id}; belum dikirim ke perangkat`,
        source: "cloud_api",
        actorId: user.userId,
        payload: { release_id: body.release_id, delivery: "NOT_IMPLEMENTED" },
        now: deps.now()
      });
      appendAudit(db, {
        actorId: user.userId,
        action: "ota.requested",
        objectType: "device",
        objectId: access.device_id,
        metadata: { release_id: body.release_id, event_id: eventId },
        now: deps.now()
      });
      return reply.status(202).send({ command_id: eventId, status: "PENDING" });
    }
  );

  app.post<{ Params: { deviceId: string } }>(
    "/api/v1/devices/:deviceId/revoke",
    { preHandler: authenticate },
    async (request, reply) => {
      const user = requireAuthUser(request);
      const access = requireDeviceAccess(db, user.userId, request.params.deviceId);
      requireOwnerRole(access);
      db.transaction(() => {
        db.run(
          `UPDATE device_credentials SET revoked_at = ? WHERE device_id = ? AND revoked_at IS NULL`,
          deps.now().toISOString(),
          access.device_id
        );
        db.run(`DELETE FROM device_claims WHERE device_id = ?`, access.device_id);
        appendDeviceEvent(db, {
          deviceId: access.device_id,
          type: "OWNERSHIP_REVOKED",
          severity: "WARNING",
          summary: "Akses perangkat dicabut oleh owner; inspeksi fisik tetap diperlukan",
          source: "cloud_api",
          actorId: user.userId,
          payload: {},
          now: deps.now()
        });
        appendAudit(db, {
          actorId: user.userId,
          action: "device.revoked",
          objectType: "device",
          objectId: access.device_id,
          now: deps.now()
        });
      });
      return reply.status(204).send();
    }
  );
}
