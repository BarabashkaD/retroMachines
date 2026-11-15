# Intel 8224 clock generator

## Function

Clock generator and driver for the 8080A: Φ1, Φ2 and Φ2 (TTL) from a crystal (÷9), the RESET and
READY synchronisers, STSTB.

## Pinout

The pins with their data sheet behaviour: `record.md`, CLK-1..CLK-10 ([D8224] 1-50 Fig. 1).

## Model status

Docs only, no component of its own (no manifest, RTL, tests or faults in this folder). Modelled
inside `rk86_clocks16`, the clock block of this machine (`machines/rk86/rtl/rk86_clocks16.v`);
its checks are the machine's test `clocks16` (`machines/rk86/tb/tb_clocks16.v`) and its faults.
It moves to `retroICs` with a model of its own when the clock block is split
(`machines/rk86/ics/README.md`).

## Equivalents

| Part | Transliteration | Level |
|---|---|---|
| КР580ГФ24 | `kr580gf24` | unverified |

Details: `equivalents.md`.

The identity it had as a `retroICs` component (its manifest's values, kept here as text): name
`intel/8224`, kind `ic`, title "Intel 8224 clock generator", reproduces `i8224`, fidelity
`datasheet`, record prefix `CLK`; one equivalent, the one in the table above.

## Sources

`record.md` (items); the documents: `retroComputersDocs/computers/rk86/index.md` ([D8224] with the
stored PDF, [ГФ24]) and `retroICs/ics/intel/8080a/datasheets/index.md` ([C78]); `docs/sources.md`
(the source IDs of this repo).

## Licence

The docs of this folder: CC BY 4.0 (`NOTICE`). The data sheets are not stored here; they keep their
own status (`retroComputersDocs/computers/rk86/index.md`).

## Notes for agents

- Scope: the data sheet record, the equivalents and the model notes of the Intel 8224. Docs
  only: the behaviour is modelled inside `rk86_clocks16`; a change of it is a change of that
  block, with its test and faults in the same change (`AGENTS.md`).
- Files: `README.md`, `record.md` (CLK-n items, SILENT, assumptions checked, timing reference a),
  `equivalents.md`, `implementation.md`. The data sheets and their index are in
  `retroComputersDocs/computers/rk86/`.
- Commands: the record checker of `retroICs`, as `docs/record-ids.md` gives it; the privacy check
  and the tools' tests as in `AGENTS.md`.
- Record prefix: `CLK` (`docs/record-ids.md`). IDs are never renumbered; a new item takes the next
  free number. CLK-11 (board use) is a board item, defined in the RK86 board record
  (`retroComputersDocs/computers/rk86/board.md`), so a new item takes the number after CLK-11.
- Review checklist: `lib/retroICs/docs/agents/review-checklist.md`; each item cites its source ID,
  page and figure; SILENT items say what was searched.
- Pitfalls: emulators ([MAME], [EMU], [APG]) are comparison-only, never a source of behaviour.
  Timing check a is in this record; b and d are in the 8257 and 8275 records of `retroICs` ("Timing
  (data sheet)", in data sheet units), with their 16 MHz values in
  `machines/rk86/ics/timing-16mhz.md`; c (the 8275 pins on the boards) is board wiring, in the RK86
  board record.
