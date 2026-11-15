import { SignJWT, jwtVerify } from "jose";
import type { AppConfig } from "../config.js";
import { unauthorized } from "../errors.js";

export interface AuthUser {
  userId: string;
  email: string;
  sessionId: string;
}

const ISSUER = "smartplug-api";
const AUDIENCE = "smartplug-web";

function key(secret: string): Uint8Array {
  return new TextEncoder().encode(secret);
}

export async function signAccessToken(user: AuthUser, config: AppConfig): Promise<string> {
  return new SignJWT({
    email: user.email,
    sid: user.sessionId,
    typ: "access"
  })
    .setProtectedHeader({ alg: "HS256", typ: "JWT" })
    .setSubject(user.userId)
    .setIssuer(ISSUER)
    .setAudience(AUDIENCE)
    .setIssuedAt()
    .setExpirationTime(`${config.accessTokenTtlSeconds}s`)
    .sign(key(config.jwtSecret));
}

export async function verifyAccessToken(token: string, config: AppConfig): Promise<AuthUser> {
  try {
    const verified = await jwtVerify(token, key(config.jwtSecret), {
      issuer: ISSUER,
      audience: AUDIENCE,
      clockTolerance: 5
    });
    const payload = verified.payload;
    if (payload.typ !== "access" || typeof payload.sub !== "string" || typeof payload.sid !== "string" || typeof payload.email !== "string") {
      throw new Error("INVALID_CLAIMS");
    }
    return {
      userId: payload.sub,
      email: payload.email,
      sessionId: payload.sid
    };
  } catch {
    throw unauthorized("Token akses tidak valid atau kedaluwarsa");
  }
}
