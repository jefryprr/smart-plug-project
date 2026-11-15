# Troubleshooting

| Symptom | Check | Do not |
|---|---|---|
| API won't start | `JWT_SECRET` length, port, DB path, logs | Disable auth to "make it work" |
| Login 500 | CORS origin, `WEB_ORIGIN`, proxy | Expose API without auth |
| Web blank | `next build`, API URL, browser console | Claim data is live |
| Device offline | MQTT broker, ACL, Wi-Fi, LWT | Assume relay is OFF |
| Command `ACCEPTED` forever | Device ACK, TTL, broker | Resend ON repeatedly |
| `LOCKOUT_ACTIVE` | Fault code, temperature/current, physical cause | Bypass lockout from cloud |
| Telemetry stale | Device clock, meter, network | Display old value as live |
| Cost looks wrong | Tariff segment/effective date, missing data | Treat estimate as PLN bill |
| Android bundle fails | Node/Expo versions, `npx expo export` log | Claim APK exists |
| KiCad CLI missing | Install KiCad, run ERC/DRC | Hand-edit Gerber |
| 3D print fits poorly | Measured module dimensions, insert depth | Force parts or reduce clearance |

## Escalation

Safety-related symptoms (heat, smell, stuck ON, PE doubt) require immediate isolation by a competent person and engineering review.
