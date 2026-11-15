import { randomUUID } from "node:crypto";
import type { AppDb } from "../db/index.js";
import type { AnalyticsBucket, AnalyticsResponse } from "@smartplug/api-contract";
import { conflict, validationError } from "../errors.js";

export interface DailyAggregateRow {
  day: string;
  energy_kwh: number;
  cost_idr: number | null;
  sample_count: number;
  gap_count: number;
}

export interface TariffRow {
  tariff_id: string;
  device_id: string;
  currency: string;
  idr_per_kwh: number;
  effective_from: string;
  effective_to: string | null;
  created_at: string;
}

function getPart(parts: Intl.DateTimeFormatPart[], type: string): string {
  return parts.find((part) => part.type === type)?.value ?? "";
}

export function dateKeyInTimeZone(iso: string, timeZone: string): string {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit"
  }).formatToParts(new Date(iso));
  return `${getPart(parts, "year")}-${getPart(parts, "month")}-${getPart(parts, "day")}`;
}

export function hourKeyInTimeZone(iso: string, timeZone: string): string {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    hour12: false
  }).formatToParts(new Date(iso));
  return `${getPart(parts, "year")}-${getPart(parts, "month")}-${getPart(parts, "day")}T${getPart(parts, "hour").padStart(2, "0")}`;
}

function timeZoneOffsetMs(date: Date, timeZone: string): number {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false
  }).formatToParts(date);
  const asUtc = Date.UTC(
    Number(getPart(parts, "year")),
    Number(getPart(parts, "month")) - 1,
    Number(getPart(parts, "day")),
    Number(getPart(parts, "hour")) % 24,
    Number(getPart(parts, "minute")),
    Number(getPart(parts, "second"))
  );
  return asUtc - date.getTime();
}

/**
 * Convert a local wall-clock date/time in an IANA timezone to UTC.
 * Iterates twice to handle ordinary DST offsets. Ambiguous/nonexistent DST
 * instants remain an engineering edge case and are documented in the test plan.
 */
export function zonedDateTimeToUtc(dateKey: string, timeText: string, timeZone: string): Date {
  const [yearText, monthText, dayText] = dateKey.split("-");
  const [hourText, minuteText] = timeText.split(":");
  const year = Number(yearText);
  const month = Number(monthText);
  const day = Number(dayText);
  const hour = Number(hourText);
  const minute = Number(minuteText);
  if (![year, month, day, hour, minute].every(Number.isFinite)) {
    throw new Error(`INVALID_ZONED_DATE:${dateKey}T${timeText}`);
  }
  let candidate = Date.UTC(year, month - 1, day, hour, minute, 0);
  for (let iteration = 0; iteration < 3; iteration += 1) {
    const offset = timeZoneOffsetMs(new Date(candidate), timeZone);
    const corrected = Date.UTC(year, month - 1, day, hour, minute, 0) - offset;
    if (corrected === candidate) break;
    candidate = corrected;
  }
  return new Date(candidate);
}

export function addDaysToDateKey(dateKey: string, days: number): string {
  const date = new Date(`${dateKey}T00:00:00.000Z`);
  date.setUTCDate(date.getUTCDate() + days);
  return date.toISOString().slice(0, 10);
}

export function enumerateDateKeys(fromKey: string, toKey: string, max = 400): string[] {
  const keys: string[] = [];
  let current = fromKey;
  while (current <= toKey && keys.length < max) {
    keys.push(current);
    current = addDaysToDateKey(current, 1);
  }
  return keys;
}

export function weekStartDateKey(dateKey: string): string {
  const date = new Date(`${dateKey}T00:00:00.000Z`);
  const dayOfWeek = date.getUTCDay();
  const diff = (dayOfWeek + 6) % 7; // Monday = 0
  date.setUTCDate(date.getUTCDate() - diff);
  return date.toISOString().slice(0, 10);
}

export function getTariffAt(db: AppDb, deviceId: string, at: string): TariffRow | null {
  const row = db.get<TariffRow>(
    `SELECT tariff_id, device_id, currency, idr_per_kwh, effective_from, effective_to, created_at
       FROM electricity_tariffs
      WHERE device_id = ?
        AND effective_from <= ?
        AND (effective_to IS NULL OR effective_to > ?)
      ORDER BY effective_from DESC
      LIMIT 1`,
    deviceId,
    at,
    at
  );
  return row ?? null;
}

export function listTariffs(db: AppDb, deviceId: string): TariffRow[] {
  return db.all<TariffRow>(
    `SELECT tariff_id, device_id, currency, idr_per_kwh, effective_from, effective_to, created_at
       FROM electricity_tariffs
      WHERE device_id = ?
      ORDER BY effective_from ASC`,
    deviceId
  );
}

export function addTariff(
  db: AppDb,
  deviceId: string,
  idrPerKwh: number,
  effectiveFrom: string,
  now: Date
): TariffRow {
  const latest = db.get<TariffRow>(
    `SELECT tariff_id, device_id, currency, idr_per_kwh, effective_from, effective_to, created_at
       FROM electricity_tariffs
      WHERE device_id = ?
      ORDER BY effective_from DESC
      LIMIT 1`,
    deviceId
  );
  if (latest && effectiveFrom <= latest.effective_from) {
    throw conflict("TARIFF_OVERLAP", "Tarif baru harus efektif setelah tarif terakhir; histori tidak diubah diam-diam");
  }

  return db.transaction(() => {
    if (latest && latest.effective_to === null) {
      db.run(
        `UPDATE electricity_tariffs SET effective_to = ? WHERE tariff_id = ?`,
        effectiveFrom,
        latest.tariff_id
      );
    }
    const tariffId = randomUUID();
    db.run(
      `INSERT INTO electricity_tariffs (tariff_id, device_id, currency, idr_per_kwh, effective_from, effective_to, created_at)
       VALUES (?, ?, 'IDR', ?, ?, NULL, ?)`,
      tariffId,
      deviceId,
      idrPerKwh,
      effectiveFrom,
      now.toISOString()
    );
    const created = db.get<TariffRow>(
      `SELECT tariff_id, device_id, currency, idr_per_kwh, effective_from, effective_to, created_at
         FROM electricity_tariffs WHERE tariff_id = ?`,
      tariffId
    );
    if (!created) {
      throw new Error("TARIFF_INSERT_FAILED");
    }
    return created;
  });
}

export function applyIntervalToDailyAggregate(
  db: AppDb,
  deviceId: string,
  startAt: string,
  deltaKwh: number,
  gap: boolean,
  sampleCount: number,
  now: Date,
  timeZone: string
): void {
  const day = dateKeyInTimeZone(startAt, timeZone);
  const tariff = deltaKwh > 0 ? getTariffAt(db, deviceId, startAt) : null;
  const cost = deltaKwh === 0 ? 0 : tariff ? deltaKwh * tariff.idr_per_kwh : null;
  db.run(
    `INSERT INTO daily_energy_aggregates (device_id, day, energy_kwh, cost_idr, sample_count, gap_count, updated_at)
     VALUES (?, ?, ?, ?, ?, ?, ?)
     ON CONFLICT(device_id, day) DO UPDATE SET
       energy_kwh = daily_energy_aggregates.energy_kwh + excluded.energy_kwh,
       cost_idr = CASE
         WHEN daily_energy_aggregates.cost_idr IS NULL OR excluded.cost_idr IS NULL THEN NULL
         ELSE daily_energy_aggregates.cost_idr + excluded.cost_idr
       END,
       sample_count = daily_energy_aggregates.sample_count + excluded.sample_count,
       gap_count = daily_energy_aggregates.gap_count + excluded.gap_count,
       updated_at = excluded.updated_at`,
    deviceId,
    day,
    deltaKwh,
    cost,
    sampleCount,
    gap ? 1 : 0,
    now.toISOString()
  );
}

interface BucketAccumulator {
  startKey: string;
  endKey: string;
  label: string;
  energyKwh: number;
  costIdr: number | null;
  sampleCount: number;
  gapCount: number;
  hasData: boolean;
}

function finalizeBucket(accumulator: BucketAccumulator, timeZone: string): AnalyticsBucket {
  return {
    period_start: zonedDateTimeToUtc(accumulator.startKey, "00:00", timeZone).toISOString(),
    period_end: zonedDateTimeToUtc(accumulator.endKey, "00:00", timeZone).toISOString(),
    label: accumulator.label,
    energy_kwh: accumulator.hasData ? accumulator.energyKwh : null,
    cost_idr: accumulator.hasData ? accumulator.costIdr : null,
    sample_count: accumulator.sampleCount,
    gap_count: accumulator.gapCount,
    data_available: accumulator.hasData
  };
}

function emptyAccumulator(startKey: string, endKey: string, label: string): BucketAccumulator {
  return {
    startKey,
    endKey,
    label,
    energyKwh: 0,
    costIdr: 0,
    sampleCount: 0,
    gapCount: 0,
    hasData: false
  };
}

function addRowToAccumulator(accumulator: BucketAccumulator, row: DailyAggregateRow): void {
  accumulator.hasData = true;
  accumulator.energyKwh += row.energy_kwh;
  accumulator.sampleCount += row.sample_count;
  accumulator.gapCount += row.gap_count;
  if (row.cost_idr === null) {
    accumulator.costIdr = null;
  } else if (accumulator.costIdr !== null) {
    accumulator.costIdr += row.cost_idr;
  }
}

export interface AnalyticsOptions {
  from: string;
  to: string;
  granularity: "hour" | "day" | "week" | "month";
  timeZone: string;
}

export function getAnalytics(db: AppDb, deviceId: string, options: AnalyticsOptions): AnalyticsResponse {
  const fromMs = new Date(options.from).getTime();
  const toMs = new Date(options.to).getTime();
  if (!Number.isFinite(fromMs) || !Number.isFinite(toMs) || fromMs >= toMs) {
    throw validationError("Rentang from/to tidak valid");
  }
  if (toMs - fromMs > 400 * 24 * 60 * 60 * 1000) {
    throw validationError("Rentang analytics maksimum 400 hari");
  }

  let buckets: AnalyticsBucket[] = [];

  if (options.granularity === "hour") {
    const intervals = db.all<{
      start_at: string;
      delta_kwh: number;
      gap: number;
      reason_code: string;
    }>(
      `SELECT start_at, delta_kwh, gap, reason_code
         FROM energy_intervals
        WHERE device_id = ? AND start_at >= ? AND start_at < ?
        ORDER BY start_at ASC`,
      deviceId,
      options.from,
      options.to
    );
    const map = new Map<string, BucketAccumulator>();
    const tariffCache = new Map<string, TariffRow | null>();
    for (const interval of intervals) {
      const hourKey = hourKeyInTimeZone(interval.start_at, options.timeZone);
      const dateKey = hourKey.slice(0, 10);
      const hour = Number(hourKey.slice(11, 13));
      const nextHour = String((hour + 1) % 24).padStart(2, "0");
      const endKey = hour === 23 ? addDaysToDateKey(dateKey, 1) : dateKey;
      const accumulator =
        map.get(hourKey) ??
        emptyAccumulator(
          dateKey,
          endKey,
          `${dateKey} ${String(hour).padStart(2, "0")}:00`
        );
      accumulator.startKey = dateKey;
      accumulator.endKey = endKey;
      accumulator.label = `${dateKey} ${String(hour).padStart(2, "0")}:00`;
      if (interval.gap) {
        accumulator.hasData = true;
        accumulator.gapCount += 1;
      } else if (interval.delta_kwh > 0) {
        accumulator.hasData = true;
        accumulator.energyKwh += interval.delta_kwh;
        if (!tariffCache.has(interval.start_at)) {
          tariffCache.set(interval.start_at, getTariffAt(db, deviceId, interval.start_at));
        }
        const tariff = tariffCache.get(interval.start_at) ?? null;
        if (!tariff) {
          accumulator.costIdr = null;
        } else if (accumulator.costIdr !== null) {
          accumulator.costIdr += interval.delta_kwh * tariff.idr_per_kwh;
        }
      }
      map.set(hourKey, accumulator);
    }
    buckets = [...map.values()].map((accumulator) => finalizeBucket(accumulator, options.timeZone));
  } else {
    const fromKey = dateKeyInTimeZone(options.from, options.timeZone);
    const toKey = dateKeyInTimeZone(options.to, options.timeZone);
    const rows = db.all<DailyAggregateRow>(
      `SELECT day, energy_kwh, cost_idr, sample_count, gap_count
         FROM daily_energy_aggregates
        WHERE device_id = ? AND day >= ? AND day <= ?
        ORDER BY day ASC`,
      deviceId,
      fromKey,
      toKey
    );
    const rowByDay = new Map(rows.map((row) => [row.day, row]));

    if (options.granularity === "day") {
      for (const day of enumerateDateKeys(fromKey, toKey)) {
        const accumulator = emptyAccumulator(day, addDaysToDateKey(day, 1), day);
        const row = rowByDay.get(day);
        if (row) addRowToAccumulator(accumulator, row);
        buckets.push(finalizeBucket(accumulator, options.timeZone));
      }
    } else if (options.granularity === "week") {
      const firstWeek = weekStartDateKey(fromKey);
      const lastWeek = weekStartDateKey(toKey);
      for (let weekStart = firstWeek; weekStart <= lastWeek; weekStart = addDaysToDateKey(weekStart, 7)) {
        const weekEnd = addDaysToDateKey(weekStart, 7);
        const accumulator = emptyAccumulator(weekStart, weekEnd, weekStart);
        for (const row of rows) {
          if (row.day >= weekStart && row.day < weekEnd) {
            addRowToAccumulator(accumulator, row);
          }
        }
        buckets.push(finalizeBucket(accumulator, options.timeZone));
      }
    } else {
      const months = new Set<string>();
      for (const day of enumerateDateKeys(fromKey, toKey)) {
        months.add(day.slice(0, 7));
      }
      for (const month of [...months].sort()) {
        const monthStart = `${month}-01`;
        const [yearText, monthText] = month.split("-");
        const nextMonthDate = new Date(Date.UTC(Number(yearText), Number(monthText), 1));
        const nextMonth = nextMonthDate.toISOString().slice(0, 7);
        const monthEnd = `${nextMonth}-01`;
        const accumulator = emptyAccumulator(monthStart, monthEnd, month);
        for (const row of rows) {
          if (row.day.startsWith(month)) {
            addRowToAccumulator(accumulator, row);
          }
        }
        buckets.push(finalizeBucket(accumulator, options.timeZone));
      }
    }
  }

  const dataBuckets = buckets.filter((bucket) => bucket.data_available);
  const dataAvailable = dataBuckets.length > 0;
  const totalEnergy = dataAvailable
    ? dataBuckets.reduce((total, bucket) => total + (bucket.energy_kwh ?? 0), 0)
    : null;
  const knownCosts = dataBuckets.filter((bucket) => bucket.cost_idr !== null);
  const totalCost = dataAvailable
    ? knownCosts.reduce((total, bucket) => total + (bucket.cost_idr ?? 0), 0)
    : null;
  const missingTariffBuckets = dataBuckets.filter(
    (bucket) => (bucket.energy_kwh ?? 0) > 0 && bucket.cost_idr === null
  ).length;

  return {
    device_id: deviceId,
    from: options.from,
    to: options.to,
    granularity: options.granularity,
    time_zone: options.timeZone,
    data_available: dataAvailable,
    total_energy_kwh: totalEnergy,
    total_cost_idr: totalCost,
    missing_tariff_buckets: missingTariffBuckets,
    buckets
  };
}
