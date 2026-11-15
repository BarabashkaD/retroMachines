# TI SN7492 divide-by-twelve counter: data sheet record

Data sheet items of the TI SN7492 (its Soviet equivalent: `equivalents.md`), with the IDs they had in `retroICs`. The board wiring (IE4-4) and the load strobe states it gives (IE4-5) are board items, defined in the RK86 board record (`retroComputersDocs/computers/rk86/board.md`, "Clock chips on the board"); this repo's `docs/record-ids.md` names their home.

## Sources

Sources: [ИЕ4] `k155ie4.pdf` (+ `.txt`); [7490] `sn74ls90.pdf` (TI SDLS940A, SN7492A: pp. 1-3, 7).

Not sources of behaviour: emulators and other FPGA cores ([MAME], [EMU], [APG]: comparison-only).

The documents cited here and their provenance: [ИЕ4] and [7490] in `retroComputersDocs/computers/rk86/index.md`; every source ID of this repo: `docs/sources.md`.

## Notation

The original IDs are kept; new functions are numbered after them. The timing checks are not repeated here: a (the 8224, p0..p8 = the 9 oscillator periods of a Φ cycle) in `machines/rk86/ics/intel-8224/record.md`, "Timing reference"; b and d in the chips' records in `retroICs` (`ics/intel/8257/record.md`, `ics/intel/8275/record.md`, "Timing (data sheet)"), their 16 MHz values in `machines/rk86/ics/timing-16mhz.md`; c (the 8275 pins on the boards) is board wiring: `retroComputersDocs/computers/rk86/board.md`, "The 8275 pins on the boards". The counter's counts 0..11 are those of IE4-1. Renders cited by name are page crops of the cited documents, kept with the maintainer's source collection, not in this repository (`<document>_pNN` = PDF page NN; `_cA_B_C_D` = a crop in percent of the page: left, top, right, bottom; `...` stands for `Radio_Magazine-1986-05-page-32-33-Schematic_p01`). Researched 2026-11-10.

## Items (IE4-n)

| ID | Function | Data sheet behaviour (pins, edges, values) | Source (document, page / figure) |
|---|---|---|---|
| IE4-1 | Count sequence | With QA connected to CKB (Note C), count QD QC QB QA: 0 0000, 1 0001, 2 0010, 3 0011, 4 0100, 5 0101, 6 1000, 7 1001, 8 1010, 9 1011, 10 1100, 11 1101 (the sequence of `ie4_of` in `machines/rk86/tb/tb_clocks16.v`). [ИЕ4] weights its outputs 1, 2, 4, 6 ([R86] D3 labels "1", "4", "6") | [7490] p. 3 '92A count sequence; [ИЕ4] p. 1 truth table |
| IE4-2 | Counting edges | Four master-slave flip-flops: QA toggles on CKA↓ (÷2); the ÷6 section (QB, QC ÷3, then QD ÷2) counts on CKB↓; QD is clocked by the ÷3 section ('92 logic symbol: DIV2 clocked by "Z4" of DIV3; QD changes when QC falls: 5→6, 11→0). Ripple: CKA→QA tPLH ≤ 16 / tPHL ≤ 18 ns; CKB→QC ≤ 16 / ≤ 21; CKB→QD ≤ 32 / ≤ 35; CKA→QD ≤ 48 / ≤ 50 ns (typ. 10-34). fmax CKA ≥ 32 MHz | [7490] p. 1 description, p. 2 logic symbol, p. 7 switching characteristics; [ИЕ4] p. 2 (≤ 100 ns from C1) |
| IE4-3 | Reset | R0(1), R0(2) (pins 6, 7): both high → all outputs low; on both boards both are grounded (no reset; the counter runs from power-up in a random state) | [7490] p. 3 reset table; [ИЕ4] p. 1 notes 2, 3; [R86] D3 pins 6, 7 to ground (crop `..._c35_63_60_95.png`); [K14] U15.6, U15.7 GND |

## Edition differences (IE4-Dn)

None recorded.

## SILENT (IE4)

- The power-up count (no reset on either board) and its phase against the 8224 (CLK SILENT, `machines/rk86/ics/intel-8224/record.md`).

## Assumptions checked

None recorded.

## Hardware checks

None planned.
