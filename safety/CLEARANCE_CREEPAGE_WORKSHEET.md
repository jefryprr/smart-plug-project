# Clearance & Creepage Worksheet — REV_D_CORE_ONLY

**Status:** `BLOCKED_INPUTS_INCOMPLETE`
**Catatan:** Dokumen ini **tidak** menetapkan angka clearance/creepage. Angka harus diturunkan dari IEC 60664-1 (edisi yang berlaku) oleh engineer kompeten, berdasarkan input di bawah. Jangan memakai angka contoh dari internet.

## 1. Input yang wajib

| Input | Nilai | Sumber | Status |
|---|---|---|---|
| Working voltage (RMS/peak) | 230 VAC nominal; peak/transient TBD | Desain | `PARTIAL` |
| Overvoltage category | TBD (II/III?) | Klasifikasi produk/instalasi | `OPEN` |
| Pollution degree | TBD (2?) | Enclosure/environment | `OPEN` |
| Material group (PCB/enclosure) | TBD (I/II/IIIa/IIIb) | Datasheet material/CTI | `OPEN` |
| Altitude | TBD (Jakarta ~8 m? site) | Lokasi | `OPEN` |
| Rated impulse voltage | TBD | Standar/kategori | `OPEN` |
| Working voltage across barrier | TBD | Isolation plan | `OPEN` |
| Transient/overvoltage test level | TBD | Standar | `OPEN` |
| PCB coating/potting | TBD | Proses | `OPEN` |
| Slot/barrier construction | TBD | Layout | `OPEN` |

## 1A. REV_D_CORE_ONLY PSU board geometry (provisional, not a compliance claim)

| Item | Value | Status |
|---|---|---|
| Board | 50 x 65 mm, 2-layer FR4 1.6 mm, 2 oz target | `PROVISIONAL` |
| Isolation notch | 2 mm routed slot at x=19..21, y=0..45; HLK bridges | `UNVERIFIED` |
| L/N traces | 4 mm; provisional spacing 6-12 mm to SELV/edges | `UNVERIFIED` |
| HLK | 38 x 23 x 18 mm; 4 pins at datasheet positions; AC/DC barrier internal | `DATASHEET_DERIVED` / sample check required |
| Terminals/fuse/TCO/JST | 5.08 mm/5x20/2.5 mm; exact ratings TBD | `DOCUMENTATION_DEFICIENT` |

DRC 0/0 only proves the KiCad geometry rules used, **not** IEC clearance/creepage. A qualified engineer must calculate and approve the final values.

## 2. Metode

1. Tentukan klasifikasi produk dan standar akhir (IEC 60884-1, IEC 60664-1, IEC 61058-1, standar relay/PSU/fuse/enclosure).
2. Tentukan overvoltage category, pollution degree, material group, altitude.
3. Hitung working voltage dan rated impulse voltage.
4. Ambil tabel clearance/creepage dari standar yang dilisensikan.
5. Terapkan pada setiap pasangan net: L-N, L-PE, N-PE, mains-SELV, PZEM-SELV, relay contact-coil, fuse holder, terminal, socket.
6. Tambahkan toleransi manufaktur dan assembly.
7. Review layout, slot, barrier, dan potensi kontaminasi.
8. Sign-off engineer.

## 3. Tabel keputusan (diisi engineer)

| Pasangan | Working voltage | Clearance min | Creepage min | Metode | Margin aktual | Status |
|---|---:|---:|---:|---|---:|---|
| L ↔ N | TBD | TBD | TBD | IEC 60664-1 | TBD | `OPEN` |
| L ↔ PE | TBD | TBD | TBD | IEC 60664-1 | TBD | `OPEN` |
| N ↔ PE | TBD | TBD | TBD | IEC 60664-1 | TBD | `OPEN` |
| Mains ↔ SELV | TBD | TBD | TBD | IEC 60664-1 | TBD | `OPEN` |
| PZEM ↔ SELV | TBD | TBD | TBD | IEC 60664-1 | TBD | `OPEN` |
| Relay contact ↔ coil | TBD | TBD | TBD | Relay datasheet + IEC 60664-1 | TBD | `OPEN` |
| Fuse holder ↔ nearby | TBD | TBD | TBD | IEC 60664-1 | TBD | `OPEN` |
| USB ↔ mains | TBD | TBD | TBD | IEC 60664-1 | TBD | `OPEN` |

## 4. Aturan desain

- Jangan mengurangi clearance untuk memenuhi target 150×100×70.
- Jangan mengandalkan solder mask sebagai isolasi.
- Slot isolasi hanya jika benar-benar menambah creepage dan tidak mengurangi kekuatan mekanik.
- Barrier enclosure harus tahan panas/kelembapan dan tidak mudah tergeser.
- Kabel mains tidak boleh melintasi area SELV tanpa barrier.
- Komponen dengan pin tajam/terminal terbuka harus dijauhkan dari akses pengguna.

## 5. Sign-off

| Peran | Nama | Tanggal | Keputusan |
|---|---|---|---|
| Engineer kompeten | **BELUM ADA** | — | `BLOCKED` |
| Reviewer regulatory | **BELUM ADA** | — | `OPEN` |

**Status:** `BLOCKED`. Jangan fabrikasi sampai tabel ini terisi dan ditandatangani.
