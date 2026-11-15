import Fastify, { type FastifyInstance } from "fastify";
import cors from "@fastify/cors";
import helmet from "@fastify/helmet";
import rateLimit from "@fastify/rate-limit";
import type { AppConfig } from "./config.js";
import type { AppDb } from "./db/index.js";
import type { CommandPublisher } from "./mqtt/publisher.js";
import { makeAuthenticate } from "./auth/middleware.js";
import { isApiError, validationError } from "./errors.js";
import { registerAuthRoutes } from "./routes/auth.js";
import { registerDeviceRoutes } from "./routes/devices.js";
import { registerTelemetryRoutes } from "./routes/telemetry.js";
import { registerAutomationRoutes } from "./routes/automation.js";
import { registerOperationsRoutes } from "./routes/operations.js";
import { registerHealthRoutes } from "./routes/health.js";
import type { RouteDeps } from "./routes/helpers.js";

export interface BuildAppOptions {
  config: AppConfig;
  db: AppDb;
  publisher: CommandPublisher;
  now?: () => Date;
  closeDbOnClose?: boolean;
}

export async function buildApp(options: BuildAppOptions): Promise<FastifyInstance> {
  const { config, db, publisher } = options;
  const now = options.now ?? (() => new Date());

  const app = Fastify({
    logger:
      config.nodeEnv === "test"
        ? false
        : {
            level: config.logLevel,
            redact: {
              paths: [
                "req.headers.authorization",
                "req.body.password",
                "req.body.refresh_token",
                "res.headers.set-cookie"
              ],
              censor: "[REDACTED]"
            }
          },
    bodyLimit: 1024 * 1024,
    requestTimeout: 15_000,
    trustProxy: false
  });

  await app.register(helmet, {
    contentSecurityPolicy: false,
    crossOriginResourcePolicy: { policy: "same-site" }
  });
  const allowedOrigins = new Set([config.webOrigin]);
  if (config.nodeEnv !== "production") {
    allowedOrigins.add("http://localhost:3000");
    allowedOrigins.add("http://127.0.0.1:3000");
  }
  await app.register(cors, {
    origin: (origin, callback) => {
      if (!origin || allowedOrigins.has(origin)) {
        callback(null, true);
        return;
      }
      // Do not turn a CORS policy decision into a 500. The browser will block
      // the response; server-side clients still receive a normal response.
      callback(null, false);
    },
    methods: ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allowedHeaders: ["Authorization", "Content-Type", "X-Request-Id"],
    exposedHeaders: ["X-Request-Id"],
    maxAge: 600
  });
  if (config.rateLimitEnabled) {
    await app.register(rateLimit, {
      global: false,
      max: 100,
      timeWindow: "1 minute"
    });
  }

  app.decorateRequest("authUser", null);
  app.addHook("onSend", async (request, reply, payload) => {
    reply.header("X-Request-Id", request.id);
    return payload;
  });

  const authenticate = makeAuthenticate(config);
  const deps: RouteDeps = { db, config, publisher, now, authenticate };

  registerHealthRoutes(app, deps);
  registerAuthRoutes(app, deps);
  registerDeviceRoutes(app, deps);
  registerTelemetryRoutes(app, deps);
  registerAutomationRoutes(app, deps);
  registerOperationsRoutes(app, deps);

  app.get("/", async () => ({
    service: "smartplug-api",
    version: "0.1.0",
    docs: "/health/live",
    note: "Kontrak API ada di packages/api-contract/openapi.yaml"
  }));

  app.setNotFoundHandler((request, reply) => {
    return reply.status(404).send({
      error: {
        code: "NOT_FOUND",
        message: "Endpoint tidak ditemukan",
        request_id: request.id
      }
    });
  });

  app.setErrorHandler((error, request, reply) => {
    if (isApiError(error)) {
      return reply.status(error.statusCode).send({
        error: {
          code: error.code,
          message: error.message,
          details: error.details,
          request_id: request.id
        }
      });
    }

    const fastifyError = error as { statusCode?: number; validation?: unknown; message?: string };
    if (fastifyError.validation) {
      const validation = validationError("Permintaan tidak valid", fastifyError.validation);
      return reply.status(422).send({
        error: {
          code: validation.code,
          message: validation.message,
          details: validation.details,
          request_id: request.id
        }
      });
    }
    if (fastifyError.statusCode === 400) {
      return reply.status(422).send({
        error: {
          code: "VALIDATION_ERROR",
          message: "Permintaan tidak valid",
          request_id: request.id
        }
      });
    }

    request.log.error({ err: error }, "Unhandled request error");
    return reply.status(500).send({
      error: {
        code: "INTERNAL_ERROR",
        message: "Kesalahan internal; tidak ada state perangkat yang diklaim berubah",
        request_id: request.id
      }
    });
  });

  if (options.closeDbOnClose) {
    app.addHook("onClose", async () => {
      db.close();
    });
  }

  return app;
}
