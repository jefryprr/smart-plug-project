-- Down migration for 001_init.sql. Destructive: use only in disposable/dev DBs.
BEGIN;

DROP TABLE IF EXISTS system_jobs;
DROP TABLE IF EXISTS audit_events;
DROP TABLE IF EXISTS push_tokens;
DROP TABLE IF EXISTS user_notifications;
DROP TABLE IF EXISTS fault_events;
DROP TABLE IF EXISTS firmware_releases;
DROP TABLE IF EXISTS device_firmware_versions;
DROP TABLE IF EXISTS automation_rules;
DROP TABLE IF EXISTS energy_budgets;
DROP TABLE IF EXISTS electricity_tariffs;
DROP TABLE IF EXISTS monthly_energy_aggregates;
DROP TABLE IF EXISTS weekly_energy_aggregates;
DROP TABLE IF EXISTS daily_energy_aggregates;
DROP TABLE IF EXISTS energy_counter_segments;
DROP TABLE IF EXISTS telemetry_samples;
DROP TABLE IF EXISTS idempotency_keys;
DROP TABLE IF EXISTS device_commands;
DROP TABLE IF EXISTS device_state_snapshots;
DROP TABLE IF EXISTS device_claims;
DROP TABLE IF EXISTS device_credentials;
DROP TABLE IF EXISTS devices;
DROP TABLE IF EXISTS memberships;
DROP TABLE IF EXISTS homes;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS users;

COMMIT;
