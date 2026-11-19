import { createHash } from "node:crypto";
import { existsSync, readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { execSync } from "node:child_process";
import { basename, resolve } from "node:path";

const ROOT = resolve(".");
const OUT = resolve("deliverables/manifest.json");
const CHECKSUMS = resolve("deliverables/CHECKSUMS.sha256");

const TEXT_EXTENSIONS = new Set([
  ".md", ".ts", ".tsx", ".js", ".mjs", ".py", ".yaml", ".yml", ".json",
  ".csv", ".sql", ".c", ".h", ".txt", ".css", ".html", ".svg", ".log", ".kicad_sch", ".kicad_pro", ".kicad_pcb", ".lock",
  ".gbr", ".gtl", ".gbl", ".gto", ".gbo", ".gm1", ".drl", ".gbrjob"
]);
const SKIP_DIRS = new Set([".git", "node_modules", ".venv", "tools", "dist", ".next", "coverage", "build", "test-results", "playwright-report"]);

function normalizeTextFiles(dir = ROOT, count = { changed: 0 }) {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (SKIP_DIRS.has(entry.name)) continue;
    const full = resolve(dir, entry.name);
    if (entry.isDirectory()) {
      normalizeTextFiles(full, count);
      continue;
    }
    if (!entry.isFile()) continue;
    const ext = entry.name.includes(".") ? entry.name.slice(entry.name.lastIndexOf(".")).toLowerCase() : "";
    if (!TEXT_EXTENSIONS.has(ext)) continue;
    const bytes = readFileSync(full);
    if (!bytes.includes(0x0d)) continue;
    const normalized = Buffer.from(bytes.toString("utf8").replace(/\r\n/g, "\n"), "utf8");
    writeFileSync(full, normalized);
    count.changed += 1;
  }
  return count;
}

const normalized = normalizeTextFiles();
if (normalized.changed > 0) {
  console.log(`Normalized ${normalized.changed} generated text files to LF before hashing.`);
}

function sha256(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function gitCommit() {
  try {
    return execSync("git rev-parse HEAD", { cwd: ROOT, encoding: "utf8" }).trim();
  } catch {
    return null;
  }
}

const CATEGORIES = [
  { category: 1, name: "Component research", status: "PARTIAL", paths: ["research/COMPONENT_RESEARCH.md", "research/PROCUREMENT_INDONESIA.md", "research/PZEM_INTERNAL_ISOLATION.md", "docs/decisions/ADR-002-METERING-ARCHITECTURE.md", "research/OFFBOARD_MODULES.md", "research/PSU_HLK_5M05.md", "research/PSU_BOARD_EVIDENCE.md", "research/TIME_SERVICE_EVIDENCE.md", "reports/RESEARCH_LOG.md", "reports/REV_D_REFERENCE_CONFLICTS.md", "docs/decisions/ADR-016-PZEM-ISOLATION-REV-C.md", "research/FEASIBILITY_STUDY.md", "research/candidates.csv", "bom/COMPONENT_APPROVALS.yaml", "docs/hardware/PROCUREMENT_AND_INCOMING_QC.md"], tests: ["T-HW-001"], release: "DIGITAL_ONLY" },
  { category: 2, name: "BOM", status: "PARTIAL", paths: ["bom/BOM_MASTER.csv", "bom/BOM_MASTER.md", "bom/BOM_MASTER.yaml", "bom/BOM_PROCUREMENT.csv", "bom/BOM_PROCUREMENT.md", "bom/BOM_SUMMARY.json", "bom/BOM_TOOLS_AND_TEST.csv", "bom/BOM_CONSUMABLES.csv"], tests: ["T-HW-001"], release: "DIGITAL_ONLY" },
  { category: 3, name: "Datasheets", status: "PARTIAL", paths: ["research/datasheets/MANIFEST.md", "research/datasheets/hlk-5m05_distributor.txt", "research/UNKNOWN_SPECIFICATIONS.md"], tests: ["DOCUMENT_REVIEW"], release: "DIGITAL_ONLY" },
  { category: 4, name: "System architecture", status: "PASS_DIGITAL", paths: ["docs/hardware/SYSTEM_ARCHITECTURE.md", "docs/hardware/SYSTEM_ARCHITECTURE.png", "docs/hardware/SYSTEM_ARCHITECTURE.svg", "docs/hardware/SYSTEM_ARCHITECTURE.pdf"], tests: ["DOCUMENT_REVIEW"], release: "DIGITAL_ONLY" },
  { category: 5, name: "Schematic", status: "PARTIAL", paths: ["hardware/kicad/smartplug.kicad_sch", "hardware/kicad/smartplug.kicad_pro", "hardware/kicad/README.md", "hardware/schematic/carrier_schematic.svg", "hardware/schematic/carrier_schematic.png", "hardware/psu/psu_schematic.svg", "hardware/psu/psu_schematic.png", "hardware/psu/netlist.csv", "hardware/psu/README.md", "hardware/kicad/PSU_MAINS_5V.kicad_sch", "hardware/carrier/netlist.csv", "hardware/carrier/README.md", "hardware/generators/generate_schematic.py", "hardware/generators/requirements.lock", "hardware/generators/README.md", "reports/kicad/erc.json"], tests: ["T-HW-002", "T-HW-002A"], release: "NOT_FOR_FABRICATION" },
  { category: 6, name: "Wiring diagram", status: "PASS_DIGITAL", paths: ["hardware/wiring/README.md", "hardware/wiring/main_harness.yaml", "hardware/wiring/metering_harness.yaml", "hardware/wiring/renders/main_harness.png", "hardware/wiring/renders/main_harness.svg", "hardware/wiring/renders/main_harness.pdf", "hardware/wiring/renders/metering_harness.svg", "hardware/wiring/renders/metering_harness.pdf"], tests: ["T-HW-003", "T-HW-010A"], release: "DIGITAL_ONLY" },
  { category: 7, name: "GPIO mapping", status: "UNVERIFIED", paths: ["hardware/interfaces/gpio_map.yaml", "hardware/interfaces/gpio_map.csv", "hardware/interfaces/gpio_map.md", "validation/GPIO_CROSSCHECK.json"], tests: ["T-HW-004"], release: "DIGITAL_ONLY" },
  { category: 8, name: "PCB native design", status: "PARTIAL", paths: ["hardware/kicad/smartplug.kicad_pcb", "hardware/kicad/psu_rev_d.kicad_pcb", "scripts/generate_psu_pcb.py", "hardware/psu/generate_psu_schematic.py", "hardware/carrier/placement.json", "hardware/psu/placement.json", "reports/kicad/psu_drc.json", "hardware/pcb/render/placement_preview.png", "hardware/pcb/render/carrier.svg", "reports/kicad/drc.json", "reports/kicad/carrier_drc.json"], tests: ["T-HW-006", "T-HW-008A"], release: "NOT_FOR_FABRICATION" },
  { category: 9, name: "PCB manufacturing", status: "PARTIAL_BLOCKED", paths: ["hardware/manufacturing/provisional/readme_WARNING_NOT_RELEASED.md", "hardware/manufacturing/provisional/fabrication_notes.md", "hardware/manufacturing/provisional/BOM_PCBA.csv", "hardware/manufacturing/provisional/BOM_PCBA_PSU.csv", "hardware/manufacturing/provisional/psu/README.md", "hardware/manufacturing/provisional/psu/Gerber/psu_rev_d-F_Cu.gtl", "hardware/manufacturing/provisional/psu/Gerber/psu_rev_d-B_Cu.gbl", "hardware/manufacturing/provisional/psu/Gerber/psu_rev_d-F_Silkscreen.gto", "hardware/manufacturing/provisional/psu/Gerber/psu_rev_d-B_Silkscreen.gbo", "hardware/manufacturing/provisional/psu/Gerber/psu_rev_d-Edge_Cuts.gm1", "hardware/manufacturing/provisional/psu/Gerber/psu_rev_d-job.gbrjob", "hardware/manufacturing/provisional/psu/Drill/psu_rev_d.drl", "hardware/manufacturing/provisional/psu/POSITION.csv", "hardware/manufacturing/provisional/POSITION_NOT_APPLICABLE.md", "hardware/manufacturing/provisional/Gerber/README_ROUTED_PROTOTYPE.md", "hardware/manufacturing/provisional/Gerber/smartplug-Edge_Cuts.gm1", "hardware/manufacturing/provisional/Gerber/smartplug-job.gbrjob", "hardware/manufacturing/provisional/Drill/README_ROUTED_PROTOTYPE.md", "hardware/manufacturing/provisional/Drill/smartplug.drl", "hardware/manufacturing/provisional/POSITION.csv"], tests: ["T-HW-008"], release: "NOT_FOR_FABRICATION" },
  { category: 10, name: "PCB visualization", status: "PARTIAL", paths: ["hardware/pcb/render/placement_preview.png", "hardware/pcb/render/placement_preview.svg", "hardware/pcb/render/carrier.svg", "hardware/pcb/render/README.md"], tests: ["T-HW-008A"], release: "DIGITAL_ONLY" },
  { category: 11, name: "Enclosure 3D", status: "PARTIAL", paths: ["hardware/mechanical/source/enclosure.py", "hardware/mechanical/source/components.py", "hardware/mechanical/source/brackets.py", "hardware/mechanical/source/assembly.py", "hardware/mechanical/source/render.py", "hardware/mechanical/parameters.yaml", "hardware/mechanical/README.md", "hardware/mechanical/MECHANICAL_BOM.csv", "hardware/mechanical/MECHANICAL_COST_ESTIMATE.md", "hardware/mechanical/export/body_bottom_recommended.step", "hardware/mechanical/export/body_top_recommended.step", "hardware/mechanical/export/body_bottom_recommended.stl", "hardware/mechanical/export/body_top_recommended.stl", "hardware/mechanical/export/gasket.step", "hardware/mechanical/export/gasket.stl", "hardware/mechanical/export/usb_cover.step", "hardware/mechanical/export/usb_cover.stl", "hardware/mechanical/export/devkit_key.step", "hardware/mechanical/export/devkit_key.stl", "hardware/mechanical/export/assembly_recommended.step", "hardware/mechanical/export/pzem_bracket.step", "hardware/mechanical/export/relay_module_bracket.step", "hardware/mechanical/export/psu_bracket.step", "hardware/mechanical/source/relay_shelf.py", "hardware/mechanical/export/relay_shelf.step", "hardware/mechanical/export/relay_shelf.stl"], tests: ["T-HW-009A"], release: "NOT_FOR_FABRICATION" },
  { category: 12, name: "Enclosure rendering", status: "PARTIAL", paths: ["hardware/mechanical/render/isometric.png", "hardware/mechanical/render/front.png", "hardware/mechanical/render/back.png", "hardware/mechanical/render/top.png", "hardware/mechanical/render/bottom.png", "hardware/mechanical/render/exploded.png", "hardware/mechanical/render/cutaway.png", "hardware/mechanical/drawings/assembly.pdf", "hardware/mechanical/drawings/dimensions.svg", "hardware/mechanical/drawings/mounting_plan.svg", "hardware/mechanical/drawings/service_access.svg", "hardware/mechanical/drawings/service_access.png", "hardware/mechanical/FIT_ANALYSIS.md", "hardware/mechanical/CLASH_REPORT.json", "hardware/mechanical/ENCLOSURE_MATERIAL_REVIEW.md", "hardware/mechanical/PRINT_PROTOTYPE_GUIDE.md"], tests: ["T-HW-009B"], release: "DIGITAL_ONLY" },
  { category: 13, name: "Firmware ESP32-S3", status: "PARTIAL", paths: ["firmware/core/smartplug_core.c", "firmware/core/include/smartplug_core.h", "firmware/components/smartplug_core/CMakeLists.txt", "firmware/main/app_main.c", "firmware/main/CMakeLists.txt", "firmware/main/board_config.h", "firmware/main/time_service.c", "firmware/main/time_service.h", "firmware/main/status_rgb.c", "firmware/main/status_rgb.h", "firmware/test/host/test_core.c", "firmware/README.md", "reports/FIRMWARE_BUILD.md", "reports/logs/firmware-host-test.log"], tests: ["T-HW-017", "T-HW-018"], release: "DIGITAL_ONLY" },
  { category: 14, name: "Firmware configuration", status: "PARTIAL", paths: ["firmware/partitions.csv", "firmware/sdkconfig.defaults", "firmware/main/board_config.h", "scripts/idf_env.ps1", "scripts/build_firmware.ps1"], tests: ["T-HW-017"], release: "DIGITAL_ONLY" },
  { category: 15, name: "Web Next.js", status: "PASS_DIGITAL", paths: ["apps/web/src/app/(app)/dashboard/page.tsx", "apps/web/src/components/PowerControl.tsx", "apps/web/src/components/TimeStatusPanel.tsx", "apps/web/src/app/globals.css", "docs/ui-ux/screenshots/02-dashboard.png"], tests: ["T-SW-011", "T-SW-012"], release: "DIGITAL_ONLY" },
  { category: 16, name: "Android", status: "PASS_DEBUG", paths: ["apps/android/App.tsx", "apps/android/README_BUILD_APK.md", "apps/android/app.json", "apps/android/android/app/build.gradle", "apps/android/android/app/src/main/AndroidManifest.xml", "apps/android/android/gradle/wrapper/gradle-wrapper.properties", "reports/ANDROID_BUILD.md", "reports/logs/android-gradle-build.log"], tests: ["T-SW-013"], release: "NOT_PRODUCTION" },
  { category: 17, name: "Backend", status: "PASS_DIGITAL", paths: ["apps/api/src/app.ts", "apps/api/src/routes/time.ts", "packages/api-contract/openapi.yaml", `reports/logs/${latestLog("T-SW-005")}`], tests: ["T-SW-001", "T-SW-005"], release: "DIGITAL_ONLY" },
  { category: 18, name: "Database", status: "PARTIAL", paths: ["database/migrations/001_init.sql", "database/migrations/002_indexes.sql", "database/migrations/down/001_init.down.sql", "database/seeds/demo.sql"], tests: ["T-SW-002"], release: "DIGITAL_ONLY" },
  { category: 19, name: "MQTT integration", status: "PASS_DIGITAL", paths: ["packages/mqtt-contract/src/index.ts", "packages/mqtt-contract/fixtures/telemetry.json", "packages/mqtt-contract/fixtures/command.json", "packages/mqtt-contract/fixtures/ack.json", "apps/api/src/mqtt/bridge.ts", "infrastructure/broker/mosquitto.prod.conf", "infrastructure/broker/aclfile.template"], tests: ["T-SW-004A", "T-SW-005"], release: "DIGITAL_ONLY" },
  { category: 20, name: "Notification system", status: "PARTIAL", paths: ["apps/api/src/services/notifications.ts", "security/PROVISIONING_SECURITY.md"], tests: ["API-NOTIFICATION"], release: "DIGITAL_ONLY" },
  { category: 21, name: "Deployment", status: "BLOCKED", paths: ["infrastructure/docker-compose.dev.yaml", "infrastructure/deployment/README.md", "infrastructure/reverse-proxy/Caddyfile"], tests: ["T-SW-020"], release: "CONFIG_ONLY" },
  { category: 22, name: "Automated testing", status: "PARTIAL", paths: ["reports/TEST_MATRIX.csv", "reports/VALIDATION_SUMMARY.json", "reports/UNIT_TEST_RESULTS.md", "reports/INTEGRATION_TEST_RESULTS.md", "reports/SECURITY_TEST_RESULTS.md", "reports/PHASE_1_ENGINEERING_REPORT.md", "reports/PHASE_2_SOFTWARE_REPORT.md", "reports/AGENT_ACTION_LOG.md", "reports/FAILURES.md", "reports/CHANGELOG.md", "reports/AMENDMENT_8A_OFFBOARD.md", "reports/FIRMWARE_BUILD.md", "reports/ANDROID_BUILD.md"], tests: ["ALL"], release: "DIGITAL_ONLY" },
  { category: 23, name: "Engineering validation", status: "PARTIAL", paths: ["validation/CONNECTIVITY_DIFF.json", "validation/WIRING_CONNECTIONS.csv", "validation/NETLIST_SCHEMATIC.csv", "validation/ISOLATION_BOUNDARY_CHECK.md", "validation/PSU_CROSSCHECK.json", "scripts/validate_psu.py", "scripts/run_psu_check.py", "scripts/export_psu_artifacts.py", "reports/kicad/psu_drc.json", "reports/kicad/erc.json", "reports/kicad/drc.json", "reports/kicad/carrier_drc.json"], tests: ["T-HW-002", "T-HW-003", "T-HW-004", "T-HW-006"], release: "DIGITAL_ONLY" },
  { category: 24, name: "Security audit", status: "PARTIAL", paths: ["security/THREAT_MODEL.md", "security/SECURITY_AUDIT_REPORT.md", "security/API_AUTHORIZATION_MATRIX.csv", "security/MQTT_ACL_PLAN.md", "security/DEVICE_SECURITY_PLAN.md", "security/SBOM.json", "security/DEPENDENCY_AUDIT.json"], tests: ["SECURITY-NEGATIVE"], release: "DIGITAL_ONLY" },
  { category: 25, name: "Engineer documentation", status: "PASS_DIGITAL", paths: ["docs/README.md", "docs/START_HERE.md", "docs/FAQ.md", "docs/GLOSSARY.md", "docs/PROJECT_STATUS.md", "docs/REPOSITORY_MAP.md", "docs/ARCHITECTURE.md", "docs/HARDWARE_GUIDE.md", "docs/SOFTWARE_GUIDE.md", "docs/TESTING.md", "docs/SAFETY.md", "docs/tutorials/README.md", "docs/tutorials/00_READ_FIRST.md", "docs/tutorials/12_MAINS_ASSEMBLY_FOR_QUALIFIED_PERSONNEL.md", "docs/tutorials/23_TESTING_AND_VALIDATION.md", "docs/software/README.md", "docs/assembly/ASSEMBLY_PLAN.md", "docs/decisions/ADR-INDEX.md", "docs/decisions/ADR-013-PSU-HLK-5M05.md", "docs/decisions/ADR-014-PROCUREMENT-STAGING.md", "docs/decisions/ADR-015-DEVKITC-1-SOCKET.md", "docs/decisions/ADR-016-PZEM-ISOLATION-REV-C.md", "docs/hardware/SYSTEM_ARCHITECTURE.md", "research/PSU_BOARD_EVIDENCE.md", "hardware/psu/README.md", "research/PROCUREMENT_INDONESIA.md", "research/PZEM_INTERNAL_ISOLATION.md", "docs/decisions/ADR-002-METERING-ARCHITECTURE.md", "safety/ISOLATION_PLAN.md", "safety/FAILURE_MODE_AND_EFFECTS_ANALYSIS.md", "safety/RESIDUAL_RISK_REGISTER.csv", "safety/ELECTRICAL_RATING_CHAIN.md", "safety/PROTECTION_COORDINATION.md", "safety/CLEARANCE_CREEPAGE_WORKSHEET.md", "safety/POLARITY_AND_EARTH_ASSESSMENT.md", "safety/THERMAL_RISK_AND_DERATING.md", "safety/THERMAL_CALCULATION.md", "safety/REVIEW_SIGNOFF_TEMPLATE.md"], tests: ["DOCUMENT_REVIEW"], release: "DIGITAL_ONLY" },
  { category: 26, name: "Final handoff", status: "PARTIAL", paths: ["deliverables/FINAL_ENGINEERING_REPORT.md", "deliverables/README.md", "README.md", "README.id.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "SUPPORT.md", "CHANGELOG.md", "ROADMAP.md", "LICENSE", "NOTICE.md", "CITATION.cff", ".editorconfig", ".github/workflows/ci.yml", ".github/dependabot.yml", ".github/CODEOWNERS", ".github/PULL_REQUEST_TEMPLATE.md", ".github/ISSUE_TEMPLATE/bug_report.yml", ".github/ISSUE_TEMPLATE/feature_request.yml", ".github/ISSUE_TEMPLATE/config.yml"], tests: ["DOCUMENT_REVIEW"], release: "DIGITAL_ONLY" }
];

function latestLog(prefix) {
  const dir = resolve("reports/logs");
  if (!existsSync(dir)) return "";
  const files = execSync(`powershell -NoProfile -Command "Get-ChildItem -Path '${dir.replaceAll("\\", "/")}' -Filter '${prefix}-*.log' | Sort-Object LastWriteTime -Descending | Select-Object -First 1 -ExpandProperty Name"`, { encoding: "utf8" }).trim();
  return files;
}

const artifacts = [];
const missing = [];
const categoryStatus = [];
for (const category of CATEGORIES) {
  let allPresent = true;
  for (const relative of category.paths) {
    const path = resolve(relative);
    if (!existsSync(path) || !statSync(path).isFile()) {
      allPresent = false;
      missing.push({ category: category.category, path: relative, status: "MISSING" });
      continue;
    }
    artifacts.push({
      category: category.category,
      path: relative,
      sha256: sha256(path),
      size_bytes: statSync(path).size,
      status: category.status,
      tests: category.tests,
      evidence: [`category-${category.category}`],
      release_classification: category.release
    });
  }
  categoryStatus.push({
    category: category.category,
    name: category.name,
    status: allPresent ? category.status : "PARTIAL_MISSING_FILES",
    artifacts: category.paths.length,
    release_classification: category.release
  });
}

const validation = JSON.parse(readFileSync(resolve("reports/VALIDATION_SUMMARY.json"), "utf8"));
const traceability = JSON.parse(readFileSync(resolve("reports/TRACEABILITY_SUMMARY.json"), "utf8"));
const bom = JSON.parse(readFileSync(resolve("bom/BOM_SUMMARY.json"), "utf8"));

const blockers = [
  { id: "BLOCK-COMPONENT-LEVEL-SCHEMATIC", kind: "DESIGN", status: "BLOCKED", action_required: "Complete component-level schematic, footprints, connectivity, routing, and functional Gerber" },
  { id: "BLOCK-ESP-IDF", kind: "TOOLCHAIN", status: "BLOCKED", action_required: "Install ESP-IDF, build target firmware, test OTA/rollback" },
  { id: "BLOCK-ANDROID-DEVICE-TEST", kind: "VALIDATION", status: "BLOCKED", action_required: "Install/test debug APK on emulator/device; production signing and push/BLE remain" },
  { id: "BLOCK-POSTGRES", kind: "DEPLOYMENT", status: "BLOCKED", action_required: "Implement PostgreSQL adapter, run migrations, test" },
  { id: "BLOCK-DOCKER", kind: "DEPLOYMENT", status: "BLOCKED", action_required: "Install Docker, run compose, TLS/MQTT ACL tests" },
  { id: "BLOCK-PHYSICAL-MAINS-LAB", kind: "PHYSICAL_MAINS_LAB", status: "BLOCKED", action_required: "Qualified lab/engineer for PE/isolation/thermal/load tests" },
  { id: "BLOCK-COMPONENT-APPROVAL", kind: "COMPONENT_APPROVAL", status: "BLOCKED", action_required: "Select/verify socket, plug, relay, fuse, PSU, terminal, PE, enclosure" },
  { id: "BLOCK-CLEARANCE", kind: "SAFETY_REVIEW", status: "BLOCKED", action_required: "Complete clearance/creepage worksheet with licensed standard and engineer" },
  { id: "BLOCK-REGULATORY", kind: "REGULATORY", status: "BLOCKED", action_required: "Classify product, consult SNI/lab, do not market" },
  { id: "BLOCK-TELEGRAM-TOKEN", kind: "CREDENTIAL", status: "BLOCKED", action_required: "Provide Telegram token/chat via secret store with user approval" },
  { id: "BLOCK-SIGNED-OTA", kind: "SECURITY", status: "BLOCKED", action_required: "Implement signing key policy, signed image, rollback test" }
];

const manifest = {
  project: "esp32-s3-iot-smart-plug",
  prd_version: "1.0",
  design_revision: "REV_D_CORE_ONLY",
  generated_at: new Date().toISOString(),
  git_commit: gitCommit(),
  manifest_note: "git_commit is the source commit at generation time; this manifest file is committed immediately after.",
  device_hardware_status: "ENGINEERING_REVIEW_REQUIRED",
  hardware_validation_status: "HARDWARE_VALIDATION_REQUIRED",
  digital_status: "PARTIAL_DIGITAL",
  phase_1_status: "PARTIAL_PROVISIONAL",
  phase_2_status: "PARTIAL_DIGITAL",
  fabrication_release: "NOT_RELEASED",
  ready_for_use: false,
  summary: {
    categories: categoryStatus.length,
    artifacts: artifacts.length,
    missing_artifacts: missing.length,
    test_counts: validation.counts,
    test_overall: validation.overall,
    traceability: traceability.by_status,
    bom_pricing_status: bom.pricing_status,
    bom_rows: bom.procurement_lines,
    bom_core_subtotal_idr: bom.prototype_1_unit?.core_subtotal_idr ?? null,
    bom_core_all_in_idr: bom.prototype_1_unit?.core_all_in_idr ?? null,
    bom_full_subtotal_idr: bom.prototype_1_unit?.full_subtotal_idr ?? null
  },
  category_status: categoryStatus,
  artifacts,
  missing_artifacts: missing,
  blockers,
  test_summary: validation,
  traceability_summary: traceability,
  bom_summary: bom,
  binaries: {
    firmware: {
      path: "firmware/build/smartplug.bin",
      bytes: 192496,
      sha256: "498356348097F45F7853747C08037B05801D34BACAC65392BA466D857EFBCF0E",
      status: "BUILD_PASS_NOT_FLASHED"
    },
    android_debug_apk: {
      path: "apps/android/android/app/build/outputs/apk/debug/app-debug.apk",
      bytes: 46852340,
      sha256: "BAFCD8BDD9EB0F79DD0807ABF73D5BBE8C42087E26AD69FB086E6976B30C2B61",
      abi: "arm64-v8a",
      signing: "debug-v2",
      status: "DEBUG_BUILD_PASS_NOT_INSTALLED"
    }
  },
  toolchain: {
    node: process.version,
    npm: execSync("npm --version", { encoding: "utf8" }).trim(),
    python: "3.11.15 (.venv)",
    kicad: "10.0.8 (portable extract)",
    esp_idf: "6.1 (esp32s3 target build PASS)",
    android_sdk: "installed on D: (debug APK PASS)",
    docker: "NOT_INSTALLED",
    postgres: "NOT_INSTALLED",
    zig: "0.17.1 (portable)",
    cadquery: "2.8.0",
    wireviz: "0.4.1",
    graphviz: "16.1.1 (portable)"
  }
};

writeFileSync(OUT, JSON.stringify(manifest, null, 2), "utf8");
const checksumLines = artifacts.map((artifact) => `${artifact.sha256}  ${artifact.path}`);
writeFileSync(CHECKSUMS, checksumLines.join("\n") + "\n", "utf8");
console.log(JSON.stringify({ categories: categoryStatus.length, artifacts: artifacts.length, missing: missing.length, commit: manifest.git_commit }, null, 2));
