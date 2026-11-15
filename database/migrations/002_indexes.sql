-- Query-oriented indexes. Add/remove only with EXPLAIN evidence.

CREATE INDEX IF NOT EXISTS sessions_user_idx ON sessions (user_id);
CREATE INDEX IF NOT EXISTS sessions_expiry_idx ON sessions (expires_at);
CREATE INDEX IF NOT EXISTS memberships_user_idx ON memberships (user_id);
CREATE INDEX IF NOT EXISTS devices_home_idx ON devices (home_id);
CREATE INDEX IF NOT EXISTS devices_last_seen_idx ON devices (last_seen_at DESC);
CREATE INDEX IF NOT EXISTS claims_code_idx ON device_claims (pairing_code_hash);
CREATE INDEX IF NOT EXISTS commands_device_time_idx ON device_commands (device_id, accepted_at DESC);
CREATE INDEX IF NOT EXISTS commands_status_expiry_idx ON device_commands (status, expires_at);
CREATE INDEX IF NOT EXISTS telemetry_device_time_idx ON telemetry_samples (device_id, sampled_at DESC);
CREATE INDEX IF NOT EXISTS telemetry_device_sequence_idx ON telemetry_samples (device_id, sequence DESC);
CREATE INDEX IF NOT EXISTS energy_segments_device_time_idx ON energy_counter_segments (device_id, started_at);
CREATE INDEX IF NOT EXISTS daily_device_day_idx ON daily_energy_aggregates (device_id, day);
CREATE INDEX IF NOT EXISTS tariffs_device_from_idx ON electricity_tariffs (device_id, effective_from);
CREATE INDEX IF NOT EXISTS events_device_time_idx ON fault_events (device_id, occurred_at DESC);
CREATE INDEX IF NOT EXISTS events_severity_time_idx ON fault_events (severity, occurred_at DESC);
CREATE INDEX IF NOT EXISTS notifications_status_time_idx ON user_notifications (status, created_at);
CREATE INDEX IF NOT EXISTS audit_time_idx ON audit_events (created_at DESC);
CREATE INDEX IF NOT EXISTS audit_actor_time_idx ON audit_events (actor_id, created_at DESC);
CREATE INDEX IF NOT EXISTS jobs_status_run_idx ON system_jobs (status, run_at);
