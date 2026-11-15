import { randomUUID } from "node:crypto";
import type { FastifyInstance } from "fastify";
import { z } from "zod";
import {
  ClaimDeviceRequestSchema,
  LoginRequestSchema,
  type ClaimDeviceResponse,
  type LoginResponse,
  type MeResponse
} from "@smartplug/api-contract";
import { sha256, verifyPassword } from "../auth/password.js";
import { createSession, findSessionByRefreshToken, revokeSession, rotateSession, sessionIsValid } from "../auth/sessions.js";
import { signAccessToken } from "../auth/tokens.js";
import { requireAuthUser } from "../auth/middleware.js";
import { conflict, unauthorized } from "../errors.js";
import { appendAudit } from "../services/audit.js";
import { parseBody, type RouteDeps } from "./helpers.js";

const RefreshRequestSchema = z.object({ refresh_token: z.string().min(20) }).strict();

interface UserRow {
  user_id: string;
  email: string;
  password_hash: string;
  display_name: string;
}

export function registerAuthRoutes(app: FastifyInstance, deps: RouteDeps): void {
  const { db, config, authenticate } = deps;

  app.post(
    "/api/v1/auth/login",
    {
      config: config.rateLimitEnabled ? { rateLimit: { max: 5, timeWindow: "1 minute" } } : {}
    },
    async (request) => {
      const body = parseBody(LoginRequestSchema, request.body);
      const user = db.get<UserRow>(
        `SELECT user_id, email, password_hash, display_name FROM users WHERE email = ?`,
        body.email.toLowerCase()
      );
      if (!user || !verifyPassword(body.password, user.password_hash)) {
        throw unauthorized("Email atau password salah");
      }
      const session = createSession(db, user.user_id, config.refreshTokenTtlDays, deps.now());
      const accessToken = await signAccessToken(
        { userId: user.user_id, email: user.email, sessionId: session.sessionId },
        config
      );
      appendAudit(db, {
        actorId: user.user_id,
        action: "auth.login",
        objectType: "session",
        objectId: session.sessionId,
        now: deps.now()
      });
      const response: LoginResponse = {
        access_token: accessToken,
        refresh_token: session.refreshToken,
        token_type: "Bearer",
        expires_in: config.accessTokenTtlSeconds
      };
      return response;
    }
  );

  app.post(
    "/api/v1/auth/refresh",
    {
      config: config.rateLimitEnabled ? { rateLimit: { max: 20, timeWindow: "1 minute" } } : {}
    },
    async (request) => {
      const body = parseBody(RefreshRequestSchema, request.body);
      const session = findSessionByRefreshToken(db, body.refresh_token);
      if (!session || !sessionIsValid(session, deps.now())) {
        throw unauthorized("Refresh token tidak valid atau sudah dicabut");
      }
      const user = db.get<UserRow>(
        `SELECT user_id, email, password_hash, display_name FROM users WHERE user_id = ?`,
        session.user_id
      );
      if (!user) {
        throw unauthorized("Pengguna tidak ditemukan");
      }
      const rotated = rotateSession(db, session, config.refreshTokenTtlDays, deps.now());
      const accessToken = await signAccessToken(
        { userId: user.user_id, email: user.email, sessionId: rotated.sessionId },
        config
      );
      appendAudit(db, {
        actorId: user.user_id,
        action: "auth.refresh",
        objectType: "session",
        objectId: rotated.sessionId,
        now: deps.now()
      });
      const response: LoginResponse = {
        access_token: accessToken,
        refresh_token: rotated.refreshToken,
        token_type: "Bearer",
        expires_in: config.accessTokenTtlSeconds
      };
      return response;
    }
  );

  app.post("/api/v1/auth/logout", { preHandler: authenticate }, async (request, reply) => {
    const user = requireAuthUser(request);
    revokeSession(db, user.sessionId, deps.now());
    appendAudit(db, {
      actorId: user.userId,
      action: "auth.logout",
      objectType: "session",
      objectId: user.sessionId,
      now: deps.now()
    });
    return reply.status(204).send();
  });

  app.get("/api/v1/me", { preHandler: authenticate }, async (request) => {
    const user = requireAuthUser(request);
    const profile = db.get<UserRow>(
      `SELECT user_id, email, password_hash, display_name FROM users WHERE user_id = ?`,
      user.userId
    );
    if (!profile) {
      throw unauthorized("Pengguna tidak ditemukan");
    }
    const homes = db.all<{ home_id: string; name: string; role: "owner" | "admin" | "viewer" }>(
      `SELECT h.home_id, h.name, m.role
         FROM homes h
         JOIN memberships m ON m.home_id = h.home_id
        WHERE m.user_id = ?
        ORDER BY h.created_at ASC`,
      user.userId
    );
    const response: MeResponse = {
      user_id: profile.user_id,
      email: profile.email,
      display_name: profile.display_name,
      homes
    };
    return response;
  });

  app.post("/api/v1/device-claims", { preHandler: authenticate }, async (request, reply) => {
    const user = requireAuthUser(request);
    const body = parseBody(ClaimDeviceRequestSchema, request.body);
    const claim = db.get<{
      claim_id: string;
      device_id: string;
      expires_at: string;
      claimed_at: string | null;
      home_id: string;
    }>(
      `SELECT c.claim_id, c.device_id, c.expires_at, c.claimed_at, d.home_id
         FROM device_claims c
         JOIN devices d ON d.device_id = c.device_id
        WHERE c.pairing_code_hash = ?`,
      sha256(body.pairing_code)
    );
    if (!claim || claim.claimed_at !== null) {
      throw conflict("PAIRING_INVALID", "Kode pairing tidak valid atau sudah dipakai");
    }
    if (new Date(claim.expires_at).getTime() <= deps.now().getTime()) {
      throw conflict("PAIRING_EXPIRED", "Kode pairing sudah kedaluwarsa");
    }

    db.transaction(() => {
      db.run(
        `UPDATE device_claims SET claimed_at = ?, claimed_by = ? WHERE claim_id = ? AND claimed_at IS NULL`,
        deps.now().toISOString(),
        user.userId,
        claim.claim_id
      );
      const existingMembership = db.get<{ role: string }>(
        `SELECT role FROM memberships WHERE home_id = ? AND user_id = ?`,
        claim.home_id,
        user.userId
      );
      if (!existingMembership) {
        db.run(
          `INSERT INTO memberships (home_id, user_id, role, created_at) VALUES (?, ?, 'owner', ?)`,
          claim.home_id,
          user.userId,
          deps.now().toISOString()
        );
      }
      if (body.device_name) {
        db.run(`UPDATE devices SET name = ? WHERE device_id = ?`, body.device_name, claim.device_id);
      }
      appendAudit(db, {
        actorId: user.userId,
        action: "device.claimed",
        objectType: "device",
        objectId: claim.device_id,
        metadata: { claim_id: claim.claim_id },
        now: deps.now()
      });
    });

    const response: ClaimDeviceResponse = {
      device_id: claim.device_id,
      home_id: claim.home_id,
      claimed_at: deps.now().toISOString()
    };
    return reply.status(201).send(response);
  });
}
