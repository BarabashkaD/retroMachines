# AGENTS.md

Instructions for coding agents in `retroMachines`. Read `lib/retroICs/docs/agents/global.md` (the
L0 rules) and `lib/retroICs/docs/agents/review-checklist.md` first. They apply to every repo of the
family.

## Repository

- Machines of 8080-based home computers, built from the IC models of `retroICs`.
- Depends on `retroICs`, pinned as the submodule `lib/retroICs` (clone with `--recursive`, or
  `git submodule update --init --recursive`). Platform repos pin this repo.
- One folder per machine: `machines/<name>/` with `rtl/`, `tb/`, `faults/`, `roms/` (each image in
  `roms/PROVENANCE.md`). Board blocks shared by two or more machines go to `blocks/` on their
  second use.
- Board records (`board.md` of a computer) live in `retroComputersDocs`. It is never a submodule.
- `machines/rk86/`: the Radio-86RK. It instantiates the `retroICs` models by their vendor names
  (`intel_8080a`, `intel_8255a`, `intel_8257`, `intel_8275`); its TBs reach the 8080 model through
  the wrapper's instance `core` (`dut.cpu.core.<name>`). The manifest is edited by hand (a
  `match = "anywhere"` fault gives its reason in its own comment).
- Docs: `README.md`, `machines/rk86/README.md`.

## Commands

From the repo root, in PowerShell 7 (`pwsh`). Python 3, standard library only, always with `-B`.

```text
git submodule update --init --recursive                      the retroICs submodule
python -B -m unittest discover -s tools/tests -v             the tools' tests
python -B lib/retroICs/tools/check_privacy.py --repo .       working tree
python -B lib/retroICs/tools/check_privacy.py --repo . --all working tree and every commit
git clone https://github.com/BarabashkaD/retroComputersDocs build/retroComputersDocs
git -C build/retroComputersDocs checkout <RCD_REF>            once: the commit RCD_REF of .github/workflows/checks.yml
python -B lib/retroICs/tools/check_records.py --repo . --records machines --external retroICs=lib/retroICs --external retroComputersDocs=build/retroComputersDocs
                                                             the record and source IDs (docs/record-ids.md, docs/sources.md),
                                                             as CI checks them; without the second --external a NOTE says
                                                             the retroComputersDocs IDs are not checked
$env:PYTHONPATH = 'lib/retroICs/tools'                       then simrun:
python -B -m simrun run machines --tier quick [--negative]   the TBs (and faults); Icarus Verilog 13.0
python -B -m simrun run lib/retroICs/ics machines --tier full --negative --search . --search lib/retroICs
                                                             every test and fault of both repos
```

The machine TB's memory model is `machines/rk86/tb/tb_rk86_mem16.v`; a platform compiles its own
memory with `simrun run ... --replace machines/rk86/tb/tb_rk86_mem16.v=FILES`. `--param FRAMES=N`
sets the machine TB's frame count (default 12).

The IC files change in retroICs under its own rules; this repo's guards cover its own RTL, TBs and
docs.

The tools' tests include the wording test (`tools/tests/test_wording.py`): the patterns and file
scope of `tools/tests/wording_lib.py` (this repo's wording and header helpers, not read by other
repos), with this repo's `KEPT` list (path, hit and a fragment of its line, with the reason: the
pattern hits kept as they are, a clock step and the fault expect texts that match it; the same hit
on another line still fails; a stale entry fails). `RETRO_PRIVATE_WORDS` adds a private word list,
as in retroICs; without it the test prints a NOTE; a word of that list in kept text is exempt only
for its file through this repo's `WORD_EXEMPT` in `test_wording.py` (path, word, reason; a stale
entry fails). The guard (`tools/tests/test_generic.py`) fails on the repository the machine was
imported from, its commits and old paths, the projects that use this repo, planning wording and
the Soviet part names, outside `GENERIC_EXEMPT` (path, word, line fragment, with its reason: an
equivalent, the provenance of a stored copy, board evidence, a quoted title, a file or module name
or a language keyword, a credit; a stale entry fails); it takes out the bracket source IDs of
`docs/sources.md` first, reads the fault patches and skips `CHANGELOG.md`.
`tools/tests/test_headers.py` applies the family's header rule (SPDX lines in every `.v`, `.vh`,
`.py`, `.toml` header, licence pointers into `LICENSES/`).

## Rules for this repo

- Every rule of `lib/retroICs/docs/agents/global.md`.
- An IC changes in `retroICs` and comes in by moving the submodule pin (its own tests first); never
  copy or patch an IC model here.
- A machine folder changes only with its own tests and faults in the same PR.
- A comment-only change of RTL is a commit of its own and passes
  `lib/retroICs/tools/check_comment_only.py --repo . <base> <head> --paths 'machines/*/rtl/*'`
  (with `--anywhere` when it changes comments below the header); the faults on a changed file are
  made again with `git diff`. The check compares the positions of the changes, so a fault that adds
  or removes lines above a changed comment line fails it (a limit of the check): keep such a
  comment as it is.
- Vendor part names (8080A, 8224, 8255A, 8257, 8275, SN7492, SN74198, SN7474) in this repo's own
  text; the Soviet names only in the equivalents (`equivalents.md`, the equivalents table of a
  README), in source IDs and quoted source titles, and in board evidence.

## Machine rules

`lib/retroICs/docs/agents/global.md` still applies (source priority, SILENT items, never an
emulator as a source of behaviour). For a machine of this repo it reads:

- Where a chip's data sheet is silent on a board point, the original board is the basis: its
  picture and its timing, cited by source ID (`docs/sources.md`), then the simplest reading of the
  data sheet.
- Sources for board items: the original board schematics and the magazine publications (Радио, the
  board makers' documents), cited by source ID; the ROM listings, read as code.
- Emulators (MAME, Emu80 and others) and other FPGA cores are `comparison-only`: they may show how
  others read a point; a decision never rests on them.
- A board item lives in the board record (`retroComputersDocs`, `computers/<name>/board.md`) under
  its board prefix; a deviation of this repo's machine from the original board uses `RK86M-DEV-n`
  (`docs/record-ids.md`).
- `NOTICE` names this repo only, with its attribution line (`Contains retroMachines by ...`), and
  credits the original authors whose work its files contain (the monitor ROM); a build that
  includes the IC models carries retroICs' `NOTICE` too. This repo never names the projects that
  use it.

## Releases

- Semver, immutable `vX.Y.Z` tags, PR-only `main` ("Rebase and merge"). The maintainer merges and
  tags by hand; an agent never creates a tag or a release.
- A release pins a tagged `retroICs`.
- CHANGELOG and release notes list features, changes, fixes and known issues only; no test results,
  no hardware results.
