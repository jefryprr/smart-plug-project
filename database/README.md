# Database

**Target:** PostgreSQL 16 for staging/production.
**Local test adapter:** the API uses Node's built-in SQLite (`node:sqlite`) so the test suite can run without Docker/Postgres. The SQLite schema is in `apps/api/src/db/schema.ts`; it mirrors the core tables but is not the production target.

## Migrations

```bash
psql "$DATABASE_URL" -f database/migrations/001_init.sql
psql "$DATABASE_URL" -f database/migrations/002_indexes.sql
```

- Down migration: `database/migrations/down/001_init.down.sql` (destructive; disposable DBs only).
- Seed (DEV ONLY): `database/seeds/demo.sql` — demo password `demo1234`, pairing `123456`. Never run in production.

## Rules

- All timestamps are UTC `timestamptz`; UI converts to `Asia/Jakarta`.
- Tenant-scoped rows are filtered through `memberships` and object-level checks.
- Energy is stored as cumulative meter counter plus delta segments; never sum raw counters.
- `cost_idr` can be NULL when a tariff is missing; NULL means "not computed", not Rp0.
- Audit events are append-only at the application layer.
- Migrations must be reviewed and backed up before production.
- The API's SQLite adapter is a development/test convenience, not a claim that PostgreSQL migrations were executed here.
