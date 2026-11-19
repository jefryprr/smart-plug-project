import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { createTestContext, createUserWithRole, setDeviceState, NOW, type TestContext } from "./helpers.js";

let ctx: TestContext;

beforeEach(async () => {
  ctx = await createTestContext();
});

afterEach(async () => {
  await ctx.app.close();
  ctx.db.close();
});

describe("time service API", () => {
  it("returns server time for fallback", async () => {
    const token = await ctx.login();
    const response = await ctx.app.inject({ method: "GET", url: "/api/v1/time", headers: ctx.auth(token) });
    expect(response.statusCode).toBe(200);
    const body = response.json();
    expect(body.time_source).toBe("api");
    expect(body.time_valid).toBe(true);
    expect(body.timezone).toBe("Asia/Jakarta");
  });

  it("sets manual time, audits it, and publishes the MQTT time message", async () => {
    const token = await ctx.login();
    const response = await ctx.app.inject({
      method: "POST",
      url: `/api/v1/devices/${ctx.seed.deviceId}/time`,
      headers: ctx.auth(token),
      payload: { utc: "2026-11-19T10:00:00.000Z", timezone: "Asia/Jakarta" }
    });
    expect(response.statusCode).toBe(200);
    expect(response.json().time_source).toBe("manual");
    expect(response.json().mqtt_delivered).toBe(true);
    expect(ctx.publisher.timeMessages).toHaveLength(1);
    expect(ctx.publisher.timeMessages[0]?.utc).toBe("2026-11-19T10:00:00.000Z");

    const event = ctx.db.get<{ action: string }>(
      `SELECT action FROM audit_events WHERE action = 'time.set.manual' ORDER BY created_at DESC LIMIT 1`
    );
    expect(event?.action).toBe("time.set.manual");

    const state = ctx.db.get<{ state_json: string }>(
      `SELECT state_json FROM devices WHERE device_id = ?`,
      ctx.seed.deviceId
    );
    const parsed = JSON.parse(state?.state_json ?? "{}");
    expect(parsed.time_valid).toBe(true);
    expect(parsed.time_source).toBe("manual");
    expect(parsed.last_sync).toBe(NOW.toISOString());
  });

  it("forbids a viewer from manual time set", async () => {
    createUserWithRole(ctx.db, "viewer-time@example.com", "viewer1234", ctx.seed.homeId, "viewer");
    const token = await ctx.login("viewer-time@example.com", "viewer1234");
    const response = await ctx.app.inject({
      method: "POST",
      url: `/api/v1/devices/${ctx.seed.deviceId}/time`,
      headers: ctx.auth(token),
      payload: { utc: "2026-11-19T10:00:00.000Z", timezone: "Asia/Jakarta" }
    });
    expect(response.statusCode).toBe(403);
    expect(ctx.publisher.timeMessages).toHaveLength(0);
  });

  it("rejects enabling a schedule when time is invalid", async () => {
    const token = await ctx.login();
    setDeviceState(ctx.db, ctx.seed.deviceId, { time_valid: false, clock_valid: false, time_source: "none" });
    const response = await ctx.app.inject({
      method: "PUT",
      url: `/api/v1/devices/${ctx.seed.deviceId}/automations`,
      headers: ctx.auth(token),
      payload: {
        version: 0,
        schedules: [{
          schedule_id: "schedule-time-invalid",
          days: [1, 2, 3, 4, 5],
          start_time: "18:00",
          duration_minutes: 30,
          action: "ON",
          time_zone: "Asia/Jakarta",
          enabled: true
        }]
      }
    });
    expect(response.statusCode).toBe(409);
    expect(response.json().error.code).toBe("TIME_INVALID");
  });

  it("rejects implausible UTC and invalid timezone", async () => {
    const token = await ctx.login();
    const implausible = await ctx.app.inject({
      method: "POST",
      url: `/api/v1/devices/${ctx.seed.deviceId}/time`,
      headers: ctx.auth(token),
      payload: { utc: "1970-01-01T00:00:00.000Z", timezone: "Asia/Jakarta" }
    });
    expect(implausible.statusCode).toBe(422);

    const badZone = await ctx.app.inject({
      method: "POST",
      url: `/api/v1/devices/${ctx.seed.deviceId}/time`,
      headers: ctx.auth(token),
      payload: { utc: "2026-11-19T10:00:00.000Z", timezone: "Mars/Olympus" }
    });
    expect(badZone.statusCode).toBe(422);
  });
});
