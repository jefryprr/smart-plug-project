import type { FastifyInstance } from "fastify";
import { z } from "zod";
import { CommandRequestSchema, type DeviceDetail, type DeviceSummary } from "@smartplug/api-contract";
import { requireAuthUser } from "../auth/middleware.js";
import { appendAudit } from "../services/audit.js";
import { listDevicesForUser, requireDeviceAccess, requireWriteRole } from "../services/access.js";
import { createDeviceCommand, getDeviceCommand } from "../services/commands.js";
import { parseBody, toDeviceDetail, toDeviceSummary, type RouteDeps } from "./helpers.js";

const PatchDeviceSchema = z
  .object({
    name: z.string().min(1).max(80).optional(),
    room: z.string().max(80).nullable().optional()
  })
  .strict()
  .refine((value) => value.name !== undefined || value.room !== undefined, {
    message: "Minimal satu field harus diisi"
  });

export function registerDeviceRoutes(app: FastifyInstance, deps: RouteDeps): void {
  const { db, authenticate, publisher } = deps;

  app.get("/api/v1/devices", { preHandler: authenticate }, async (request) => {
    const user = requireAuthUser(request);
    const devices: DeviceSummary[] = listDevicesForUser(db, user.userId).map((access) =>
      toDeviceSummary(access, deps.now())
    );
    return { devices };
  });

  app.get<{ Params: { deviceId: string } }>(
    "/api/v1/devices/:deviceId",
    { preHandler: authenticate },
    async (request) => {
      const user = requireAuthUser(request);
      const access = requireDeviceAccess(db, user.userId, request.params.deviceId);
      const detail: DeviceDetail = toDeviceDetail(access, deps.now());
      return detail;
    }
  );

  app.patch<{ Params: { deviceId: string } }>(
    "/api/v1/devices/:deviceId",
    { preHandler: authenticate },
    async (request) => {
      const user = requireAuthUser(request);
      const access = requireDeviceAccess(db, user.userId, request.params.deviceId);
      requireWriteRole(access);
      const body = parseBody(PatchDeviceSchema, request.body);
      if (body.name !== undefined) {
        db.run(`UPDATE devices SET name = ? WHERE device_id = ?`, body.name, access.device_id);
      }
      if (body.room !== undefined) {
        db.run(`UPDATE devices SET room = ? WHERE device_id = ?`, body.room, access.device_id);
      }
      appendAudit(db, {
        actorId: user.userId,
        action: "device.updated",
        objectType: "device",
        objectId: access.device_id,
        metadata: { name: body.name, room: body.room },
        now: deps.now()
      });
      const updated = requireDeviceAccess(db, user.userId, access.device_id);
      return toDeviceDetail(updated, deps.now());
    }
  );

  app.post<{ Params: { deviceId: string } }>(
    "/api/v1/devices/:deviceId/commands",
    {
      preHandler: authenticate,
      config: deps.config.rateLimitEnabled ? { rateLimit: { max: 30, timeWindow: "1 minute" } } : {}
    },
    async (request, reply) => {
      const user = requireAuthUser(request);
      const access = requireDeviceAccess(db, user.userId, request.params.deviceId);
      requireWriteRole(access);
      const body = parseBody(CommandRequestSchema, request.body);
      const response = await createDeviceCommand({
        db,
        publisher,
        access,
        userId: user.userId,
        requestedOutput: body.requested_output,
        idempotencyKey: body.idempotency_key,
        ttlSeconds: body.ttl_seconds,
        reason: body.reason ?? null,
        now: deps.now()
      });
      return reply.status(202).send(response);
    }
  );

  app.get<{ Params: { deviceId: string; commandId: string } }>(
    "/api/v1/devices/:deviceId/commands/:commandId",
    { preHandler: authenticate },
    async (request) => {
      const user = requireAuthUser(request);
      requireDeviceAccess(db, user.userId, request.params.deviceId);
      return getDeviceCommand(db, user.userId, request.params.deviceId, request.params.commandId);
    }
  );
}
