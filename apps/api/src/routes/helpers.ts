import type { preHandlerHookHandler, FastifyRequest } from "fastify";
import type { z } from "zod";
import type { AppDb } from "../db/index.js";
import type { AppConfig } from "../config.js";
import type { CommandPublisher } from "../mqtt/publisher.js";
import { validationError } from "../errors.js";
import { computeFreshness } from "@smartplug/domain";
import type { DeviceDetail, DeviceSummary } from "@smartplug/api-contract";
import { parseDeviceState, type DeviceAccessRow } from "../services/access.js";

export interface RouteDeps {
  db: AppDb;
  config: AppConfig;
  publisher: CommandPublisher;
  now: () => Date;
  authenticate: preHandlerHookHandler;
}

export function parseBody<T>(schema: z.ZodType<T>, body: unknown): T {
  const result = schema.safeParse(body);
  if (!result.success) {
    throw validationError("Body permintaan tidak valid", result.error.issues);
  }
  return result.data;
}

export function parseQuery<T>(schema: z.ZodType<T>, query: unknown): T {
  const result = schema.safeParse(query);
  if (!result.success) {
    throw validationError("Query parameter tidak valid", result.error.issues);
  }
  return result.data;
}

export function validateTimeZone(timeZone: string): void {
  try {
    new Intl.DateTimeFormat("en-US", { timeZone }).format(new Date());
  } catch {
    throw validationError(`Timezone tidak valid: ${timeZone}`);
  }
}

export function toDeviceSummary(access: DeviceAccessRow, now: Date): DeviceSummary {
  const state = parseDeviceState(access.state_json);
  const freshness =
    access.availability === "OFFLINE"
      ? "OFFLINE"
      : access.last_seen_at === null
        ? "NEVER_SEEN"
        : computeFreshness(access.last_seen_at, now).status;
  return {
    device_id: access.device_id,
    name: access.name,
    room: access.room,
    availability: freshness,
    last_seen_at: access.last_seen_at,
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
    },
    firmware_version: access.firmware_version,
    data_source: access.data_source as DeviceSummary["data_source"],
    created_at: access.created_at
  };
}

export function toDeviceDetail(access: DeviceAccessRow, now: Date): DeviceDetail {
  return {
    ...toDeviceSummary(access, now),
    home_id: access.home_id,
    hardware_revision: access.hardware_revision,
    role: access.role
  };
}

export function requireNow(deps: RouteDeps): Date {
  return deps.now();
}

export function getHeader(request: FastifyRequest, name: string): string | null {
  const value = request.headers[name];
  return typeof value === "string" ? value : null;
}
