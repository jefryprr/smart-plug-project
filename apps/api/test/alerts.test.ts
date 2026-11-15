import { afterEach, beforeEach, describe, expect, it } from "vitest";
import type { TelemetryMessage } from "@smartplug/mqtt-contract";
import { createTestContext, NOW, type TestContext } from "./helpers.js";
import { ingestTelemetry } from "../src/services/telemetry.js";

let ctx: TestContext;

beforeEach(async () => {
  ctx = await createTestContext();
  ctx.db.run(`UPDATE energy_budgets SET enabled = 0 WHERE device_id = ?`, ctx.seed.deviceId);
});

afterEach(async () => {
  await ctx.app.close();
  ctx.db.close();
});

function telemetry(sequence: number, overrides: Partial<TelemetryMessage> = {}): TelemetryMessage {
  return {
    schema_version: 1,
    device_id: ctx.seed.deviceId,
    message_id: `alert-test-${sequence}`,
    sequence,
    sampled_at: new Date(NOW.getTime() + sequence * 60_000).toISOString(),
    quality: "VALID",
    measurements: {
      voltage_v: 230,
      current_a: 13.04,
      active_power_w: 3000,
      energy_kwh_total: 20 + sequence * 0.01,
      power_factor: 0.92,
      frequency_hz: 50
    },
    state: {
      commanded_output: "ON",
      observed_output: null,
      fault: null,
      lockout: false,
      state_version: sequence,
      clock_valid: true,
      meter_valid: true,
      temperature_valid: true
    },
    ...overrides
  };
}

describe("explainable telemetry alerts", () => {
  it("fires high power only after three consecutive samples and deduplicates", () => {
    const first = ingestTelemetry(
      ctx.db,
      ctx.seed.deviceId,
      telemetry(1000),
      new Date(NOW.getTime() + 60_000).toISOString(),
      "Asia/Jakarta"
    );
    const second = ingestTelemetry(
      ctx.db,
      ctx.seed.deviceId,
      telemetry(1001),
      new Date(NOW.getTime() + 120_000).toISOString(),
      "Asia/Jakarta"
    );
    const third = ingestTelemetry(
      ctx.db,
      ctx.seed.deviceId,
      telemetry(1002),
      new Date(NOW.getTime() + 180_000).toISOString(),
      "Asia/Jakarta"
    );
    expect(first.alertsFired).not.toContain("high_power");
    expect(second.alertsFired).not.toContain("high_power");
    expect(third.alertsFired).toContain("high_power");

    const fourth = ingestTelemetry(
      ctx.db,
      ctx.seed.deviceId,
      telemetry(1003),
      new Date(NOW.getTime() + 240_000).toISOString(),
      "Asia/Jakarta"
    );
    expect(fourth.alertsFired).not.toContain("high_power");

    const count = ctx.db.get<{ count: number }>(
      `SELECT COUNT(*) AS count FROM fault_events WHERE device_id = ? AND type = 'HIGH_POWER_ALERT'`,
      ctx.seed.deviceId
    );
    expect(count?.count).toBe(1);
  });

  it("fires a sensor invalid alert for an invalid meter report", () => {
    const result = ingestTelemetry(
      ctx.db,
      ctx.seed.deviceId,
      telemetry(1100, { quality: "INVALID" }),
      new Date(NOW.getTime() + 60_000).toISOString(),
      "Asia/Jakarta"
    );
    expect(result.alertsFired).toContain("sensor_invalid");
  });

  it("fires a critical alert when firmware reports OVERTEMP", () => {
    const result = ingestTelemetry(
      ctx.db,
      ctx.seed.deviceId,
      telemetry(1200, {
        state: {
          commanded_output: "OFF",
          observed_output: null,
          fault: "OVERTEMP",
          lockout: true,
          state_version: 1200,
          clock_valid: true,
          meter_valid: true,
          temperature_valid: true
        }
      }),
      new Date(NOW.getTime() + 60_000).toISOString(),
      "Asia/Jakarta"
    );
    expect(result.alertsFired).toContain("high_temperature");
    const event = ctx.db.get<{ severity: string }>(
      `SELECT severity FROM fault_events WHERE device_id = ? AND type = 'HIGH_TEMPERATURE_ALERT'`,
      ctx.seed.deviceId
    );
    expect(event?.severity).toBe("CRITICAL");
  });

  it("fires a budget alert once per period", () => {
    ctx.db.run(
      `UPDATE energy_budgets SET enabled = 1, kwh_limit = 0.001, idr_limit = NULL, period = 'monthly' WHERE device_id = ?`,
      ctx.seed.deviceId
    );
    const first = ingestTelemetry(
      ctx.db,
      ctx.seed.deviceId,
      telemetry(1300),
      new Date(NOW.getTime() + 60_000).toISOString(),
      "Asia/Jakarta"
    );
    expect(first.alertsFired).toContain("budget_crossing");

    const second = ingestTelemetry(
      ctx.db,
      ctx.seed.deviceId,
      telemetry(1301),
      new Date(NOW.getTime() + 120_000).toISOString(),
      "Asia/Jakarta"
    );
    expect(second.alertsFired).not.toContain("budget_crossing");
    const count = ctx.db.get<{ count: number }>(
      `SELECT COUNT(*) AS count FROM fault_events WHERE device_id = ? AND type = 'BUDGET_ALERT'`,
      ctx.seed.deviceId
    );
    expect(count?.count).toBe(1);
  });
});
