# ROM provenance

The ROM images of the RK86 machine, as the system TBs and the platforms load them. They stay with
this machine: they are specific to the Radio-86RK, not generic for a platform.

| File | What it is | Size | SHA-256 |
|---|---|---|---|
| `monitor.bin` | the Radio-86RK monitor, 2 KB (F800-FFFF, mirrored through E000-FFFF) | 2048 | `b52bc01ce40fc03e4c6e2369b74e30ef9e9cebc6db73c03988d76587af3eb946` |
| `font.bin` | the character generator ROM of the board's video path (6 x 8 dots, 128 characters, 8 bytes each) | 1024 | `6e59b35d5595353bcc1a7dc9da1f45a84d0596e482d06f1fecc3a68367e7f156` |

## Authors

- `monitor.bin`: the Radio-86RK and its monitor were published in Радио (Moscow), 1986, by
  Д. Горшков, Г. Зеленко, Ю. Озеров and С. Попов (transliterated: D. Gorshkov, G. Zelenko,
  Yu. Ozerov, S. Popov): they sign the series' first article (No. 4, end on p. 26) and the software
  article that describes the monitor (end on No. 9, p. 28). Not yet checked against the published
  listing or a dump of an original ROM.
- `font.bin`: the character generator of the Radio-86RK. Its authorship and publication are not
  established (open): the series names the character generator ROM (No. 4, p. 24), but no scan
  read so far shows its contents; the character code table of Радио 1987 No. 5 (insert) shows the
  character set, not the ROM's bytes, and names no author.

## Origin and copy

- **Copied from:** `karabas-go-core-rk86` (fork `BarabashkaD/karabas-go-core-rk86`, upstream
  `andykarpov/karabas-go-core-rk86`) at commit `35e86e7dfdeae112873a5d727bdd5f5bd67e0e97`:
  `src/roms/BIOS.BIN` -> `monitor.bin`, `src/roms/FONT.BIN` -> `font.bin`, byte for byte.
- **Direct download:**
  https://github.com/BarabashkaD/karabas-go-core-rk86/raw/35e86e7dfdeae112873a5d727bdd5f5bd67e0e97/src/roms/BIOS.BIN
  and https://github.com/BarabashkaD/karabas-go-core-rk86/raw/35e86e7dfdeae112873a5d727bdd5f5bd67e0e97/src/roms/FONT.BIN

## Licence check

Not done yet. The repository they were copied from names its licence (`src/LICENSE.TXT`, modified
BSD; here `LICENSES/LicenseRef-Tselikov-BSD.txt`) for the monitor and the font; that is the only
licence statement found for them. The status of the original publication's code (the monitor)
and the font's status are open.
Packaging copies the files as they are.
