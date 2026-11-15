# Assembly Plan — REV_A_PROVISIONAL

**Status:** `DIGITAL_PLAN_ONLY`; no physical assembly performed.

## Three separate scopes

1. **Mechanical assembly, no energy** — anyone trained for basic tools.
2. **Low-voltage assembly** — trained person, ESD/solder QC.
3. **Mains assembly** — qualified personnel only, lab procedure, engineer sign-off.

Never combine scope 3 with scope 1/2 in one unsupervised session.

## Order

1. Incoming inspection: photos, marking, dimensions, datasheet match.
2. Mechanical: inserts, standoffs, carrier, OLED/button/RGB, gland, PE stud.
3. Low-voltage: headers, I2C/UART, relay driver, sensors; continuity/ESD QC.
4. Mains modules: fuse/MOV/TCO/relay/PSU/terminal/socket; ferrules, torque, strain relief.
5. Inspection: PE continuity, clearance, barrier, no loose metal, label.
6. Lab: insulation/hipot, thermal rise, load/inrush, relay lifecycle.
7. Sign-off: `safety/REVIEW_SIGNOFF_TEMPLATE.md`.
8. Only then consider energization under lab procedure.

## Stop conditions

- PE not continuous.
- Clearance/creepage not reviewed.
- Relay/fuse/terminal/socket rating unverified.
- Enclosure not rated/certified.
- Any doubt about isolation.
- No engineer/lab.

## Evidence to record

- Component photos/serials/lots.
- Torque values, wire gauge/ferrules.
- PE continuity and insulation results.
- Thermal/load curves.
- Firmware version/hash.
- Photos of final assembly.
- Signed checklist.
