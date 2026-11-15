# Sources

Each bracket source ID used under `machines/`, once. Checked by `tools/check_records.py` of
`retroICs` (the command is in `docs/record-ids.md`): every bracket ID (Latin or Cyrillic capital
first, or four digits first) in any markdown file under `machines/` must be listed here. Rules for
adding a source: `retroICs/docs/sources-policy.md`.

- Home: the index that describes the document (provenance, licence check, SHA-256). The data sheets
  of the large chips (8080A, 8255A, 8257, 8275) live in the `datasheets/index.md` of their IC
  folder in `retroICs`; the board sources of a computer, the data sheets of its board parts and of
  the clock chips modelled here (8224, SN7492) live in `retroComputersDocs/computers/<name>/index.md`.
  No document is stored in this repo.
- Kind: `vendor` (a data sheet, data book, user's manual or application note of the maker, Soviet
  reference sheets included), `board` (a schematic, PCB or magazine article of a board), `listing`
  (a ROM image or its listing, read as code), `comparison-only` (an emulator or another core: shows
  how others read a point, never a source of behaviour).

| ID | Home | Kind | Document |
|---|---|---|---|
| [C78] | retroICs/ics/intel/8080a/datasheets/index.md | vendor | Intel Component Data Catalog 1978: the 8080A, 8255A and 8257 data sheets; the 8224 pages 11-24..11-27 (`retroComputersDocs/computers/rk86/index.md`) |
| [UM83] | retroICs/ics/intel/8080a/datasheets/index.md | vendor | Intel MCS-80/85 Family User's Manual, January 1983 |
| [D79] | retroICs/ics/intel/8275/datasheets/index.md | vendor | Intel 8275 data sheet 1979, 00224A, preliminary |
| [D84] | retroICs/ics/intel/8275/datasheets/index.md | vendor | Intel 8275 data sheet 1984, AFN-00224B/C |
| [D8224] | retroComputersDocs/computers/rk86/index.md | vendor | Intel 8224 clock generator data sheet, order 231464-001, November 1992 |
| [ГФ24] | retroComputersDocs/computers/rk86/index.md | vendor | КР580ГФ24 reference sheet (the Soviet equivalent of the 8224) |
| [7490] | retroComputersDocs/computers/rk86/index.md | vendor | TI SN7490A, SN7492A, SN7493A data sheet, SDLS940A |
| [ИЕ4] | retroComputersDocs/computers/rk86/index.md | vendor | К155ИЕ4 reference sheet (the Soviet equivalent of the SN7492) |
| [R86] | retroComputersDocs/computers/rk86/index.md | board | Радио 1986 No. 5, pp. 31-34: text and the main board schematic, Fig. 3 |
| [K14] | retroComputersDocs/computers/rk86/index.md | board | S. Kiselev, Radio-86RK re-make rev. 1.4: schematic and KiCad nets |
| [APG] | retroComputersDocs/computers/rk86/index.md | comparison-only | MiSTer-devel/Apogee_MiSTer at `4b37da2`: `k580vt57.v`, `k580vg75.sv` |
| [MAME] | retroComputersDocs/computers/rk86/index.md | comparison-only | mamedev/mame at `d077ea2`: `i8275.cpp`, `i8257.cpp`, `radio86.cpp` |
| [EMU] | retroComputersDocs/computers/rk86/index.md | comparison-only | vpyk/emu80v4 at `a243b8e`: `Crt8275.cpp`, `Dma8257.cpp` |
