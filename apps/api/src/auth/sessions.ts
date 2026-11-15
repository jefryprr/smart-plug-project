import { randomUUID } from "node:crypto";
import type { AppDb, Row } from "../db/index.js";
import { hashPassword, randomToken, sha256 } from "./password.js";

export interface SessionTokens {
  sessionId: string;
  refreshToken: string;
  expiresAt: string;
}

export function createSession(
  db: AppDb,
  userId: string,
  ttlDays: number,
  now: Date = new Date()
): SessionTokens {
  const sessionId = randomUUID();
  const refreshToken = randomToken(48);
  const expiresAt = new Date(now.getTime() + ttlDays * 24 * 60 * 60 * 1000).toISOString();
  db.run(
    `INSERT INTO sessions (session_id, user_id, refresh_token_hash, expires_at, revoked_at, created_at)
     VALUES (?, ?, ?, ?, NULL, ?)`,
    sessionId,
    userId,
    sha256(refreshToken),
    expiresAt,
    now.toISOString()
  );
  return { sessionId, refreshToken, expiresAt };
}

export interface SessionRow extends Row {
  session_id: string;
  user_id: string;
  expires_at: string;
  revoked_at: string | null;
}

export function findSessionByRefreshToken(db: AppDb, refreshToken: string): SessionRow | null {
  const row = db.get<SessionRow>(
    `SELECT session_id, user_id, expires_at, revoked_at FROM sessions WHERE refresh_token_hash = ?`,
    sha256(refreshToken)
  );
  return row ?? null;
}

export function sessionIsValid(session: SessionRow, now: Date = new Date()): boolean {
  return session.revoked_at === null && new Date(session.expires_at).getTime() > now.getTime();
}

export function revokeSession(db: AppDb, sessionId: string, now: Date = new Date()): void {
  db.run(`UPDATE sessions SET revoked_at = ? WHERE session_id = ? AND revoked_at IS NULL`, now.toISOString(), sessionId);
}

export function revokeAllUserSessions(db: AppDb, userId: string, now: Date = new Date()): void {
  db.run(`UPDATE sessions SET revoked_at = ? WHERE user_id = ? AND revoked_at IS NULL`, now.toISOString(), userId);
}

export function rotateSession(
  db: AppDb,
  oldSession: SessionRow,
  ttlDays: number,
  now: Date = new Date()
): SessionTokens {
  return db.transaction(() => {
    revokeSession(db, oldSession.session_id, now);
    return createSession(db, oldSession.user_id, ttlDays, now);
  });
}

export function ensureDemoUser(db: AppDb, email: string, password: string, displayName: string, now: Date): string {
  const existing = db.get<{ user_id: string }>(`SELECT user_id FROM users WHERE email = ?`, email);
  if (existing) {
    return existing.user_id;
  }
  const userId = randomUUID();
  db.run(
    `INSERT INTO users (user_id, email, password_hash, display_name, created_at) VALUES (?, ?, ?, ?, ?)`,
    userId,
    email,
    hashPassword(password),
    displayName,
    now.toISOString()
  );
  return userId;
}
