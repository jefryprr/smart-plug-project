import { randomUUID } from "node:crypto";
import type { FastifyInstance } from "fastify";
import { z } from "zod";
import {
  AutomationsRequestSchema,
  BudgetRequestSchema,
  TariffRequestSchema,
  type AutomationsResponse,
  type Budget,
  type Schedule,
  type Tariff
} from "@smartplug/api-contract";
import { requireAuthUser } from "../auth/middleware.js";
import { conflict } from "../errors.js";
import { appendAudit } from "../services/audit.js";
import { requireDeviceAccess, requireWriteRole } from "../services/access.js";
import { addTariff, listTariffs, type TariffRow } from "../services/energy.js";
import { parseBody, validateTimeZone, type RouteDeps } from "./helpers.js";

const BudgetRowSchema = z
  .object({
    budget_id: z.string(),
    period: z.enum(["daily", "weekly", "monthly"]),
    kwh_limit: z.number().nullable(),
    idr_limit: z.number().nullable(),
    enabled: z.number(),
    updated_at: z.string()
  })
  .strict();

export function registerAutomationRoutes(app: FastifyInstance, deps: RouteDeps): void {
  const { db, authenticate } = deps;

  app.get<{ Params: { deviceId: string } }>(
    "/api/v1/devices/:deviceId/tariff",
    { preHandler: authenticate },
    async (request) => {
      const user = requireAuthUser(request);
      const access = requireDeviceAccess(db, user.userId, request.params.deviceId);
      const tariffs: Tariff[] = listTariffs(db, access.device_id).map((row: TariffRow) => ({
        tariff_id: row.tariff_id,
        currency: "IDR",
        idr_per_kwh: row.idr_per_kwh,
        effective_from: row.effective_from,
        effective_to: row.effective_to,
        created_at: row.created_at
      }));
      return { device_id: access.device_id, tariffs };
    }
  );

  app.put<{ Params: { deviceId: string } }>(
    "/api/v1/devices/:deviceId/tariff",
    { preHandler: authenticate },
    async (request, reply) => {
      const user = requireAuthUser(request);
      const access = requireDeviceAccess(db, user.userId, request.params.deviceId);
      requireWriteRole(access);
      const body = parseBody(TariffRequestSchema, request.body);
      const created = addTariff(db, access.device_id, body.idr_per_kwh, body.effective_from, deps.now());
      appendAudit(db, {
        actorId: user.userId,
        action: "tariff.created",
        objectType: "device",
        objectId: access.device_id,
        metadata: { tariff_id: created.tariff_id, idr_per_kwh: created.idr_per_kwh, effective_from: created.effective_from },
        now: deps.now()
      });
      const response: Tariff = {
        tariff_id: created.tariff_id,
        currency: "IDR",
        idr_per_kwh: created.idr_per_kwh,
        effective_from: created.effective_from,
        effective_to: created.effective_to,
        created_at: created.created_at
      };
      return reply.status(201).send(response);
    }
  );

  app.get<{ Params: { deviceId: string } }>(
    "/api/v1/devices/:deviceId/budget",
    { preHandler: authenticate },
    async (request) => {
      const user = requireAuthUser(request);
      const access = requireDeviceAccess(db, user.userId, request.params.deviceId);
      const row = db.get<z.infer<typeof BudgetRowSchema>>(
        `SELECT budget_id, period, kwh_limit, idr_limit, enabled, updated_at FROM energy_budgets WHERE device_id = ?`,
        access.device_id
      );
      const budget: Budget = row
        ? {
            budget_id: row.budget_id,
            period: row.period,
            kwh_limit: row.kwh_limit,
            idr_limit: row.idr_limit,
            enabled: row.enabled === 1,
            updated_at: row.updated_at
          }
        : {
            budget_id: "unset",
            period: "monthly",
            kwh_limit: null,
            idr_limit: null,
            enabled: false,
            updated_at: deps.now().toISOString()
          };
      return budget;
    }
  );

  app.put<{ Params: { deviceId: string } }>(
    "/api/v1/devices/:deviceId/budget",
    { preHandler: authenticate },
    async (request) => {
      const user = requireAuthUser(request);
      const access = requireDeviceAccess(db, user.userId, request.params.deviceId);
      requireWriteRole(access);
      const body = parseBody(BudgetRequestSchema, request.body);
      const existing = db.get<{ budget_id: string }>(
        `SELECT budget_id FROM energy_budgets WHERE device_id = ?`,
        access.device_id
      );
      const budgetId = existing?.budget_id ?? randomUUID();
      db.run(
        `INSERT INTO energy_budgets (budget_id, device_id, period, kwh_limit, idr_limit, enabled, updated_at)
         VALUES (?, ?, ?, ?, ?, ?, ?)
         ON CONFLICT(device_id) DO UPDATE SET
           period = excluded.period,
           kwh_limit = excluded.kwh_limit,
           idr_limit = excluded.idr_limit,
           enabled = excluded.enabled,
           updated_at = excluded.updated_at`,
        budgetId,
        access.device_id,
        body.period,
        body.kwh_limit ?? null,
        body.idr_limit ?? null,
        body.enabled ? 1 : 0,
        deps.now().toISOString()
      );
      appendAudit(db, {
        actorId: user.userId,
        action: "budget.updated",
        objectType: "device",
        objectId: access.device_id,
        metadata: { period: body.period, enabled: body.enabled },
        now: deps.now()
      });
      const row = db.get<z.infer<typeof BudgetRowSchema>>(
        `SELECT budget_id, period, kwh_limit, idr_limit, enabled, updated_at FROM energy_budgets WHERE device_id = ?`,
        access.device_id
      );
      if (!row) throw new Error("BUDGET_UPSERT_FAILED");
      const response: Budget = {
        budget_id: row.budget_id,
        period: row.period,
        kwh_limit: row.kwh_limit,
        idr_limit: row.idr_limit,
        enabled: row.enabled === 1,
        updated_at: row.updated_at
      };
      return response;
    }
  );

  app.get<{ Params: { deviceId: string } }>(
    "/api/v1/devices/:deviceId/automations",
    { preHandler: authenticate },
    async (request) => {
      const user = requireAuthUser(request);
      const access = requireDeviceAccess(db, user.userId, request.params.deviceId);
      const row = db.get<{ version: number; schedules_json: string }>(
        `SELECT version, schedules_json FROM automation_rules WHERE device_id = ?`,
        access.device_id
      );
      const schedules = row ? (JSON.parse(row.schedules_json) as Schedule[]) : [];
      const response: AutomationsResponse = {
        device_id: access.device_id,
        schedules,
        version: row?.version ?? 0
      };
      return response;
    }
  );

  app.put<{ Params: { deviceId: string } }>(
    "/api/v1/devices/:deviceId/automations",
    { preHandler: authenticate },
    async (request) => {
      const user = requireAuthUser(request);
      const access = requireDeviceAccess(db, user.userId, request.params.deviceId);
      requireWriteRole(access);
      const body = parseBody(AutomationsRequestSchema, request.body);
      const current = db.get<{ version: number }>(
        `SELECT version FROM automation_rules WHERE device_id = ?`,
        access.device_id
      );
      if ((current?.version ?? 0) !== body.version) {
        throw conflict("AUTOMATION_VERSION_CONFLICT", "Versi jadwal berubah; muat ulang sebelum menyimpan");
      }
      const schedules: Schedule[] = body.schedules.map((schedule) => {
        validateTimeZone(schedule.time_zone);
        if (new Set(schedule.days).size !== schedule.days.length) {
          throw conflict("DUPLICATE_SCHEDULE_DAY", "Hari jadwal tidak boleh duplikat");
        }
        return {
          schedule_id: schedule.schedule_id ?? randomUUID(),
          days: [...schedule.days].sort((a, b) => a - b),
          start_time: schedule.start_time,
          duration_minutes: schedule.duration_minutes,
          action: schedule.action,
          time_zone: schedule.time_zone,
          enabled: schedule.enabled
        };
      });
      const nextVersion = (current?.version ?? 0) + 1;
      db.run(
        `INSERT INTO automation_rules (device_id, version, schedules_json, updated_at)
         VALUES (?, ?, ?, ?)
         ON CONFLICT(device_id) DO UPDATE SET
           version = excluded.version,
           schedules_json = excluded.schedules_json,
           updated_at = excluded.updated_at`,
        access.device_id,
        nextVersion,
        JSON.stringify(schedules),
        deps.now().toISOString()
      );
      appendAudit(db, {
        actorId: user.userId,
        action: "automations.updated",
        objectType: "device",
        objectId: access.device_id,
        metadata: { version: nextVersion, schedule_count: schedules.length },
        now: deps.now()
      });
      const response: AutomationsResponse = {
        device_id: access.device_id,
        schedules,
        version: nextVersion
      };
      return response;
    }
  );
}
