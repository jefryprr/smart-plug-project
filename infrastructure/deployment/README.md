# Deployment — Reproducible Local/Staging

**Status:** `CONFIG_ONLY`
**Docker:** not installed in the current environment; the compose stack was **not executed**.
**Production:** not deployed. No domain, TLS certificate, VPS, or provider account is claimed.

## Local development stack

```powershell
Copy-Item infrastructure\.env.docker.example infrastructure\.env.docker
# edit POSTGRES_PASSWORD and JWT_SECRET
docker compose -f infrastructure/docker-compose.dev.yaml --env-file infrastructure\.env.docker up --build
```

Expected services:
- Web: http://localhost:3000
- API: http://localhost:4000/health/live
- MQTT: localhost:1883 (dev anonymous only)
- Caddy: http://localhost:8080 (reverse proxy)

## What is not wired yet

- The API currently uses the SQLite test adapter. The PostgreSQL schema exists, but the API has **no PostgreSQL adapter** yet. Do not claim the Postgres path is integration-tested.
- The dev compose broker allows anonymous connections. Production requires `mosquitto.prod.conf`, a password file, ACL, and TLS certificates.
- Caddy uses `{$DOMAIN:localhost}`; production TLS requires a real domain and DNS.
- No secrets are committed. `.env.docker` is gitignored.

## Staging/production checklist

- [ ] Real domain + DNS.
- [ ] TLS certificates and renewal.
- [ ] MQTT TLS + password file + per-device ACL.
- [ ] PostgreSQL adapter implemented and tested (currently missing).
- [ ] `JWT_SECRET` rotated, not default.
- [ ] Backups configured and restore tested.
- [ ] Monitoring/alerting configured.
- [ ] Security review and dependency scan.
- [ ] User approval for any paid provider/domain/VPS.

## Commands

```powershell
docker compose -f infrastructure/docker-compose.dev.yaml ps
docker compose -f infrastructure/docker-compose.dev.yaml logs -f api
docker compose -f infrastructure/docker-compose.dev.yaml down
```

## Rollback

See `docs/operations/ROLLBACK_SERVER.md`. Never roll back a database migration without a backup and compatibility review.
