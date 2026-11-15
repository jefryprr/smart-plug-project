# Backup and Restore

**Status:** procedure only; not executed because PostgreSQL/Docker are not installed.

## PostgreSQL

```bash
pg_dump --format=custom --file=smartplug_$(date +%Y%m%dT%H%M%SZ).dump "$DATABASE_URL"
pg_restore --clean --if-exists --dbname="$DATABASE_URL" smartplug_YYYYMMDDTHHMMSSZ.dump
```

Test restore into a disposable database first. Verify row counts, latest telemetry, audit continuity, and tenant isolation.

## SQLite dev database

Stop the API, copy `data/smartplug.db` plus `-wal`/`-shm`, then restart. Do not copy while writes are active.

## Secrets

Back up `.env`/`.env.docker` in a secret manager, not in the repo. Rotate after any suspected exposure.

## Broker/TLS

Back up Mosquitto config, ACL, password file, and certificates from the secret store. Certificates are not database backups.

## Restore validation

- [ ] API `/health/ready` returns expected status.
- [ ] Login works with a test user.
- [ ] Device list and latest telemetry timestamps are sane.
- [ ] Command history/audit is not truncated.
- [ ] No cross-tenant data appears.
- [ ] MQTT ACL still denies cross-device topics.
