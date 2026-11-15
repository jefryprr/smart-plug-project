# Operations Runbook

**Scope:** local/staging smart plug stack. No production deployment exists yet.

## 1. Health checks

```powershell
Invoke-RestMethod http://localhost:4000/health/live
Invoke-RestMethod http://localhost:4000/health/ready
```

- `ready` returns `degraded` when MQTT is down. API read endpoints can still work.
- A degraded broker does **not** mean the relay is OFF. Do not claim physical state.

## 2. Start/stop

```powershell
docker compose -f infrastructure/docker-compose.dev.yaml up --build
docker compose -f infrastructure/docker-compose.dev.yaml down
```

If Docker is unavailable, run the local Node stack:

```powershell
npm run dev:api
npm run sim:dev
npm run web:dev
```

## 3. Common failures

| Symptom | Likely cause | Safe action |
|---|---|---|
| `/health/ready` degraded | MQTT down | Check broker; commands will return 503, not fake success |
| Command stuck `ACCEPTED` | Device offline/no ACK | Wait for TTL expiry; inspect events; do not claim applied |
| `ON` rejected `LOCKOUT_ACTIVE` | Fault/lockout | Inspect device safely; reset only after cause is resolved |
| Web login 500 | CORS/API misconfig | Check API logs, `WEB_ORIGIN`, reverse proxy |
| Telemetry missing | Device/network/meter | Check device diagnostics; do not display stale as live |
| DB locked (SQLite) | Concurrent writes | Stop duplicate API processes; migrate to Postgres for multi-instance |

## 4. Command troubleshooting

1. Check API command row and event history by `command_id`.
2. Check MQTT topic/ACL and broker logs.
3. Check device state/ACK; `observed_output` null means no physical proof.
4. Never send repeated ON commands to bypass a lockout.

## 5. Stop conditions

Stop and escalate if:
- relay is stuck ON or the device is heating;
- PE continuity is suspect;
- lockout cannot be cleared safely;
- any secret is exposed;
- database/broker integrity is uncertain.

**Emergency:** disconnect the load at the installation breaker/socket by a competent person. Do not touch a suspect mains assembly.
