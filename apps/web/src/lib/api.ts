import { z } from "zod";
import {
  AnalyticsResponseSchema,
  AutomationsResponseSchema,
  BudgetSchema,
  ClaimDeviceResponseSchema,
  CommandResponseSchema,
  DeviceDetailSchema,
  DeviceSummarySchema,
  DiagnosticsResponseSchema,
  EventsResponseSchema,
  LoginResponseSchema,
  MeResponseSchema,
  TariffSchema,
  TelemetryListResponseSchema,
  type AnalyticsResponse,
  type AutomationsRequest,
  type AutomationsResponse,
  type Budget,
  type ClaimDeviceResponse,
  type CommandResponse,
  type DeviceDetail,
  type DeviceSummary,
  type DiagnosticsResponse,
  type EventsResponse,
  type LoginResponse,
  type MeResponse,
  type Tariff,
  type TelemetryListResponse
} from "@smartplug/api-contract";
import { clearTokens, getTokens, setTokens } from "./token-store";

const BASE = "/api/backend";

export class ApiClientError extends Error {
  readonly status: number;
  readonly code: string;
  readonly details: unknown;

  constructor(status: number, code: string, message: string, details?: unknown) {
    super(message);
    this.name = "ApiClientError";
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

interface RequestOptions {
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  body?: unknown;
  auth?: boolean;
  retry?: boolean;
}

async function refreshTokens(): Promise<boolean> {
  const { refresh } = getTokens();
  if (!refresh) return false;
  const response = await fetch(`${BASE}/v1/auth/refresh`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ refresh_token: refresh })
  });
  if (!response.ok) {
    clearTokens();
    return false;
  }
  const body = LoginResponseSchema.safeParse(await response.json());
  if (!body.success) {
    clearTokens();
    return false;
  }
  setTokens(body.data.access_token, body.data.refresh_token);
  return true;
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { access } = getTokens();
  const headers: Record<string, string> = {};
  if (options.body !== undefined) {
    headers["content-type"] = "application/json";
  }
  if (options.auth !== false && access) {
    headers.authorization = `Bearer ${access}`;
  }

  const response = await fetch(`${BASE}${path}`, {
    method: options.method ?? "GET",
    headers,
    body: options.body === undefined ? undefined : JSON.stringify(options.body),
    cache: "no-store"
  });

  if (response.status === 401 && options.auth !== false && options.retry !== false) {
    const refreshed = await refreshTokens();
    if (refreshed) {
      return request<T>(path, { ...options, retry: false });
    }
  }

  if (!response.ok) {
    let code = "HTTP_ERROR";
    let message = `Permintaan gagal (${response.status})`;
    let details: unknown;
    try {
      const body = (await response.json()) as { error?: { code?: string; message?: string; details?: unknown } };
      code = body.error?.code ?? code;
      message = body.error?.message ?? message;
      details = body.error?.details;
    } catch {
      // Keep the generic message.
    }
    throw new ApiClientError(response.status, code, message, details);
  }

  if (response.status === 204) {
    return undefined as T;
  }
  return (await response.json()) as T;
}

function parseOrThrow<T>(schema: z.ZodType<T>, value: unknown, label: string): T {
  const parsed = schema.safeParse(value);
  if (!parsed.success) {
    throw new ApiClientError(502, "CONTRACT_MISMATCH", `Respons ${label} tidak sesuai kontrak`, parsed.error.issues);
  }
  return parsed.data;
}

export const api = {
  async login(email: string, password: string): Promise<LoginResponse> {
    const raw = await request<unknown>("/v1/auth/login", {
      method: "POST",
      auth: false,
      body: { email, password }
    });
    const parsed = parseOrThrow(LoginResponseSchema, raw, "login");
    setTokens(parsed.access_token, parsed.refresh_token);
    return parsed;
  },

  async logout(): Promise<void> {
    try {
      await request<void>("/v1/auth/logout", { method: "POST" });
    } finally {
      clearTokens();
    }
  },

  async me(): Promise<MeResponse> {
    return parseOrThrow(MeResponseSchema, await request<unknown>("/v1/me"), "profil");
  },

  async devices(): Promise<DeviceSummary[]> {
    const raw = await request<{ devices: unknown }>("/v1/devices");
    return parseOrThrow(z.array(DeviceSummarySchema), raw.devices, "daftar perangkat");
  },

  async device(deviceId: string): Promise<DeviceDetail> {
    return parseOrThrow(DeviceDetailSchema, await request<unknown>(`/v1/devices/${deviceId}`), "detail perangkat");
  },

  async renameDevice(deviceId: string, name: string, room: string | null): Promise<DeviceDetail> {
    return parseOrThrow(
      DeviceDetailSchema,
      await request<unknown>(`/v1/devices/${deviceId}`, { method: "PATCH", body: { name, room } }),
      "perubahan perangkat"
    );
  },

  async command(deviceId: string, requestedOutput: "ON" | "OFF", idempotencyKey: string): Promise<CommandResponse> {
    return parseOrThrow(
      CommandResponseSchema,
      await request<unknown>(`/v1/devices/${deviceId}/commands`, {
        method: "POST",
        body: { requested_output: requestedOutput, idempotency_key: idempotencyKey, ttl_seconds: 30 }
      }),
      "perintah"
    );
  },

  async commandStatus(deviceId: string, commandId: string): Promise<CommandResponse> {
    return parseOrThrow(
      CommandResponseSchema,
      await request<unknown>(`/v1/devices/${deviceId}/commands/${commandId}`),
      "status perintah"
    );
  },

  async telemetry(deviceId: string, limit = 60): Promise<TelemetryListResponse> {
    return parseOrThrow(
      TelemetryListResponseSchema,
      await request<unknown>(`/v1/devices/${deviceId}/telemetry?limit=${limit}`),
      "telemetry"
    );
  },

  async analytics(
    deviceId: string,
    from: string,
    to: string,
    granularity: "hour" | "day" | "week" | "month"
  ): Promise<AnalyticsResponse> {
    const params = new URLSearchParams({ from, to, granularity, timezone: "Asia/Jakarta" });
    return parseOrThrow(
      AnalyticsResponseSchema,
      await request<unknown>(`/v1/devices/${deviceId}/analytics?${params.toString()}`),
      "analytics"
    );
  },

  async events(deviceId: string, limit = 50): Promise<EventsResponse> {
    return parseOrThrow(
      EventsResponseSchema,
      await request<unknown>(`/v1/devices/${deviceId}/events?limit=${limit}`),
      "event"
    );
  },

  async diagnostics(deviceId: string): Promise<DiagnosticsResponse> {
    return parseOrThrow(
      DiagnosticsResponseSchema,
      await request<unknown>(`/v1/devices/${deviceId}/diagnostics`),
      "diagnostik"
    );
  },

  async automations(deviceId: string): Promise<AutomationsResponse> {
    return parseOrThrow(
      AutomationsResponseSchema,
      await request<unknown>(`/v1/devices/${deviceId}/automations`),
      "jadwal"
    );
  },

  async saveAutomations(deviceId: string, body: AutomationsRequest): Promise<AutomationsResponse> {
    return parseOrThrow(
      AutomationsResponseSchema,
      await request<unknown>(`/v1/devices/${deviceId}/automations`, { method: "PUT", body }),
      "jadwal"
    );
  },

  async tariffs(deviceId: string): Promise<Tariff[]> {
    const raw = await request<{ tariffs: unknown }>(`/v1/devices/${deviceId}/tariff`);
    return parseOrThrow(z.array(TariffSchema), raw.tariffs, "tarif");
  },

  async addTariff(deviceId: string, idrPerKwh: number, effectiveFrom: string): Promise<Tariff> {
    return parseOrThrow(
      TariffSchema,
      await request<unknown>(`/v1/devices/${deviceId}/tariff`, {
        method: "PUT",
        body: { idr_per_kwh: idrPerKwh, effective_from: effectiveFrom }
      }),
      "tarif"
    );
  },

  async budget(deviceId: string): Promise<Budget> {
    return parseOrThrow(BudgetSchema, await request<unknown>(`/v1/devices/${deviceId}/budget`), "anggaran");
  },

  async saveBudget(
    deviceId: string,
    body: { period: "daily" | "weekly" | "monthly"; kwh_limit: number | null; idr_limit: number | null; enabled: boolean }
  ): Promise<Budget> {
    return parseOrThrow(
      BudgetSchema,
      await request<unknown>(`/v1/devices/${deviceId}/budget`, { method: "PUT", body }),
      "anggaran"
    );
  },

  async testNotification(deviceId: string): Promise<{ notification_id: string; provider: string; status: string }> {
    return request(`/v1/devices/${deviceId}/notifications/test`, { method: "POST" });
  },

  async requestOta(deviceId: string, releaseId: string): Promise<{ command_id: string; status: string }> {
    return request(`/v1/devices/${deviceId}/ota`, { method: "POST", body: { release_id: releaseId } });
  },

  async revoke(deviceId: string): Promise<void> {
    await request<void>(`/v1/devices/${deviceId}/revoke`, { method: "POST" });
  },

  async claim(pairingCode: string, deviceName?: string): Promise<ClaimDeviceResponse> {
    return parseOrThrow(
      ClaimDeviceResponseSchema,
      await request<unknown>("/v1/device-claims", {
        method: "POST",
        body: { pairing_code: pairingCode, ...(deviceName ? { device_name: deviceName } : {}) }
      }),
      "pairing"
    );
  }
};
