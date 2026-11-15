# Incident Response

## Severity

| Level | Example | First action |
|---|---|---|
| S1 | Suspected fire/shock/relay stuck ON | Evacuate/isolate at breaker by competent person; call emergency services if needed |
| S2 | Unauthorized ON/OFF, credential leak | Revoke sessions/device credentials, block network, preserve logs |
| S3 | Broker/API outage, stale data | Fail safe, communicate uncertainty, restore service |
| S4 | Minor UI/notification issue | Triage, no safety claim |

## Containment

1. Do not touch a suspect mains assembly.
2. Isolate power at the installation protection device.
3. Preserve logs, command IDs, event timestamps, and configuration (redact secrets).
4. Revoke compromised credentials.
5. Disable remote commands if safety is uncertain.

## Evidence

- API `audit_events`, `fault_events`, `device_commands`.
- Broker logs/ACL.
- Device serial log (if safely accessible low-voltage).
- Database snapshot.
- Exact times in UTC and Asia/Jakarta.

## Communication

State what is known, what is not known, and what the user must do. Never say "device is OFF" without verified observation.

## Post-incident

- Root cause and contributing factors.
- Corrective actions with owner/date.
- Regression tests.
- Update FMEA/risk register.
- If safety-related, stop release and require engineering review.
