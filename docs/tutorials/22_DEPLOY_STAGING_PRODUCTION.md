# 22 — Deploy Staging/Production

**Status:** `BLOCKED` — no Docker/VPS/domain/TLS/credentials.

## Staging lokal

```powershell
Copy-Item infrastructure\.env.docker.example infrastructure\.env.docker
docker compose -f infrastructure/docker-compose.dev.yaml --env-file infrastructure\.env.docker up --build
```

## Production checklist

- Domain/DNS/TLS.
- MQTT TLS + password + ACL.
- PostgreSQL adapter (belum ada).
- Secrets/backup/monitoring.
- Security review.
- User approval for paid services.

## Jangan

- Jangan mengklaim URL/deploy yang tidak ada.
- Jangan memakai dev broker anonymous di production.
