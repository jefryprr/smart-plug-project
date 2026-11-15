import { SimulatedDevice } from "./simulator.js";

const brokerUrl = process.env.MQTT_URL ?? "mqtt://localhost:1883";
const deviceId = process.env.SIM_DEVICE_ID ?? "dev-sim-001";
const telemetryIntervalMs = Number(process.env.SIM_TELEMETRY_INTERVAL_MS ?? "2000");
const startState = process.env.SIM_START_STATE === "ON" ? "ON" : "OFF";

const device = new SimulatedDevice({
  deviceId,
  brokerUrl,
  telemetryIntervalMs: Number.isFinite(telemetryIntervalMs) ? telemetryIntervalMs : 2000,
  startState,
  logger: (message, detail) => {
    process.stdout.write(`${JSON.stringify({ at: new Date().toISOString(), message, detail })}\n`);
  }
});

const shutdown = async (): Promise<void> => {
  await device.stop();
  process.exit(0);
};

process.on("SIGINT", () => {
  void shutdown();
});
process.on("SIGTERM", () => {
  void shutdown();
});

device.start().then(
  () => {
    process.stdout.write(
      `${JSON.stringify({
        at: new Date().toISOString(),
        message: "device_simulator_ready",
        deviceId,
        brokerUrl,
        startState
      })}\n`
    );
  },
  (error: unknown) => {
    process.stderr.write(`SIMULATOR_START_FAILED: ${error instanceof Error ? error.message : String(error)}\n`);
    process.exit(1);
  }
);
