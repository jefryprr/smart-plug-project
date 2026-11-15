export const SCHEMA_SQL = `
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
  user_id TEXT PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  display_name TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
  session_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  refresh_token_hash TEXT NOT NULL UNIQUE,
  expires_at TEXT NOT NULL,
  revoked_at TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS homes (
  home_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS memberships (
  home_id TEXT NOT NULL REFERENCES homes(home_id) ON DELETE CASCADE,
  user_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('owner', 'admin', 'viewer')),
  created_at TEXT NOT NULL,
  PRIMARY KEY (home_id, user_id)
);

CREATE TABLE IF NOT EXISTS devices (
  device_id TEXT PRIMARY KEY,
  home_id TEXT NOT NULL REFERENCES homes(home_id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  room TEXT,
  hardware_revision TEXT,
  firmware_version TEXT,
  data_source TEXT NOT NULL DEFAULT 'UNKNOWN' CHECK (data_source IN ('DEVICE', 'SIMULATOR', 'SYNTHETIC_DEMO', 'UNKNOWN')),
  state_json TEXT NOT NULL,
  diagnostics_json TEXT,
  last_seen_at TEXT,
  availability TEXT NOT NULL DEFAULT 'NEVER_SEEN' CHECK (availability IN ('ONLINE', 'STALE', 'OFFLINE', 'NEVER_SEEN')),
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS device_credentials (
  credential_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
  secret_hash TEXT NOT NULL,
  created_at TEXT NOT NULL,
  revoked_at TEXT
);

CREATE TABLE IF NOT EXISTS device_claims (
  claim_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL UNIQUE REFERENCES devices(device_id) ON DELETE CASCADE,
  pairing_code_hash TEXT NOT NULL,
  expires_at TEXT NOT NULL,
  claimed_at TEXT,
  claimed_by TEXT REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS device_commands (
  command_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
  actor_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  requested_output TEXT NOT NULL CHECK (requested_output IN ('ON', 'OFF')),
  status TEXT NOT NULL CHECK (status IN ('PENDING', 'ACCEPTED', 'DELIVERED', 'APPLIED', 'REJECTED', 'EXPIRED', 'TIMEOUT')),
  source TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  issued_at TEXT NOT NULL,
  expires_at TEXT NOT NULL,
  accepted_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  reason_code TEXT,
  reason TEXT,
  observed_output TEXT CHECK (observed_output IN ('ON', 'OFF') OR observed_output IS NULL),
  state_version INTEGER NOT NULL DEFAULT 0,
  correlation_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS idempotency_keys (
  scope TEXT NOT NULL,
  key TEXT NOT NULL,
  command_id TEXT NOT NULL,
  request_hash TEXT NOT NULL,
  created_at TEXT NOT NULL,
  PRIMARY KEY (scope, key)
);

CREATE TABLE IF NOT EXISTS telemetry_samples (
  sample_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
  sequence INTEGER NOT NULL,
  sampled_at TEXT NOT NULL,
  received_at TEXT NOT NULL,
  quality TEXT NOT NULL CHECK (quality IN ('VALID', 'STALE', 'INVALID')),
  voltage_v REAL,
  current_a REAL,
  active_power_w REAL,
  energy_kwh_total REAL,
  power_factor REAL,
  frequency_hz REAL,
  state_json TEXT NOT NULL,
  UNIQUE (device_id, sequence)
);

CREATE TABLE IF NOT EXISTS energy_intervals (
  interval_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
  start_at TEXT NOT NULL,
  end_at TEXT NOT NULL,
  delta_kwh REAL NOT NULL,
  gap INTEGER NOT NULL,
  reason_code TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS daily_energy_aggregates (
  device_id TEXT NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
  day TEXT NOT NULL,
  energy_kwh REAL NOT NULL DEFAULT 0,
  cost_idr REAL,
  sample_count INTEGER NOT NULL DEFAULT 0,
  gap_count INTEGER NOT NULL DEFAULT 0,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (device_id, day)
);

CREATE TABLE IF NOT EXISTS electricity_tariffs (
  tariff_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
  currency TEXT NOT NULL DEFAULT 'IDR',
  idr_per_kwh REAL NOT NULL CHECK (idr_per_kwh > 0),
  effective_from TEXT NOT NULL,
  effective_to TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS energy_budgets (
  budget_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL UNIQUE REFERENCES devices(device_id) ON DELETE CASCADE,
  period TEXT NOT NULL CHECK (period IN ('daily', 'weekly', 'monthly')),
  kwh_limit REAL,
  idr_limit REAL,
  enabled INTEGER NOT NULL DEFAULT 0,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS automation_rules (
  device_id TEXT PRIMARY KEY REFERENCES devices(device_id) ON DELETE CASCADE,
  version INTEGER NOT NULL DEFAULT 0,
  schedules_json TEXT NOT NULL DEFAULT '[]',
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fault_events (
  event_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
  type TEXT NOT NULL,
  severity TEXT NOT NULL CHECK (severity IN ('INFO', 'WARNING', 'CRITICAL')),
  occurred_at TEXT NOT NULL,
  actor_id TEXT,
  source TEXT NOT NULL,
  correlation_id TEXT,
  summary TEXT NOT NULL,
  payload_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_notifications (
  notification_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
  user_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  provider TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('QUEUED', 'SENT', 'FAILED')),
  created_at TEXT NOT NULL,
  sent_at TEXT,
  error TEXT
);

CREATE TABLE IF NOT EXISTS audit_events (
  event_id TEXT PRIMARY KEY,
  actor_id TEXT,
  action TEXT NOT NULL,
  object_type TEXT NOT NULL,
  object_id TEXT NOT NULL,
  correlation_id TEXT,
  created_at TEXT NOT NULL,
  metadata_json TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_memberships_user ON memberships(user_id);
CREATE INDEX IF NOT EXISTS idx_devices_home ON devices(home_id);
CREATE INDEX IF NOT EXISTS idx_commands_device ON device_commands(device_id, accepted_at DESC);
CREATE INDEX IF NOT EXISTS idx_commands_actor_key ON device_commands(actor_id, idempotency_key);
CREATE INDEX IF NOT EXISTS idx_telemetry_device_time ON telemetry_samples(device_id, sampled_at DESC);
CREATE INDEX IF NOT EXISTS idx_intervals_device_time ON energy_intervals(device_id, start_at);
CREATE INDEX IF NOT EXISTS idx_daily_device_day ON daily_energy_aggregates(device_id, day);
CREATE INDEX IF NOT EXISTS idx_tariffs_device_from ON electricity_tariffs(device_id, effective_from);
CREATE INDEX IF NOT EXISTS idx_events_device_time ON fault_events(device_id, occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_time ON audit_events(created_at DESC);
`;
