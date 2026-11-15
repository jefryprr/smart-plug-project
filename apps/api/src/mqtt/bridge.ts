import mqtt, { type MqttClient } from "mqtt";
import { randomUUID } from "node:crypto";
import {
  AckMessageSchema,
  AvailabilityMessageSchema,
  EventMessageSchema,
  StateMessageSchema,
  TelemetryMessageSchema,
  decodeJson,
  parseTopic,
  qosFor,
  topicFor,
  type CommandMessage
} from "@smartplug/mqtt-contract";
import type { AppConfig } from "../config.js";
import type { AppDb } from "../db/index.js";
import type { CommandPublisher } from "./publisher.js";
import {
  ingestAck,
  ingestAvailability,
  ingestDeviceEvent,
  ingestState,
  ingestTelemetry,
  storeDiagnostics
} from "../services/telemetry.js";

export interface LoggerLike {
  info: (obj: unknown, message?: string) => void;
  warn: (obj: unknown, message?: string) => void;
  error: (obj: unknown, message?: string) => void;
}

const SUBSCRIPTIONS: Array<{ topic: string; qos: 0 | 1 }> = [
  { topic: "smartplug/v1/+/telemetry", qos: 0 },
  { topic: "smartplug/v1/+/state", qos: 1 },
  { topic: "smartplug/v1/+/event", qos: 1 },
  { topic: "smartplug/v1/+/availability", qos: 1 },
  { topic: "smartplug/v1/+/ack", qos: 1 },
  { topic: "smartplug/v1/+/diag", qos: 0 },
  { topic: "smartplug/v1/+/config/reported", qos: 1 }
];

export class MqttBridge implements CommandPublisher {
  private client: MqttClient | null = null;
  private connected = false;
  private readonly startedAt = Date.now();

  constructor(
    private readonly config: AppConfig,
    private readonly db: AppDb,
    private readonly logger: LoggerLike,
    private readonly now: () => Date = () => new Date()
  ) {}

  async connect(): Promise<void> {
    const clientId = `smartplug-api-${randomUUID().slice(0, 12)}`;
    const client = mqtt.connect(this.config.mqttUrl, {
      clientId,
      username: this.config.mqttUsername,
      password: this.config.mqttPassword,
      rejectUnauthorized: this.config.mqttTlsRejectUnauthorized,
      clean: true,
      reconnectPeriod: 5000,
      connectTimeout: 10000
    });
    this.client = client;

    client.on("connect", () => {
      this.connected = true;
      this.logger.info({ clientId, broker: this.config.mqttUrl }, "MQTT bridge connected");
      for (const subscription of SUBSCRIPTIONS) {
        client.subscribe(subscription.topic, { qos: subscription.qos }, (error) => {
          if (error) {
            this.logger.error({ topic: subscription.topic, error: error.message }, "MQTT subscribe failed");
          }
        });
      }
    });
    client.on("close", () => {
      this.connected = false;
      this.logger.warn({}, "MQTT bridge disconnected");
    });
    client.on("error", (error) => {
      this.logger.error({ error: error.message }, "MQTT bridge error");
    });
    client.on("message", (topic, payload) => {
      this.handleMessage(topic, payload);
    });

    await new Promise<void>((resolve, reject) => {
      const timeout = setTimeout(() => {
        reject(new Error("MQTT_CONNECT_TIMEOUT"));
      }, 12000);
      client.once("connect", () => {
        clearTimeout(timeout);
        resolve();
      });
      client.once("error", (error) => {
        clearTimeout(timeout);
        reject(error);
      });
    });
  }

  private handleMessage(topic: string, payload: Buffer): void {
    const parsed = parseTopic(topic);
    if (!parsed) {
      this.logger.warn({ topic }, "Ignoring message on unknown topic");
      return;
    }
    const receivedAt = this.now().toISOString();

    try {
      switch (parsed.kind) {
        case "telemetry": {
          const decoded = decodeJson(TelemetryMessageSchema, payload);
          if (!decoded.ok) {
            this.logger.warn({ topic, error: decoded.error }, "Invalid telemetry payload");
            return;
          }
          if (decoded.value.device_id !== parsed.deviceId) {
            this.logger.warn({ topic }, "Telemetry device_id does not match topic");
            return;
          }
          const result = ingestTelemetry(this.db, parsed.deviceId, decoded.value, receivedAt, this.config.defaultTimeZone);
          if (result.duplicate) {
            this.logger.warn({ topic, sequence: decoded.value.sequence }, "Duplicate telemetry sequence ignored");
          }
          return;
        }
        case "state": {
          const decoded = decodeJson(StateMessageSchema, payload);
          if (!decoded.ok || decoded.value.device_id !== parsed.deviceId) {
            this.logger.warn({ topic }, "Invalid state payload");
            return;
          }
          ingestState(this.db, parsed.deviceId, decoded.value, receivedAt);
          return;
        }
        case "ack": {
          const decoded = decodeJson(AckMessageSchema, payload);
          if (!decoded.ok || decoded.value.device_id !== parsed.deviceId) {
            this.logger.warn({ topic }, "Invalid ACK payload");
            return;
          }
          ingestAck(this.db, parsed.deviceId, decoded.value, receivedAt);
          return;
        }
        case "availability": {
          const decoded = decodeJson(AvailabilityMessageSchema, payload);
          if (!decoded.ok || decoded.value.device_id !== parsed.deviceId) {
            this.logger.warn({ topic }, "Invalid availability payload");
            return;
          }
          ingestAvailability(this.db, parsed.deviceId, decoded.value, receivedAt);
          return;
        }
        case "event": {
          const decoded = decodeJson(EventMessageSchema, payload);
          if (!decoded.ok || decoded.value.device_id !== parsed.deviceId) {
            this.logger.warn({ topic }, "Invalid event payload");
            return;
          }
          ingestDeviceEvent(this.db, parsed.deviceId, decoded.value, receivedAt);
          return;
        }
        case "diag": {
          const value: unknown = JSON.parse(payload.toString("utf8"));
          if (typeof value !== "object" || value === null) {
            this.logger.warn({ topic }, "Invalid diagnostics payload");
            return;
          }
          storeDiagnostics(this.db, parsed.deviceId, value as Record<string, unknown>, this.now());
          return;
        }
        case "config/reported":
        case "config/desired":
        case "command":
          return;
      }
    } catch (error) {
      this.logger.error(
        { topic, error: error instanceof Error ? error.message : "unknown" },
        "MQTT message handling failed"
      );
    }
  }

  async publishCommand(message: CommandMessage): Promise<void> {
    const client = this.client;
    if (!client || !this.connected) {
      throw new Error("MQTT_NOT_CONNECTED");
    }
    const topic = topicFor(message.device_id, "command");
    await new Promise<void>((resolve, reject) => {
      client.publish(topic, JSON.stringify(message), { qos: 1, retain: false }, (error) => {
        if (error) {
          reject(error);
        } else {
          resolve();
        }
      });
    });
  }

  isConnected(): boolean {
    return this.connected;
  }

  uptimeSeconds(): number {
    return Math.floor((Date.now() - this.startedAt) / 1000);
  }

  async close(): Promise<void> {
    const client = this.client;
    this.client = null;
    this.connected = false;
    if (!client) return;
    await new Promise<void>((resolve) => {
      client.end(false, {}, () => resolve());
    });
  }
}
