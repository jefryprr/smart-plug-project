import type { FastifyInstance } from "fastify";
import { z } from "zod";
import type { AnalyticsResponse, TelemetryListResponse } from "@smartplug/api-contract";
import { requireAuthUser } from "../auth/middleware.js";
import { requireDeviceAccess } from "../services/access.js";
import { getAnalytics } from "../services/energy.js";
import { toTelemetrySample, type TelemetryRow } from "../services/telemetry.js";
import { parseQuery, validateTimeZone, type RouteDeps } from "./helpers.js";

const TelemetryQuerySchema = z
  .object({
    from: z.string().datetime().optional(),
    to: z.string().datetime().optional(),
    limit: z.coerce.number().int().min(1).max(500).default(100),
    cursor: z.string().datetime().optional()
  })
  .strict();

const AnalyticsQuerySchema = z
  .object({
    from: z.string().datetime(),
    to: z.string().datetime(),
    granularity: z.enum(["hour", "day", "week", "month"]).default("day"),
    timezone: z.string().min(1).max(64).optional()
  })
  .strict();

export function registerTelemetryRoutes(app: FastifyInstance, deps: RouteDeps): void {
  const { db, authenticate } = deps;

  app.get<{ Params: { deviceId: string } }>(
    "/api/v1/devices/:deviceId/telemetry",
    { preHandler: authenticate },
    async (request) => {
      const user = requireAuthUser(request);
      const access = requireDeviceAccess(db, user.userId, request.params.deviceId);
      const query = parseQuery(TelemetryQuerySchema, request.query);

      let sql = `SELECT * FROM telemetry_samples WHERE device_id = ?`;
      const params: Array<string | number> = [access.device_id];
      if (query.from) {
        sql += ` AND sampled_at >= ?`;
        params.push(query.from);
      }
      if (query.to) {
        sql += ` AND sampled_at <= ?`;
        params.push(query.to);
      }
      if (query.cursor) {
        sql += ` AND sampled_at < ?`;
        params.push(query.cursor);
      }
      sql += ` ORDER BY sampled_at DESC LIMIT ?`;
      params.push(query.limit + 1);

      const rows = db.all<TelemetryRow>(sql, ...params);
      const hasMore = rows.length > query.limit;
      const page = hasMore ? rows.slice(0, query.limit) : rows;
      const response: TelemetryListResponse = {
        device_id: access.device_id,
        samples: page.map(toTelemetrySample),
        next_cursor: hasMore && page.length > 0 ? (page[page.length - 1]?.sampled_at ?? null) : null,
        data_available: page.length > 0
      };
      return response;
    }
  );

  app.get<{ Params: { deviceId: string } }>(
    "/api/v1/devices/:deviceId/analytics",
    { preHandler: authenticate },
    async (request) => {
      const user = requireAuthUser(request);
      const access = requireDeviceAccess(db, user.userId, request.params.deviceId);
      const query = parseQuery(AnalyticsQuerySchema, request.query);
      const timeZone = query.timezone ?? deps.config.defaultTimeZone;
      validateTimeZone(timeZone);
      const response: AnalyticsResponse = getAnalytics(db, access.device_id, {
        from: query.from,
        to: query.to,
        granularity: query.granularity,
        timeZone
      });
      return response;
    }
  );
}
