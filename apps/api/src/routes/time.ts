import type { FastifyInstance } from "fastify";
import { randomUUID } from "node:crypto";
import { ManualTimeRequestSchema, TimeStatusResponseSchema, type ManualTimeResponse } from "@smartplug/api-contract";
import type { TimeMessage } from "@smartplug/mqtt-contract";
import { requireAuthUser } from "../auth/middleware.js";
import { appendAudit, appendDeviceEvent } from "../services/audit.js";
import { parseDeviceState, requireDeviceAccess, requireWriteRole, serializeDeviceState } from "../services/access.js";
import { validationError } from "../errors.js";
import { parseBody, requireNow, validateTimeZone, type RouteDeps } from "./helpers.js";

const MIN_UTC_MS = Date.parse("2020-01-01T00:00:00.000Z");
const MAX_UTC_MS = Date.parse("2100-01-01T00:00:00.000Z");

export function registerTimeRoutes(app: FastifyInstance, deps: RouteDeps): void {
  const { db, authenticate, publisher } = deps;

  app.get("/api/v1/time", { preHandler: authenticate }, async () => {
    const now = requireNow(deps);
    return TimeStatusResponseSchema.parse({
      server_time: now.toISOString(),
      timezone: deps.config.defaultTimeZone,
      time_valid: true,
      time_source: "api",
      last_sync: now.toISOString(),
      time_age_s: 0
    });
  });

  app.post<{ Params: { deviceId: string } }>(
    "/api/v1/devices/:deviceId/time",
    {
      preHandler: authenticate,
      config: deps.config.rateLimitEnabled ? { rateLimit: { max: 10, timeWindow: "1 minute" } } : {}
    },
    async (request) => {
      const user = requireAuthUser(request);
      const access = requireDeviceAccess(db, user.userId, request.params.deviceId);
      requireWriteRole(access);
      const body = parseBody(ManualTimeRequestSchema, request.body);
      validateTimeZone(body.timezone);

      const utcMs = Date.parse(body.utc);
      if (!Number.isFinite(utcMs) || utcMs < MIN_UTC_MS || utcMs >= MAX_UTC_MS) {
        throw validationError("UTC time tidak masuk akal");
      }

      const now = requireNow(deps);
      const state = parseDeviceState(access.state_json);
      const nextState = {
        ...state,
        clock_valid: true,
        time_valid: true,
        time_source: "manual" as const,
        last_sync: now.toISOString(),
        last_known_time: new Date(utcMs).toISOString(),
        time_age_s: 0
      };
      db.run(`UPDATE devices SET state_json = ? WHERE device_id = ?`, serializeDeviceState(nextState), access.device_id);

      appendAudit(db, {
        actorId: user.userId,
        action: "time.set.manual",
        objectType: "device",
        objectId: access.device_id,
        metadata: { utc: new Date(utcMs).toISOString(), timezone: body.timezone },
        now
      });
      appendDeviceEvent(db, {
        deviceId: access.device_id,
        type: "TIME_SET_MANUAL",
        severity: "INFO",
        summary: "Waktu perangkat diset manual oleh owner/admin",
        source: "api",
        actorId: user.userId,
        payload: { utc: new Date(utcMs).toISOString(), timezone: body.timezone },
        now
      });

      const message: TimeMessage = {
        schema_version: 1,
        device_id: access.device_id,
        utc: new Date(utcMs).toISOString(),
        source: "manual",
        request_id: `time-${randomUUID()}`
      };
      let mqttDelivered = false;
      try {
        await publisher.publishTime(message);
        mqttDelivered = true;
      } catch {
        // Manual set is still persisted/audited; delivery is reported honestly.
      }

      const response: ManualTimeResponse = {
        device_id: access.device_id,
        utc: message.utc,
        timezone: body.timezone,
        time_source: "manual",
        accepted_at: now.toISOString(),
        mqtt_delivered: mqttDelivered
      };
      return response;
    }
  );
}
