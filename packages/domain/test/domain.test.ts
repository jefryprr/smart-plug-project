import { describe, expect, it } from "vitest";
import {
  canIssueOutputCommand,
  computeEnergyDelta,
  computeFreshness,
  decideOutputCommand,
  estimateCostIdr,
  evaluateWeeklySchedule,
  formatIdr,
  redactSecrets,
  selectTariff,
  validateMeasurement,
  type DeviceSafetySnapshot,
  type EnergyReading,
  type OutputRequest,
  type TariffSegment,
  type WeeklySchedule
} from "../src/index.js";

const NOW = new Date("2026-11-15T12:00:00.000Z");

function state(overrides: Partial<DeviceSafetySnapshot> = {}): DeviceSafetySnapshot {
  return {
    deviceId: "dev-test-001",
    mode: "READY_OFF",
    commandedOutput: "OFF",
    observedOutput: "OFF",
    lockout: false,
    faultCode: null,
    clockValid: true,
    meterValid: true,
    temperatureValid: true,
    lastCommandSequence: 0,
    lastCommandId: null,
    stateVersion: 1,
    ...overrides
  };
}

function request(overrides: Partial<OutputRequest> = {}): OutputRequest {
  return {
    commandId: "cmd-001",
    deviceId: "dev-test-001",
    requestedOutput: "ON",
    source: "local_api",
    issuedAt: "2026-11-15T11:59:50.000Z",
    expiresAt: "2026-11-15T12:00:30.000Z",
    sequence: 1,
    actorId: "user-001",
    reason: "test",
    ...overrides
  };
}

describe("output command priority", () => {
  it("accepts ON when every available interlock passes", () => {
    const decision = decideOutputCommand(state(), request(), NOW);
    expect(decision.accepted).toBe(true);
    expect(decision.resultingCommand).toBe("ON");
    expect(decision.reasonCode).toBe("ON_ACCEPTED");
    expect(decision.stateChanged).toBe(true);
    expect(decision.requiresObservedConfirmation).toBe(true);
  });

  it("rejects ON during hard lockout", () => {
    const decision = decideOutputCommand(
      state({ mode: "FAULT_LOCKOUT", lockout: true, faultCode: "OVERTEMP" }),
      request(),
      NOW
    );
    expect(decision.accepted).toBe(false);
    expect(decision.resultingCommand).toBe("OFF");
    expect(decision.reasonCode).toBe("LOCKOUT_ACTIVE");
  });

  it("still accepts OFF during lockout because OFF is safer", () => {
    const decision = decideOutputCommand(
      state({ mode: "FAULT_LOCKOUT", lockout: true, commandedOutput: "ON", faultCode: "OVERTEMP" }),
      request({ requestedOutput: "OFF" }),
      NOW
    );
    expect(decision.accepted).toBe(true);
    expect(decision.resultingCommand).toBe("OFF");
    expect(decision.reasonCode).toBe("OFF_ACCEPTED");
  });

  it("toggles from the commanded state", () => {
    const decision = decideOutputCommand(state({ commandedOutput: "ON" }), request({ requestedOutput: "TOGGLE" }), NOW);
    expect(decision.accepted).toBe(true);
    expect(decision.resultingCommand).toBe("OFF");
  });

  it("rejects an expired command", () => {
    const decision = decideOutputCommand(
      state(),
      request({ issuedAt: "2026-11-15T11:58:00.000Z", expiresAt: "2026-11-15T11:59:00.000Z" }),
      NOW
    );
    expect(decision.accepted).toBe(false);
    expect(decision.reasonCode).toBe("COMMAND_EXPIRED");
  });

  it("rejects a replayed command id", () => {
    const decision = decideOutputCommand(state({ lastCommandId: "cmd-001", lastCommandSequence: 1 }), request(), NOW);
    expect(decision.accepted).toBe(false);
    expect(decision.reasonCode).toBe("REPLAY_DETECTED");
  });

  it("rejects a stale sequence", () => {
    const decision = decideOutputCommand(state({ lastCommandSequence: 7 }), request({ sequence: 7 }), NOW);
    expect(decision.accepted).toBe(false);
    expect(decision.reasonCode).toBe("STALE_SEQUENCE");
  });

  it("rejects a command for another device", () => {
    const decision = decideOutputCommand(state(), request({ deviceId: "dev-other" }), NOW);
    expect(decision.accepted).toBe(false);
    expect(decision.reasonCode).toBe("WRONG_DEVICE");
  });

  it("rejects automatic ON when the clock is invalid", () => {
    const decision = decideOutputCommand(
      state({ clockValid: false }),
      request({ source: "schedule" }),
      NOW
    );
    expect(decision.accepted).toBe(false);
    expect(decision.reasonCode).toBe("CLOCK_INVALID");
  });

  it("allows authorized manual ON when only the clock is invalid", () => {
    const decision = decideOutputCommand(
      state({ clockValid: false }),
      request({ source: "physical_button" }),
      NOW
    );
    expect(decision.accepted).toBe(true);
  });

  it("rejects ON in degraded mode", () => {
    const decision = decideOutputCommand(state({ mode: "DEGRADED" }), request(), NOW);
    expect(decision.accepted).toBe(false);
    expect(decision.reasonCode).toBe("DEGRADED_MODE_BLOCKS_ON");
  });

  it("rejects ON when metering is invalid", () => {
    const decision = decideOutputCommand(state({ meterValid: false }), request(), NOW);
    expect(decision.accepted).toBe(false);
    expect(decision.reasonCode).toBe("METER_INVALID");
  });

  it("rejects ON when temperature sensing is invalid", () => {
    const decision = decideOutputCommand(state({ temperatureValid: false }), request(), NOW);
    expect(decision.accepted).toBe(false);
    expect(decision.reasonCode).toBe("TEMPERATURE_INVALID");
  });

  it("rejects a future-issued command beyond clock skew", () => {
    const decision = decideOutputCommand(
      state(),
      request({ issuedAt: "2026-11-15T12:01:00.000Z", expiresAt: "2026-11-15T12:02:00.000Z" }),
      NOW
    );
    expect(decision.accepted).toBe(false);
    expect(decision.reasonCode).toBe("COMMAND_FROM_FUTURE");
  });
});

describe("measurement validation", () => {
  it("accepts a plausible 230 V sample", () => {
    const result = validateMeasurement({
      voltageV: 230.1,
      currentA: 0.45,
      activePowerW: 92.7,
      energyKwhTotal: 15.214,
      powerFactor: 0.9,
      frequencyHz: 50,
      sampledAt: "2026-11-15T12:00:00.000Z",
      quality: "VALID"
    });
    expect(result.valid).toBe(true);
    expect(result.issues).toEqual([]);
  });

  it("marks a NaN measurement invalid instead of coercing it", () => {
    const result = validateMeasurement({
      voltageV: Number.NaN,
      currentA: null,
      activePowerW: 92.7,
      energyKwhTotal: 15.214,
      powerFactor: 0.9,
      frequencyHz: 50,
      sampledAt: "2026-11-15T12:00:00.000Z",
      quality: "VALID"
    });
    expect(result.valid).toBe(false);
    expect(result.quality).toBe("INVALID");
    expect(result.issues.some((issue) => issue.includes("voltage_v"))).toBe(true);
    expect(result.issues.some((issue) => issue.includes("current_a"))).toBe(true);
  });

  it("warns on overvoltage without claiming surge protection", () => {
    const result = validateMeasurement({
      voltageV: 260,
      currentA: 1,
      activePowerW: 230,
      energyKwhTotal: 1,
      powerFactor: 1,
      frequencyHz: 50,
      sampledAt: "2026-11-15T12:00:00.000Z",
      quality: "VALID"
    });
    expect(result.valid).toBe(true);
    expect(result.warnings).toContain("OVERVOLTAGE_WARNING");
  });

  it("rejects out-of-range current", () => {
    const result = validateMeasurement({
      voltageV: 230,
      currentA: 40,
      activePowerW: 9200,
      energyKwhTotal: 1,
      powerFactor: 1,
      frequencyHz: 50,
      sampledAt: "2026-11-15T12:00:00.000Z",
      quality: "VALID"
    });
    expect(result.valid).toBe(false);
    expect(result.issues).toContain("CURRENT_OUT_OF_RANGE");
  });
});

function reading(overrides: Partial<EnergyReading> = {}): EnergyReading {
  return {
    energyKwhTotal: 10,
    sampledAt: "2026-11-15T12:00:00.000Z",
    meterId: "meter-001",
    sequence: 1,
    quality: "VALID",
    ...overrides
  };
}

describe("energy delta", () => {
  it("computes a normal delta", () => {
    const result = computeEnergyDelta(
      reading({ energyKwhTotal: 10, sequence: 1 }),
      reading({ energyKwhTotal: 10.5, sequence: 2, sampledAt: "2026-11-15T12:05:00.000Z" })
    );
    expect(result.deltaKwh).toBeCloseTo(0.5);
    expect(result.gap).toBe(false);
  });

  it("marks a counter reset as a gap without inventing consumption", () => {
    const result = computeEnergyDelta(
      reading({ energyKwhTotal: 10, sequence: 1 }),
      reading({ energyKwhTotal: 0.2, sequence: 2, sampledAt: "2026-11-15T12:05:00.000Z" })
    );
    expect(result.deltaKwh).toBe(0);
    expect(result.gap).toBe(true);
    expect(result.resetDetected).toBe(true);
    expect(result.reasonCode).toBe("COUNTER_RESET_OR_ROLLOVER");
  });

  it("rejects non-monotonic sequence", () => {
    const result = computeEnergyDelta(
      reading({ sequence: 5 }),
      reading({ sequence: 5, energyKwhTotal: 12, sampledAt: "2026-11-15T12:05:00.000Z" })
    );
    expect(result.gap).toBe(true);
    expect(result.reasonCode).toBe("NON_MONOTONIC_SEQUENCE");
  });

  it("rejects an implausible delta", () => {
    const result = computeEnergyDelta(
      reading({ energyKwhTotal: 10 }),
      reading({ energyKwhTotal: 100, sequence: 2, sampledAt: "2026-11-15T12:05:00.000Z" }),
      { maxDeltaKwh: 20 }
    );
    expect(result.gap).toBe(true);
    expect(result.reasonCode).toBe("IMPLAUSIBLE_DELTA");
  });

  it("rejects invalid meter quality", () => {
    const result = computeEnergyDelta(
      reading({ quality: "STALE" }),
      reading({ energyKwhTotal: 11, sequence: 2, sampledAt: "2026-11-15T12:05:00.000Z" })
    );
    expect(result.gap).toBe(true);
    expect(result.reasonCode).toBe("INVALID_METER_QUALITY");
  });
});

describe("tariff and cost", () => {
  const tariffs: TariffSegment[] = [
    { tariffId: "t-old", idrPerKwh: 1000, effectiveFrom: "2026-01-01T00:00:00.000Z", effectiveTo: "2026-11-01T00:00:00.000Z" },
    { tariffId: "t-new", idrPerKwh: 1500, effectiveFrom: "2026-11-01T00:00:00.000Z", effectiveTo: null }
  ];

  it("selects the tariff effective at the interval start", () => {
    expect(selectTariff(tariffs, "2026-10-15T00:00:00.000Z")?.tariffId).toBe("t-old");
    expect(selectTariff(tariffs, "2026-11-15T00:00:00.000Z")?.tariffId).toBe("t-new");
  });

  it("does not retroactively rewrite historical cost", () => {
    const result = estimateCostIdr(
      [
        { start: "2026-10-15T00:00:00.000Z", end: "2026-10-16T00:00:00.000Z", deltaKwh: 2 },
        { start: "2026-11-15T00:00:00.000Z", end: "2026-11-16T00:00:00.000Z", deltaKwh: 2 }
      ],
      tariffs
    );
    expect(result.totalIdr).toBe(5000);
    expect(result.lineItems[0]?.idrPerKwh).toBe(1000);
    expect(result.lineItems[1]?.idrPerKwh).toBe(1500);
  });

  it("marks intervals without a tariff instead of assuming zero", () => {
    const result = estimateCostIdr(
      [{ start: "2025-01-01T00:00:00.000Z", end: "2025-01-02T00:00:00.000Z", deltaKwh: 2 }],
      tariffs
    );
    expect(result.totalIdr).toBe(0);
    expect(result.missingTariffCount).toBe(1);
    expect(result.lineItems[0]?.costIdr).toBeNull();
  });

  it("formats IDR for the Indonesian locale", () => {
    expect(formatIdr(1234)).toContain("1.234");
  });
});

describe("freshness", () => {
  it("classifies online, stale, offline, and never seen", () => {
    expect(computeFreshness("2026-11-15T11:59:50.000Z", NOW).status).toBe("ONLINE");
    expect(computeFreshness("2026-11-15T11:58:00.000Z", NOW).status).toBe("STALE");
    expect(computeFreshness("2026-11-15T11:00:00.000Z", NOW).status).toBe("OFFLINE");
    expect(computeFreshness(null, NOW).status).toBe("NEVER_SEEN");
  });
});

describe("weekly schedule", () => {
  const schedule: WeeklySchedule = {
    scheduleId: "sched-1",
    days: [0],
    startTime: "12:00",
    durationMinutes: 30,
    action: "ON",
    timeZone: "UTC",
    enabled: true
  };

  it("is due inside the window on the selected weekday", () => {
    const result = evaluateWeeklySchedule(schedule, NOW);
    expect(result.due).toBe(true);
    expect(result.action).toBe("ON");
  });

  it("does not run twice on the same date", () => {
    const result = evaluateWeeklySchedule(schedule, NOW, "2026-11-15");
    expect(result.due).toBe(false);
    expect(result.reasonCode).toBe("ALREADY_RAN_TODAY");
  });

  it("does not fire on another weekday", () => {
    const monday = new Date("2026-11-16T12:00:00.000Z");
    const result = evaluateWeeklySchedule(schedule, monday);
    expect(result.due).toBe(false);
    expect(result.reasonCode).toBe("WRONG_WEEKDAY");
  });

  it("does not fire outside the duration window", () => {
    const later = new Date("2026-11-15T12:45:00.000Z");
    const result = evaluateWeeklySchedule(schedule, later);
    expect(result.due).toBe(false);
    expect(result.reasonCode).toBe("OUTSIDE_WINDOW");
  });
});

describe("authorization and redaction", () => {
  it("allows owner/admin to issue commands but not viewer", () => {
    expect(canIssueOutputCommand({ actorId: "u1", role: "owner", source: "web" })).toBe(true);
    expect(canIssueOutputCommand({ actorId: "u2", role: "admin", source: "web" })).toBe(true);
    expect(canIssueOutputCommand({ actorId: "u3", role: "viewer", source: "web" })).toBe(false);
  });

  it("redacts common secret patterns", () => {
    const redacted = redactSecrets("Authorization: Bearer abc123 password=hunter2 token=xyz");
    expect(redacted).not.toContain("abc123");
    expect(redacted).not.toContain("hunter2");
    expect(redacted).not.toContain("xyz");
    expect(redacted).toContain("[REDACTED]");
  });
});
