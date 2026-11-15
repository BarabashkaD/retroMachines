# rk86 ics: the chips modelled inside this machine

The records of the two chips that this machine models inside its own clock block, and the 16 MHz
values of the chip timing.

| Path | Content |
|---|---|
| `intel-8224/` | Intel 8224 clock generator: `record.md` (CLK-n), `equivalents.md`, `implementation.md`, `README.md` |
| `ti-sn7492/` | TI SN7492 divide-by-twelve counter: `record.md` (IE4-n), `equivalents.md`, `implementation.md`, `README.md` |
| `timing-16mhz.md` | the chip timing of the `retroICs` records (8257, 8275: data sheet units) in the 16 MHz timebase of this machine: oscillator periods p0..p8, `rel N` |

## Why these two chips live here

- The 8224 and the SN7492 have no model of their own. Both are modelled inside the RK86 clock
  block `rk86_clocks16` (`machines/rk86/rtl/rk86_clocks16.v`), so
  their records live with that block: docs only (record, equivalents, model notes), no manifest,
  no RTL, tests or faults of their own; the clock block's test `clocks16` checks their items.
- They move to `retroICs`, each with a model of its own, when the clock block is split (when a
  second machine needs either chip). Their IDs (CLK-n, IE4-n) go with them.
- Their board-wiring items (CLK-11 board use, IE4-4 board wiring, IE4-5 the load strobe states)
  are listed one by one in `docs/record-ids.md`, with their home in the RK86 board record
  (`retroComputersDocs/computers/rk86/board.md`).
- The data sheets and their index are in `retroComputersDocs/computers/rk86/` (`index.md`,
  `datasheets/`); the [C78] data book in `retroICs/ics/intel/8080a/datasheets/`.
