import { z } from "zod";

export const MQTT_SCHEMA_VERSION = 1 as const;

export const DeviceIdSchema = z
  .string()
  .min(1)
  .max(64)
  .regex(/^[A-Za-z0-9_-]+$/, "device_id hanya boleh huruf, angka, underscore, dan dash");

export type DeviceId = z.infer<typeof DeviceIdSchema>;

export const TopicKindSchema = z.enum([
  "telemetry",
  "state",
  "event",
  "availability",
  "command",
  "ack",
  "diag",
  "time",
  "config/desired",
  "config/reported"
]);
export type TopicKind = z.infer<typeof TopicKindSchema>;

export type TopicDirection = "device_publish" | "device_subscribe" | "backend_publish" | "backend_subscribe";

const DEVICE_PUBLISH_KINDS: ReadonlySet<TopicKind> = new Set([
  "telemetry",
  "state",
  "event",
  "availability",
  "ack",
  "diag",
  "config/reported"
]);

const DEVICE_SUBSCRIBE_KINDS: ReadonlySet<TopicKind> = new Set(["command", "time", "config/desired"]);

export function topicFor(deviceId: string, kind: TopicKind): string {
  const parsed = DeviceIdSchema.parse(deviceId);
  return `smartplug/v1/${parsed}/${kind}`;
}

export function topicsFor(deviceId: string): Record<TopicKind, string> {
  return {
    telemetry: topicFor(deviceId, "telemetry"),
    state: topicFor(deviceId, "state"),
    event: topicFor(deviceId, "event"),
    availability: topicFor(deviceId, "availability"),
    command: topicFor(deviceId, "command"),
    ack: topicFor(deviceId, "ack"),
    diag: topicFor(deviceId, "diag"),
    time: topicFor(deviceId, "time"),
    "config/desired": topicFor(deviceId, "config/desired"),
    "config/reported": topicFor(deviceId, "config/reported")
  };
}

export interface ParsedTopic {
  deviceId: string;
  kind: TopicKind;
}

export function parseTopic(topic: string): ParsedTopic | null {
  const match = /^smartplug\/v1\/([A-Za-z0-9_-]{1,64})\/(telemetry|state|event|availability|command|ack|diag|time|config\/desired|config\/reported)$/.exec(
    topic
  );
  if (!match || match[1] === undefined || match[2] === undefined) {
    return null;
  }
  const kind = TopicKindSchema.safeParse(match[2]);
  if (!kind.success) {
    return null;
  }
  return { deviceId: match[1], kind: kind.data };
}

export function canDevicePublish(deviceId: string, topic: string): boolean {
  const parsed = parseTopic(topic);
  return parsed !== null && parsed.deviceId === deviceId && DEVICE_PUBLISH_KINDS.has(parsed.kind);
}

export function canDeviceSubscribe(deviceId: string, topic: string): boolean {
  const parsed = parseTopic(topic);
  return parsed !== null && parsed.deviceId === deviceId && DEVICE_SUBSCRIBE_KINDS.has(parsed.kind);
}

export function mustNotRetain(kind: TopicKind): boolean {
  // A retained ON command can be replayed to a device after reconnect.
  return kind === "command" || kind === "time" || kind === "config/desired";
}

export function qosFor(kind: TopicKind): 0 | 1 {
  switch (kind) {
    case "telemetry":
    case "diag":
      return 0;
    case "state":
    case "event":
    case "availability":
    case "ack":
    case "command":
    case "time":
    case "config/desired":
    case "config/reported":
      return 1;
  }
}

const NullableFiniteNumber = z.number().finite().nullable();

export const MqttMeasurementSchema = z
  .object({
    voltage_v: NullableFiniteNumber,
    current_a: NullableFiniteNumber,
    active_power_w: NullableFiniteNumber,
    energy_kwh_total: NullableFiniteNumber,
    power_factor: NullableFiniteNumber,
    frequency_hz: NullableFiniteNumber
  })
  .strict();
export type MqttMeasurement = z.infer<typeof MqttMeasurementSchema>;

export const MqttDeviceStateSchema = z
  .object({
    commanded_output: z.enum(["ON", "OFF"]),
    observed_output: z.enum(["ON", "OFF"]).nullable(),
    fault: z.string().max(120).nullable(),
    lockout: z.boolean(),
    state_version: z.number().int().nonnegative(),
    clock_valid: z.boolean(),
    meter_valid: z.boolean(),
    temperature_valid: z.boolean(),
    time_valid: z.boolean().optional(),
    time_source: z.enum(["sntp", "api", "mqtt", "manual", "none"]).optional(),
    last_sync: z.string().datetime().nullable().optional(),
    last_known_time: z.string().datetime().nullable().optional(),
    time_age_s: z.number().int().nonnegative().nullable().optional()
  })
  .strict();
export type MqttDeviceState = z.infer<typeof MqttDeviceStateSchema>;

export const TelemetryMessageSchema = z
  .object({
    schema_version: z.literal(MQTT_SCHEMA_VERSION),
    device_id: DeviceIdSchema,
    message_id: z.string().min(1).max(96),
    sequence: z.number().int().nonnegative(),
    sampled_at: z.string().datetime(),
    quality: z.enum(["VALID", "STALE", "INVALID"]),
    measurements: MqttMeasurementSchema,
    state: MqttDeviceStateSchema
  })
  .strict();
export type TelemetryMessage = z.infer<typeof TelemetryMessageSchema>;

export const StateMessageSchema = z
  .object({
    schema_version: z.literal(MQTT_SCHEMA_VERSION),
    device_id: DeviceIdSchema,
    message_id: z.string().min(1).max(96),
    sequence: z.number().int().nonnegative(),
    state: MqttDeviceStateSchema,
    updated_at: z.string().datetime()
  })
  .strict();
export type StateMessage = z.infer<typeof StateMessageSchema>;

export const CommandMessageSchema = z
  .object({
    schema_version: z.literal(MQTT_SCHEMA_VERSION),
    command_id: z.string().min(1).max(96),
    device_id: DeviceIdSchema,
    issued_at: z.string().datetime(),
    expires_at: z.string().datetime(),
    actor_id: z.string().min(1).max(96),
    requested_output: z.enum(["ON", "OFF"]),
    source: z.enum(["physical_button", "local_api", "cloud_api", "schedule", "automation", "emergency"]),
    correlation_id: z.string().min(1).max(96),
    sequence: z.number().int().nonnegative(),
    signature: z.string().max(256).optional()
  })
  .strict()
  .refine((value) => new Date(value.expires_at).getTime() > new Date(value.issued_at).getTime(), {
    message: "expires_at harus setelah issued_at",
    path: ["expires_at"]
  });
export type CommandMessage = z.infer<typeof CommandMessageSchema>;

export const TimeMessageSchema = z
  .object({
    schema_version: z.literal(MQTT_SCHEMA_VERSION),
    device_id: DeviceIdSchema,
    utc: z.string().datetime(),
    source: z.enum(["mqtt", "manual", "api"]),
    request_id: z.string().min(1).max(96)
  })
  .strict();
export type TimeMessage = z.infer<typeof TimeMessageSchema>;

export const AckMessageSchema = z
  .object({
    schema_version: z.literal(MQTT_SCHEMA_VERSION),
    device_id: DeviceIdSchema,
    command_id: z.string().min(1).max(96),
    sequence: z.number().int().nonnegative(),
    status: z.enum(["APPLIED", "REJECTED", "EXPIRED", "TIMEOUT"]),
    reason_code: z.string().min(1).max(80),
    observed_output: z.enum(["ON", "OFF"]).nullable(),
    state_version: z.number().int().nonnegative(),
    acknowledged_at: z.string().datetime()
  })
  .strict();
export type AckMessage = z.infer<typeof AckMessageSchema>;

export const AvailabilityMessageSchema = z
  .object({
    schema_version: z.literal(MQTT_SCHEMA_VERSION),
    device_id: DeviceIdSchema,
    status: z.enum(["online", "offline"]),
    last_will: z.boolean(),
    sent_at: z.string().datetime()
  })
  .strict();
export type AvailabilityMessage = z.infer<typeof AvailabilityMessageSchema>;

export const EventMessageSchema = z
  .object({
    schema_version: z.literal(MQTT_SCHEMA_VERSION),
    device_id: DeviceIdSchema,
    event_id: z.string().min(1).max(96),
    type: z.string().min(1).max(80),
    severity: z.enum(["INFO", "WARNING", "CRITICAL"]),
    occurred_at: z.string().datetime(),
    summary: z.string().min(1).max(300),
    payload: z.record(z.string(), z.unknown())
  })
  .strict();
export type EventMessage = z.infer<typeof EventMessageSchema>;

export const ConfigSchema = z
  .object({
    schema_version: z.literal(MQTT_SCHEMA_VERSION),
    device_id: DeviceIdSchema,
    version: z.number().int().nonnegative(),
    time_zone: z.string().min(1).max(64),
    power_restore_policy: z.enum(["ALWAYS_OFF", "PREVIOUS_STATE", "USER_SETTING"]),
    schedules: z.array(
      z.object({
        schedule_id: z.string().min(1),
        days: z.array(z.number().int().min(0).max(6)).min(1).max(7),
        start_time: z.string().regex(/^([01]\d|2[0-3]):[0-5]\d$/),
        duration_minutes: z.number().int().min(1).max(1440),
        action: z.enum(["ON", "OFF"]),
        time_zone: z.string().min(1).max(64),
        enabled: z.boolean()
      })
    )
  })
  .strict();
export type ConfigMessage = z.infer<typeof ConfigSchema>;

export function decodeJson<T>(schema: z.ZodType<T>, raw: string | Buffer): { ok: true; value: T } | { ok: false; error: string } {
  try {
    const parsed: unknown = JSON.parse(raw.toString("utf8"));
    const result = schema.safeParse(parsed);
    if (!result.success) {
      return { ok: false, error: result.error.issues.map((issue) => `${issue.path.join(".")}:${issue.message}`).join("; ") };
    }
    return { ok: true, value: result.data };
  } catch {
    return { ok: false, error: "INVALID_JSON" };
  }
}

export function encodeMessage(message: unknown): string {
  return JSON.stringify(message);
}

export const SAMPLE_TELEMETRY: TelemetryMessage = {
  schema_version: 1,
  device_id: "dev-sim-001",
  message_id: "msg-telemetry-001",
  sequence: 1042,
  sampled_at: "2026-11-15T02:00:00.000Z",
  quality: "VALID",
  measurements: {
    voltage_v: 230.1,
    current_a: 0.45,
    active_power_w: 92.7,
    energy_kwh_total: 15.214,
    power_factor: 0.9,
    frequency_hz: 50
  },
  state: {
    commanded_output: "ON",
    observed_output: null,
    fault: null,
    lockout: false,
    state_version: 7,
    clock_valid: true,
    meter_valid: true,
    temperature_valid: true
  }
};

export const SAMPLE_COMMAND: CommandMessage = {
  schema_version: 1,
  command_id: "cmd-20261115-0001",
  device_id: "dev-sim-001",
  issued_at: "2026-11-15T02:00:00.000Z",
  expires_at: "2026-11-15T02:00:30.000Z",
  actor_id: "user-demo",
  requested_output: "OFF",
  source: "cloud_api",
  correlation_id: "corr-001",
  sequence: 1043
};

export const SAMPLE_ACK: AckMessage = {
  schema_version: 1,
  device_id: "dev-sim-001",
  command_id: "cmd-20261115-0001",
  sequence: 1043,
  status: "APPLIED",
  reason_code: "OFF_ACCEPTED",
  observed_output: null,
  state_version: 8,
  acknowledged_at: "2026-11-15T02:00:02.000Z"
};
