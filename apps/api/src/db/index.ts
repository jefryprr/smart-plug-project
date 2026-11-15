import { mkdirSync } from "node:fs";
import { dirname } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { SCHEMA_SQL } from "./schema.js";

export type Row = Record<string, unknown>;

export class AppDb {
  readonly db: DatabaseSync;

  constructor(path: string) {
    if (path !== ":memory:") {
      mkdirSync(dirname(path), { recursive: true });
    }
    this.db = new DatabaseSync(path);
    this.db.exec("PRAGMA foreign_keys = ON");
    this.db.exec("PRAGMA busy_timeout = 5000");
  }

  migrate(): void {
    this.db.exec(SCHEMA_SQL);
  }

  transaction<T>(work: () => T): T {
    this.db.exec("BEGIN IMMEDIATE");
    try {
      const result = work();
      this.db.exec("COMMIT");
      return result;
    } catch (error) {
      this.db.exec("ROLLBACK");
      throw error;
    }
  }

  get<T = Row>(sql: string, ...params: Array<string | number | null>): T | undefined {
    const statement = this.db.prepare(sql);
    return statement.get(...params) as T | undefined;
  }

  all<T = Row>(sql: string, ...params: Array<string | number | null>): T[] {
    const statement = this.db.prepare(sql);
    return statement.all(...params) as T[];
  }

  run(sql: string, ...params: Array<string | number | null>): void {
    const statement = this.db.prepare(sql);
    statement.run(...params);
  }

  close(): void {
    this.db.close();
  }
}

export function nowIso(now: () => Date = () => new Date()): string {
  return now().toISOString();
}

export function rowString(row: Row | undefined, key: string): string | null {
  if (!row) return null;
  const value = row[key];
  return typeof value === "string" ? value : null;
}

export function rowNumber(row: Row | undefined, key: string): number | null {
  if (!row) return null;
  const value = row[key];
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}
