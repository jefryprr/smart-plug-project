# Glossary

**Design revision:** `REV_C_PSU_BOARD`

Plain-language definitions for terms used across the repository. Where a term has a specific meaning in this project, that meaning is noted.

---

## Electrical and safety

| Term | Meaning |
|---|---|
| **AC** | Alternating current. The wall supply here is 230 VAC, 50 Hz. |
| **DC** | Direct current. The PSU output is 5 VDC; the ESP32 uses 3.3 VDC. |
| **Mains** | The hazardous 230 VAC side of the product: plug, fuse, MOV, TCO, relay contacts, PZEM voltage terminals, PSU input. |
| **SELV** | Safety Extra-Low Voltage. The 5 V/3.3 V side that is designed to be separated from mains. In this project the carrier is SELV-only **by design**, but the assembly-level isolation is not yet proven. |
| **Galvanic isolation** | No direct electrical conduction path between two circuits. Energy or data crosses via a transformer, optocoupler, or digital isolator. |
| **Creepage** | Shortest distance along a surface (e.g., PCB or plastic) between two conductors. |
| **Clearance** | Shortest distance through air between two conductors. |
| **Working voltage** | The voltage a barrier sees during normal operation. It is not the same as a transient/test voltage. |
| **Overvoltage category (OVC)** | A classification of expected transient overvoltages (IEC 60664-1). The project has not finalized its OVC. |
| **Pollution degree (PD)** | A classification of contamination in the environment (IEC 60664-1). The project has not finalized its PD. |
| **Material group / CTI** | A classification of insulation material tracking resistance. The project has not finalized it. |
| **Hipot (dielectric strength test)** | Applying a specified high voltage for a specified time to verify insulation. Not performed. |
| **Insulation resistance** | Resistance across an insulation barrier, usually measured at 500 VDC. Not performed. |
| **Leakage current** | Small current that flows through or across insulation. Must be measured for mains products. Not measured. |
| **PE (Protective Earth)** | The safety ground conductor. In this project it goes from plug PE to a dedicated chassis stud to socket PE. It is never switched, fused, or routed through a relay. |
| **Class I / Class II** | Equipment classes related to PE and insulation. The final product classification is not settled. |
| **TCO (thermal cutoff)** | A one-shot thermal fuse that opens at a rated temperature. REV_C uses a SEFUSE SF96E, 99 °C rated functioning temperature, 84 °C holding, 10 A / 250 VAC. |
| **MOV (metal-oxide varistor)** | A voltage-dependent resistor used to clamp surges. REV_C uses a 275 VAC-class MOV across L/N after the fuse. |
| **Fuse** | Overcurrent protective device. REV_C uses a 5 × 20 mm 10 A / 250 VAC time-lag fuse. |
| **PTC** | Positive temperature coefficient device. Used as a resettable current limiter on the 5 V output (1.1 A in REV_C). |
| **TVS** | Transient voltage suppressor. REV_C uses an SMBJ5.0A on the 5 V rail. |
| **SPDT** | Single-pole double-throw relay contact (COM, NO, NC). The relay module has two independent SPDT channels. |
| **DPST** | Double-pole single-throw. The relay module is **not** a mechanically linked DPST. |
| **NO / NC** | Normally open / normally closed relay contact. |
| **Inrush current** | Short high current when a load or power supply starts. |
| **Derating** | Reducing a rating for temperature, load, altitude, or lifetime margin. |
| **HIL (hardware-in-the-loop)** | Testing real hardware with real inputs in a controlled loop. Not performed. |
| **DUT** | Device under test. |

---

## Components and hardware

| Term | Meaning |
|---|---|
| **ESP32-S3** | Espressif microcontroller with Wi-Fi/BLE, used on the DevKitC-1 board. |
| **DevKitC-1** | Espressif development board carrying an ESP32-S3 module. The project assumes the N16R8 variant with two 1×22 headers at 22.86 mm row spacing. |
| **Carrier** | The 100 × 70 mm SELV PCB that holds the ESP32 sockets and low-voltage peripherals. |
| **PSU board** | The separate 50 × 65 mm mains-entry PCB with fuse, MOV, TCO, HLK-5M05, and three JST 5 V outputs. |
| **HLK-5M05** | Hi-Link 5 V / 1 A / 5 W AC/DC module, 90–264 VAC input, 4 pins. Datasheet isolation claim is 2500 VAC; batch/certificate are unverified. |
| **PZEM-004T V4** | Peacefair AC energy meter module with UART and CT input. The project uses the 100 A CT variant. Batch documentation is deficient. |
| **CT (current transformer)** | Clamp that measures current without breaking the conductor. Must clamp around **one** conductor only (L), never around L and N together. |
| **Relay module** | Off-board 2-channel 5 V optocoupler relay board. Active-LOW inputs, two independent SPDT channels. |
| **OLED** | SSD1306 I²C display (128 × 64 typical). |
| **RTC** | Real-time clock. REV_C uses a DS3231 module. |
| **TMP102** | Temperature sensor present in earlier revisions; removed in REV_C. Hardware thermal protection is fuse + TCO only. |
| **JST-XH** | 2.5 mm pitch wire-to-board connector family. REV_C uses 2-pin JST-XH for 5 V outputs and several peripherals. |
| **Terminal block** | Screw-clamp connector for mains wires. REV_C uses 5.08 mm pitch parts. |
| **Gerber** | Standard PCB fabrication file format. The exported files are provisional and not released. |
| **DRC** | Design Rule Check in KiCad. `0/0` means zero violations and zero unconnected items at the checked settings. It does not prove the circuit is correct or safe. |
| **ERC** | Electrical Rule Check in KiCad. The project’s ERC is on a block-level schematic, not a component-level production schematic. |
| **Footprint** | PCB pad geometry for a component. Vendor footprint review is still required. |
| **BOM** | Bill of Materials: the list of parts, quantities, references, and status. |
| **PCBA** | Printed Circuit Board Assembly: the board plus assembled components. |
| **POS / pick-and-place** | File describing component positions for assembly. |
| **STEP / STL** | 3D CAD exchange formats. STEP is parametric/CAD; STL is a mesh for printing. |

---

## Firmware and software

| Term | Meaning |
|---|---|
| **Firmware** | Software that runs on the ESP32-S3. |
| **ESP-IDF** | Espressif IoT Development Framework. The project targets v6.1. |
| **UART** | Universal Asynchronous Receiver/Transmitter, used for PZEM serial communication (TX/RX). |
| **TX / RX** | Transmit / receive lines. TX of one side goes to RX of the other. |
| **Baud rate** | UART speed in bits per second. The PZEM batch baud rate is not yet verified. |
| **CRC** | Cyclic redundancy check, used to detect corrupted serial data. |
| **GPIO** | General-purpose input/output pin on the microcontroller. |
| **I²C** | Two-wire bus (SDA/SCL) used by the OLED and RTC. |
| **MQTT** | Lightweight publish/subscribe protocol used between device, simulator, and API. |
| **Topic** | MQTT address, e.g. `smartplug/v1/{device_id}/telemetry`. |
| **QoS** | MQTT quality-of-service level. |
| **ACK** | Acknowledgement that a command was received/applied. |
| **Telemetry** | Measurement data sent by the device (voltage, current, power, energy, status). |
| **Command** | A request to change state (ON/OFF), with ID, timestamps, actor, TTL, and idempotency. |
| **Idempotency** | Repeating the same command does not duplicate the effect. |
| **TTL** | Time-to-live; a command expires after this time. |
| **Lockout** | A fault state that prevents unsafe commands until cleared. |
| **`commanded_output`** | The state the device was asked to apply. |
| **`observed_output`** | The state verified by feedback. It is not invented by the API. |
| **`APPLIED`** | UI state shown only after a device ACK. |
| **API** | HTTP interface for auth, devices, commands, telemetry, events, analytics, automations, tariffs, budgets, diagnostics, OTA requests. |
| **OpenAPI** | Machine-readable API contract. |
| **Zod** | TypeScript schema validation library used in contracts. |
| **Fastify** | Node.js web framework used by the API. |
| **Next.js** | React framework used by the web dashboard. |
| **Expo** | React Native toolchain used by the Android app. |
| **SQLite** | Embedded database used by the development API. |
| **PostgreSQL** | Target production database; adapter/deployment not implemented. |
| **Docker Compose** | Container orchestration template included but not executed. |
| **TLS** | Encrypted transport. Production MQTT/HTTPS TLS is not deployed/tested. |
| **ACL** | Access control list, e.g. which MQTT topic a device may publish/subscribe to. |
| **RBAC** | Role-based access control. |
| **JWT** | JSON Web Token used for API access tokens. |
| **Refresh token** | Long-lived token used to rotate access tokens; stored as a hash server-side. |
| **scrypt** | Password hashing function used by the API. |
| **SBOM** | Software Bill of Materials. |
| **OTA** | Over-the-air firmware update. Signed OTA/rollback is not implemented. |

---

## Project process

| Term | Meaning |
|---|---|
| **PRD** | Product Requirements Document. The contract for the project. |
| **ADR** | Architecture Decision Record. A short document recording a decision and its consequences. |
| **Assumption register** | List of assumptions that still need evidence. |
| **Traceability** | Mapping requirements → implementation → tests → evidence. |
| **Validation** | Evidence that the right thing was built and works in the intended environment. |
| **Verification** | Evidence that the implementation matches the specification. |
| **`PASS` / `FAIL` / `BLOCKED`** | Test outcome statuses. `BLOCKED` means the test cannot run yet, not that it failed. |
| **`UNVERIFIED`** | A value or claim has not been checked. |
| **`PROVISIONAL`** | A temporary design choice that may change after review/test. |
| **`ENGINEERING_REVIEW_REQUIRED`** | A competent engineer must review before fabrication/use. |
| **`HARDWARE_VALIDATION_REQUIRED`** | Physical lab tests are still required. |
| **`NOT_FOR_FABRICATION`** | Do not send the files to a PCB manufacturer as a functional board. |
| **`READY_FOR_FABRICATION`** | Release gate F4. Not used in this repository. |
| **`READY_FOR_USE`** | Release gate for actual use. Not used. |
| **Mock** | Software fake used for tests; not physical evidence. |
| **Simulator** | Software device twin that speaks MQTT; not physical evidence. |
