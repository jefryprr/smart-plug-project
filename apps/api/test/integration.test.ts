import { createServer, type Server } from "node:net";
import type { AddressInfo } from "node:net";
import { once } from "node:events";
import { Aedes } from "aedes";
import { afterEach, beforeEach, describe, expect, it } from "vitest";
import type { FastifyInstance } from "fastify";
import { SimulatedDevice } from "@smartplug/device-simulator";
import { buildApp } from "../src/app.js";
import { AppDb } from "../src/db/index.js";
import { seedDemo, type SeedResult } from "../src/seed.js";
import { testConfig } from "../src/config.js";
import { MqttBridge } from "../src/mqtt/bridge.js";
import { NOW } from "./helpers.js";

const DEVICE_ID = "dev-sim-001";

async function waitFor<T>(fn: () => Promise<T | null>, timeoutMs = 8000, intervalMs = 100): Promise<T> {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const value = await fn();
    if (value !== null) return value;
    await new Promise((resolve) => setTimeout(resolve, intervalMs));
  }
  throw new Error("WAIT_FOR_TIMEOUT");
}

describe("API to MQTT to simulator integration", () => {
  let broker: Aedes;
  let server: Server;
  let bridge: MqttBridge;
  let device: SimulatedDevice;
  let app: FastifyInstance;
  let db: AppDb;
  let seed: SeedResult;
  let token: string;

  beforeEach(async () => {
    broker = await Aedes.createBroker();
    server = createServer(broker.handle);
    server.listen(0, "127.0.0.1");
    await once(server, "listening");
    const address = server.address() as AddressInfo;
    const brokerUrl = `mqtt://127.0.0.1:${address.port}`;

    db = new AppDb(":memory:");
    db.migrate();
    seed = seedDemo(db, NOW, { withSyntheticTelemetry: false });

    const config = testConfig({ mqttUrl: brokerUrl });
    bridge = new MqttBridge(config, db, { info: () => undefined, warn: () => undefined, error: () => undefined });
    await bridge.connect();

    app = await buildApp({ config, db, publisher: bridge, now: () => new Date() });

    const login = await app.inject({
      method: "POST",
      url: "/api/v1/auth/login",
      payload: { email: "demo@example.com", password: "demo1234" }
    });
    token = login.json<{ access_token: string }>().access_token;

    device = new SimulatedDevice({
      deviceId: DEVICE_ID,
      brokerUrl,
      telemetryIntervalMs: 300,
      startState: "OFF"
    });
    await device.start();
    await waitFor(async () => {
      const response = await app.inject({
        method: "GET",
        url: `/api/v1/devices/${DEVICE_ID}`,
        headers: { authorization: `Bearer ${token}` }
      });
      return response.statusCode === 200 && response.json().availability === "ONLINE" ? response.json() : null;
    });
  });

  afterEach(async () => {
    await device?.stop().catch(() => undefined);
    await bridge?.close().catch(() => undefined);
    await app?.close().catch(() => undefined);
    db?.close();
    await new Promise<void>((resolve) => broker?.close(() => resolve()));
    await new Promise<void>((resolve) => server?.close(() => resolve()));
  });

  it("completes POST command -> MQTT -> simulator ACK -> APPLIED", async () => {
    const created = await app.inject({
      method: "POST",
      url: `/api/v1/devices/${DEVICE_ID}/commands`,
      headers: { authorization: `Bearer ${token}` },
      payload: { requested_output: "ON", idempotency_key: "integration-on-001", ttl_seconds: 30 }
    });
    expect(created.statusCode).toBe(202);
    const commandId = created.json<{ command_id: string }>().command_id;

    const applied = await waitFor(async () => {
      const response = await app.inject({
        method: "GET",
        url: `/api/v1/devices/${DEVICE_ID}/commands/${commandId}`,
        headers: { authorization: `Bearer ${token}` }
      });
      if (response.statusCode !== 200) return null;
      return response.json().status === "APPLIED" ? response.json() : null;
    });
    expect(applied.status).toBe("APPLIED");
    expect(applied.observed_output).toBeNull();
    expect(device.getState().commandedOutput).toBe("ON");

    const deviceResponse = await app.inject({
      method: "GET",
      url: `/api/v1/devices/${DEVICE_ID}`,
      headers: { authorization: `Bearer ${token}` }
    });
    expect(deviceResponse.json().state.commanded_output).toBe("ON");
  });

  it("propagates a simulator fault lockout and rejects ON while accepting OFF", async () => {
    device.injectFault("OVERTEMP");
    await waitFor(async () => {
      const response = await app.inject({
        method: "GET",
        url: `/api/v1/devices/${DEVICE_ID}`,
        headers: { authorization: `Bearer ${token}` }
      });
      return response.json().state.lockout === true ? response.json() : null;
    });

    const rejected = await app.inject({
      method: "POST",
      url: `/api/v1/devices/${DEVICE_ID}/commands`,
      headers: { authorization: `Bearer ${token}` },
      payload: { requested_output: "ON", idempotency_key: "integration-lockout-on" }
    });
    expect(rejected.statusCode).toBe(409);
    expect(rejected.json().error.details.reason_code).toBe("LOCKOUT_ACTIVE");

    const off = await app.inject({
      method: "POST",
      url: `/api/v1/devices/${DEVICE_ID}/commands`,
      headers: { authorization: `Bearer ${token}` },
      payload: { requested_output: "OFF", idempotency_key: "integration-lockout-off" }
    });
    expect(off.statusCode).toBe(202);
    const commandId = off.json<{ command_id: string }>().command_id;
    const applied = await waitFor(async () => {
      const response = await app.inject({
        method: "GET",
        url: `/api/v1/devices/${DEVICE_ID}/commands/${commandId}`,
        headers: { authorization: `Bearer ${token}` }
      });
      return response.json().status === "APPLIED" ? response.json() : null;
    });
    expect(applied.status).toBe("APPLIED");
    expect(device.getState().commandedOutput).toBe("OFF");
  });

  it("ingests simulator telemetry and serves it through the API", async () => {
    const samples = await waitFor(async () => {
      const response = await app.inject({
        method: "GET",
        url: `/api/v1/devices/${DEVICE_ID}/telemetry?limit=5`,
        headers: { authorization: `Bearer ${token}` }
      });
      return response.statusCode === 200 && response.json().samples.length > 0 ? response.json() : null;
    });
    expect(samples.data_available).toBe(true);
    expect(samples.samples[0].device_id).toBe(DEVICE_ID);
    expect(samples.samples[0].quality).toBe("VALID");
  });

  it("marks the device OFFLINE when the simulator publishes availability offline", async () => {
    await device.stop();
    const offline = await waitFor(async () => {
      const response = await app.inject({
        method: "GET",
        url: `/api/v1/devices/${DEVICE_ID}`,
        headers: { authorization: `Bearer ${token}` }
      });
      return response.json().availability === "OFFLINE" ? response.json() : null;
    });
    expect(offline.availability).toBe("OFFLINE");
  });
});
