# Server Rollback

1. Identify the last known-good image/tag and database backup.
2. Stop new writes or put the API in maintenance mode.
3. Do **not** run a down migration unless the backup and compatibility review are complete.
4. Deploy the previous image.
5. Restore the matching database snapshot if the schema changed.
6. Verify `/health/live`, `/health/ready`, login, device list, command/ACK path, and MQTT ACL.
7. Record the rollback in the incident log.

## Rules

- A code rollback does not automatically roll back a database migration.
- A rollback must not enable a load or bypass a lockout.
- If the rollback cannot restore a safe state, keep the device OFF and escalate.
