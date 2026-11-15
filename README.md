# retroMachines

Machines built from the `retroICs` models: the board glue, clocks and video path of each original
computer, its ROMs, testbenches and faults. The machine tops are platform-neutral.

## Status

One machine: the Radio-86RK with the original 16 MHz timing.

| Machine | Folder | Content |
|---|---|---|
| Radio-86RK, 16 MHz timing | `machines/rk86/` | `component.toml`, `rtl/` (clocks, video path, machine), `tb/`, `faults/`, `roms/` (monitor, font, `PROVENANCE.md`), `ics/` (the records of the 8224 and the SN7492, modelled in the clock block; the 16 MHz timing values), `README.md` |

The machine instantiates the `retroICs` models `intel_8080a`, `intel_8255a`, `intel_8257` and
`intel_8275`; the board records, schematics and magazine scans it cites by source ID
(`docs/sources.md`) are in `retroComputersDocs`.

## Layout

| Path | Content |
|---|---|
| `AGENTS.md` | rules for coding agents in this repo |
| `lib/retroICs/` | submodule: the IC models, the agent rules (L0) and the tools (`check_privacy.py`, `check_records.py`, `simrun`) |
| `machines/<name>/` | one folder per machine |
| `docs/record-ids.md`, `docs/sources.md` | the record ID prefixes and the source IDs that the docs under `machines/` define or cite, with their homes |
| `tools/tests/` | the tools' tests; `wording_lib.py`, this repo's wording and header helpers; `test_generic.py`, the guard of the repo's own text |

## Clone

```text
git clone --recursive https://github.com/BarabashkaD/retroMachines
git submodule update --init --recursive      in a clone made without --recursive
```

## Licences

- The owner's files: every Markdown file CC BY 4.0, every other file BSD-3-Clause (`LICENSE`).
- Third-party files keep their own licence, named in each file header; all texts are in
  `LICENSES/`. Faults are under the licence of the file they patch.
- The ROM images are not the owner's work: their authors (the monitor's; the font's is open),
  where the copies come from and their licence status are in `machines/rk86/roms/PROVENANCE.md`.
- Copies and derived works keep `NOTICE`: the owner's copyright notice (BSD-3-Clause) and the
  attribution to Dmitry Veremeev (BarabashkaD) (CC BY 4.0), which the licences require, and the
  credit to the monitor's authors; the IC models carry the credits of `retroICs` (its `NOTICE`).
