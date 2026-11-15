import { mkdirSync, rmSync } from "node:fs";
import { spawn } from "node:child_process";
import { createServer } from "node:net";
import { once } from "node:events";
import { Aedes } from "aedes";
import { SimulatedDevice } from "../apps/device-simulator/dist/simulator.js";

mkdirSync("data", { recursive: true });
for (const file of ["data/e2e.db", "data/e2e.db-wal", "data/e2e.db-shm"]) {
  rmSync(file, { force: true });
}

const broker = await Aedes.createBroker();
const server = createServer(broker.handle);
server.listen(0, "127.0.0.1");
await once(server, "listening");
const port = server.address().port;
const brokerUrl = `mqtt://127.0.0.1:${port}`;

const device = new SimulatedDevice({
  deviceId: "dev-sim-001",
  brokerUrl,
  telemetryIntervalMs: 1000,
  startState: "OFF",
  logger: (message, detail) => {
    if (message === "simulator_started" || message === "command_applied" || message === "command_rejected") {
      console.log(JSON.stringify({ at: new Date().toISOString(), component: "simulator", message, detail }));
    }
  }
});
await device.start();

const child = spawn(process.execPath, ["node_modules/tsx/dist/cli.mjs", "apps/api/src/index.ts"], {
  stdio: "inherit",
  env: {
    ...process.env,
    NODE_ENV: "development",
    PORT: "4000",
    HOST: "127.0.0.1",
    SQLITE_PATH: "./data/e2e.db",
    SEED_DEMO: "true",
    MQTT_URL: brokerUrl,
    LOG_LEVEL: "warn",
    RATE_LIMIT_ENABLED: "true"
  }
});

let shuttingDown = false;
const shutdown = async () => {
  if (shuttingDown) return;
  shuttingDown = true;
  child.kill("SIGTERM");
  await device.stop().catch(() => undefined);
  await new Promise((resolve) => broker.close(() => resolve(undefined)));
  await new Promise((resolve) => server.close(() => resolve(undefined)));
  process.exit(0);
};

process.on("SIGINT", () => {
  void shutdown();
});
process.on("SIGTERM", () => {
  void shutdown();
});
child.on("exit", (code) => {
  if (!shuttingDown) {
    void shutdown().then(() => process.exit(code ?? 0));
  }
});
