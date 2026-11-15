export class ApiError extends Error {
  readonly statusCode: number;
  readonly code: string;
  readonly details: unknown;

  constructor(statusCode: number, code: string, message: string, details?: unknown) {
    super(message);
    this.name = "ApiError";
    this.statusCode = statusCode;
    this.code = code;
    this.details = details;
  }
}

export function isApiError(error: unknown): error is ApiError {
  return error instanceof ApiError;
}

export function unauthorized(message = "Autentikasi diperlukan"): ApiError {
  return new ApiError(401, "UNAUTHORIZED", message);
}

export function forbidden(message = "Akses ditolak"): ApiError {
  return new ApiError(403, "FORBIDDEN", message);
}

export function notFound(message = "Sumber daya tidak ditemukan"): ApiError {
  return new ApiError(404, "NOT_FOUND", message);
}

export function conflict(code: string, message: string, details?: unknown): ApiError {
  return new ApiError(409, code, message, details);
}

export function validationError(message: string, details?: unknown): ApiError {
  return new ApiError(422, "VALIDATION_ERROR", message, details);
}

export function rateLimited(message = "Terlalu banyak permintaan"): ApiError {
  return new ApiError(429, "RATE_LIMITED", message);
}

export function downstreamUnavailable(message = "Broker atau layanan downstream tidak tersedia"): ApiError {
  return new ApiError(503, "DOWNSTREAM_UNAVAILABLE", message);
}
