import { loadConfig } from "./config.js";
import { AppDb } from "./db/index.js";
import { buildApp } from "./app.js";
import { seedDemo } from "./seed.js";
import { DeferredPublisher } from "./mqtt/publisher.js";
import { MqttBridge } from "./mqtt/bridge.js";
import { expireStaleCommands } from "./services/commands.js";

async function main(): Promise<void> {
  const config = loadConfig();
  const db = new AppDb(config.sqlitePath);
  db.migrate();

  if (config.seedDemo) {
    seedDemo(db, new Date());
  }

  const deferred = new DeferredPublisher();
  const app = await buildApp({ config, db, publisher: deferred });

  const bridge = new MqttBridge(config, db, {
    info: (obj, message) => app.log.info(obj as object, message),
    warn: (obj, message) => app.log.warn(obj as object, message),
    error: (obj, message) => app.log.error(obj as object, message)
  });

  try {
    await bridge.connect();
  } catch (error) {
    app.log.warn(
      { error: error instanceof Error ? error.message : "unknown", broker: config.mqttUrl },
      "MQTT bridge not connected at startup; API will run in degraded mode"
    );
  }
  deferred.setInner(bridge);

  const expiryTimer = setInterval(() => {
    try {
      const expired = expireStaleCommands(db);
      if (expired > 0) {
        app.log.warn({ expired }, "Expired stale commands without ACK");
      }
    } catch (error) {
      app.log.error({ error: error instanceof Error ? error.message : "unknown" }, "Command expiry job failed");
    }
  }, 15_000);
  expiryTimer.unref();

  const shutdown = async (signal: string): Promise<void> => {
    app.log.info({ signal }, "Shutting down");
    clearInterval(expiryTimer);
    await bridge.close().catch(() => undefined);
    await app.close().catch(() => undefined);
    db.close();
    process.exit(0);
  };

  process.on("SIGINT", () => {
    void shutdown("SIGINT");
  });
  process.on("SIGTERM", () => {
    void shutdown("SIGTERM");
  });

  await app.listen({ port: config.port, host: config.host });
  app.log.info(
    { port: config.port, host: config.host, demoSeed: config.seedDemo },
    "Smart Plug API listening"
  );
}

main().catch((error: unknown) => {
  const message = error instanceof Error ? error.stack ?? error.message : String(error);
  process.stderr.write(`API_STARTUP_FAILED: ${message}\n`);
  process.exit(1);
});
