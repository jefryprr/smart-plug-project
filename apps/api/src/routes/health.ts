import type { FastifyInstance } from "fastify";
import type { HealthResponse } from "@smartplug/api-contract";
import type { RouteDeps } from "./helpers.js";

export function registerHealthRoutes(app: FastifyInstance, deps: RouteDeps): void {
  const startedAt = Date.now();

  app.get("/health/live", async () => {
    const response: HealthResponse = {
      status: "ok",
      service: "smartplug-api",
      version: "0.1.0",
      uptime_seconds: Math.floor((Date.now() - startedAt) / 1000),
      checks: { process: "ok" }
    };
    return response;
  });

  app.get("/health/ready", async (_request, reply) => {
    let database: "ok" | "down" = "ok";
    try {
      deps.db.get("SELECT 1 AS ok");
    } catch {
      database = "down";
    }
    const mqtt = deps.publisher.isConnected() ? "ok" : "down";
    const status: HealthResponse["status"] = database === "down" ? "down" : mqtt === "ok" ? "ok" : "degraded";
    const response: HealthResponse = {
      status,
      service: "smartplug-api",
      version: "0.1.0",
      uptime_seconds: Math.floor((Date.now() - startedAt) / 1000),
      checks: { database, mqtt }
    };
    return reply.status(database === "down" ? 503 : 200).send(response);
  });
}
