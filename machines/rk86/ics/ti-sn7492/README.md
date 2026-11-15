# TI SN7492 divide-by-twelve counter

## Function

Ripple counter: a ÷2 stage (QA) and a ÷6 stage (QB, QC, QD); with QA connected to CKB it counts
0..11 (÷12).

## Pinout

The pins with their data sheet behaviour: `record.md`, IE4-1..IE4-3 ([7490] pp. 1-3).

## Model status

Docs only, no component of its own (no manifest, RTL, tests or faults in this folder). Modelled
inside `rk86_clocks16`, the clock block of this machine (`machines/rk86/rtl/rk86_clocks16.v`);
its checks are the machine's test `clocks16` (`machines/rk86/tb/tb_clocks16.v`) and its faults.
It moves to `retroICs` with a model of its own when the clock block is split
(`machines/rk86/ics/README.md`).

## Equivalents

| Part | Transliteration | Level |
|---|---|---|
| К155ИЕ4 | `k155ie4` | unverified |

Details: `equivalents.md`.

The identity it had as a `retroICs` component (its manifest's values, kept here as text): name
`ti/sn7492`, kind `ic`, title "TI SN7492 divide-by-twelve counter", reproduces `sn7492`, fidelity
`datasheet`, record prefix `IE4`; one equivalent, the one in the table above.

## Sources

`record.md` (items); the documents: `retroComputersDocs/computers/rk86/index.md` ([7490], [ИЕ4]);
`docs/sources.md` (the source IDs of this repo).

## Licence

The docs of this folder: CC BY 4.0 (`NOTICE`). The data sheets are not stored here; they keep their
own status (`retroComputersDocs/computers/rk86/index.md`).

## Notes for agents

- Scope: the data sheet record, the equivalents and the model notes of the TI SN7492. Docs
  only: the behaviour is modelled inside `rk86_clocks16`; a change of it is a change of that
  block, with its test and faults in the same change (`AGENTS.md`).
- Files: `README.md`, `record.md` (IE4-n items, SILENT, assumptions checked), `equivalents.md`,
  `implementation.md`. The data sheets' index is in `retroComputersDocs/computers/rk86/`.
- Commands: the record checker of `retroICs`, as `docs/record-ids.md` gives it; the privacy check
  and the tools' tests as in `AGENTS.md`.
- Record prefix: `IE4` (`docs/record-ids.md`). IDs are never renumbered; a new item takes the next
  free number. IE4-4 (board wiring) and IE4-5 (load strobe states) are board items, defined in the
  RK86 board record (`retroComputersDocs/computers/rk86/board.md`), so a new item takes the number
  after IE4-5.
- Review checklist: `lib/retroICs/docs/agents/review-checklist.md`; each item cites its source ID,
  page and figure; SILENT items say what was searched.
- Pitfalls: emulators ([MAME], [EMU], [APG]) are comparison-only, never a source of behaviour.
  Timing check a (the 8224) is in `machines/rk86/ics/intel-8224/record.md`; b and d are in the 8257
  and 8275 records of `retroICs` ("Timing (data sheet)", in data sheet units), with their 16 MHz
  values in `machines/rk86/ics/timing-16mhz.md`; c (the 8275 pins on the boards) is board wiring, in
  the RK86 board record.
