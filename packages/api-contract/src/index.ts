import { z } from "zod";

export const OutputStateSchema = z.enum(["ON", "OFF"]);
export type OutputState = z.infer<typeof OutputStateSchema>;

export const RoleSchema = z.enum(["owner", "admin", "viewer"]);
export type Role = z.infer<typeof RoleSchema>;

export const CommandSourceSchema = z.enum([
  "physical_button",
  "local_api",
  "cloud_api",
  "schedule",
  "automation",
  "emergency"
]);
export type CommandSource = z.infer<typeof CommandSourceSchema>;

export const CommandStatusSchema = z.enum([
  "PENDING",
  "ACCEPTED",
  "DELIVERED",
  "APPLIED",
  "REJECTED",
  "EXPIRED",
  "TIMEOUT"
]);
export type CommandStatus = z.infer<typeof CommandStatusSchema>;

export const AvailabilitySchema = z.enum(["ONLINE", "STALE", "OFFLINE", "NEVER_SEEN"]);
export type Availability = z.infer<typeof AvailabilitySchema>;

export const MeasurementQualitySchema = z.enum(["VALID", "STALE", "INVALID"]);
export type MeasurementQuality = z.infer<typeof MeasurementQualitySchema>;

export const DeviceStateSchema = z
  .object({
    commanded_output: OutputStateSchema,
    observed_output: OutputStateSchema.nullable(),
    lockout: z.boolean(),
    fault_code: z.string().max(120).nullable(),
    state_version: z.number().int().nonnegative(),
    last_transition_at: z.string().datetime(),
    clock_valid: z.boolean(),
    meter_valid: z.boolean(),
    temperature_valid: z.boolean()
  })
  .strict();
export type DeviceState = z.infer<typeof DeviceStateSchema>;

export const DataSourceSchema = z.enum(["DEVICE", "SIMULATOR", "SYNTHETIC_DEMO", "UNKNOWN"]);
export type DataSource = z.infer<typeof DataSourceSchema>;

export const DeviceSummarySchema = z
  .object({
    device_id: z.string().min(1).max(64),
    name: z.string().min(1).max(80),
    room: z.string().max(80).nullable(),
    availability: AvailabilitySchema,
    last_seen_at: z.string().datetime().nullable(),
    state: DeviceStateSchema,
    firmware_version: z.string().max(40).nullable(),
    data_source: DataSourceSchema,
    created_at: z.string().datetime()
  })
  .strict();
export type DeviceSummary = z.infer<typeof DeviceSummarySchema>;

export const DeviceDetailSchema = DeviceSummarySchema.extend({
  home_id: z.string().min(1),
  hardware_revision: z.string().max(40).nullable(),
  role: RoleSchema
});
export type DeviceDetail = z.infer<typeof DeviceDetailSchema>;

export const LoginRequestSchema = z
  .object({
    email: z.string().email().max(254),
    password: z.string().min(8).max(200)
  })
  .strict();
export type LoginRequest = z.infer<typeof LoginRequestSchema>;

export const LoginResponseSchema = z
  .object({
    access_token: z.string().min(20),
    refresh_token: z.string().min(20),
    token_type: z.literal("Bearer"),
    expires_in: z.number().int().positive()
  })
  .strict();
export type LoginResponse = z.infer<typeof LoginResponseSchema>;

export const MeResponseSchema = z
  .object({
    user_id: z.string().min(1),
    email: z.string().email(),
    display_name: z.string().max(80),
    homes: z.array(
      z.object({
        home_id: z.string().min(1),
        name: z.string().min(1).max(80),
        role: RoleSchema
      })
    )
  })
  .strict();
export type MeResponse = z.infer<typeof MeResponseSchema>;

export const ClaimDeviceRequestSchema = z
  .object({
    pairing_code: z.string().regex(/^\d{6,10}$/),
    device_name: z.string().min(1).max(80).optional()
  })
  .strict();
export type ClaimDeviceRequest = z.infer<typeof ClaimDeviceRequestSchema>;

export const ClaimDeviceResponseSchema = z
  .object({
    device_id: z.string().min(1),
    home_id: z.string().min(1),
    claimed_at: z.string().datetime()
  })
  .strict();
export type ClaimDeviceResponse = z.infer<typeof ClaimDeviceResponseSchema>;

export const CommandRequestSchema = z
  .object({
    requested_output: z.enum(["ON", "OFF"]),
    idempotency_key: z.string().min(8).max(128),
    ttl_seconds: z.number().int().min(5).max(300).default(30),
    reason: z.string().max(200).optional()
  })
  .strict();
export type CommandRequest = z.infer<typeof CommandRequestSchema>;

export const CommandResponseSchema = z
  .object({
    command_id: z.string().min(1),
    device_id: z.string().min(1),
    requested_output: OutputStateSchema,
    status: CommandStatusSchema,
    accepted_at: z.string().datetime(),
    expires_at: z.string().datetime(),
    state_version: z.number().int().nonnegative(),
    observed_output: OutputStateSchema.nullable(),
    message: z.string().max(300),
    idempotent_replay: z.boolean()
  })
  .strict();
export type CommandResponse = z.infer<typeof CommandResponseSchema>;

export const TelemetrySampleSchema = z
  .object({
    sample_id: z.string().min(1),
    device_id: z.string().min(1),
    sequence: z.number().int().nonnegative(),
    sampled_at: z.string().datetime(),
    received_at: z.string().datetime(),
    quality: MeasurementQualitySchema,
    voltage_v: z.number().finite().nullable(),
    current_a: z.number().finite().nullable(),
    active_power_w: z.number().finite().nullable(),
    energy_kwh_total: z.number().finite().nullable(),
    power_factor: z.number().finite().nullable(),
    frequency_hz: z.number().finite().nullable(),
    state: DeviceStateSchema
  })
  .strict();
export type TelemetrySample = z.infer<typeof TelemetrySampleSchema>;

export const TelemetryListResponseSchema = z
  .object({
    device_id: z.string().min(1),
    samples: z.array(TelemetrySampleSchema),
    next_cursor: z.string().nullable(),
    data_available: z.boolean()
  })
  .strict();
export type TelemetryListResponse = z.infer<typeof TelemetryListResponseSchema>;

export const AnalyticsBucketSchema = z
  .object({
    period_start: z.string().datetime(),
    period_end: z.string().datetime(),
    label: z.string().min(1),
    energy_kwh: z.number().finite().nonnegative().nullable(),
    cost_idr: z.number().finite().nonnegative().nullable(),
    sample_count: z.number().int().nonnegative(),
    gap_count: z.number().int().nonnegative(),
    data_available: z.boolean()
  })
  .strict();
export type AnalyticsBucket = z.infer<typeof AnalyticsBucketSchema>;

export const AnalyticsResponseSchema = z
  .object({
    device_id: z.string().min(1),
    from: z.string().datetime(),
    to: z.string().datetime(),
    granularity: z.enum(["hour", "day", "week", "month"]),
    time_zone: z.string().min(1),
    data_available: z.boolean(),
    total_energy_kwh: z.number().finite().nonnegative().nullable(),
    total_cost_idr: z.number().finite().nonnegative().nullable(),
    missing_tariff_buckets: z.number().int().nonnegative(),
    buckets: z.array(AnalyticsBucketSchema)
  })
  .strict();
export type AnalyticsResponse = z.infer<typeof AnalyticsResponseSchema>;

export const TariffSchema = z
  .object({
    tariff_id: z.string().min(1),
    currency: z.literal("IDR"),
    idr_per_kwh: z.number().finite().positive().max(100000),
    effective_from: z.string().datetime(),
    effective_to: z.string().datetime().nullable(),
    created_at: z.string().datetime()
  })
  .strict();
export type Tariff = z.infer<typeof TariffSchema>;

export const TariffRequestSchema = z
  .object({
    idr_per_kwh: z.number().finite().positive().max(100000),
    effective_from: z.string().datetime()
  })
  .strict();
export type TariffRequest = z.infer<typeof TariffRequestSchema>;

export const BudgetSchema = z
  .object({
    budget_id: z.string().min(1),
    period: z.enum(["daily", "weekly", "monthly"]),
    kwh_limit: z.number().finite().positive().nullable(),
    idr_limit: z.number().finite().positive().nullable(),
    enabled: z.boolean(),
    updated_at: z.string().datetime()
  })
  .strict();
export type Budget = z.infer<typeof BudgetSchema>;

export const BudgetRequestSchema = z
  .object({
    period: z.enum(["daily", "weekly", "monthly"]),
    kwh_limit: z.number().finite().positive().nullable().optional(),
    idr_limit: z.number().finite().positive().nullable().optional(),
    enabled: z.boolean()
  })
  .strict();
export type BudgetRequest = z.infer<typeof BudgetRequestSchema>;

export const ScheduleSchema = z
  .object({
    schedule_id: z.string().min(1),
    days: z.array(z.number().int().min(0).max(6)).min(1).max(7),
    start_time: z.string().regex(/^([01]\d|2[0-3]):[0-5]\d$/),
    duration_minutes: z.number().int().min(1).max(1440),
    action: z.enum(["ON", "OFF"]),
    time_zone: z.string().min(1).max(64),
    enabled: z.boolean()
  })
  .strict();
export type Schedule = z.infer<typeof ScheduleSchema>;

export const AutomationsResponseSchema = z
  .object({
    device_id: z.string().min(1),
    schedules: z.array(ScheduleSchema),
    version: z.number().int().nonnegative()
  })
  .strict();
export type AutomationsResponse = z.infer<typeof AutomationsResponseSchema>;

export const AutomationsRequestSchema = z
  .object({
    schedules: z.array(ScheduleSchema.omit({ schedule_id: true }).extend({ schedule_id: z.string().min(1).optional() })),
    version: z.number().int().nonnegative()
  })
  .strict();
export type AutomationsRequest = z.infer<typeof AutomationsRequestSchema>;

export const EventItemSchema = z
  .object({
    event_id: z.string().min(1),
    device_id: z.string().min(1),
    type: z.string().min(1).max(80),
    severity: z.enum(["INFO", "WARNING", "CRITICAL"]),
    occurred_at: z.string().datetime(),
    actor_id: z.string().nullable(),
    source: z.string().min(1).max(40),
    correlation_id: z.string().nullable(),
    summary: z.string().min(1).max(300),
    payload: z.record(z.string(), z.unknown())
  })
  .strict();
export type EventItem = z.infer<typeof EventItemSchema>;

export const EventsResponseSchema = z
  .object({
    device_id: z.string().min(1),
    events: z.array(EventItemSchema),
    next_cursor: z.string().nullable()
  })
  .strict();
export type EventsResponse = z.infer<typeof EventsResponseSchema>;

export const DiagnosticsResponseSchema = z
  .object({
    device_id: z.string().min(1),
    firmware_version: z.string().max(40).nullable(),
    build_sha: z.string().max(64).nullable(),
    uptime_seconds: z.number().int().nonnegative().nullable(),
    rssi_dbm: z.number().int().nullable(),
    heap_free_bytes: z.number().int().nonnegative().nullable(),
    last_error: z.string().max(200).nullable(),
    sensor_health: z.object({
      meter: z.enum(["OK", "STALE", "INVALID", "UNKNOWN"]),
      temperature: z.enum(["OK", "STALE", "INVALID", "UNKNOWN"]),
      relay_feedback: z.enum(["OK", "NOT_INSTALLED", "MISMATCH", "UNKNOWN"])
    }),
    wifi_state: z.enum(["CONNECTED", "DISCONNECTED", "PROVISIONING", "UNKNOWN"]),
    command_counts: z.object({
      accepted: z.number().int().nonnegative(),
      rejected: z.number().int().nonnegative(),
      expired: z.number().int().nonnegative()
    }),
    checked_at: z.string().datetime()
  })
  .strict();
export type DiagnosticsResponse = z.infer<typeof DiagnosticsResponseSchema>;

export const ErrorResponseSchema = z
  .object({
    error: z.object({
      code: z.string().min(1).max(80),
      message: z.string().min(1).max(300),
      details: z.unknown().optional(),
      request_id: z.string().max(80).optional()
    })
  })
  .strict();
export type ErrorResponse = z.infer<typeof ErrorResponseSchema>;

export const HealthResponseSchema = z
  .object({
    status: z.enum(["ok", "degraded", "down"]),
    service: z.string(),
    version: z.string(),
    uptime_seconds: z.number().nonnegative(),
    checks: z.record(z.string(), z.enum(["ok", "degraded", "down", "not_configured"]))
  })
  .strict();
export type HealthResponse = z.infer<typeof HealthResponseSchema>;

export const OpenApiInfo = {
  title: "Smart Plug API",
  version: "1.0.0",
  description: "Contract for the ESP32-S3 smart plug backend. All timestamps are UTC ISO-8601."
} as const;

export type ApiErrorCode =
  | "UNAUTHORIZED"
  | "FORBIDDEN"
  | "NOT_FOUND"
  | "CONFLICT"
  | "VALIDATION_ERROR"
  | "RATE_LIMITED"
  | "COMMAND_REJECTED"
  | "LOCKOUT_ACTIVE"
  | "DEVICE_OFFLINE"
  | "PAIRING_INVALID"
  | "PAIRING_EXPIRED"
  | "IDEMPOTENCY_CONFLICT"
  | "DOWNSTREAM_UNAVAILABLE"
  | "INTERNAL_ERROR";
