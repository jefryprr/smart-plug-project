-- DEV ONLY. Never run in production.
-- Demo password: demo1234 (documented in README/login screen).
-- Demo pairing code: 123456 (single-use in the API; seed is for local demo only).
-- The scrypt hash below was generated for this seed; it is not a production secret.

BEGIN;

INSERT INTO users (user_id, email, password_hash, display_name)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'demo@example.com',
    'scrypt$16384$8$1$02d2e2d0c40bd541e91486aeab19ca0d$964d068de84dc884f9f675245d72470df008cc1d96706863fb3f8b797586fafc5d6c87d1de82290d53ac4657374dc84ee4d81fc62e9707ce02818ca9ed9fe3aa',
    'Demo User'
) ON CONFLICT (user_id) DO NOTHING;

INSERT INTO homes (home_id, name)
VALUES ('00000000-0000-0000-0000-000000000010', 'Rumah Demo')
ON CONFLICT (home_id) DO NOTHING;

INSERT INTO memberships (home_id, user_id, role)
VALUES ('00000000-0000-0000-0000-000000000010', '00000000-0000-0000-0000-000000000001', 'owner')
ON CONFLICT (home_id, user_id) DO NOTHING;

INSERT INTO devices (
    device_id, home_id, name, room, hardware_revision, firmware_version,
    data_source, state_json, diagnostics_json, last_seen_at, availability
) VALUES (
    'dev-sim-001',
    '00000000-0000-0000-0000-000000000010',
    'Smart Plug Demo',
    'Ruang Tamu',
    'REV_A_PROVISIONAL',
    '0.1.0-demo',
    'SYNTHETIC_DEMO',
    '{"commanded_output":"OFF","observed_output":null,"lockout":false,"fault_code":null,"state_version":4,"last_transition_at":"2026-11-15T00:00:00Z","clock_valid":true,"meter_valid":true,"temperature_valid":true}'::jsonb,
    '{"firmware_version":"0.1.0-demo","build_sha":"synthetic-demo","sensor_health":{"meter":"OK","temperature":"OK","relay_feedback":"NOT_INSTALLED"},"wifi_state":"CONNECTED"}'::jsonb,
    now(),
    'ONLINE'
) ON CONFLICT (device_id) DO NOTHING;

INSERT INTO device_claims (claim_id, device_id, pairing_code_hash, expires_at)
VALUES (
    '00000000-0000-0000-0000-000000000020',
    'dev-sim-001',
    '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
    now() + interval '30 days'
) ON CONFLICT (device_id) DO NOTHING;

INSERT INTO electricity_tariffs (tariff_id, device_id, currency, idr_per_kwh, effective_from, effective_to)
VALUES (
    '00000000-0000-0000-0000-000000000030',
    'dev-sim-001',
    'IDR',
    1500.0000,
    '2026-01-01T00:00:00Z',
    NULL
) ON CONFLICT (tariff_id) DO NOTHING;

INSERT INTO energy_budgets (budget_id, device_id, period, kwh_limit, idr_limit, enabled)
VALUES (
    '00000000-0000-0000-0000-000000000040',
    'dev-sim-001',
    'monthly',
    30.00000,
    50000.00,
    true
) ON CONFLICT (device_id) DO NOTHING;

INSERT INTO automation_rules (device_id, version, schedules)
VALUES (
    'dev-sim-001',
    0,
    '[{"schedule_id":"schedule-demo-1","days":[1,2,3,4,5],"start_time":"18:00","duration_minutes":120,"action":"ON","time_zone":"Asia/Jakarta","enabled":false}]'::jsonb
) ON CONFLICT (device_id) DO NOTHING;

COMMIT;
