# Isolation Plan — REV_A_PROVISIONAL

**Status:** `BLOCKED_PENDING_ENGINEER_REVIEW`
**Prinsip:** mains dan SELV tidak boleh tercampur. Optocoupler/isolator pada komponen bukan bukti isolasi assembly.

## 1. Boundary map

```
DOMAIN A — MAINS (230 VAC, 50 Hz)
  Plug L/N/PE → fuse → MOV → thermal cutoff → relay contacts → socket L/N
  PZEM voltage sense + CT (sisi mains)
  PSU input

DOMAIN B — PZEM ISOLATED SIDE (provisional)
  PZEM UART + isolated 5 V (B0505S output)
  Barrier: ADuM1201 (UART) + B0505S (power)

DOMAIN C — SELV (5 V / 3.3 V)
  HLK-5M05 output → carrier → ESP32-S3, OLED, button, RGB, TMP102, RTC
  Relay coil driver (SELV side)

DOMAIN D — SERVICE/USB
  DevKitC-1 USB (SELV, but physically near mains assembly)
  USB access restricted until isolation verified
```

## 2. Barrier components

| Barrier | Komponen | Rating | Bukti | Status |
|---|---|---|---|---|
| PSU AC/DC | Hi-Link HLK-5M05 | Datasheet claims 2500 VAC input-output; batch/hipot unverified | Distributor datasheet; exact batch/certificate required | `DOCUMENTATION_DEFICIENT` |
| UART | ADuM1201ARZ (bare or CJMCU module) | 2.5 kVrms class (component); module creepage unverified | Datasheet + module inspection; assembly creepage belum | `PENDING` |
| PZEM power | Mornsun B0505S-1WR3 | 1 W isolated; genuine Mornsun preferred | Datasheet; clone rejected | `PENDING` |
| Relay module coil/contact | 2-channel optocoupler module | Optocoupler input/coil; mains contact barrier UNVERIFIED | Module datasheet/batch; creepage review | `DOCUMENTATION_DEFICIENT` |
| PCB slots/barriers | Layout | TBD | Belum dirancang/diukur | `BLOCKED` |
| Enclosure barrier | Mechanical wall | TBD | Belum ada | `BLOCKED` |

## 3. Ground policy

| Ground | Koneksi | Aturan |
|---|---|---|
| PE | Plug PE → dedicated terminal/stud → socket PE | Tidak melalui relay/fuse/PCB; kontinu |
| Mains N | Relay module CH2 (COM2/NO2) → socket N | Bukan "GND"; jangan disatukan dengan SELV GND |
| PZEM isolated GND | Hanya sisi B | Tidak boleh ke SELV GND |
| SELV GND | Carrier/ESP32/OLED/sensor | Tidak boleh ke mains/PZEM GND |
| USB GND | DevKitC-1 USB | Sama dengan SELV GND; akses dibatasi saat mains |

## 4. Working voltage dan clearance

- Working voltage, overvoltage category, pollution degree, material group, dan altitude **belum ditetapkan**.
- Tidak ada nilai creepage/clearance yang diklaim di dokumen ini.
- Gunakan `safety/CLEARANCE_CREEPAGE_WORKSHEET.md` dan IEC 60664-1 yang dilisensikan.
- Slot isolasi, jarak komponen, dan barrier enclosure harus digambar pada layout final.

## 5. USB/debug restriction

- Sampai isolasi assembly diverifikasi, **jangan hubungkan USB saat mains aktif**.
- Service cover harus memerlukan alat atau memiliki label jelas.
- Jangan menaruh USB di panel depan yang mudah diakses.
- USB hanya untuk bench low-voltage pada prototipe.

## 6. Verification plan (belum dilakukan)

1. Visual inspection barrier dan creepage/clearance oleh engineer.
2. Insulation resistance test pada tegangan yang ditentukan engineer (bukan angka improvisasi).
3. Dielectric strength/hipot test oleh lab kompeten.
4. PE continuity test.
5. Leakage current test.
6. Fault injection: PSU failure, UART short, relay weld, USB connected while mains (simulasi/prosedur).
7. Review hasil dan sign-off.

**Status:** `BLOCKED`. Tidak ada klaim SELV, isolated, atau aman disentuh sampai verifikasi.
