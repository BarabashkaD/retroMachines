# Record ID registry

Every record ID prefix that the docs under `machines/` define or cite, and where its items are.
Checked by `tools/check_records.py` of `retroICs` (`python -B <retroICs>/tools/check_records.py
--repo . --records machines --external retroICs=<checkout> --external
retroComputersDocs=<checkout>`).

- Status `here`: defined in this repo, by the first cell of a table row of a `record.md` under
  `machines/` (the row's Home). `pending`: the home does not exist yet; nothing is checked.
  `external`: defined in another repo, the first segment of the Home; checked only with
  `--external <repo>=<checkout>`, else one NOTE per repo.
- IDs: empty for a whole prefix. A list when the items of one prefix are split over several homes;
  that row then covers only the listed IDs.
- Existing IDs keep their prefix and number forever; a moved item keeps its ID in its new home. New
  items take the prefix of their home file.
- ID pattern: `[A-Z][A-Z0-9]{1,9}(?:-DEV)?-[DEM]?\d+`. Kinds in a chip record: `<P>-n` data sheet
  statement, `<P>-Dn` difference, `<P>-En` vendor erratum, `<P>-Mn` model note. This repo's
  deviations from the original machines use `RK86M-DEV-n`.
- The 8224 (CLK) and the SN7492 (IE4) are docs only: both are modelled inside the RK86 clock block
  `rk86_clocks16` (`machines/rk86/ics/README.md`). Their data sheet items are here; their board
  items live in the RK86 board record (`retroComputersDocs/computers/rk86/board.md`): CLK-11 (board
  use), IE4-4 (board wiring) and IE4-5 (the load strobe states, derived from the board's gate QD·QC
  and the 8275 CCLK).
- The CPU items that are board wiring only (CPU-5, CPU-7) are in the RK86 board record; the other
  CPU items are in the 8080A record of `retroICs`.

| Prefix | Home | Status | IDs |
|---|---|---|---|
| CLK | retroMachines/machines/rk86/ics/intel-8224/record.md | here | |
| CLK | retroComputersDocs/computers/rk86/board.md | external | CLK-11 |
| IE4 | retroMachines/machines/rk86/ics/ti-sn7492/record.md | here | |
| IE4 | retroComputersDocs/computers/rk86/board.md | external | IE4-4, IE4-5 |
| CPU | retroICs/ics/intel/8080a/record.md | external | |
| CPU | retroComputersDocs/computers/rk86/board.md | external | CPU-5, CPU-7 |
| PPI | retroICs/ics/intel/8255a/record.md | external | |
| DMA | retroICs/ics/intel/8257/record.md | external | |
| CRT | retroICs/ics/intel/8275/record.md | external | |
| VID | retroComputersDocs/computers/rk86/board.md | external | |
| GLUE | retroComputersDocs/computers/rk86/board.md | external | |
| MEM | retroComputersDocs/computers/rk86/board.md | external | |
| TAPE | retroComputersDocs/computers/rk86/board.md | external | |
| SND | retroComputersDocs/computers/rk86/board.md | external | |
| RK86M-DEV | retroMachines/machines/rk86/implementation.md | pending | |
