import type { AuthUser } from "./auth/tokens.js";

declare module "fastify" {
  interface FastifyRequest {
    authUser: AuthUser | null;
  }
}
