import type { FastifyRequest } from "fastify";
import type { AppConfig } from "../config.js";
import { unauthorized } from "../errors.js";
import { verifyAccessToken, type AuthUser } from "./tokens.js";

export function makeAuthenticate(config: AppConfig) {
  return async function authenticate(request: FastifyRequest): Promise<void> {
    const header = request.headers.authorization;
    if (!header || !header.startsWith("Bearer ")) {
      throw unauthorized("Header Authorization Bearer diperlukan");
    }
    const token = header.slice("Bearer ".length).trim();
    if (token.length === 0) {
      throw unauthorized("Token akses kosong");
    }
    request.authUser = await verifyAccessToken(token, config);
  };
}

export function requireAuthUser(request: FastifyRequest): AuthUser {
  if (!request.authUser) {
    throw unauthorized();
  }
  return request.authUser;
}
