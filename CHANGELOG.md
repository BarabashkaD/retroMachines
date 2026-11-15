# Changelog

Features, changes, fixes and known issues of each release. Versions follow semver.

## Unreleased

- The Radio-86RK machine (`machines/rk86/`): the clock, video and machine RTL, the machine TBs and
  faults, the monitor and font ROMs.
- `retroICs` as the submodule `lib/retroICs`.
- Licences: BSD-3-Clause for the owner's code, CC BY 4.0 for the owner's docs; `NOTICE`; licence
  texts in `LICENSES/`.
- The import tools (`tools/import/`: the file map, `check_map.py`, `compare_runs.py`) with their
  tests, and the compatibility matrix `docs/compat.md`, removed: the import is history.
- `NOTICE` and `machines/rk86/roms/PROVENANCE.md` credit the authors of the Radio-86RK
  publication (Radio magazine, 1986) for the monitor; the font's authorship is open. The docs use
  vendor part names.
- The RTL and TB comments use vendor part names and name no origin of the files (comment text
  only; the faults made again). A guard test (`tools/tests/test_generic.py`) keeps the repo's own
  text so. CI checks the retroComputersDocs IDs against a pinned checkout.
