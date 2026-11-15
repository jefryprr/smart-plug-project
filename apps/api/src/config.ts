import { z } from "zod";

const BooleanString = z
  .enum(["true", "false"])
  .transform((value) => value === "true");

const EnvSchema = z.object({
  NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
  PORT: z.coerce.number().int().min(1).max(65535).default(4000),
  HOST: z.string().default("0.0.0.0"),
  WEB_ORIGIN: z.string().default("http://localhost:3000"),
  LOG_LEVEL: z.enum(["fatal", "error", "warn", "info", "debug", "trace", "silent"]).default("info"),
  JWT_SECRET: z.string().default("dev-only-change-me-32-characters-minimum"),
  ACCESS_TOKEN_TTL_SECONDS: z.coerce.number().int().min(60).max(86400).default(900),
  REFRESH_TOKEN_TTL_DAYS: z.coerce.number().int().min(1).max(90).default(7),
  SQLITE_PATH: z.string().default("./data/smartplug.db"),
  MQTT_URL: z.string().default("mqtt://localhost:1883"),
  MQTT_USERNAME: z.string().optional(),
  MQTT_PASSWORD: z.string().optional(),
  MQTT_TLS_REJECT_UNAUTHORIZED: BooleanString.default(true),
  TELEGRAM_BOT_TOKEN: z.string().optional(),
  TELEGRAM_CHAT_ID: z.string().optional(),
  DEFAULT_TIMEZONE: z.string().default("Asia/Jakarta"),
  RATE_LIMIT_ENABLED: BooleanString.default(true),
  SEED_DEMO: BooleanString.default(true)
});

export interface AppConfig {
  nodeEnv: "development" | "test" | "production";
  port: number;
  host: string;
  webOrigin: string;
  logLevel: "fatal" | "error" | "warn" | "info" | "debug" | "trace" | "silent";
  jwtSecret: string;
  accessTokenTtlSeconds: number;
  refreshTokenTtlDays: number;
  sqlitePath: string;
  mqttUrl: string;
  mqttUsername: string | undefined;
  mqttPassword: string | undefined;
  mqttTlsRejectUnauthorized: boolean;
  telegramBotToken: string | undefined;
  telegramChatId: string | undefined;
  defaultTimeZone: string;
  rateLimitEnabled: boolean;
  seedDemo: boolean;
}

const DEV_SECRET = "dev-only-change-me-32-characters-minimum";

export function loadConfig(env: NodeJS.ProcessEnv = process.env): AppConfig {
  const parsed = EnvSchema.safeParse(env);
  if (!parsed.success) {
    const details = parsed.error.issues.map((issue) => `${issue.path.join(".")}: ${issue.message}`).join("; ");
    throw new Error(`INVALID_ENVIRONMENT: ${details}`);
  }

  const value = parsed.data;
  if (value.NODE_ENV === "production" && value.JWT_SECRET === DEV_SECRET) {
    throw new Error("INSECURE_CONFIGURATION: JWT_SECRET default tidak boleh dipakai di production");
  }
  if (value.NODE_ENV === "production" && value.JWT_SECRET.length < 32) {
    throw new Error("INSECURE_CONFIGURATION: JWT_SECRET minimal 32 karakter");
  }

  return {
    nodeEnv: value.NODE_ENV,
    port: value.PORT,
    host: value.HOST,
    webOrigin: value.WEB_ORIGIN,
    logLevel: value.LOG_LEVEL,
    jwtSecret: value.JWT_SECRET,
    accessTokenTtlSeconds: value.ACCESS_TOKEN_TTL_SECONDS,
    refreshTokenTtlDays: value.REFRESH_TOKEN_TTL_DAYS,
    sqlitePath: value.SQLITE_PATH,
    mqttUrl: value.MQTT_URL,
    mqttUsername: value.MQTT_USERNAME,
    mqttPassword: value.MQTT_PASSWORD,
    mqttTlsRejectUnauthorized: value.MQTT_TLS_REJECT_UNAUTHORIZED,
    telegramBotToken: value.TELEGRAM_BOT_TOKEN,
    telegramChatId: value.TELEGRAM_CHAT_ID,
    defaultTimeZone: value.DEFAULT_TIMEZONE,
    rateLimitEnabled: value.RATE_LIMIT_ENABLED,
    seedDemo: env.SEED_DEMO === undefined ? value.NODE_ENV !== "production" : value.SEED_DEMO
  };
}

export function testConfig(overrides: Partial<AppConfig> = {}): AppConfig {
  return {
    nodeEnv: "test",
    port: 0,
    host: "127.0.0.1",
    webOrigin: "http://localhost:3000",
    logLevel: "silent",
    jwtSecret: "test-secret-that-is-at-least-32-characters-long",
    accessTokenTtlSeconds: 900,
    refreshTokenTtlDays: 7,
    sqlitePath: ":memory:",
    mqttUrl: "mqtt://localhost:1883",
    mqttUsername: undefined,
    mqttPassword: undefined,
    mqttTlsRejectUnauthorized: true,
    telegramBotToken: undefined,
    telegramChatId: undefined,
    defaultTimeZone: "Asia/Jakarta",
    rateLimitEnabled: false,
    seedDemo: false,
    ...overrides
  };
}
