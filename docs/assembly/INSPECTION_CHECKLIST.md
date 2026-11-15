# Inspection Checklist — Before Any Power

**Status:** `TEMPLATE`; not executed.

## Identity/traceability

- [ ] BOM revision matches assembly.
- [ ] Each safety part MPN/lot/photo recorded.
- [ ] PZEM/CT/socket/relay/PSU/terminal datasheets available.
- [ ] Firmware version/hash recorded.

## Mechanical

- [ ] Enclosure rated for purpose; no 3D print in mains path.
- [ ] Barrier and clearances intact.
- [ ] Cable gland/strain relief anchored.
- [ ] Socket cannot rotate/pull out.
- [ ] No loose screws/metal/strands.
- [ ] OLED/button/RGB accessible without mains exposure.
- [ ] USB service cover/label.

## Electrical (low voltage first)

- [ ] 3.3 V/5 V rails not shorted.
- [ ] Relay driver OFF with MCU floating.
- [ ] I2C/UART levels correct.
- [ ] PE continuity (qualified test).
- [ ] L-N/L-PE/N-PE insulation (lab).
- [ ] Fuse/relay/terminal torque and rating.
- [ ] Thermal cutoff mounting.

## Documentation

- [ ] Photos of assembly.
- [ ] Test log with dates/instruments/operators.
- [ ] Open findings list.
- [ ] Engineer sign-off.

**If any safety item is unchecked, do not energize.**
