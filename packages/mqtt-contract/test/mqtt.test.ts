import { describe, expect, it } from "vitest";
import {
  AckMessageSchema,
  CommandMessageSchema,
  DeviceIdSchema,
  SAMPLE_ACK,
  SAMPLE_COMMAND,
  SAMPLE_TELEMETRY,
  TimeMessageSchema,
  TelemetryMessageSchema,
  canDevicePublish,
  canDeviceSubscribe,
  decodeJson,
  mustNotRetain,
  parseTopic,
  qosFor,
  topicFor,
  topicsFor
} from "../src/index.js";

describe("topic contract", () => {
  it("builds stable versioned topics", () => {
    expect(topicFor("dev-001", "telemetry")).toBe("smartplug/v1/dev-001/telemetry");
    expect(topicsFor("dev-001")["config/desired"]).toBe("smartplug/v1/dev-001/config/desired");
    expect(topicsFor("dev-001").time).toBe("smartplug/v1/dev-001/time");
  });

  it("parses only the documented topic shape", () => {
    expect(parseTopic("smartplug/v1/dev-001/ack")).toEqual({ deviceId: "dev-001", kind: "ack" });
    expect(parseTopic("smartplug/v1/dev-001/unknown")).toBeNull();
    expect(parseTopic("smartplug/v1/dev-001/telemetry/extra")).toBeNull();
    expect(parseTopic("smartplug/v2/dev-001/telemetry")).toBeNull();
  });

  it("rejects wildcard and path characters in device ids", () => {
    expect(DeviceIdSchema.safeParse("dev/001").success).toBe(false);
    expect(DeviceIdSchema.safeParse("dev+001").success).toBe(false);
    expect(DeviceIdSchema.safeParse("dev_001-ok").success).toBe(true);
  });

  it("enforces device publish and subscribe ACL direction", () => {
    expect(canDevicePublish("dev-001", "smartplug/v1/dev-001/telemetry")).toBe(true);
    expect(canDevicePublish("dev-001", "smartplug/v1/dev-001/command")).toBe(false);
    expect(canDeviceSubscribe("dev-001", "smartplug/v1/dev-001/command")).toBe(true);
    expect(canDeviceSubscribe("dev-001", "smartplug/v1/dev-001/time")).toBe(true);
    expect(canDevicePublish("dev-001", "smartplug/v1/dev-001/time")).toBe(false);
    expect(canDeviceSubscribe("dev-001", "smartplug/v1/dev-001/telemetry")).toBe(false);
    expect(canDevicePublish("dev-001", "smartplug/v1/dev-002/telemetry")).toBe(false);
    expect(canDeviceSubscribe("dev-001", "smartplug/v1/dev-002/command")).toBe(false);
  });

  it("marks command, time, and desired config as non-retained", () => {
    expect(mustNotRetain("command")).toBe(true);
    expect(mustNotRetain("time")).toBe(true);
    expect(mustNotRetain("config/desired")).toBe(true);
    expect(mustNotRetain("availability")).toBe(false);
    expect(qosFor("command")).toBe(1);
    expect(qosFor("telemetry")).toBe(0);
  });
});

describe("payload contract", () => {
  it("accepts the synthetic telemetry fixture", () => {
    expect(TelemetryMessageSchema.safeParse(SAMPLE_TELEMETRY).success).toBe(true);
  });

  it("rejects telemetry with missing measurements", () => {
    const invalid = { ...SAMPLE_TELEMETRY, measurements: {} };
    expect(TelemetryMessageSchema.safeParse(invalid).success).toBe(false);
  });

  it("rejects telemetry with an invalid device id", () => {
    const invalid = { ...SAMPLE_TELEMETRY, device_id: "dev/001" };
    expect(TelemetryMessageSchema.safeParse(invalid).success).toBe(false);
  });

  it("accepts a valid MQTT time message and rejects a bad UTC", () => {
    const valid = {
      schema_version: 1,
      device_id: "dev-001",
      utc: "2026-11-19T10:00:00.000Z",
      source: "mqtt",
      request_id: "time-001"
    };
    expect(TimeMessageSchema.safeParse(valid).success).toBe(true);
    expect(TimeMessageSchema.safeParse({ ...valid, utc: "not-a-date" }).success).toBe(false);
    expect(TimeMessageSchema.safeParse({ ...valid, device_id: "dev/001" }).success).toBe(false);
  });

  it("accepts a valid command and rejects an inverted TTL", () => {
    expect(CommandMessageSchema.safeParse(SAMPLE_COMMAND).success).toBe(true);
    const invalid = { ...SAMPLE_COMMAND, expires_at: "2026-11-15T01:59:00.000Z" };
    expect(CommandMessageSchema.safeParse(invalid).success).toBe(false);
  });

  it("accepts an ACK and rejects an unknown status", () => {
    expect(AckMessageSchema.safeParse(SAMPLE_ACK).success).toBe(true);
    expect(AckMessageSchema.safeParse({ ...SAMPLE_ACK, status: "DONE" }).success).toBe(false);
  });

  it("decodes JSON safely and reports schema errors", () => {
    const ok = decodeJson(TelemetryMessageSchema, JSON.stringify(SAMPLE_TELEMETRY));
    expect(ok.ok).toBe(true);
    const bad = decodeJson(TelemetryMessageSchema, "{not json");
    expect(bad.ok).toBe(false);
    if (!bad.ok) {
      expect(bad.error).toBe("INVALID_JSON");
    }
  });
});
