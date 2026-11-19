import mqtt, { type MqttClient } from "mqtt";
import { randomUUID } from "node:crypto";
import {
  AckMessageSchema,
  CommandMessageSchema,
  TimeMessageSchema,
  decodeJson,
  topicFor,
  type AckMessage,
  type CommandMessage,
  type TelemetryMessage
} from "@smartplug/mqtt-contract";
import { decideOutputCommand, type DeviceSafetySnapshot } from "@smartplug/domain";

export interface SimulatorOptions {
  deviceId: string;
  brokerUrl: string;
  telemetryIntervalMs?: number;
  startState?: "ON" | "OFF";
  startTimeValid?: boolean;
  logger?: (message: string, detail?: Record<string, unknown>) => void;
}

interface SimulatorState {
  commandedOutput: "ON" | "OFF";
  observedOutput: "ON" | "OFF" | null;
  lockout: boolean;
  faultCode: string | null;
  clockValid: boolean;
  meterValid: boolean;
  temperatureValid: boolean;
  timeValid: boolean;
  timeSource: "sntp" | "api" | "mqtt" | "manual" | "none";
  lastSync: string | null;
  lastKnownTime: string | null;
  timeAgeS: number | null;
  stateVersion: number;
  lastCommandId: string | null;
  lastCommandSequence: number;
}

export class SimulatedDevice {
  private client: MqttClient | null = null;
  private timer: NodeJS.Timeout | null = null;
  private sequence = 1;
  private energyKwhTotal = 0;
  private state: SimulatorState;
  private readonly startedAt = Date.now();

  constructor(private readonly options: SimulatorOptions) {
    this.state = {
      commandedOutput: options.startState ?? "OFF",
      observedOutput: null,
      lockout: false,
      faultCode: null,
      clockValid: true,
      meterValid: true,
      temperatureValid: true,
      timeValid: options.startTimeValid ?? true,
      timeSource: (options.startTimeValid ?? true) ? "sntp" : "none",
      lastSync: (options.startTimeValid ?? true) ? new Date().toISOString() : null,
      lastKnownTime: (options.startTimeValid ?? true) ? new Date().toISOString() : null,
      timeAgeS: (options.startTimeValid ?? true) ? 0 : null,
      stateVersion: 1,
      lastCommandId: null,
      lastCommandSequence: 0
    };
  }

  async start(): Promise<void> {
    const client = mqtt.connect(this.options.brokerUrl, {
      clientId: `sim-${this.options.deviceId}-${randomUUID().slice(0, 6)}`,
      clean: true,
      reconnectPeriod: 2000,
      connectTimeout: 10000,
      will: {
        topic: topicFor(this.options.deviceId, "availability"),
        payload: Buffer.from(
          JSON.stringify({
            schema_version: 1,
            device_id: this.options.deviceId,
            status: "offline",
            last_will: true,
            sent_at: new Date().toISOString()
          })
        ),
        qos: 1,
        retain: true
      }
    });
    this.client = client;

    client.on("message", (topic, payload) => {
      if (topic === topicFor(this.options.deviceId, "command")) {
        void this.handleCommandPayload(payload);
      }
      if (topic === topicFor(this.options.deviceId, "time")) {
        void this.handleTimePayload(payload);
      }
    });

    await new Promise<void>((resolve, reject) => {
      const timeout = setTimeout(() => reject(new Error("SIMULATOR_CONNECT_TIMEOUT")), 12000);
      client.once("connect", () => {
        clearTimeout(timeout);
        resolve();
      });
      client.once("error", (error) => {
        clearTimeout(timeout);
        reject(error);
      });
    });

    await new Promise<void>((resolve, reject) => {
      client.subscribe(topicFor(this.options.deviceId, "command"), { qos: 1 }, (error) => {
        if (error) reject(error);
        else resolve();
      });
    });

    await new Promise<void>((resolve, reject) => {
      client.subscribe(topicFor(this.options.deviceId, "time"), { qos: 1 }, (error) => {
        if (error) reject(error);
        else resolve();
      });
    });

    await this.publish(topicFor(this.options.deviceId, "availability"), {
      schema_version: 1,
      device_id: this.options.deviceId,
      status: "online",
      last_will: false,
      sent_at: new Date().toISOString()
    }, 1, true);
    await this.publishState();

    const interval = this.options.telemetryIntervalMs ?? 2000;
    this.timer = setInterval(() => {
      void this.publishTelemetry().catch((error: unknown) => {
        this.log("telemetry_publish_failed", { error: error instanceof Error ? error.message : "unknown" });
      });
    }, interval);
    this.timer.unref();
    this.log("simulator_started", { deviceId: this.options.deviceId });
  }

  getState(): Readonly<SimulatorState> {
    return { ...this.state };
  }

  getEnergyKwhTotal(): number {
    return this.energyKwhTotal;
  }

  injectFault(code: string): void {
    this.state.lockout = true;
    this.state.faultCode = code;
    this.state.commandedOutput = "OFF";
    this.state.stateVersion += 1;
    void this.publishState();
    void this.publishEvent("FAULT_INJECTED", "CRITICAL", `Fault disuntikkan: ${code}`, { fault_code: code });
    this.log("fault_injected", { code });
  }

  clearFault(): void {
    this.state.lockout = false;
    this.state.faultCode = null;
    this.state.stateVersion += 1;
    void this.publishState();
    this.log("fault_cleared");
  }

  private snapshot(): DeviceSafetySnapshot {
    return {
      deviceId: this.options.deviceId,
      mode: this.state.lockout || this.state.faultCode
        ? "FAULT_LOCKOUT"
        : !this.state.meterValid || !this.state.temperatureValid
          ? "DEGRADED"
          : this.state.commandedOutput === "ON"
            ? "READY_ON"
            : "READY_OFF",
      commandedOutput: this.state.commandedOutput,
      observedOutput: this.state.observedOutput,
      lockout: this.state.lockout,
      faultCode: this.state.faultCode,
      clockValid: this.state.timeValid,
      time: {
        valid: this.state.timeValid,
        source: this.state.timeSource,
        lastSync: this.state.lastSync,
        lastKnown: this.state.lastKnownTime,
        ageSeconds: this.state.timeAgeS
      },
      meterValid: this.state.meterValid,
      temperatureValid: this.state.temperatureValid,
      lastCommandSequence: this.state.lastCommandSequence,
      lastCommandId: this.state.lastCommandId,
      stateVersion: this.state.stateVersion
    };
  }

  async handleTimePayload(payload: Buffer): Promise<void> {
    const decoded = decodeJson(TimeMessageSchema, payload);
    if (!decoded.ok || decoded.value.device_id !== this.options.deviceId) {
      this.log("invalid_time_payload", { error: decoded.ok ? "device_mismatch" : decoded.error });
      return;
    }
    this.setTime(decoded.value.source, decoded.value.utc);
  }

  setTime(source: "sntp" | "api" | "mqtt" | "manual", utc: string): void {
    const parsed = Date.parse(utc);
    if (!Number.isFinite(parsed) || parsed <= Date.parse("2020-01-01T00:00:00.000Z")) {
      this.log("time_rejected", { source, utc });
      return;
    }
    this.state.timeValid = true;
    this.state.timeSource = source;
    this.state.lastSync = new Date().toISOString();
    this.state.lastKnownTime = new Date(parsed).toISOString();
    this.state.timeAgeS = 0;
    this.state.stateVersion += 1;
    void this.publishState();
    this.log("time_synced", { source, utc: this.state.lastKnownTime });
  }

  invalidateTime(): void {
    this.state.timeValid = false;
    this.state.timeSource = "none";
    this.state.lastSync = null;
    this.state.timeAgeS = null;
    this.state.stateVersion += 1;
    if (this.state.commandedOutput === "ON") {
      this.state.commandedOutput = "OFF";
    }
    void this.publishState();
    void this.publishEvent("TIME_INVALID_SCHEDULE_BLOCKED", "WARNING", "Waktu invalid; output schedule dipaksa OFF", {});
  }

  async handleCommandPayload(payload: Buffer): Promise<void> {
    const decoded = decodeJson(CommandMessageSchema, payload);
    if (!decoded.ok) {
      this.log("invalid_command_payload", { error: decoded.error });
      return;
    }
    const command = decoded.value;
    if (command.device_id !== this.options.deviceId) {
      return;
    }

    const now = new Date();
    if (new Date(command.expires_at).getTime() <= now.getTime()) {
      await this.publishAck(command, "EXPIRED", "COMMAND_EXPIRED", this.state.observedOutput);
      return;
    }

    const decision = decideOutputCommand(this.snapshot(), {
      commandId: command.command_id,
      deviceId: command.device_id,
      requestedOutput: command.requested_output,
      source: command.source,
      issuedAt: command.issued_at,
      expiresAt: command.expires_at,
      sequence: command.sequence,
      actorId: command.actor_id
    }, now);

    this.state.lastCommandId = command.command_id;
    this.state.lastCommandSequence = command.sequence;

    if (!decision.accepted) {
      await this.publishAck(command, "REJECTED", decision.reasonCode, this.state.observedOutput);
      this.log("command_rejected", { commandId: command.command_id, reason: decision.reasonCode });
      return;
    }

    this.state.commandedOutput = decision.resultingCommand;
    this.state.stateVersion += 1;
    await this.publishState();
    await this.publishAck(command, "APPLIED", decision.reasonCode, this.state.observedOutput);
    this.log("command_applied", {
      commandId: command.command_id,
      output: decision.resultingCommand,
      reason: decision.reasonCode
    });
  }

  private async publishAck(
    command: CommandMessage,
    status: AckMessage["status"],
    reasonCode: string,
    observedOutput: "ON" | "OFF" | null
  ): Promise<void> {
    const ack: AckMessage = {
      schema_version: 1,
      device_id: this.options.deviceId,
      command_id: command.command_id,
      sequence: command.sequence,
      status,
      reason_code: reasonCode,
      observed_output: observedOutput,
      state_version: this.state.stateVersion,
      acknowledged_at: new Date().toISOString()
    };
    const parsed = AckMessageSchema.safeParse(ack);
    if (!parsed.success) {
      this.log("ack_schema_invalid", { issues: parsed.error.issues });
      return;
    }
    await this.publish(topicFor(this.options.deviceId, "ack"), ack, 1, false);
  }

  private async publishState(): Promise<void> {
    await this.publish(topicFor(this.options.deviceId, "state"), {
      schema_version: 1,
      device_id: this.options.deviceId,
      message_id: randomUUID(),
      sequence: ++this.sequence,
      state: this.mqttState(),
      updated_at: new Date().toISOString()
    }, 1, true);
  }

  private async publishTelemetry(): Promise<void> {
    const voltage = 230 + Math.sin(Date.now() / 5000) * 1.1;
    const on = this.state.commandedOutput === "ON" && !this.state.lockout;
    const activePower = on ? 140 + Math.sin(Date.now() / 4000) * 35 : 0.3;
    const powerFactor = 0.91;
    const current = activePower / (voltage * powerFactor);
    const elapsedHours = 1 / 3600;
    this.energyKwhTotal += (activePower * elapsedHours) / 1000;

    const telemetry: TelemetryMessage = {
      schema_version: 1,
      device_id: this.options.deviceId,
      message_id: randomUUID(),
      sequence: ++this.sequence,
      sampled_at: new Date().toISOString(),
      quality: "VALID",
      measurements: {
        voltage_v: Number(voltage.toFixed(2)),
        current_a: Number(current.toFixed(3)),
        active_power_w: Number(activePower.toFixed(2)),
        energy_kwh_total: Number(this.energyKwhTotal.toFixed(5)),
        power_factor: powerFactor,
        frequency_hz: 50
      },
      state: this.mqttState()
    };
    await this.publish(topicFor(this.options.deviceId, "telemetry"), telemetry, 0, false);
  }

  private mqttState(): TelemetryMessage["state"] {
    return {
      commanded_output: this.state.commandedOutput,
      observed_output: this.state.observedOutput,
      fault: this.state.faultCode,
      lockout: this.state.lockout,
      state_version: this.state.stateVersion,
      clock_valid: this.state.clockValid,
      meter_valid: this.state.meterValid,
      temperature_valid: this.state.temperatureValid
    };
  }

  private async publishEvent(type: string, severity: "INFO" | "WARNING" | "CRITICAL", summary: string, payload: Record<string, unknown>): Promise<void> {
    await this.publish(topicFor(this.options.deviceId, "event"), {
      schema_version: 1,
      device_id: this.options.deviceId,
      event_id: randomUUID(),
      type,
      severity,
      occurred_at: new Date().toISOString(),
      summary,
      payload
    }, 1, false);
  }

  private async publish(topic: string, payload: unknown, qos: 0 | 1, retain: boolean): Promise<void> {
    const client = this.client;
    if (!client || !client.connected) {
      throw new Error("SIMULATOR_MQTT_NOT_CONNECTED");
    }
    await new Promise<void>((resolve, reject) => {
      client.publish(topic, JSON.stringify(payload), { qos, retain }, (error) => {
        if (error) reject(error);
        else resolve();
      });
    });
  }

  async stop(): Promise<void> {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
    const client = this.client;
    this.client = null;
    if (!client) return;
    await this.publishOfflineIfPossible(client);
    await new Promise<void>((resolve) => {
      client.end(false, {}, () => resolve());
    });
    this.log("simulator_stopped", { deviceId: this.options.deviceId, uptimeMs: Date.now() - this.startedAt });
  }

  private async publishOfflineIfPossible(client: MqttClient): Promise<void> {
    if (!client.connected) return;
    await new Promise<void>((resolve) => {
      client.publish(
        topicFor(this.options.deviceId, "availability"),
        JSON.stringify({
          schema_version: 1,
          device_id: this.options.deviceId,
          status: "offline",
          last_will: false,
          sent_at: new Date().toISOString()
        }),
        { qos: 1, retain: true },
        () => resolve()
      );
    });
  }

  private log(message: string, detail?: Record<string, unknown>): void {
    this.options.logger?.(message, detail);
  }
}
