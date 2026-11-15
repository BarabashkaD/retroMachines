# rk86: the Radio-86RK machine with the original 16 MHz timing

Every chip is reproduced to its own data sheet (Intel 8224, 8255A, 8257, 8275; TI SN7492,
SN74198, SN7474; the 8080A is Vslav's die-derived model) and the board schematics (Радио 1986 No. 4-5, [R86]; S. Kiselev's re-make 1.4,
[K14]); emulators are not sources of behaviour.

| File | Content |
|---|---|
| `rtl/rk86_clocks16.v` | the clock block: the 8224 and the SN7492 of the board |
| `rtl/rk86_video16.v` | the video path up to the composite mixer: the font ROM, the SN74198 shift register, the SN7474 flip-flop that re-times LTEN |
| `rtl/rk86_machine16.v` | the machine: the board glue around the chip models and the two blocks above |
| `tb/`, `faults/` | the TBs of the three files and their faults (`component.toml`) |
| `roms/` | the monitor and the font, with their provenance (`roms/PROVENANCE.md`) |
| `ics/` | the records of the 8224 and the SN7492, and the 16 MHz timing values |

The chip models are those of `retroICs` (the submodule `lib/retroICs`): `intel_8080a` (the 8080
model `ics/intel/8080a/rtl/upstream/k580vm80a.v` is the wrapper's instance `core`),
`intel_8255a`, `intel_8257`, `intel_8275`, under `ics/intel/<part>/rtl/`. Their authors, origins
and licences are in retroICs' `NOTICE`. Each file's SPDX header names its licence; this
machine's own files are BSD-3-Clause (this README CC BY 4.0, `NOTICE`).

The two clock chips that `rk86_clocks16.v` models (the Intel 8224 and the TI SN7492)
have their data sheet records in this folder: `ics/intel-8224/` (CLK-n) and `ics/ti-sn7492/`
(IE4-n); why they live here: `ics/README.md`. The timing of the 8257 and 8275 records of
`retroICs` (data sheet units) in this machine's 16 MHz timebase: `ics/timing-16mhz.md`.

## The board glue (`rk86_machine16.v`)

The address decoder (D11 on A13-A15) works on the system address, which is the 8257's while its AEN is
high, and ЧТЕНИЕ (DBIN XOR the 8257 MEMW) enables whatever it selects. So a read, by the CPU or by the DMA,
gets the device at the system address: the RAM at 0000-7FFF, the keyboard 8255 at 8000-9FFF, the window
(`ext_di`) at A000-BFFF, the 8275's own read data at C000-DFFF, the monitor ROM (`rom` high) at E000-FFFF;
during start-up the monitor at every address (the 8257 is reset then). The 8275 takes the DMA byte from that
same read path (GLUE-1, GLUE-2, GLUE-3, GLUE-10). The RK86 monitor points the
8257 only at the RAM; a program that puts the screen elsewhere sees what the boards show. The 8275 WR is the
CPU WR AND the 8257 IOR; the memory write strobe is the CPU WR. Machine TB: the glue checks at every clk,
and a forced DMA read pass over 0000-FFFF after the frames (fault `dma_rom_from_ram`).

## Decisions where the data sheets are silent

Where a data sheet does not decide a behaviour, the board decides (the picture and timing of the Радио 1986
and Kiselev 1.4 boards); the decision is marked `// SILENT` (with its record ID where it has one) at the
code line that decides it. These recorded decisions are in the code without an inline marker:

- `intel_8255a.v`: PC3 takes its direction from control bit 0 and a port C byte write changes the free upper
  bits (PPI-24, PPI-29); RD and WR act only with CS low and the port's A1 A0 (PPI-31); the input latch
  follows the port while STB is low (PPI-32).
- `intel_8257.v`: a mode write resets the rotating priority (DMA-2); a status read clears the TC bits at IOR↑
  (DMA-8); CS is ignored only in S1-S4 (DMA-14); RESET keeps the address and count registers (DMA-13);
  the back-to-back channel is chosen at the θ↓ that starts S4, after any wait states (DMA-1, DMA-7, DMA-29);
  the update flag clears at the θ↑ after the reload cycle's S4 (DMA-24).
- `intel_8275.v`: field attributes reset at the VRTC rise (CRT-31); the first DRQ of a row fill is not
  delayed by the burst space (CRT-20); commands are decoded by bits 7-5 (CRT-42); Disable Interrupt leaves
  IR set (CRT-8).

The one below is approved for now and waits for a check on a real chip (next section).

### 8275: the DMA restart after an underrun (`intel_8275.v`, S11; decided 2026-11-11)

- Data sheet: "Upon detection of DU, the DMA operation is stopped and the screen is blanked until after the
  vertical retrace interval" ([D79] 1-180; 1984 data sheet 8-68). And: "The first DMA request for a row will
  start at the first character clock of the preceding row" (1984 data sheet 8-60): row 0's buffer is filled
  during the last row of the vertical retrace, inside the retrace interval.
- Silent: whether that row-0 fill belongs to "until after the vertical retrace interval".
- Model: the DMA stop ends at the start of the last retrace row, so the row-0 fill of the next frame runs as
  in every frame; the screen stays blanked until row 0 starts (after the retrace), which meets the blanking
  sentence word for word. DU, IRQ and the status are as the data sheet says.
- The strict reading (the DMA stopped until VRTC falls, the row-0 fill skipped) was the model's first rule.
  It is not taken: the 8257 hands out its block in order whatever row asks, so a skipped row-0 fill puts
  row 0's bytes into row 1 and the picture stays one row down in every later frame (the 8257's autoload
  repeats the same block; nothing re-synchronises it). On the Radio-86RK that would happen after the boot
  underrun (the monitor sends Start Display before it enables the 8257; whether the underrun hits depends on
  the phase of the boot against the raster) and after every tape operation. The boards show an aligned
  picture.
- Tests: `tb_vg75_dma.v` check 6 (no DRQ and VSP high from the underrun row to the last retrace row; the
  row-0 fill there within 0..84 ce16, 78 transfers; blanking until VRTC falls) and check 6b (the same when a
  burst space ends at the CCLK that finds the underrun; fault `vg75_underrun_space_redrq`); the fault
  `vg75_underrun_restart_late` (the strict reading) fails in `vg75`, `vg75_dma`, `vg75_attr` and `machine16`
  (the 8257 out of step with the frame).
- To return to the strict reading: in `retroICs`, undo the row-0 restart in `intel_8275.v`
  (`ics/intel/8275/record.md`, S11) and swap the fault back (`vg75_underrun_restart_early`).

### 8257: the state after the DRQ sample (`intel_8257.v`; 2026-11-11; not merged for now)

- Data sheet: Fig. 6 note 1 and the waveform on 12-110 ([C78] 1978 Intel Component Data Catalog): after
  the DRQ sample the 8257 stays in SI with HRQ raised and enters S0 one θ↓ later (both blind readings of
  2026-11-11 agree).
- Model on the main line: S0 at the θ↓ that samples DRQ. The pins are the same unless HLDA is already
  high 9 ce16 after the sample; an 8080 raises HLDA later than that, so the Radio-86RK cannot show the
  difference.
- The data sheet version (the RTL change, a check with HLDA held high, a fault) was written as a
  patch and not merged (the maintainer, 2026-11-11); it is not kept in this repo or in `retroICs`. The decision waits for the real-hardware check below; a
  machine whose bus master raises HLDA early would need the data sheet version.

## Follow-up: checks on real hardware

Planned by the maintainer: on a real Radio-86RK (or any board with a real 8275 and 8257), with a logic
analyser. Not on the FPGA: an FPGA runs this model, so it cannot tell how the chip behaves.

1. 8275 underrun restart (the decision above). A test program (8080, on the ROM disk or from tape):
   - write each row's number at the start of the row (00..29), so a shift of one row is visible;
   - wait for IR (the start of the last display row), disable the 8257 (E008h <- 80h) for about one frame,
     so that the 8275 finds a row buffer not full and sets DU;
   - at the next IR, before the retrace, program the 8257 as the monitor does (76D0h, 4923h, mode A4h);
   - read the status (DU, bit 1) and show it; hold the picture.
   Result: rows aligned ("00" on the top row) = the model; the picture one row down = the strict reading.
   Logic analyser: 8275 DRQ (pin 5), DACK (pin 6), HRTC, VRTC, triggered on the underrun: whether DRQ pulses
   in the last retrace row after DU.
2. 8275 status read against IR: whether a status read can lose an IR flag set during the read (a status read
   clears IR; seen in simulation at the monitor's second video init: the monitor then waits one more frame).
   Analyser: RD, CS, A0, IRQ (pin 4) around the start of the last display row.
3. 8275 Reset command during a row fill: whether the fill in progress stops at once (the model: DMA and the
   fill stop; the partly filled row is shown as it is) and when DMA resumes after Start Display (S9: the
   model starts at the next row start with a fill due). Analyser: DRQ, DACK, WR, CS, A0.
4. 8257 SI -> S0 after the DRQ sample (the decision above): not visible with an
   8080 (HLDA comes later than the difference). On the bench: hold the 8257's HLDA input high from a
   test fixture (not from the CPU) before DRQ rises, and capture CLK, DRQ, HRQ, AEN with the analyser:
   AEN (S1) 9 ce16 after the DRQ sample = the main line; one clock period later = the data sheet
   reading.

Record each result with the board, the chip markings and the analyser capture; a result that differs from
the model changes the model and its tests, and this section.
