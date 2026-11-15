# POSITION / Pick-and-Place — NOT APPLICABLE

**Status:** `NOT_APPLICABLE`
**Reason:** The PCB is placement-only; no footprints, nets, or assembly release exist. No SMT pick-and-place file can be truthfully generated.

Do not create a fake `POSITION.csv`. When the board is routed and footprints are approved, export the position file from KiCad with the correct origin, rotation, and side conventions, then validate against the assembly drawing.
