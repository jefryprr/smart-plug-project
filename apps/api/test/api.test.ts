import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { createTestContext, createUserWithRole, setDeviceState, NOW, type TestContext } from "./helpers.js";
import { ingestAck } from "../src/services/telemetry.js";
import { hashPassword } from "../src/auth/password.js";

let ctx: TestContext;

beforeEach(async () => {
  ctx = await createTestContext();
});

afterEach(async () => {
  await ctx.app.close();
  ctx.db.close();
});

describe("auth and tenancy", () => {
  it("reports liveness and readiness", async () => {
    const live = await ctx.app.inject({ method: "GET", url: "/health/live" });
    expect(live.statusCode).toBe(200);
    expect(live.json().status).toBe("ok");

    const ready = await ctx.app.inject({ method: "GET", url: "/health/ready" });
    expect(ready.statusCode).toBe(200);
    expect(ready.json().checks.database).toBe("ok");
    expect(ready.json().checks.mqtt).toBe("ok");
  });

  it("rejects a wrong password with a generic 401", async () => {
    const response = await ctx.app.inject({
      method: "POST",
      url: "/api/v1/auth/login",
      payload: { email: "demo@example.com", password: "wrong-password" }
    });
    expect(response.statusCode).toBe(401);
    expect(response.json().error.code).toBe("UNAUTHORIZED");
  });

  it("logs in and returns the profile", async () => {
    const token = await ctx.login();
    const me = await ctx.app.inject({ method: "GET", url: "/api/v1/me", headers: ctx.auth(token) });
    expect(me.statusCode).toBe(200);
    expect(me.json().email).toBe("demo@example.com");
    expect(me.json().homes[0].role).toBe("owner");
  });

  it("rejects missing and tampered access tokens", async () => {
    const missing = await ctx.app.inject({ method: "GET", url: "/api/v1/devices" });
    expect(missing.statusCode).toBe(401);

    const tampered = await ctx.app.inject({
      method: "GET",
      url: "/api/v1/devices",
      headers: { authorization: "Bearer not-a-token" }
    });
    expect(tampered.statusCode).toBe(401);
  });

  it("rotates refresh tokens and revokes the old session on logout", async () => {
    const login = await ctx.app.inject({
      method: "POST",
      url: "/api/v1/auth/login",
      payload: { email: "demo@example.com", password: "demo1234" }
    });
    const first = login.json<{ access_token: string; refresh_token: string }>();
    const refreshed = await ctx.app.inject({
      method: "POST",
      url: "/api/v1/auth/refresh",
      payload: { refresh_token: first.refresh_token }
    });
    expect(refreshed.statusCode).toBe(200);
    const second = refreshed.json<{ access_token: string; refresh_token: string }>();
    expect(second.refresh_token).not.toBe(first.refresh_token);

    const replayOld = await ctx.app.inject({
      method: "POST",
      url: "/api/v1/auth/refresh",
      payload: { refresh_token: first.refresh_token }
    });
    expect(replayOld.statusCode).toBe(401);

    const logout = await ctx.app.inject({
      method: "POST",
      url: "/api/v1/auth/logout",
      headers: ctx.auth(second.access_token)
    });
    expect(logout.statusCode).toBe(204);

    const afterLogout = await ctx.app.inject({
      method: "POST",
      url: "/api/v1/auth/refresh",
      payload: { refresh_token: second.refresh_token }
    });
    expect(afterLogout.statusCode).toBe(401);
  });

  it("returns 404 for a device in another tenant", async () => {
    ctx.db.run(
      `INSERT INTO homes (home_id, name, created_at) VALUES ('home-other', 'Rumah Lain', ?)`,
      NOW.toISOString()
    );
    createUserWithRole(ctx.db, "other@example.com", "other1234", "home-other", "owner");
    const token = await ctx.login("other@example.com", "other1234");
    const response = await ctx.app.inject({
      method: "GET",
      url: `/api/v1/devices/${ctx.seed.deviceId}`,
      headers: ctx.auth(token)
    });
    expect(response.statusCode).toBe(404);
  });

  it("claims a device once with a single-use pairing code", async () => {
    const userId = "user-claimer";
    ctx.db.run(
      `INSERT INTO users (user_id, email, password_hash, display_name, created_at) VALUES (?, ?, ?, ?, ?)`,
      userId,
      "claimer@example.com",
      hashPassword("claimer1234"),
      "Claimer",
      NOW.toISOString()
    );
    const token = await ctx.login("claimer@example.com", "claimer1234");

    const claim = await ctx.app.inject({
      method: "POST",
      url: "/api/v1/device-claims",
      headers: ctx.auth(token),
      payload: { pairing_code: "123456", device_name: "Plug Klaim" }
    });
    expect(claim.statusCode).toBe(201);
    expect(claim.json().device_id).toBe(ctx.seed.deviceId);

    const device = await ctx.app.inject({
      method: "GET",
      url: `/api/v1/devices/${ctx.seed.deviceId}`,
      headers: ctx.auth(token)
    });
    expect(device.statusCode).toBe(200);
    expect(device.json().name).toBe("Plug Klaim");

    const replay = await ctx.app.inject({
      method: "POST",
      url: "/api/v1/device-claims",
      headers: ctx.auth(token),
      payload: { pairing_code: "123456" }
    });
    expect(replay.statusCode).toBe(409);
    expect(replay.json().error.code).toBe("PAIRING_INVALID");
  });
});

describe("devices and commands", () => {
  it("lists the demo device with an explicit synthetic data source", async () => {
    const token = await ctx.login();
    const response = await ctx.app.inject({ method: "GET", url: "/api/v1/devices", headers: ctx.auth(token) });
    expect(response.statusCode).toBe(200);
    const devices = response.json().devices;
    expect(devices).toHaveLength(1);
    expect(devices[0].device_id).toBe(ctx.seed.deviceId);
    expect(devices[0].data_source).toBe("SYNTHETIC_DEMO");
    expect(devices[0].role).toBeUndefined();
  });

  it("returns device detail with role and home", async () => {
    const token = await ctx.login();
    const response = await ctx.app.inject({
      method: "GET",
      url: `/api/v1/devices/${ctx.seed.deviceId}`,
      headers: ctx.auth(token)
    });
    expect(response.statusCode).toBe(200);
    expect(response.json().home_id).toBe(ctx.seed.homeId);
    expect(response.json().role).toBe("owner");
  });

  it("renames a device and rejects a viewer write", async () => {
    const token = await ctx.login();
    const rename = await ctx.app.inject({
      method: "PATCH",
      url: `/api/v1/devices/${ctx.seed.deviceId}`,
      headers: ctx.auth(token),
      payload: { name: "Plug Dapur" }
    });
    expect(rename.statusCode).toBe(200);
    expect(rename.json().name).toBe("Plug Dapur");

    createUserWithRole(ctx.db, "viewer@example.com", "viewer1234", ctx.seed.homeId, "viewer");
    const viewerToken = await ctx.login("viewer@example.com", "viewer1234");
    const denied = await ctx.app.inject({
      method: "PATCH",
      url: `/api/v1/devices/${ctx.seed.deviceId}`,
      headers: ctx.auth(viewerToken),
      payload: { name: "Tidak Boleh" }
    });
    expect(denied.statusCode).toBe(403);
  });

  it("accepts ON, publishes to the broker, and records an ACK", async () => {
    setDeviceState(ctx.db, ctx.seed.deviceId, {
      commanded_output: "OFF",
      observed_output: null,
      lockout: false,
      fault_code: null,
      meter_valid: true,
      temperature_valid: true,
      state_version: 50
    });
    const token = await ctx.login();
    const response = await ctx.app.inject({
      method: "POST",
      url: `/api/v1/devices/${ctx.seed.deviceId}/commands`,
      headers: ctx.auth(token),
      payload: { requested_output: "ON", idempotency_key: "test-key-0001", ttl_seconds: 30 }
    });
    expect(response.statusCode).toBe(202);
    const command = response.json<{ command_id: string; status: string }>();
    expect(command.status).toBe("ACCEPTED");
    expect(ctx.publisher.messages).toHaveLength(1);
    expect(ctx.publisher.messages[0]?.requested_output).toBe("ON");

    const polled = await ctx.app.inject({
      method: "GET",
      url: `/api/v1/devices/${ctx.seed.deviceId}/commands/${command.command_id}`,
      headers: ctx.auth(token)
    });
    expect(polled.statusCode).toBe(200);
    expect(polled.json().status).toBe("ACCEPTED");

    ingestAck(
      ctx.db,
      ctx.seed.deviceId,
      {
        schema_version: 1,
        device_id: ctx.seed.deviceId,
        command_id: command.command_id,
        sequence: ctx.publisher.messages[0]?.sequence ?? 1,
        status: "APPLIED",
        reason_code: "ON_ACCEPTED",
        observed_output: null,
        state_version: 51,
        acknowledged_at: NOW.toISOString()
      },
      NOW.toISOString()
    );

    const applied = await ctx.app.inject({
      method: "GET",
      url: `/api/v1/devices/${ctx.seed.deviceId}/commands/${command.command_id}`,
      headers: ctx.auth(token)
    });
    expect(applied.json().status).toBe("APPLIED");
  });

  it("replays the same idempotency key without a second publish", async () => {
    setDeviceState(ctx.db, ctx.seed.deviceId, {
      commanded_output: "OFF",
      lockout: false,
      fault_code: null,
      meter_valid: true,
      temperature_valid: true
    });
    const token = await ctx.login();
    const payload = { requested_output: "ON", idempotency_key: "test-key-replay", ttl_seconds: 30 };
    const first = await ctx.app.inject({
      method: "POST",
      url: `/api/v1/devices/${ctx.seed.deviceId}/commands`,
      headers: ctx.auth(token),
      payload
    });
    const second = await ctx.app.inject({
      method: "POST",
      url: `/api/v1/devices/${ctx.seed.deviceId}/commands`,
      headers: ctx.auth(token),
      payload
    });
    expect(first.statusCode).toBe(202);
    expect(second.statusCode).toBe(202);
    expect(second.json().command_id).toBe(first.json().command_id);
    expect(second.json().idempotent_replay).toBe(true);
    expect(ctx.publisher.messages).toHaveLength(1);
  });

  it("rejects an idempotency key reused for a different request", async () => {
    setDeviceState(ctx.db, ctx.seed.deviceId, {
      commanded_output: "OFF",
      lockout: false,
      fault_code: null,
      meter_valid: true,
      temperature_valid: true
    });
    const token = await ctx.login();
    const first = await ctx.app.inject({
      method: "POST",
      url: `/api/v1/devices/${ctx.seed.deviceId}/commands`,
      headers: ctx.auth(token),
      payload: { requested_output: "ON", idempotency_key: "test-key-conflict" }
    });
    expect(first.statusCode).toBe(202);
    const second = await ctx.app.inject({
      method: "POST",
      url: `/api/v1/devices/${ctx.seed.deviceId}/commands`,
      headers: ctx.auth(token),
      payload: { requested_output: "OFF", idempotency_key: "test-key-conflict" }
    });
    expect(second.statusCode).toBe(409);
    expect(second.json().error.code).toBe("IDEMPOTENCY_CONFLICT");
  });

  it("rejects ON during a hard lockout but still accepts OFF", async () => {
    const token = await ctx.login();
    setDeviceState(ctx.db, ctx.seed.deviceId, {
      commanded_output: "OFF",
      lockout: true,
      fault_code: "OVERTEMP",
      meter_valid: true,
      temperature_valid: true
    });
    const on = await ctx.app.inject({
      method: "POST",
      url: `/api/v1/devices/${ctx.seed.deviceId}/commands`,
      headers: ctx.auth(token),
      payload: { requested_output: "ON", idempotency_key: "test-lockout-on" }
    });
    expect(on.statusCode).toBe(409);
    expect(on.json().error.code).toBe("COMMAND_REJECTED");
    expect(on.json().error.details.reason_code).toBe("LOCKOUT_ACTIVE");

    setDeviceState(ctx.db, ctx.seed.deviceId, { commanded_output: "ON", lockout: true, fault_code: "OVERTEMP" });
    const off = await ctx.app.inject({
      method: "POST",
      url: `/api/v1/devices/${ctx.seed.deviceId}/commands`,
      headers: ctx.auth(token),
      payload: { requested_output: "OFF", idempotency_key: "test-lockout-off" }
    });
    expect(off.statusCode).toBe(202);
  });

  it("rejects ON when metering is invalid", async () => {
    const token = await ctx.login();
    setDeviceState(ctx.db, ctx.seed.deviceId, {
      commanded_output: "OFF",
      lockout: false,
      fault_code: null,
      meter_valid: false,
      temperature_valid: true
    });
    const response = await ctx.app.inject({
      method: "POST",
      url: `/api/v1/devices/${ctx.seed.deviceId}/commands`,
      headers: ctx.auth(token),
      payload: { requested_output: "ON", idempotency_key: "test-meter-invalid" }
    });
    expect(response.statusCode).toBe(409);
    expect(response.json().error.details.reason_code).toBe("METER_INVALID");
  });

  it("returns 503 and does not claim success when the broker is unavailable", async () => {
    setDeviceState(ctx.db, ctx.seed.deviceId, {
      commanded_output: "OFF",
      lockout: false,
      fault_code: null,
      meter_valid: true,
      temperature_valid: true
    });
    ctx.publisher.connected = false;
    const token = await ctx.login();
    const response = await ctx.app.inject({
      method: "POST",
      url: `/api/v1/devices/${ctx.seed.deviceId}/commands`,
      headers: ctx.auth(token),
      payload: { requested_output: "ON", idempotency_key: "test-broker-down" }
    });
    expect(response.statusCode).toBe(503);
    expect(response.json().error.code).toBe("DOWNSTREAM_UNAVAILABLE");
  });

  it("forbids a viewer from issuing commands", async () => {
    createUserWithRole(ctx.db, "viewer2@example.com", "viewer1234", ctx.seed.homeId, "viewer");
    const token = await ctx.login("viewer2@example.com", "viewer1234");
    const response = await ctx.app.inject({
      method: "POST",
      url: `/api/v1/devices/${ctx.seed.deviceId}/commands`,
      headers: ctx.auth(token),
      payload: { requested_output: "OFF", idempotency_key: "viewer-command" }
    });
    expect(response.statusCode).toBe(403);
  });

  it("validates the command body", async () => {
    const token = await ctx.login();
    const response = await ctx.app.inject({
      method: "POST",
      url: `/api/v1/devices/${ctx.seed.deviceId}/commands`,
      headers: ctx.auth(token),
      payload: { requested_output: "MAYBE", idempotency_key: "short" }
    });
    expect(response.statusCode).toBe(422);
    expect(response.json().error.code).toBe("VALIDATION_ERROR");
  });
});

describe("telemetry, analytics, tariff, budget, and schedules", () => {
  it("returns seeded telemetry with an explicit data_available flag", async () => {
    const token = await ctx.login();
    const response = await ctx.app.inject({
      method: "GET",
      url: `/api/v1/devices/${ctx.seed.deviceId}/telemetry?limit=10`,
      headers: ctx.auth(token)
    });
    expect(response.statusCode).toBe(200);
    expect(response.json().data_available).toBe(true);
    expect(response.json().samples).toHaveLength(10);
    expect(response.json().samples[0].voltage_v).toBeGreaterThan(200);
  });

  it("aggregates daily energy and cost without pretending that missing data is zero", async () => {
    const token = await ctx.login();
    const response = await ctx.app.inject({
      method: "GET",
      url: `/api/v1/devices/${ctx.seed.deviceId}/analytics?from=2026-11-13T00:00:00Z&to=2026-11-16T00:00:00Z&granularity=day&timezone=Asia%2FJakarta`,
      headers: ctx.auth(token)
    });
    expect(response.statusCode).toBe(200);
    const analytics = response.json();
    expect(analytics.data_available).toBe(true);
    expect(analytics.total_energy_kwh).toBeGreaterThan(0);
    expect(analytics.total_cost_idr).toBeGreaterThan(0);
    expect(analytics.buckets.length).toBe(4);
  });

  it("returns data_available=false for an empty range", async () => {
    const token = await ctx.login();
    const response = await ctx.app.inject({
      method: "GET",
      url: `/api/v1/devices/${ctx.seed.deviceId}/analytics?from=2020-01-01T00:00:00Z&to=2020-01-02T00:00:00Z&granularity=day`,
      headers: ctx.auth(token)
    });
    expect(response.statusCode).toBe(200);
    expect(response.json().data_available).toBe(false);
    expect(response.json().total_energy_kwh).toBeNull();
  });

  it("rejects an invalid timezone and an inverted range", async () => {
    const token = await ctx.login();
    const badZone = await ctx.app.inject({
      method: "GET",
      url: `/api/v1/devices/${ctx.seed.deviceId}/analytics?from=2026-11-13T00:00:00Z&to=2026-11-16T00:00:00Z&timezone=Mars%2FBase`,
      headers: ctx.auth(token)
    });
    expect(badZone.statusCode).toBe(422);

    const inverted = await ctx.app.inject({
      method: "GET",
      url: `/api/v1/devices/${ctx.seed.deviceId}/analytics?from=2026-11-16T00:00:00Z&to=2026-11-13T00:00:00Z`,
      headers: ctx.auth(token)
    });
    expect(inverted.statusCode).toBe(422);
  });

  it("adds a future tariff without rewriting historical cost", async () => {
    const token = await ctx.login();
    const before = await ctx.app.inject({
      method: "GET",
      url: `/api/v1/devices/${ctx.seed.deviceId}/analytics?from=2026-11-13T00:00:00Z&to=2026-11-16T00:00:00Z&granularity=day`,
      headers: ctx.auth(token)
    });
    const beforeCost = before.json().total_cost_idr;

    const created = await ctx.app.inject({
      method: "PUT",
      url: `/api/v1/devices/${ctx.seed.deviceId}/tariff`,
      headers: ctx.auth(token),
      payload: { idr_per_kwh: 1700, effective_from: "2026-12-01T00:00:00Z" }
    });
    expect(created.statusCode).toBe(201);

    const after = await ctx.app.inject({
      method: "GET",
      url: `/api/v1/devices/${ctx.seed.deviceId}/analytics?from=2026-11-13T00:00:00Z&to=2026-11-16T00:00:00Z&granularity=day`,
      headers: ctx.auth(token)
    });
    expect(after.json().total_cost_idr).toBe(beforeCost);

    const overlap = await ctx.app.inject({
      method: "PUT",
      url: `/api/v1/devices/${ctx.seed.deviceId}/tariff`,
      headers: ctx.auth(token),
      payload: { idr_per_kwh: 1200, effective_from: "2026-06-01T00:00:00Z" }
    });
    expect(overlap.statusCode).toBe(409);
    expect(overlap.json().error.code).toBe("TARIFF_OVERLAP");
  });

  it("reads and updates the energy budget", async () => {
    const token = await ctx.login();
    const initial = await ctx.app.inject({
      method: "GET",
      url: `/api/v1/devices/${ctx.seed.deviceId}/budget`,
      headers: ctx.auth(token)
    });
    expect(initial.statusCode).toBe(200);
    expect(initial.json().enabled).toBe(true);

    const updated = await ctx.app.inject({
      method: "PUT",
      url: `/api/v1/devices/${ctx.seed.deviceId}/budget`,
      headers: ctx.auth(token),
      payload: { period: "monthly", kwh_limit: 40, idr_limit: 60000, enabled: true }
    });
    expect(updated.statusCode).toBe(200);
    expect(updated.json().kwh_limit).toBe(40);
  });

  it("saves schedules with optimistic versioning", async () => {
    const token = await ctx.login();
    const initial = await ctx.app.inject({
      method: "GET",
      url: `/api/v1/devices/${ctx.seed.deviceId}/automations`,
      headers: ctx.auth(token)
    });
    expect(initial.statusCode).toBe(200);
    expect(initial.json().version).toBe(0);

    const saved = await ctx.app.inject({
      method: "PUT",
      url: `/api/v1/devices/${ctx.seed.deviceId}/automations`,
      headers: ctx.auth(token),
      payload: {
        version: 0,
        schedules: [
          {
            days: [1, 2, 3, 4, 5],
            start_time: "07:30",
            duration_minutes: 60,
            action: "ON",
            time_zone: "Asia/Jakarta",
            enabled: true
          }
        ]
      }
    });
    expect(saved.statusCode).toBe(200);
    expect(saved.json().version).toBe(1);
    expect(saved.json().schedules[0].schedule_id).toBeTruthy();

    const stale = await ctx.app.inject({
      method: "PUT",
      url: `/api/v1/devices/${ctx.seed.deviceId}/automations`,
      headers: ctx.auth(token),
      payload: { version: 0, schedules: [] }
    });
    expect(stale.statusCode).toBe(409);
    expect(stale.json().error.code).toBe("AUTOMATION_VERSION_CONFLICT");
  });
});

describe("operations, diagnostics, notifications, and OTA", () => {
  it("lists device events with pagination metadata", async () => {
    const token = await ctx.login();
    const response = await ctx.app.inject({
      method: "GET",
      url: `/api/v1/devices/${ctx.seed.deviceId}/events?limit=5`,
      headers: ctx.auth(token)
    });
    expect(response.statusCode).toBe(200);
    expect(response.json().events.length).toBeGreaterThan(0);
    expect(response.json().events.some((event: { type: string }) => event.type === "DEMO_DATA_SEEDED")).toBe(true);
  });

  it("returns diagnostics to owner and denies viewer", async () => {
    const token = await ctx.login();
    const owner = await ctx.app.inject({
      method: "GET",
      url: `/api/v1/devices/${ctx.seed.deviceId}/diagnostics`,
      headers: ctx.auth(token)
    });
    expect(owner.statusCode).toBe(200);
    expect(owner.json().sensor_health.relay_feedback).toBe("NOT_INSTALLED");

    createUserWithRole(ctx.db, "viewer3@example.com", "viewer1234", ctx.seed.homeId, "viewer");
    const viewerToken = await ctx.login("viewer3@example.com", "viewer1234");
    const denied = await ctx.app.inject({
      method: "GET",
      url: `/api/v1/devices/${ctx.seed.deviceId}/diagnostics`,
      headers: ctx.auth(viewerToken)
    });
    expect(denied.statusCode).toBe(403);
  });

  it("sends a mock notification once per minute", async () => {
    const token = await ctx.login();
    const first = await ctx.app.inject({
      method: "POST",
      url: `/api/v1/devices/${ctx.seed.deviceId}/notifications/test`,
      headers: ctx.auth(token)
    });
    expect(first.statusCode).toBe(202);
    expect(first.json().provider).toBe("mock");
    expect(first.json().status).toBe("SENT");

    const second = await ctx.app.inject({
      method: "POST",
      url: `/api/v1/devices/${ctx.seed.deviceId}/notifications/test`,
      headers: ctx.auth(token)
    });
    expect(second.statusCode).toBe(429);
  });

  it("records an OTA request without claiming delivery", async () => {
    const token = await ctx.login();
    const response = await ctx.app.inject({
      method: "POST",
      url: `/api/v1/devices/${ctx.seed.deviceId}/ota`,
      headers: ctx.auth(token),
      payload: { release_id: "fw-0.2.0-rc1" }
    });
    expect(response.statusCode).toBe(202);
    expect(response.json().status).toBe("PENDING");

    const events = await ctx.app.inject({
      method: "GET",
      url: `/api/v1/devices/${ctx.seed.deviceId}/events?limit=10`,
      headers: ctx.auth(token)
    });
    expect(events.json().events.some((event: { type: string }) => event.type === "OTA_REQUESTED")).toBe(true);
  });

  it("revokes ownership and removes the pairing claim", async () => {
    const token = await ctx.login();
    const response = await ctx.app.inject({
      method: "POST",
      url: `/api/v1/devices/${ctx.seed.deviceId}/revoke`,
      headers: ctx.auth(token)
    });
    expect(response.statusCode).toBe(204);
    const claim = ctx.db.get<{ claim_id: string }>(
      `SELECT claim_id FROM device_claims WHERE device_id = ?`,
      ctx.seed.deviceId
    );
    expect(claim).toBeUndefined();
  });
});
