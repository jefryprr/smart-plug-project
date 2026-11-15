import type { FastifyInstance } from "fastify";
import type { CommandMessage } from "@smartplug/mqtt-contract";
import { buildApp } from "../src/app.js";
import { AppDb } from "../src/db/index.js";
import { seedDemo, type SeedResult } from "../src/seed.js";
import { testConfig } from "../src/config.js";
import type { CommandPublisher } from "../src/mqtt/publisher.js";
import { hashPassword } from "../src/auth/password.js";

export const NOW = new Date("2026-11-15T12:00:00.000Z");

export class FakePublisher implements CommandPublisher {
  readonly messages: CommandMessage[] = [];
  connected = true;

  async publishCommand(message: CommandMessage): Promise<void> {
    if (!this.connected) {
      throw new Error("MQTT_NOT_CONNECTED");
    }
    this.messages.push(message);
  }

  isConnected(): boolean {
    return this.connected;
  }
}

export interface TestContext {
  app: FastifyInstance;
  db: AppDb;
  seed: SeedResult;
  publisher: FakePublisher;
  login: (email?: string, password?: string) => Promise<string>;
  auth: (token: string) => { authorization: string };
}

export async function createTestContext(): Promise<TestContext> {
  const db = new AppDb(":memory:");
  db.migrate();
  const seed = seedDemo(db, NOW, { withSyntheticTelemetry: true });
  const publisher = new FakePublisher();
  const app = await buildApp({
    config: testConfig(),
    db,
    publisher,
    now: () => NOW
  });

  const login = async (email = "demo@example.com", password = "demo1234"): Promise<string> => {
    const response = await app.inject({
      method: "POST",
      url: "/api/v1/auth/login",
      payload: { email, password }
    });
    if (response.statusCode !== 200) {
      throw new Error(`LOGIN_FAILED:${response.statusCode}:${response.body}`);
    }
    const body = response.json<{ access_token: string }>();
    return body.access_token;
  };

  return {
    app,
    db,
    seed,
    publisher,
    login,
    auth: (token: string) => ({ authorization: `Bearer ${token}` })
  };
}

export function setDeviceState(db: AppDb, deviceId: string, overrides: Record<string, unknown>): void {
  const row = db.get<{ state_json: string }>(`SELECT state_json FROM devices WHERE device_id = ?`, deviceId);
  if (!row) throw new Error("DEVICE_NOT_FOUND");
  const current = JSON.parse(row.state_json) as Record<string, unknown>;
  db.run(
    `UPDATE devices SET state_json = ? WHERE device_id = ?`,
    JSON.stringify({ ...current, ...overrides }),
    deviceId
  );
}

export function createUserWithRole(
  db: AppDb,
  email: string,
  password: string,
  homeId: string,
  role: "owner" | "admin" | "viewer"
): string {
  const userId = `user-${role}-${Math.random().toString(36).slice(2, 10)}`;
  db.run(
    `INSERT INTO users (user_id, email, password_hash, display_name, created_at) VALUES (?, ?, ?, ?, ?)`,
    userId,
    email,
    hashPassword(password),
    `${role} user`,
    NOW.toISOString()
  );
  db.run(
    `INSERT INTO memberships (home_id, user_id, role, created_at) VALUES (?, ?, ?, ?)`,
    homeId,
    userId,
    role,
    NOW.toISOString()
  );
  return userId;
}
