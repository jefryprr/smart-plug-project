"use client";

import { useCallback, useEffect, useState } from "react";
import type {
  AnalyticsResponse,
  AutomationsResponse,
  Budget,
  DeviceDetail,
  DeviceSummary,
  DiagnosticsResponse,
  EventsResponse,
  Tariff,
  TelemetryListResponse
} from "@smartplug/api-contract";
import { api } from "./api";

export interface ResourceState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  reload: () => Promise<void>;
}

export function errorMessage(error: unknown): string {
  if (error instanceof Error) return error.message;
  return "Terjadi kesalahan yang tidak diketahui";
}

export function useResource<T>(
  loader: () => Promise<T>,
  deps: ReadonlyArray<unknown>,
  intervalMs = 0
): ResourceState<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const run = useCallback(async () => {
    try {
      const value = await loader();
      setData(value);
      setError(null);
    } catch (caught) {
      setError(errorMessage(caught));
    } finally {
      setLoading(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  useEffect(() => {
    let active = true;
    const execute = async (): Promise<void> => {
      try {
        const value = await loader();
        if (!active) return;
        setData(value);
        setError(null);
      } catch (caught) {
        if (!active) return;
        setError(errorMessage(caught));
      } finally {
        if (active) setLoading(false);
      }
    };
    void execute();
    if (intervalMs <= 0) {
      return () => {
        active = false;
      };
    }
    const timer = window.setInterval(() => {
      void execute();
    }, intervalMs);
    return () => {
      active = false;
      window.clearInterval(timer);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...deps, intervalMs]);

  return { data, loading, error, reload: run };
}

export function useDevices(): ResourceState<DeviceSummary[]> {
  return useResource(() => api.devices(), [], 5000);
}

export function useDevice(deviceId: string): ResourceState<DeviceDetail> {
  return useResource(() => api.device(deviceId), [deviceId], 5000);
}

export function useTelemetry(deviceId: string, limit = 60): ResourceState<TelemetryListResponse> {
  return useResource(() => api.telemetry(deviceId, limit), [deviceId, limit], 5000);
}

export function useAnalytics(
  deviceId: string,
  from: string,
  to: string,
  granularity: "hour" | "day" | "week" | "month"
): ResourceState<AnalyticsResponse> {
  return useResource(() => api.analytics(deviceId, from, to, granularity), [deviceId, from, to, granularity], 15000);
}

export function useEvents(deviceId: string, limit = 50): ResourceState<EventsResponse> {
  return useResource(() => api.events(deviceId, limit), [deviceId, limit], 10000);
}

export function useDiagnostics(deviceId: string): ResourceState<DiagnosticsResponse> {
  return useResource(() => api.diagnostics(deviceId), [deviceId], 10000);
}

export function useAutomations(deviceId: string): ResourceState<AutomationsResponse> {
  return useResource(() => api.automations(deviceId), [deviceId]);
}

export function useTariffs(deviceId: string): ResourceState<Tariff[]> {
  return useResource(() => api.tariffs(deviceId), [deviceId]);
}

export function useBudget(deviceId: string): ResourceState<Budget> {
  return useResource(() => api.budget(deviceId), [deviceId]);
}
