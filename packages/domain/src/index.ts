/**
 * @smartplug/domain
 *
 * Unit-safe domain rules shared by the device simulator, backend, and UI.
 * This package intentionally has no runtime dependencies so the same rules
 * can be tested quickly and mirrored in firmware C code.
 */

export type OutputState = "ON" | "OFF";

export type DeviceMode =
  | "BOOT_SAFE"
  | "PROVISIONING"
  | "READY_OFF"
  | "READY_ON"
  | "WARNING"
  | "FAULT_LOCKOUT"
  | "UPDATING"
  | "DEGRADED";

export type CommandSource =
  | "physical_button"
  | "local_api"
  | "cloud_api"
  | "schedule"
  | "automation"
  | "emergency";

export type RequestedOutput = "ON" | "OFF" | "TOGGLE";

export type MeasurementQuality = "VALID" | "STALE" | "INVALID";

export type AvailabilityStatus = "ONLINE" | "STALE" | "OFFLINE" | "NEVER_SEEN";

export interface DeviceSafetySnapshot {
  deviceId: string;
  mode: DeviceMode;
  commandedOutput: OutputState;
  observedOutput: OutputState | null;
  lockout: boolean;
  faultCode: string | null;
  clockValid: boolean;
  meterValid: boolean;
  temperatureValid: boolean;
  lastCommandSequence: number;
  lastCommandId: string | null;
  stateVersion: number;
}

export interface OutputRequest {
  commandId: string;
  deviceId: string;
  requestedOutput: RequestedOutput;
  source: CommandSource;
  issuedAt: string;
  expiresAt: string;
  sequence: number;
  actorId?: string | null;
  reason?: string | null;
}

export interface CommandDecision {
  accepted: boolean;
  resultingCommand: OutputState;
  reasonCode: string;
  reason: string;
  priority: number;
  requiresObservedConfirmation: boolean;
  stateChanged: boolean;
}

const COMMAND_PRIORITY: Record<CommandSource, number> = {
  emergency: 900,
  physical_button: 600,
  local_api: 550,
  cloud_api: 500,
  schedule: 400,
  automation: 300
};

export function commandPriority(source: CommandSource): number {
  return COMMAND_PRIORITY[source];
}

export function isAutomaticSource(source: CommandSource): boolean {
  return source === "schedule" || source === "automation";
}

export function parseIsoDate(value: string, field: string): Date {
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    throw new Error(`INVALID_ISO_DATE:${field}`);
  }
  return parsed;
}

/**
 * Decide whether an output request may be executed.
 *
 * Safety wins over convenience. An OFF request is always accepted because it
 * moves toward a safer state, even during lockout. An ON request is rejected
 * during boot, provisioning, updating, degraded mode, and any hard lockout.
 */
export function decideOutputCommand(
  state: DeviceSafetySnapshot,
  request: OutputRequest,
  now: Date = new Date(),
  maxClockSkewSeconds = 30
): CommandDecision {
  const base = {
    resultingCommand: state.commandedOutput,
    priority: commandPriority(request.source),
    requiresObservedConfirmation: false,
    stateChanged: false
  } as const;

  if (request.deviceId.length === 0 || request.commandId.length === 0) {
    return {
      ...base,
      accepted: false,
      reasonCode: "MALFORMED_COMMAND",
      reason: "command_id dan device_id wajib diisi"
    };
  }

  if (request.deviceId !== state.deviceId) {
    return {
      ...base,
      accepted: false,
      reasonCode: "WRONG_DEVICE",
      reason: "command_id ditujukan untuk perangkat lain"
    };
  }

  if (request.commandId === state.lastCommandId) {
    return {
      ...base,
      accepted: false,
      reasonCode: "REPLAY_DETECTED",
      reason: "command_id sudah pernah diproses"
    };
  }

  if (request.sequence <= state.lastCommandSequence) {
    return {
      ...base,
      accepted: false,
      reasonCode: "STALE_SEQUENCE",
      reason: "sequence tidak lebih baru dari perintah terakhir"
    };
  }

  const issuedAt = parseIsoDate(request.issuedAt, "issued_at");
  const expiresAt = parseIsoDate(request.expiresAt, "expires_at");
  const nowMs = now.getTime();

  if (expiresAt.getTime() <= nowMs) {
    return {
      ...base,
      accepted: false,
      reasonCode: "COMMAND_EXPIRED",
      reason: "perintah sudah kedaluwarsa"
    };
  }

  if (issuedAt.getTime() > nowMs + maxClockSkewSeconds * 1000) {
    return {
      ...base,
      accepted: false,
      reasonCode: "COMMAND_FROM_FUTURE",
      reason: "issued_at berada di masa depan di luar toleransi"
    };
  }

  if (expiresAt.getTime() <= issuedAt.getTime()) {
    return {
      ...base,
      accepted: false,
      reasonCode: "INVALID_TTL",
      reason: "expires_at harus setelah issued_at"
    };
  }

  const requested: OutputState =
    request.requestedOutput === "TOGGLE"
      ? state.commandedOutput === "ON"
        ? "OFF"
        : "ON"
      : request.requestedOutput;

  if (requested === "OFF") {
    if (state.commandedOutput === "OFF") {
      return {
        ...base,
        accepted: true,
        resultingCommand: "OFF",
        reasonCode: "ALREADY_OFF",
        reason: "output sudah commanded OFF"
      };
    }
    return {
      ...base,
      accepted: true,
      resultingCommand: "OFF",
      reasonCode: "OFF_ACCEPTED",
      reason: "perintah OFF diizinkan; keselamatan menang atas lockout",
      requiresObservedConfirmation: true,
      stateChanged: true
    };
  }

  if (state.lockout || state.mode === "FAULT_LOCKOUT") {
    return {
      ...base,
      accepted: false,
      reasonCode: "LOCKOUT_ACTIVE",
      reason: `ON ditolak: lockout aktif${state.faultCode ? ` (${state.faultCode})` : ""}`
    };
  }

  if (state.faultCode !== null) {
    return {
      ...base,
      accepted: false,
      reasonCode: "HARD_FAULT_ACTIVE",
      reason: `ON ditolak: fault aktif (${state.faultCode})`
    };
  }

  if (state.mode === "BOOT_SAFE" || state.mode === "PROVISIONING" || state.mode === "UPDATING") {
    return {
      ...base,
      accepted: false,
      reasonCode: `MODE_${state.mode}_BLOCKS_ON`,
      reason: `ON ditolak pada mode ${state.mode}`
    };
  }

  if (!state.meterValid) {
    return {
      ...base,
      accepted: false,
      reasonCode: "METER_INVALID",
      reason: "ON ditolak: metering tidak valid"
    };
  }

  if (!state.temperatureValid) {
    return {
      ...base,
      accepted: false,
      reasonCode: "TEMPERATURE_INVALID",
      reason: "ON ditolak: sensor suhu tidak valid"
    };
  }

  if (state.mode === "DEGRADED") {
    return {
      ...base,
      accepted: false,
      reasonCode: "DEGRADED_MODE_BLOCKS_ON",
      reason: "ON ditolak: waktu/meter tidak valid atau kondisi terdegradasi"
    };
  }

  if (isAutomaticSource(request.source) && !state.clockValid) {
    return {
      ...base,
      accepted: false,
      reasonCode: "CLOCK_INVALID",
      reason: "ON otomatis ditolak: jam tidak valid"
    };
  }

  if (state.mode !== "READY_OFF" && state.mode !== "READY_ON" && state.mode !== "WARNING") {
    return {
      ...base,
      accepted: false,
      reasonCode: `MODE_${state.mode}_BLOCKS_ON`,
      reason: `ON ditolak pada mode ${state.mode}`
    };
  }

  if (state.commandedOutput === "ON") {
    return {
      ...base,
      accepted: true,
      resultingCommand: "ON",
      reasonCode: "ALREADY_ON",
      reason: "output sudah commanded ON",
      requiresObservedConfirmation: state.observedOutput !== "ON"
    };
  }

  return {
    ...base,
    accepted: true,
    resultingCommand: "ON",
    reasonCode: "ON_ACCEPTED",
    reason: "semua interlock yang tersedia lolos",
    requiresObservedConfirmation: true,
    stateChanged: true
  };
}

export interface MeasurementInput {
  voltageV: number | null;
  currentA: number | null;
  activePowerW: number | null;
  energyKwhTotal: number | null;
  powerFactor: number | null;
  frequencyHz: number | null;
  sampledAt: string;
  quality: MeasurementQuality;
}

export interface MeasurementValidation {
  valid: boolean;
  quality: MeasurementQuality;
  issues: string[];
  warnings: string[];
}

export interface MeasurementLimits {
  voltageMinV: number;
  voltageMaxV: number;
  currentMaxA: number;
  activePowerMaxW: number;
  frequencyMinHz: number;
  frequencyMaxHz: number;
}

export const DEFAULT_MEASUREMENT_LIMITS: MeasurementLimits = {
  voltageMinV: 0,
  voltageMaxV: 300,
  currentMaxA: 16,
  activePowerMaxW: 4000,
  frequencyMinHz: 45,
  frequencyMaxHz: 65
};

function isFiniteNumber(value: number | null): value is number {
  return typeof value === "number" && Number.isFinite(value);
}

/**
 * Validate a meter sample. Out-of-range values are never silently clamped.
 * A warning keeps the sample usable; an invalid sample must not be displayed
 * as live data or used for cost calculations.
 */
export function validateMeasurement(
  input: MeasurementInput,
  limits: MeasurementLimits = DEFAULT_MEASUREMENT_LIMITS
): MeasurementValidation {
  const issues: string[] = [];
  const warnings: string[] = [];

  try {
    parseIsoDate(input.sampledAt, "sampled_at");
  } catch {
    issues.push("INVALID_TIMESTAMP");
  }

  if (input.quality === "INVALID") {
    issues.push("METER_REPORTED_INVALID");
  }
  if (input.quality === "STALE") {
    warnings.push("METER_REPORTED_STALE");
  }

  const required: Array<[string, number | null]> = [
    ["voltage_v", input.voltageV],
    ["current_a", input.currentA],
    ["active_power_w", input.activePowerW],
    ["energy_kwh_total", input.energyKwhTotal]
  ];

  for (const [name, value] of required) {
    if (!isFiniteNumber(value)) {
      issues.push(`MISSING_OR_NON_FINITE:${name}`);
    }
  }

  if (isFiniteNumber(input.voltageV)) {
    if (input.voltageV < limits.voltageMinV || input.voltageV > limits.voltageMaxV) {
      issues.push("VOLTAGE_OUT_OF_RANGE");
    } else if (input.voltageV > 253) {
      warnings.push("OVERVOLTAGE_WARNING");
    } else if (input.voltageV > 0 && input.voltageV < 207) {
      warnings.push("UNDERVOLTAGE_WARNING");
    }
  }

  if (isFiniteNumber(input.currentA)) {
    if (input.currentA < 0 || input.currentA > limits.currentMaxA) {
      issues.push("CURRENT_OUT_OF_RANGE");
    } else if (input.currentA > 10.5) {
      warnings.push("OVERCURRENT_WARNING");
    }
  }

  if (isFiniteNumber(input.activePowerW)) {
    if (input.activePowerW < 0 || input.activePowerW > limits.activePowerMaxW) {
      issues.push("POWER_OUT_OF_RANGE");
    } else if (input.activePowerW > 2300) {
      warnings.push("HIGH_POWER_WARNING");
    }
  }

  if (isFiniteNumber(input.energyKwhTotal) && input.energyKwhTotal < 0) {
    issues.push("NEGATIVE_ENERGY");
  }

  if (input.powerFactor !== null) {
    if (!isFiniteNumber(input.powerFactor) || input.powerFactor < 0 || input.powerFactor > 1) {
      issues.push("POWER_FACTOR_OUT_OF_RANGE");
    }
  }

  if (input.frequencyHz !== null) {
    if (
      !isFiniteNumber(input.frequencyHz) ||
      input.frequencyHz < limits.frequencyMinHz ||
      input.frequencyHz > limits.frequencyMaxHz
    ) {
      issues.push("FREQUENCY_OUT_OF_RANGE");
    }
  }

  const valid = issues.length === 0;
  return {
    valid,
    quality: valid ? (warnings.length > 0 ? "VALID" : "VALID") : "INVALID",
    issues,
    warnings
  };
}

export interface EnergyReading {
  energyKwhTotal: number;
  sampledAt: string;
  meterId: string;
  sequence: number;
  quality: MeasurementQuality;
}

export interface EnergyDeltaOptions {
  maxDeltaKwh?: number;
  maxGapMs?: number;
}

export interface EnergyDeltaResult {
  deltaKwh: number;
  gap: boolean;
  resetDetected: boolean;
  reasonCode: string;
  reason: string;
}

/**
 * Compute a non-negative energy delta between two cumulative meter readings.
 * Reset, rollover, invalid quality, non-monotonic sequence, and implausible
 * jumps become explicit gaps. They are never converted into fake consumption.
 */
export function computeEnergyDelta(
  previous: EnergyReading,
  current: EnergyReading,
  options: EnergyDeltaOptions = {}
): EnergyDeltaResult {
  const maxDeltaKwh = options.maxDeltaKwh ?? 20;
  const maxGapMs = options.maxGapMs ?? 24 * 60 * 60 * 1000;

  if (previous.quality !== "VALID" || current.quality !== "VALID") {
    return {
      deltaKwh: 0,
      gap: true,
      resetDetected: false,
      reasonCode: "INVALID_METER_QUALITY",
      reason: "delta tidak dihitung karena kualitas sampel tidak valid"
    };
  }

  if (previous.meterId !== current.meterId) {
    return {
      deltaKwh: 0,
      gap: true,
      resetDetected: true,
      reasonCode: "METER_ID_CHANGED",
      reason: "identitas meter berubah; segmen baru diperlukan"
    };
  }

  if (current.sequence <= previous.sequence) {
    return {
      deltaKwh: 0,
      gap: true,
      resetDetected: false,
      reasonCode: "NON_MONOTONIC_SEQUENCE",
      reason: "sequence meter tidak maju"
    };
  }

  const previousAt = parseIsoDate(previous.sampledAt, "previous.sampled_at").getTime();
  const currentAt = parseIsoDate(current.sampledAt, "current.sampled_at").getTime();

  if (currentAt < previousAt) {
    return {
      deltaKwh: 0,
      gap: true,
      resetDetected: false,
      reasonCode: "NON_MONOTONIC_TIME",
      reason: "waktu sampel mundur"
    };
  }

  if (currentAt - previousAt > maxGapMs) {
    return {
      deltaKwh: 0,
      gap: true,
      resetDetected: false,
      reasonCode: "TELEMETRY_GAP_TOO_LARGE",
      reason: "jarak waktu sampel melebihi batas; delta tidak diklaim"
    };
  }

  if (
    !Number.isFinite(previous.energyKwhTotal) ||
    !Number.isFinite(current.energyKwhTotal) ||
    previous.energyKwhTotal < 0 ||
    current.energyKwhTotal < 0
  ) {
    return {
      deltaKwh: 0,
      gap: true,
      resetDetected: false,
      reasonCode: "INVALID_ENERGY_VALUE",
      reason: "nilai energi tidak valid"
    };
  }

  if (current.energyKwhTotal < previous.energyKwhTotal) {
    return {
      deltaKwh: 0,
      gap: true,
      resetDetected: true,
      reasonCode: "COUNTER_RESET_OR_ROLLOVER",
      reason: "counter energi menurun; segmen baru dimulai"
    };
  }

  const delta = current.energyKwhTotal - previous.energyKwhTotal;
  if (delta > maxDeltaKwh) {
    return {
      deltaKwh: 0,
      gap: true,
      resetDetected: false,
      reasonCode: "IMPLAUSIBLE_DELTA",
      reason: `delta ${delta.toFixed(3)} kWh melebihi batas ${maxDeltaKwh} kWh`
    };
  }

  return {
    deltaKwh: delta,
    gap: false,
    resetDetected: false,
    reasonCode: "OK",
    reason: "delta valid"
  };
}

export interface TariffSegment {
  tariffId: string;
  idrPerKwh: number;
  effectiveFrom: string;
  effectiveTo: string | null;
}

export interface EnergyInterval {
  start: string;
  end: string;
  deltaKwh: number;
}

export interface CostLineItem {
  start: string;
  end: string;
  deltaKwh: number;
  tariffId: string | null;
  idrPerKwh: number | null;
  costIdr: number | null;
  reasonCode: string;
}

export interface CostResult {
  totalIdr: number;
  lineItems: CostLineItem[];
  missingTariffCount: number;
  invalidIntervalCount: number;
}

export function selectTariff(
  segments: TariffSegment[],
  at: string
): TariffSegment | null {
  const atMs = parseIsoDate(at, "tariff_at").getTime();
  const candidates = segments.filter((segment) => {
    const from = parseIsoDate(segment.effectiveFrom, "tariff_from").getTime();
    const to = segment.effectiveTo === null ? Number.POSITIVE_INFINITY : parseIsoDate(segment.effectiveTo, "tariff_to").getTime();
    return atMs >= from && atMs < to;
  });

  candidates.sort((a, b) => {
    const aFrom = parseIsoDate(a.effectiveFrom, "tariff_from").getTime();
    const bFrom = parseIsoDate(b.effectiveFrom, "tariff_from").getTime();
    return bFrom - aFrom;
  });

  return candidates[0] ?? null;
}

/**
 * Estimate energy cost with historical tariff segments. Rounding only happens
 * at presentation; this function returns the unrounded decimal value.
 */
export function estimateCostIdr(
  intervals: EnergyInterval[],
  tariffs: TariffSegment[]
): CostResult {
  const lineItems: CostLineItem[] = [];
  let total = 0;
  let missingTariffCount = 0;
  let invalidIntervalCount = 0;

  for (const interval of intervals) {
    if (!Number.isFinite(interval.deltaKwh) || interval.deltaKwh < 0) {
      invalidIntervalCount += 1;
      lineItems.push({
        ...interval,
        tariffId: null,
        idrPerKwh: null,
        costIdr: null,
        reasonCode: "INVALID_DELTA"
      });
      continue;
    }

    const tariff = selectTariff(tariffs, interval.start);
    if (!tariff) {
      missingTariffCount += 1;
      lineItems.push({
        ...interval,
        tariffId: null,
        idrPerKwh: null,
        costIdr: null,
        reasonCode: "NO_TARIFF_FOR_PERIOD"
      });
      continue;
    }

    const cost = interval.deltaKwh * tariff.idrPerKwh;
    total += cost;
    lineItems.push({
      ...interval,
      tariffId: tariff.tariffId,
      idrPerKwh: tariff.idrPerKwh,
      costIdr: cost,
      reasonCode: "OK"
    });
  }

  return {
    totalIdr: total,
    lineItems,
    missingTariffCount,
    invalidIntervalCount
  };
}

export function formatIdr(value: number): string {
  return new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    maximumFractionDigits: 0
  }).format(value);
}

export interface Freshness {
  status: AvailabilityStatus;
  ageSeconds: number | null;
}

export function computeFreshness(
  lastSeenAt: string | null,
  now: Date = new Date(),
  staleAfterSeconds = 30,
  offlineAfterSeconds = 120
): Freshness {
  if (lastSeenAt === null) {
    return { status: "NEVER_SEEN", ageSeconds: null };
  }
  const lastSeenMs = parseIsoDate(lastSeenAt, "last_seen_at").getTime();
  const ageSeconds = Math.max(0, Math.floor((now.getTime() - lastSeenMs) / 1000));
  if (ageSeconds <= staleAfterSeconds) {
    return { status: "ONLINE", ageSeconds };
  }
  if (ageSeconds <= offlineAfterSeconds) {
    return { status: "STALE", ageSeconds };
  }
  return { status: "OFFLINE", ageSeconds };
}

const WEEKDAY_INDEX: Record<string, number> = {
  Sun: 0,
  Mon: 1,
  Tue: 2,
  Wed: 3,
  Thu: 4,
  Fri: 5,
  Sat: 6
};

function zonedParts(date: Date, timeZone: string): {
  weekday: number;
  hour: number;
  minute: number;
  dateKey: string;
} {
  const formatter = new Intl.DateTimeFormat("en-GB", {
    timeZone,
    weekday: "short",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false
  });
  const parts = formatter.formatToParts(date);
  const get = (type: string): string => parts.find((part) => part.type === type)?.value ?? "";
  const weekday = WEEKDAY_INDEX[get("weekday")];
  if (weekday === undefined) {
    throw new Error(`UNSUPPORTED_TIMEZONE:${timeZone}`);
  }
  return {
    weekday,
    hour: Number(get("hour")) % 24,
    minute: Number(get("minute")),
    dateKey: `${get("year")}-${get("month")}-${get("day")}`
  };
}

export interface WeeklySchedule {
  scheduleId: string;
  days: number[];
  startTime: string;
  durationMinutes: number;
  action: "ON" | "OFF";
  timeZone: string;
  enabled: boolean;
}

export interface ScheduleEvaluation {
  due: boolean;
  reasonCode: string;
  scheduledFor: string | null;
  action: "ON" | "OFF" | null;
}

/**
 * Evaluate a weekly schedule at a valid instant. Callers must reject ON when
 * the clock is invalid; this function only decides time-window membership.
 * `lastRunDateKey` prevents duplicate execution when the scheduler polls.
 */
export function evaluateWeeklySchedule(
  schedule: WeeklySchedule,
  now: Date,
  lastRunDateKey: string | null = null
): ScheduleEvaluation {
  if (!schedule.enabled) {
    return { due: false, reasonCode: "SCHEDULE_DISABLED", scheduledFor: null, action: null };
  }
  if (!/^\d{2}:\d{2}$/.test(schedule.startTime)) {
    return { due: false, reasonCode: "INVALID_START_TIME", scheduledFor: null, action: null };
  }
  if (schedule.days.length === 0 || schedule.days.some((day) => day < 0 || day > 6)) {
    return { due: false, reasonCode: "INVALID_DAYS", scheduledFor: null, action: null };
  }
  if (!Number.isInteger(schedule.durationMinutes) || schedule.durationMinutes <= 0) {
    return { due: false, reasonCode: "INVALID_DURATION", scheduledFor: null, action: null };
  }

  const parts = zonedParts(now, schedule.timeZone);
  if (lastRunDateKey === parts.dateKey) {
    return { due: false, reasonCode: "ALREADY_RAN_TODAY", scheduledFor: null, action: null };
  }
  if (!schedule.days.includes(parts.weekday)) {
    return { due: false, reasonCode: "WRONG_WEEKDAY", scheduledFor: null, action: null };
  }

  const [hourText, minuteText] = schedule.startTime.split(":");
  const startMinutes = Number(hourText) * 60 + Number(minuteText);
  const nowMinutes = parts.hour * 60 + parts.minute;
  const endMinutes = startMinutes + schedule.durationMinutes;

  if (nowMinutes < startMinutes || nowMinutes >= endMinutes) {
    return { due: false, reasonCode: "OUTSIDE_WINDOW", scheduledFor: null, action: null };
  }

  return {
    due: true,
    reasonCode: "DUE",
    scheduledFor: `${parts.dateKey}T${schedule.startTime}`,
    action: schedule.action
  };
}

export interface AuditActor {
  actorId: string;
  role: "owner" | "admin" | "viewer" | "system" | "device";
  source: string;
}

export function canIssueOutputCommand(actor: AuditActor): boolean {
  return actor.role === "owner" || actor.role === "admin" || actor.role === "system";
}

export function canViewDiagnostics(actor: AuditActor): boolean {
  return actor.role === "owner" || actor.role === "admin" || actor.role === "system";
}

export function canManageOwnership(actor: AuditActor): boolean {
  return actor.role === "owner" || actor.role === "system";
}

export function redactSecrets(input: string): string {
  return input
    .replace(/(authorization\s*[:=]\s*bearer\s+)[^\s,;]+/gi, "$1[REDACTED]")
    .replace(/(password\s*[:=]\s*)[^\s,;]+/gi, "$1[REDACTED]")
    .replace(/(token\s*[:=]\s*)[^\s,;]+/gi, "$1[REDACTED]")
    .replace(/(ssid\s*[:=]\s*)[^\s,;]+/gi, "$1[REDACTED]");
}

export function clamp(value: number, minimum: number, maximum: number): number {
  if (!Number.isFinite(value)) {
    throw new Error("NON_FINITE_CLAMP_INPUT");
  }
  return Math.min(maximum, Math.max(minimum, value));
}

export function sum(values: number[]): number {
  return values.reduce((total, value) => total + value, 0);
}
