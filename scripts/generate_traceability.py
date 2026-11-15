#!/usr/bin/env python3
"""Generate requirements/traceability.yaml for FR-001..FR-080."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "requirements"
OUT.mkdir(parents=True, exist_ok=True)

# (id, name, priority, phase, status, paths, tests, evidence, blocker, risks)
# Status is deliberately conservative. PARTIAL means some digital evidence exists
# but the full acceptance criterion (especially physical/HIL) is not met.
ROWS = [
    ("FR-001", "Real-time voltage monitoring", "P0", "F1+F2", "PARTIAL", ["apps/api/src/services/telemetry.ts", "apps/web/src/components/ElectricalReadings.tsx"], ["T-SW-006"], ["API telemetry tests; no physical meter"], ["BLOCK-PHYSICAL-METER"], ["RR-08"]),
    ("FR-002", "Real-time current monitoring", "P0", "F1+F2", "PARTIAL", ["apps/api/src/services/telemetry.ts", "apps/web/src/components/ElectricalReadings.tsx"], ["T-SW-006"], ["API telemetry tests; no physical meter"], ["BLOCK-PHYSICAL-METER"], ["RR-08"]),
    ("FR-003", "Real-time active power", "P0", "F1+F2", "PARTIAL", ["apps/api/src/services/telemetry.ts"], ["T-SW-006"], ["Uses meter register fixture; no physical calibration"], ["BLOCK-PHYSICAL-METER"], ["RR-08"]),
    ("FR-004", "Energy consumption (kWh)", "P0", "F1+F2", "PASS", ["packages/domain/src/index.ts", "apps/api/src/services/telemetry.ts"], ["T-SW-008", "DOMAIN-ENERGY"], ["34 domain tests + 38 API tests; reset/gap covered"], [], ["RR-08"]),
    ("FR-005", "Power factor monitoring", "P1", "F1+F2", "PARTIAL", ["apps/api/src/services/telemetry.ts", "apps/web/src/components/ElectricalReadings.tsx"], ["T-SW-006"], ["Displays null/valid PF; no physical calibration"], ["BLOCK-PHYSICAL-METER"], ["RR-08"]),
    ("FR-006", "Electricity cost calculator", "P0", "F2", "PASS", ["packages/domain/src/index.ts", "apps/api/src/services/energy.ts"], ["DOMAIN-COST"], ["Historical tariff test; IDR formatting"], [], ["RR-16"]),
    ("FR-007", "Custom electricity tariff", "P0", "F2", "PASS", ["apps/api/src/routes/automation.ts", "apps/api/src/services/energy.ts"], ["API-TARIFF"], ["Tariff history/overlap tests"], [], ["RR-16"]),
    ("FR-008", "Energy history", "P0", "F2", "PASS", ["apps/api/src/routes/telemetry.ts", "apps/api/src/db/schema.ts"], ["API-TELEMETRY"], ["Telemetry pagination tests; seeded fixtures"], [], ["RR-08"]),
    ("FR-009", "Energy analytics", "P1", "F2", "PASS", ["apps/api/src/services/energy.ts", "apps/web/src/components/EnergyGraph.tsx"], ["API-ANALYTICS", "T-SW-011"], ["Daily/weekly/monthly aggregation tests; missing data null"], [], ["RR-08"]),
    ("FR-010", "Peak power tracking", "P1", "F2", "NOT_STARTED", [], [], [], ["BLOCK-NOT-IMPLEMENTED"], ["RR-08"]),
    ("FR-011", "Energy budget monitoring", "P1", "F2", "PASS", ["apps/api/src/routes/automation.ts", "apps/api/src/services/alerts.ts"], ["API-BUDGET", "ALERT-BUDGET"], ["Budget API + crossing alert dedup tests"], [], ["RR-16"]),
    ("FR-012", "Energy data CSV export", "P2", "F2", "NOT_STARTED", [], [], [], ["BLOCK-NOT-IMPLEMENTED"], ["RR-08"]),
    ("FR-013", "Remote ON/OFF", "P0", "F2", "PASS", ["apps/api/src/services/commands.ts", "apps/api/src/mqtt/bridge.ts", "apps/device-simulator/src/simulator.ts"], ["API-COMMAND", "INTEGRATION-COMMAND"], ["38 API tests incl. simulator ACK; no cloud deploy"], ["BLOCK-CLOUD-CREDENTIALS"], ["RR-10", "RR-23"]),
    ("FR-014", "Local ON/OFF", "P0", "F1+F2", "PARTIAL", ["firmware/main/app_main.c", "apps/api/src/services/commands.ts"], ["CORE-BUTTON"], ["Physical button code; LAN API not implemented"], ["BLOCK-LOCAL-TRANSPORT"], ["RR-10"]),
    ("FR-015", "Physical ON/OFF button", "P0", "F1", "PARTIAL", ["firmware/main/app_main.c"], ["CORE-BUTTON"], ["50 ms debounce code; no hardware test"], ["BLOCK-BOARD"], ["RR-14"]),
    ("FR-016", "Scheduled ON/OFF", "P0", "F1+F2", "PARTIAL", ["packages/domain/src/index.ts", "firmware/core/smartplug_core.c", "apps/api/src/routes/automation.ts"], ["DOMAIN-SCHEDULE", "CORE-SCHEDULE"], ["Schedule evaluator tested; firmware time integration pending"], ["BLOCK-RTC-INTEGRATION"], ["RR-17"]),
    ("FR-017", "Weekly scheduling", "P1", "F1+F2", "PASS", ["packages/domain/src/index.ts", "firmware/core/smartplug_core.c", "apps/api/src/routes/automation.ts"], ["DOMAIN-SCHEDULE", "CORE-SCHEDULE", "API-AUTOMATION"], ["Day/window/duplicate tests"], [], ["RR-17"]),
    ("FR-018", "Countdown timer", "P0", "F1+F2", "NOT_STARTED", [], [], [], ["BLOCK-NOT-IMPLEMENTED"], ["RR-17"]),
    ("FR-019", "Automatic standby detection", "P1", "F1+F2", "NOT_STARTED", [], [], [], ["BLOCK-NOT-IMPLEMENTED"], ["RR-08"]),
    ("FR-020", "Automatic standby cut-off", "P1", "F1+F2", "NOT_STARTED", [], [], [], ["BLOCK-NOT-IMPLEMENTED"], ["RR-01"]),
    ("FR-021", "Idle detection", "P1", "F1+F2", "NOT_STARTED", [], [], [], ["BLOCK-NOT-IMPLEMENTED"], ["RR-08"]),
    ("FR-022", "Power threshold automation", "P1", "F1+F2", "NOT_STARTED", [], [], [], ["BLOCK-NOT-IMPLEMENTED"], ["RR-08"]),
    ("FR-023", "Power recovery settings", "P0", "F1+F2", "PARTIAL", ["firmware/main/app_main.c", "docs/decisions/USER_ANSWERS.md"], ["CORE-BOOT"], ["Default OFF in code/docs; NVS policy not implemented"], ["BLOCK-NVS"], ["RR-14"]),
    ("FR-024", "Offline scheduling", "P0", "F1+F2", "PARTIAL", ["firmware/core/smartplug_core.c"], ["CORE-SCHEDULE"], ["Clock validity rule tested; RTC integration pending"], ["BLOCK-RTC-INTEGRATION"], ["RR-17"]),
    ("FR-025", "Automation priority management", "P0", "F1+F2", "PASS", ["packages/domain/src/index.ts", "firmware/core/smartplug_core.c"], ["DOMAIN-PRIORITY", "CORE-PRIORITY"], ["Lockout/OFF/ON priority tests"], [], ["RR-01"]),
    ("FR-026", "Overcurrent protection", "P0", "F1", "PARTIAL", ["firmware/core/smartplug_core.c", "apps/api/src/services/alerts.ts", "safety/PROTECTION_COORDINATION.md"], ["CORE-MEASUREMENT", "ALERT-HIGH-POWER"], ["Software validation/alert; fuse/thermal physical test blocked"], ["BLOCK-FUSE-RATING"], ["RR-03"]),
    ("FR-027", "Overtemperature protection", "P0", "F1", "PARTIAL", ["firmware/core/smartplug_core.c", "apps/api/src/services/alerts.ts", "safety/THERMAL_RISK_AND_DERATING.md"], ["CORE-MEASUREMENT", "ALERT-TEMP"], ["Alert/state logic; thermal cutoff hardware blocked"], ["BLOCK-THERMAL-LAB"], ["RR-04"]),
    ("FR-028", "Overvoltage warning", "P0", "F1+F2", "PASS", ["firmware/core/smartplug_core.c", "packages/domain/src/index.ts"], ["CORE-MEASUREMENT", "DOMAIN-MEASUREMENT"], ["260 V warning test; no surge claim"], [], ["RR-07"]),
    ("FR-029", "Undervoltage warning", "P0", "F1+F2", "PASS", ["firmware/core/smartplug_core.c", "packages/domain/src/index.ts"], ["CORE-MEASUREMENT", "DOMAIN-MEASUREMENT"], ["207 V threshold test"], [], ["RR-07"]),
    ("FR-030", "Surge protection", "P0", "F1", "BLOCKED", ["safety/PROTECTION_COORDINATION.md", "bom/BOM_MASTER.csv"], ["T-HW-013"], ["MOV candidate only; no surge test"], ["BLOCK-SURGE-STUDY"], ["RR-07"]),
    ("FR-031", "Thermal cutoff", "P0", "F1", "BLOCKED", ["safety/THERMAL_RISK_AND_DERATING.md", "bom/BOM_MASTER.csv"], ["T-HW-019"], ["TCO candidate; no physical trip test"], ["BLOCK-THERMAL-LAB"], ["RR-04"]),
    ("FR-032", "Fuse protection", "P0", "F1", "BLOCKED", ["safety/ELECTRICAL_RATING_CHAIN.md", "safety/PROTECTION_COORDINATION.md"], ["T-HW-013"], ["Fuse candidate; breaking capacity/coordination unverified"], ["BLOCK-FUSE-RATING"], ["RR-03"]),
    ("FR-033", "Fail-safe startup", "P0", "F1", "PARTIAL", ["firmware/main/app_main.c", "firmware/core/smartplug_core.c"], ["CORE-BOOT"], ["Relay GPIO forced OFF; no low-voltage waveform test"], ["BLOCK-BOARD"], ["RR-14"]),
    ("FR-034", "Sensor failure detection", "P0", "F1", "PASS", ["firmware/core/smartplug_core.c", "packages/domain/src/index.ts", "apps/api/src/services/alerts.ts"], ["CORE-MEASUREMENT", "DOMAIN-MEASUREMENT", "ALERT-SENSOR"], ["NaN/out-of-range/invalid quality tests"], [], ["RR-08"]),
    ("FR-035", "Electrical fault logging", "P0", "F1+F2", "PASS", ["apps/api/src/services/audit.ts", "apps/api/src/routes/operations.ts"], ["API-EVENTS"], ["Event history tests"], [], ["RR-08"]),
    ("FR-036", "Fault lockout", "P0", "F1", "PASS", ["firmware/core/smartplug_core.c", "packages/domain/src/index.ts", "apps/api/src/services/commands.ts"], ["CORE-LOCKOUT", "DOMAIN-LOCKOUT", "API-LOCKOUT"], ["ON rejected, OFF accepted under lockout"], [], ["RR-01"]),
    ("FR-037", "OLED display", "P0", "F1", "NOT_STARTED", [], [], [], ["BLOCK-OLED-FIRMWARE"], ["RR-14"]),
    ("FR-038", "OLED page navigation", "P1", "F1", "NOT_STARTED", [], [], [], ["BLOCK-OLED-FIRMWARE"], ["RR-14"]),
    ("FR-039", "RGB NeoPixel status", "P1", "F1", "NOT_STARTED", [], [], [], ["BLOCK-RGB-FIRMWARE"], ["RR-14"]),
    ("FR-040", "RGB engineering debug", "P2", "F1", "NOT_STARTED", [], [], [], ["BLOCK-RGB-FIRMWARE"], ["RR-14"]),
    ("FR-041", "RGB fault indicator", "P0", "F1", "NOT_STARTED", [], [], [], ["BLOCK-RGB-FIRMWARE"], ["RR-14"]),
    ("FR-042", "RGB night mode", "P2", "F1", "NOT_STARTED", [], [], [], ["BLOCK-RGB-FIRMWARE"], ["RR-14"]),
    ("FR-043", "Web dashboard", "P0", "F2", "PASS", ["apps/web/src/app", "apps/web/src/components"], ["T-SW-011", "T-SW-012"], ["Next build + 5 Playwright tests + axe"], [], ["RR-10"]),
    ("FR-044", "Android application", "P0", "F2", "PARTIAL", ["apps/android/App.tsx"], ["T-SW-013", "T-SW-014"], ["Typecheck + Expo Android bundle export; APK blocked"], ["BLOCK-ANDROID-SDK"], ["RR-10"]),
    ("FR-045", "Device naming", "P1", "F2", "PASS", ["apps/api/src/routes/devices.ts", "apps/web/src/components/DeviceSettings.tsx"], ["API-DEVICE-PATCH"], ["Validation and UI rename"], [], ["RR-10"]),
    ("FR-046", "Device status dashboard", "P0", "F2", "PASS", ["apps/web/src/components/DeviceSummaryCard.tsx", "apps/web/src/app/(app)/dashboard/page.tsx"], ["T-SW-011"], ["Online/stale/offline/commanded UI + E2E"], [], ["RR-10"]),
    ("FR-047", "Engineering diagnostics dashboard", "P1", "F1+F2", "PASS", ["apps/web/src/components/DeviceHealth.tsx", "apps/api/src/routes/operations.ts"], ["API-DIAGNOSTICS", "T-SW-011"], ["Diagnostics API/UI; role check"], [], ["RR-10"]),
    ("FR-048", "Wi-Fi connectivity", "P0", "F1", "NOT_STARTED", [], [], [], ["BLOCK-WIFI-FIRMWARE"], ["RR-16"]),
    ("FR-049", "BLE provisioning", "P1", "F1+F2", "NOT_STARTED", [], [], [], ["BLOCK-PROVISIONING"], ["RR-10"]),
    ("FR-050", "SoftAP setup", "P1", "F1+F2", "NOT_STARTED", [], [], [], ["BLOCK-PROVISIONING"], ["RR-10"]),
    ("FR-051", "Hybrid local-cloud control", "P0", "F2", "PARTIAL", ["apps/api/src/services/commands.ts", "apps/api/src/mqtt/bridge.ts"], ["INTEGRATION-COMMAND"], ["Cloud/MQTT path tested; local LAN transport missing"], ["BLOCK-LOCAL-TRANSPORT"], ["RR-10"]),
    ("FR-052", "MQTT integration", "P0", "F1+F2", "PASS", ["packages/mqtt-contract/src/index.ts", "apps/api/src/mqtt/bridge.ts"], ["T-SW-003", "T-SW-004", "INTEGRATION-COMMAND"], ["Contract tests + aedes integration"], [], ["RR-10"]),
    ("FR-053", "Home Assistant integration", "P1", "F2", "NOT_STARTED", [], [], [], ["BLOCK-NOT-IMPLEMENTED"], ["RR-10"]),
    ("FR-054", "REST API", "P0", "F2", "PASS", ["packages/api-contract/openapi.yaml", "apps/api/src"], ["T-SW-001", "API-TESTS"], ["OpenAPI + 38 API tests"], [], ["RR-10"]),
    ("FR-055", "Real-time synchronization", "P0", "F2", "PARTIAL", ["apps/api/src/mqtt/bridge.ts", "apps/web/src/lib/hooks.ts"], ["INTEGRATION-COMMAND"], ["Polling/MQTT; no WS/SSE and no device sequence shadow"], ["BLOCK-SYNC"], ["RR-10"]),
    ("FR-056", "Wi-Fi auto reconnection", "P0", "F1", "NOT_STARTED", [], [], [], ["BLOCK-WIFI-FIRMWARE"], ["RR-16"]),
    ("FR-057", "Offline data buffering", "P1", "F1+F2", "NOT_STARTED", [], [], [], ["BLOCK-NOT-IMPLEMENTED"], ["RR-16"]),
    ("FR-058", "Cloud database", "P0", "F2", "PARTIAL", ["apps/api/src/db/schema.ts", "database/migrations/001_init.sql"], ["T-SW-002"], ["SQLite local schema/tests; PostgreSQL deployment not run"], ["BLOCK-POSTGRES"], ["RR-10"]),
    ("FR-059", "Multi-device management", "P1", "F2", "PARTIAL", ["apps/api/src/routes/devices.ts", "apps/web/src/app/(app)/devices/page.tsx"], ["API-DEVICES"], ["List/claim/rename; no remove/reassign UI"], ["BLOCK-NOT-IMPLEMENTED"], ["RR-10"]),
    ("FR-060", "Power anomaly detection", "P1", "F2", "NOT_STARTED", [], [], [], ["BLOCK-NOT-IMPLEMENTED"], ["RR-08"]),
    ("FR-061", "Historical pattern analysis", "P1", "F2", "NOT_STARTED", [], [], [], ["BLOCK-NOT-IMPLEMENTED"], ["RR-08"]),
    ("FR-062", "High power alert", "P0", "F1+F2", "PASS", ["apps/api/src/services/alerts.ts"], ["ALERT-HIGH-POWER"], ["3-sample threshold + dedup test"], [], ["RR-08"]),
    ("FR-063", "High temperature alert", "P0", "F1+F2", "PARTIAL", ["apps/api/src/services/alerts.ts", "firmware/core/smartplug_core.c"], ["ALERT-TEMP"], ["Event rule; physical thermal test blocked"], ["BLOCK-THERMAL-LAB"], ["RR-04"]),
    ("FR-064", "Standby consumption alert", "P1", "F2", "NOT_STARTED", [], [], [], ["BLOCK-NOT-IMPLEMENTED"], ["RR-08"]),
    ("FR-065", "Energy budget alert", "P1", "F2", "PASS", ["apps/api/src/services/alerts.ts"], ["ALERT-BUDGET"], ["Period dedup test"], [], ["RR-16"]),
    ("FR-066", "Telegram notification", "P1", "F2", "PARTIAL", ["apps/api/src/services/notifications.ts"], ["API-NOTIFICATION"], ["Mock provider test; no live Telegram token/sandbox"], ["BLOCK-TELEGRAM-TOKEN"], ["RR-10"]),
    ("FR-067", "Android push notification", "P1", "F2", "NOT_STARTED", [], [], [], ["BLOCK-FCM"], ["RR-10"]),
    ("FR-068", "Event history", "P0", "F2", "PASS", ["apps/api/src/routes/operations.ts", "apps/web/src/app/(app)/devices/[id]/events/page.tsx"], ["API-EVENTS"], ["Pagination/filter test"], [], ["RR-10"]),
    ("FR-069", "OTA firmware update", "P0", "F1+F2", "PARTIAL", ["apps/api/src/routes/operations.ts", "firmware/partitions.csv"], ["API-OTA"], ["OTA request event only; no image delivery"], ["BLOCK-OTA"], ["RR-09"]),
    ("FR-070", "OTA rollback", "P0", "F1+F2", "PARTIAL", ["firmware/sdkconfig.defaults", "firmware/partitions.csv"], ["T-SW-018"], ["Config only; ESP-IDF build/test blocked"], ["BLOCK-ESP-IDF"], ["RR-09"]),
    ("FR-071", "Firmware integrity verification", "P0", "F1+F2", "PARTIAL", ["security/OTA_SIGNING_AND_RECOVERY.md"], ["T-SW-018"], ["Plan only; no signed image"], ["BLOCK-OTA"], ["RR-09"]),
    ("FR-072", "Watchdog system", "P0", "F1", "PARTIAL", ["firmware/sdkconfig.defaults"], ["T-HW-017"], ["Task WDT config only; no build/fault injection"], ["BLOCK-ESP-IDF"], ["RR-09"]),
    ("FR-073", "Secure authentication", "P0", "F2", "PASS", ["apps/api/src/auth", "apps/api/src/routes/auth.ts"], ["API-AUTH", "SECURITY-NEGATIVE"], ["Password hash, JWT, refresh rotation, negative tests"], [], ["RR-10"]),
    ("FR-074", "Role-based access control", "P0", "F2", "PASS", ["apps/api/src/services/access.ts", "apps/api/src/routes"], ["API-RBAC"], ["Owner/viewer/negative tests"], [], ["RR-10"]),
    ("FR-075", "Encrypted communication", "P0", "F2", "PARTIAL", ["security/THREAT_MODEL.md", "infrastructure/reverse-proxy/Caddyfile"], ["T-SW-019"], ["TLS config/docs; no deployed certificate"], ["BLOCK-DEPLOY"], ["RR-10"]),
    ("FR-076", "Device pairing security", "P0", "F1+F2", "PASS", ["apps/api/src/routes/auth.ts", "apps/api/src/services/commands.ts"], ["API-PAIRING", "T-SW-015"], ["Single-use code + expiry/replay test"], [], ["RR-10"]),
    ("FR-077", "Command validation", "P0", "F1+F2", "PASS", ["firmware/core/smartplug_core.c", "packages/domain/src/index.ts", "apps/api/src/services/commands.ts"], ["CORE-COMMAND", "DOMAIN-COMMAND", "API-COMMAND"], ["Replay/stale/expiry/wrong device/lockout tests"], [], ["RR-23"]),
    ("FR-078", "Activity and audit logging", "P0", "F2", "PASS", ["apps/api/src/services/audit.ts", "apps/api/src/db/schema.ts"], ["API-AUDIT"], ["Append-only audit table and tests"], [], ["RR-10"]),
    ("FR-079", "Factory reset", "P0", "F1+F2", "NOT_STARTED", [], [], [], ["BLOCK-NOT-IMPLEMENTED"], ["RR-10"]),
    ("FR-080", "Device diagnostics", "P0", "F1+F2", "PARTIAL", ["apps/api/src/routes/operations.ts", "apps/web/src/components/DeviceHealth.tsx", "firmware/main/app_main.c"], ["API-DIAGNOSTICS"], ["API/UI diagnostics; firmware counters minimal"], ["BLOCK-ESP-IDF"], ["RR-08"]),
]


def source_id(fr_id: str) -> int:
    number = int(fr_id.split("-")[1])
    return number if number <= 36 else number + 1


def main() -> None:
    entries = []
    for fr_id, name, priority, phase, status, paths, tests, evidence, blockers, risks in ROWS:
        entries.append({
            "id": fr_id,
            "source_id": source_id(fr_id),
            "description": name,
            "priority": priority,
            "phase": phase,
            "implementation_paths": paths,
            "test_ids": tests,
            "status": status,
            "evidence": evidence,
            "blocked_by": blockers,
            "risk_ids": risks,
            "last_verified_at": "2026-11-15T00:00:00Z" if status in {"PASS", "PARTIAL", "BLOCKED"} else None,
            "reviewer": None,
        })
    document = {
        "project": "esp32-s3-iot-smart-plug",
        "design_revision": "REV_A_PROVISIONAL",
        "prd_version": "1.0",
        "generated_at": "2026-11-15T00:00:00Z",
        "status_legend": {
            "PASS": "Digital evidence exists and the tested criterion passed; physical/HIL not implied.",
            "PARTIAL": "Some implementation/evidence exists, full criterion not met.",
            "BLOCKED": "Cannot proceed without hardware/lab/tool/approval.",
            "NOT_STARTED": "No implementation yet.",
            "UNVERIFIED": "Claim exists without sufficient test."
        },
        "requirements": entries,
    }
    (OUT / "traceability.yaml").write_text(yaml.safe_dump(document, sort_keys=False, allow_unicode=True), encoding="utf-8")
    counts = Counter(entry["status"] for entry in entries)
    priorities = Counter(entry["priority"] for entry in entries)
    summary = {
        "total": len(entries),
        "by_status": dict(counts),
        "by_priority": dict(priorities),
        "p0_not_pass": [entry["id"] for entry in entries if entry["priority"] == "P0" and entry["status"] != "PASS"],
        "note": "PASS is digital evidence only; it does not imply hardware validation or safety sign-off."
    }
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "reports" / "TRACEABILITY_SUMMARY.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
