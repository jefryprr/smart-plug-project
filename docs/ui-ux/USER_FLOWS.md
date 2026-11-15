# User Flows — REV_A_PROVISIONAL

## 1. First-time setup

```
Open web → Login → Dashboard (empty) → Pair device → Enter single-use code → Device overview → Verify status/sensors
```

- The user must not be told the output is OFF just because the device is online.
- Pairing code is single-use; show expiry and failure reasons.
- If sensor validity is unknown, ON is blocked.

## 2. Everyday ON/OFF

```
Device overview → Nyalakan/Matikan → Pending → ACCEPTED → APPLIED/REJECTED/TIMEOUT
```

- The UI shows command status, not instant success.
- Emergency OFF is always visible; it still requires an ACK.
- If lockout/fault, ON is disabled with a reason.
- If offline, ON is disabled and the UI says the physical state is unverified.

## 3. Monitoring

```
Dashboard → device card → overview → readings/energy graph → analytics range → events
```

- Stale/invalid readings are labeled; no stale value is presented as live.
- Missing analytics buckets show "Tidak ada data", not zero.

## 4. Schedules

```
Device → Jadwal → add/edit → save (version check) → device executes locally when clock valid
```

- Saving a schedule does not immediately switch the load.
- A version conflict asks the user to reload.
- Auto ON is blocked if clock/lockout/sensor checks fail.

## 5. Settings and risk actions

```
Device → Pengaturan → rename/tariff/budget/OTA/revoke
```

- OTA request is an event, not a firmware delivery.
- Revoke requires two confirmations and does not fix physical faults.
- Tariff changes do not rewrite historical cost.

## 6. Failure paths

| State | UI behavior |
|---|---|
| API down | Error panel with retry; no fake values |
| Device offline | Status OFFLINE; ON disabled; OFF allowed with warning |
| Command timeout | Show TIMEOUT; state unverified |
| Lockout | Red banner; ON disabled; OFF accepted |
| Invalid meter | Dashes + warning; cost not computed |
| Empty history | Empty state, not zero |
| Synthetic demo | Persistent demo banner/chip |
