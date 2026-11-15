# 17 — Setup Backend, DB, MQTT

## Local (tanpa Docker/Postgres)

```powershell
npm install
npm run dev:api
```

API memakai SQLite (`data/smartplug.db`), seed demo. Health:
```powershell
Invoke-RestMethod http://localhost:4000/health/live
```

## Target PostgreSQL/Mosquitto (belum dieksekusi)

- `database/migrations/001_init.sql`, `002_indexes.sql`
- `infrastructure/docker-compose.dev.yaml`
- `infrastructure/broker/mosquitto.prod.conf`, `aclfile.template`

## Blocker

- Docker/Postgres/Mosquitto tidak terpasang.
- API PostgreSQL adapter belum ada.
- Dev broker anonymous; production butuh TLS+ACL.

## Jangan

- Jangan mengklaim deploy berhasil tanpa container/health check.
