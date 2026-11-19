# Low-Voltage Assembly

**Scope:** CORE-only SELV carrier, headers, button, 5 V input. No OLED/RTC/external RGB. **No mains.**

## Tools

- ESD strap/mat, temperature-controlled iron, SAC305, flux, magnification, multimeter.
- Low-voltage bench supply with current limit.

## Steps

1. Inspect PCB for defects.
2. Solder low-profile passives, then ICs/connectors.
3. Install headers/standoffs; do not force.
4. Connect only the physical button and the 5 V/PZEM/relay harnesses via keyed JST-XH. OLED/RTC/external RGB are not fitted.
5. Continuity check: 3.3 V/GND not shorted; I2C/UART nets correct.
6. Apply 5 V current-limited; measure current; check no heat/smell.
7. Flash/test only with a low-voltage fixture (no mains).

## QC

- [ ] No solder bridges.
- [ ] IC/LED polarity correct.
- [ ] Connectors keyed/latched.
- [ ] No exposed wire strands.
- [ ] Current within expected budget.
- [ ] Relay driver defaults OFF (gate pulldown).

## Stop

Stop on short, overcurrent, hot component, or damaged pad. Rework before power.
