import { createServer, type Server } from "node:net";
import { once } from "node:events";
import type { AddressInfo } from "node:net";
import { Aedes } from "aedes";
import mqtt, { type MqttClient } from "mqtt";
import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { AckMessageSchema, decodeJson, topicFor, type AckMessage, type CommandMessage } from "@smartplug/mqtt-contract";
import { SimulatedDevice } from "../src/simulator.js";

let broker: Aedes;
let server: Server;
let brokerUrl: string;
let device: SimulatedDevice;
let observer: MqttClient;

async function startBroker(): Promise<void> {
  broker = await Aedes.createBroker();
  server = createServer(broker.handle);
  server.listen(0, "127.0.0.1");
  await once(server, "listening");
  const address = server.address() as AddressInfo;
  brokerUrl = `mqtt://127.0.0.1:${address.port}`;
}

async function connectObserver(clientId: string): Promise<MqttClient> {
  const client = mqtt.connect(brokerUrl, { clientId, clean: true, reconnectPeriod: 0 });
  await once(client, "connect");
  return client;
}

function waitForAck(commandId: string, timeoutMs = 5000): Promise<AckMessage> {
  return new Promise<AckMessage>((resolve, reject) => {
    const timeout = setTimeout(() => {
      observer.off("message", handler);
      reject(new Error(`ACK_TIMEOUT:${commandId}`));
    }, timeoutMs);
    const handler = (topic: string, payload: Buffer): void => {
      if (topic !== topicFor("dev-sim-test", "ack")) return;
      const decoded = decodeJson(AckMessageSchema, payload);
      if (!decoded.ok || decoded.value.command_id !== commandId) return;
      clearTimeout(timeout);
      observer.off("message", handler);
      resolve(decoded.value);
    };
    observer.on("message", handler);
  });
}

function command(overrides: Partial<CommandMessage> = {}): CommandMessage {
  const now = Date.now();
  return {
    schema_version: 1,
    command_id: `cmd-${Math.random().toString(36).slice(2, 10)}`,
    device_id: "dev-sim-test",
    issued_at: new Date(now).toISOString(),
    expires_at: new Date(now + 30_000).toISOString(),
    actor_id: "user-test",
    requested_output: "ON",
    source: "cloud_api",
    correlation_id: "corr-test",
    sequence: 1,
    ...overrides
  };
}

beforeEach(async () => {
  await startBroker();
  observer = await connectObserver(`observer-${Math.random().toString(36).slice(2, 8)}`);
  await new Promise<void>((resolve, reject) => {
    observer.subscribe(topicFor("dev-sim-test", "ack"), { qos: 1 }, (error) => {
      if (error) reject(error);
      else resolve();
    });
  });
  device = new SimulatedDevice({
    deviceId: "dev-sim-test",
    brokerUrl,
    telemetryIntervalMs: 60_000
  });
  await device.start();
});

afterEach(async () => {
  await device?.stop().catch(() => undefined);
  await new Promise<void>((resolve) => observer?.end(false, {}, () => resolve()));
  await new Promise<void>((resolve) => broker?.close(() => resolve()));
  await new Promise<void>((resolve) => server?.close(() => resolve()));
});

describe("device simulator", () => {
  it("applies a valid ON command and emits an ACK", async () => {
    const cmd = command({ sequence: 1 });
    const ackPromise = waitForAck(cmd.command_id);
    await new Promise<void>((resolve, reject) => {
      observer.publish(topicFor("dev-sim-test", "command"), JSON.stringify(cmd), { qos: 1 }, (error) => {
        if (error) reject(error);
        else resolve();
      });
    });
    const ack = await ackPromise;
    expect(ack.status).toBe("APPLIED");
    expect(ack.reason_code).toBe("ON_ACCEPTED");
    expect(device.getState().commandedOutput).toBe("ON");
  });

  it("rejects a replayed command id", async () => {
    const cmd = command({ sequence: 1 });
    const firstAck = waitForAck(cmd.command_id);
    await new Promise<void>((resolve, reject) => {
      observer.publish(topicFor("dev-sim-test", "command"), JSON.stringify(cmd), { qos: 1 }, (error) => {
        if (error) reject(error);
        else resolve();
      });
    });
    await firstAck;

    const replayAck = waitForAck(cmd.command_id);
    await new Promise<void>((resolve, reject) => {
      observer.publish(topicFor("dev-sim-test", "command"), JSON.stringify(cmd), { qos: 1 }, (error) => {
        if (error) reject(error);
        else resolve();
      });
    });
    const ack = await replayAck;
    expect(ack.status).toBe("REJECTED");
    expect(ack.reason_code).toBe("REPLAY_DETECTED");
  });

  it("rejects ON while a fault lockout is active", async () => {
    device.injectFault("OVERTEMP");
    const cmd = command({ sequence: 5, command_id: "cmd-lockout-test" });
    const ackPromise = waitForAck(cmd.command_id);
    await new Promise<void>((resolve, reject) => {
      observer.publish(topicFor("dev-sim-test", "command"), JSON.stringify(cmd), { qos: 1 }, (error) => {
        if (error) reject(error);
        else resolve();
      });
    });
    const ack = await ackPromise;
    expect(ack.status).toBe("REJECTED");
    expect(ack.reason_code).toBe("LOCKOUT_ACTIVE");
    expect(device.getState().commandedOutput).toBe("OFF");
  });

  it("rejects an expired command", async () => {
    const cmd = command({
      command_id: "cmd-expired-test",
      issued_at: new Date(Date.now() - 60_000).toISOString(),
      expires_at: new Date(Date.now() - 30_000).toISOString(),
      sequence: 9
    });
    const ackPromise = waitForAck(cmd.command_id);
    await new Promise<void>((resolve, reject) => {
      observer.publish(topicFor("dev-sim-test", "command"), JSON.stringify(cmd), { qos: 1 }, (error) => {
        if (error) reject(error);
        else resolve();
      });
    });
    const ack = await ackPromise;
    expect(ack.status).toBe("EXPIRED");
    expect(ack.reason_code).toBe("COMMAND_EXPIRED");
  });
});
