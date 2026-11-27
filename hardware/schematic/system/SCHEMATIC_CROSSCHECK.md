# Schematic Cross-Check — REV_D_CORE_ONLY

Source: `hardware/psu/netlist.csv` and `hardware/carrier/netlist.csv`.

This checks net membership only. It does **not** prove creepage, clearance,
isolation, hipot, thermal, or physical fit.

## PSU board

### PASS — PSU L_IN

`F1.1, TB1.2`

### PASS — PSU L_FUSED

`F1.2, MOV1.1, TF1.1`

### PASS — PSU L_LOAD

`PS1.1, TB2.2, TF1.2`

### PASS — PSU N_MAINS

`MOV1.2, PS1.2, TB1.1, TB2.1`

### PASS — PSU +5V_PRE

`F2.2, PS1.4`

### PASS — PSU +5V

`C1.1, C2.1, D1.1, F2.1, J5.1, J6.1, J7.1`

### PASS — PSU GND

`C1.2, C2.2, D1.2, J5.2, J6.2, J7.2, PS1.3`

## Carrier board

### PASS — Carrier +3V3

`J1A.1, J1A.2, R8.1`

### PASS — Carrier RELAY_CTRL

`J1A.4, R1.1`

### PASS — Carrier BUTTON

`J1A.5, J6.1, R8.2, TP5.1`

### PASS — Carrier PZEM_TX_3V3

`J1A.10, U9.2`

### PASS — Carrier PZEM_RX_3V3

`J1A.11, R4.2, R5.1`

### PASS — Carrier PZEM_RX_5V

`J2.2, U9.3`

### PASS — Carrier PZEM_TX_5V

`J2.3, R4.1`

### PASS — Carrier RELAY_GATE

`C4.1, Q1.1, R1.2, R2.1, TP4.1`

### PASS — Carrier RELAY_IN

`J3.3, J3.4, Q1.3`

### PASS — Carrier +5V_IN

`J8.1, JP1.1`

### PASS — Carrier +5V

`C1.1, C2.1, C3.1, J1A.21, JP1.2, TP1.1, U9.14`

### PASS — Carrier GND

`C1.2, C2.2, C3.2, C4.2, J1A.22, J1B.1, J1B.21, J1B.22, J2.4, J3.2, J6.2, J8.2, Q1.2, R2.2, R5.2, TP2.1, U9.1, U9.10, U9.12, U9.13, U9.4, U9.5, U9.7, U9.9`

## Harness checks (from wiring YAML / drawing)

The following are **PASS by design review** if the drawing matches:

- P1 L -> TB1.2; P1 N -> TB1.1; P1 PE -> PE1 -> X1 PE.
- TB2 L -> K1 COM1; TB2 N -> K1 COM2; K1 NO1 -> X1 L; K1 NO2 -> X1 N.
- PSU J5 +5V/GND -> CAR J8 +5V_IN/GND; JP1 between +5V_IN and +5V.
- PSU J6 +5V/GND -> K1 VCC/GND; PSU J7 +5V/GND -> PZEM +5V/GND.
- CAR J3.3/4 (RELAY_IN) -> K1 IN1/IN2 (both tied).
- CAR J2.2 (PZEM_RX_5V) -> PZEM RX; CAR J2.3 (PZEM_TX_5V) -> PZEM TX.
- CAR J2.4 and CAR J3.2 are GND on PCB but SPARE in the harness.
- PZEM L/N sense from TB2 L/N; CT1 clamps ONLY L.
- PE is direct: plug -> stud -> socket; never fused/switched.

## Notes

- The drawing uses the design terminal **KF129-2P 25 A**. The current cart
  substitute **KF301-2P 15 A** is PROVISIONAL; it is adequate for the 6 A
  provisional load but body/creepage/terminal retention need review.
- 100 uF capacitor: 10 V or 25 V both acceptable on the 5 V rail; 25 V is
  the current cart variant.
- The PZEM V4 batch pinout must be checked against the module received.
- TCO body/pitch and socket body/depth remain UNVERIFIED until measured.

## Result

**ALL CHECKS PASS**
