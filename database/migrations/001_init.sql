-- PostgreSQL 16 target schema. The local test API uses a SQLite adapter with
-- equivalent tables. This migration is NOT applied in the current environment
-- because PostgreSQL/Docker are not installed.
-- Design revision: REV_A_PROVISIONAL
-- All timestamps are UTC timestamptz.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS users (
    user_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    email text NOT NULL,
    password_hash text NOT NULL,
    display_name text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    disabled_at timestamptz
);
CREATE UNIQUE INDEX IF NOT EXISTS users_email_lower_uidx ON users (lower(email));

CREATE TABLE IF NOT EXISTS sessions (
    session_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    refresh_token_hash text NOT NULL UNIQUE,
    expires_at timestamptz NOT NULL,
    revoked_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    user_agent text,
    ip_hash text
);

CREATE TABLE IF NOT EXISTS homes (
    home_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS memberships (
    home_id uuid NOT NULL REFERENCES homes(home_id) ON DELETE CASCADE,
    user_id uuid NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    role text NOT NULL CHECK (role IN ('owner', 'admin', 'viewer')),
    created_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (home_id, user_id)
);

CREATE TABLE IF NOT EXISTS devices (
    device_id text PRIMARY KEY,
    home_id uuid NOT NULL REFERENCES homes(home_id) ON DELETE CASCADE,
    name text NOT NULL,
    room text,
    hardware_revision text,
    firmware_version text,
    data_source text NOT NULL DEFAULT 'UNKNOWN'
        CHECK (data_source IN ('DEVICE', 'SIMULATOR', 'SYNTHETIC_DEMO', 'UNKNOWN')),
    state_json jsonb NOT NULL DEFAULT '{}'::jsonb,
    diagnostics_json jsonb,
    last_seen_at timestamptz,
    availability text NOT NULL DEFAULT 'NEVER_SEEN'
        CHECK (availability IN ('ONLINE', 'STALE', 'OFFLINE', 'NEVER_SEEN')),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS device_credentials (
    credential_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id text NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
    secret_hash text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    revoked_at timestamptz
);

CREATE TABLE IF NOT EXISTS device_claims (
    claim_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id text NOT NULL UNIQUE REFERENCES devices(device_id) ON DELETE CASCADE,
    pairing_code_hash text NOT NULL,
    expires_at timestamptz NOT NULL,
    claimed_at timestamptz,
    claimed_by uuid REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS device_state_snapshots (
    snapshot_id bigserial PRIMARY KEY,
    device_id text NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
    state_version bigint NOT NULL,
    state jsonb NOT NULL,
    quality text NOT NULL CHECK (quality IN ('VALID', 'STALE', 'INVALID')),
    received_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (device_id, state_version)
);

CREATE TABLE IF NOT EXISTS device_commands (
    command_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id text NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
    actor_id uuid NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    requested_output text NOT NULL CHECK (requested_output IN ('ON', 'OFF')),
    status text NOT NULL CHECK (status IN ('PENDING', 'ACCEPTED', 'DELIVERED', 'APPLIED', 'REJECTED', 'EXPIRED', 'TIMEOUT')),
    source text NOT NULL,
    idempotency_key text NOT NULL,
    sequence bigint NOT NULL,
    issued_at timestamptz NOT NULL,
    expires_at timestamptz NOT NULL,
    accepted_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    reason_code text,
    reason text,
    observed_output text CHECK (observed_output IN ('ON', 'OFF') OR observed_output IS NULL),
    state_version bigint NOT NULL DEFAULT 0,
    correlation_id text NOT NULL
);

CREATE TABLE IF NOT EXISTS idempotency_keys (
    scope text NOT NULL,
    key text NOT NULL,
    command_id uuid NOT NULL,
    request_hash text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (scope, key)
);

CREATE TABLE IF NOT EXISTS telemetry_samples (
    sample_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id text NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
    sequence bigint NOT NULL,
    sampled_at timestamptz NOT NULL,
    received_at timestamptz NOT NULL DEFAULT now(),
    quality text NOT NULL CHECK (quality IN ('VALID', 'STALE', 'INVALID')),
    voltage_v numeric(10, 3),
    current_a numeric(10, 4),
    active_power_w numeric(12, 3),
    energy_kwh_total numeric(14, 5),
    power_factor numeric(5, 4),
    frequency_hz numeric(6, 3),
    state jsonb NOT NULL,
    UNIQUE (device_id, sequence)
);

CREATE TABLE IF NOT EXISTS energy_counter_segments (
    segment_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id text NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
    started_at timestamptz NOT NULL,
    ended_at timestamptz,
    start_counter numeric(14, 5),
    end_counter numeric(14, 5),
    reset_detected boolean NOT NULL DEFAULT false,
    gap boolean NOT NULL DEFAULT false,
    reason_code text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS daily_energy_aggregates (
    device_id text NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
    day date NOT NULL,
    energy_kwh numeric(14, 5) NOT NULL DEFAULT 0,
    cost_idr numeric(14, 2),
    sample_count integer NOT NULL DEFAULT 0,
    gap_count integer NOT NULL DEFAULT 0,
    updated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (device_id, day)
);

CREATE TABLE IF NOT EXISTS weekly_energy_aggregates (
    device_id text NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
    week_start date NOT NULL,
    energy_kwh numeric(14, 5) NOT NULL DEFAULT 0,
    cost_idr numeric(14, 2),
    updated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (device_id, week_start)
);

CREATE TABLE IF NOT EXISTS monthly_energy_aggregates (
    device_id text NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
    month_start date NOT NULL,
    energy_kwh numeric(14, 5) NOT NULL DEFAULT 0,
    cost_idr numeric(14, 2),
    updated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (device_id, month_start)
);

CREATE TABLE IF NOT EXISTS electricity_tariffs (
    tariff_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id text NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
    currency text NOT NULL DEFAULT 'IDR' CHECK (currency = 'IDR'),
    idr_per_kwh numeric(12, 4) NOT NULL CHECK (idr_per_kwh > 0),
    effective_from timestamptz NOT NULL,
    effective_to timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    CHECK (effective_to IS NULL OR effective_to > effective_from)
);

CREATE TABLE IF NOT EXISTS energy_budgets (
    budget_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id text NOT NULL UNIQUE REFERENCES devices(device_id) ON DELETE CASCADE,
    period text NOT NULL CHECK (period IN ('daily', 'weekly', 'monthly')),
    kwh_limit numeric(14, 5),
    idr_limit numeric(14, 2),
    enabled boolean NOT NULL DEFAULT false,
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS automation_rules (
    device_id text PRIMARY KEY REFERENCES devices(device_id) ON DELETE CASCADE,
    version bigint NOT NULL DEFAULT 0,
    schedules jsonb NOT NULL DEFAULT '[]'::jsonb,
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS device_firmware_versions (
    version_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id text NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
    version text NOT NULL,
    build_sha text,
    installed_at timestamptz,
    active boolean NOT NULL DEFAULT false
);

CREATE TABLE IF NOT EXISTS firmware_releases (
    release_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    version text NOT NULL,
    channel text NOT NULL CHECK (channel IN ('dev', 'staging', 'production')),
    image_sha256 text NOT NULL,
    signature text NOT NULL,
    min_version text,
    notes text,
    published_at timestamptz,
    revoked_at timestamptz
);

CREATE TABLE IF NOT EXISTS fault_events (
    event_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id text NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
    type text NOT NULL,
    severity text NOT NULL CHECK (severity IN ('INFO', 'WARNING', 'CRITICAL')),
    occurred_at timestamptz NOT NULL DEFAULT now(),
    actor_id uuid,
    source text NOT NULL,
    correlation_id text,
    summary text NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS user_notifications (
    notification_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id text NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
    user_id uuid NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    provider text NOT NULL,
    status text NOT NULL CHECK (status IN ('QUEUED', 'SENT', 'FAILED')),
    created_at timestamptz NOT NULL DEFAULT now(),
    sent_at timestamptz,
    error text,
    dedup_key text
);

CREATE TABLE IF NOT EXISTS push_tokens (
    token_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    platform text NOT NULL CHECK (platform IN ('android', 'ios')),
    token_hash text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    revoked_at timestamptz
);

CREATE TABLE IF NOT EXISTS audit_events (
    event_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_id uuid,
    action text NOT NULL,
    object_type text NOT NULL,
    object_id text NOT NULL,
    correlation_id text,
    created_at timestamptz NOT NULL DEFAULT now(),
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS system_jobs (
    job_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    type text NOT NULL,
    status text NOT NULL CHECK (status IN ('PENDING', 'RUNNING', 'DONE', 'FAILED')),
    run_at timestamptz NOT NULL DEFAULT now(),
    attempts integer NOT NULL DEFAULT 0,
    last_error text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);
