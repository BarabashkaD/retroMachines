# Intel 8224 clock generator: data sheet record

Data sheet items of the Intel 8224 (its Soviet equivalent: `equivalents.md`), with the IDs they had in `retroICs`. The board use (CLK-11) is a board item, defined in the RK86 board record (`retroComputersDocs/computers/rk86/board.md`, "Clock chips on the board"); this repo's `docs/record-ids.md` names its home.

## Sources

Sources: [D8224] `Intel - 8224 - Clock Generator.pdf` (order 231464-001, November 1992; pp. 1-50..1-54 = PDF 1-5; scanned, no text layer); [C78] 11-24..11-27 (PDF 440-443), the same figures and formulas; [ГФ24] `kr580gf24.pdf` (pin list, 27 MHz maximum, "phase period 9/fOP"; no timing diagram). Notation (below): p0..p8 = the 9 oscillator periods of a Φ cycle from Φ1↑.

Not sources of behaviour: emulators and other FPGA cores ([MAME], [EMU], [APG]: comparison-only).

Timing reference (section a below):

- [C78] Intel Component Data Catalog 1978: 8080A pp. 11-11..11-15, 8224 pp. 11-24..11-27, 8257 pp. 12-98..12-110. bitsavers `components/intel/_dataBooks/1978_Intel_Component_Data_Catalog.pdf` (read from the bitsavers.trailing-edge.com mirror; PDF pages 427-431, 440-443, 606-618).

The documents cited here and their provenance: [D8224] and [ГФ24] in `retroComputersDocs/computers/rk86/index.md` (the PDF in its `datasheets/`), [C78] in `retroICs/ics/intel/8080a/datasheets/index.md`; every source ID of this repo: `docs/sources.md`.

## Notation

The original IDs are kept; new functions are numbered after them. What the section "Timing reference" below establishes (section a, the 8224) is cited as "timing reference a", not repeated. The other timing checks are in the chips' records in `retroICs`, in data sheet units: b in `ics/intel/8257/record.md`, "Transfer states" and "HOLD overhead with an 8080A"; d in `ics/intel/8275/record.md`, "Timing (data sheet)". Their 16 MHz values (p0..p8, oscillator periods): `machines/rk86/ics/timing-16mhz.md`. c (the 8275 pins on the boards) is board wiring: `retroComputersDocs/computers/rk86/board.md`, "The 8275 pins on the boards". Renders cited by name are page crops of the cited documents, kept with the maintainer's source collection, not in this repository (`<document>_pNN` = PDF page NN). Researched 2026-11-10.

Notation: one Φ cycle = 9 periods of the 16 MHz oscillator (62.5 ns each), numbered p0..p8 from the rise of Φ1; p0 is `f1`, p2 is `f2`. The 8257 CLK is the 8224's Φ2 (TTL): θ↑ = p2, θ↓ = p7. An 8257 state runs from one θ↓ to the next (the state bars of the [C78] 12-110 waveforms sit on the falling clock edges, and the widths TRWM = 2TCY + Tθ for "Rd↓ at θ↑(S2) to Rd↑ at θ↓(S1)" and TWWME = 2TCY for "θ↑(S2) to θ↑(S4)" in the 12-109 table hold only with that boundary). So θ↑(Sx) is p2 of the Φ cycle that holds the last 7 periods of Sx.

## Items (CLK-n)

| ID | Function | Data sheet behaviour (pins, edges, values) | Source (document, page / figure) |
|---|---|---|---|
| CLK-1 | ÷9 clock generator | Φ1 (pin 11) and Φ2 (pin 10) from the oscillator (XTAL1 15, XTAL2 14, TANK 13) through "CLOCK GEN. ÷9"; the table's "CLK period" tCLK = tcy / 9, i.e. one Φ cycle tcy = 9 oscillator periods: timing reference a (Φ cycle row) | [D8224] 1-50 Fig. 1, 1-52; [C78] 11-26 |
| CLK-2 | Φ2↑ | Φ2 rises at p2 (tD3 = 2tcy/9 .. 2tcy/9 + 20 ns after Φ1↑, tD1 ≥ 0): timing reference a | [D8224] 1-52, 1-54; [C78] 11-26, 11-27 |
| CLK-3 | Φ2↓ | Φ2 high 5 periods (tΦ2 ≥ 5tcy/9 - 35 ns), falls at p7; tD2 ≥ 2tcy/9 - 14 ns before Φ1↑: timing reference a | [D8224] 1-52; [C78] 11-26 |
| CLK-4 | Phase widths | Φ1 high p0-p1 (tΦ1 ≥ 2tcy/9 - 20 ns), Φ2 high p2-p6, both low p7-p8: timing reference a | [D8224] 1-52, 1-53 (example at tCY = 488.28 ns: 89 / 236 / 95 / 109-129 ns) |
| CLK-5 | RESET synchroniser | RESIN (pin 2, active low) → Schmitt-trigger input (hysteresis VIH - VIL ≥ 0.25 V; VIH ≥ 2.6 V for the reset input) → D of a flip-flop clocked by the internal clock "Φ2 D" of the ÷9 generator; RESET (pin 1, active high) = the flip-flop's Q̄ (Fig. 1). The clocking edge from the AC table and Fig. "Waveforms": RESIN (and RDYIN) setup tDRS ≥ 50 ns - 4tcy/9 and hold tDRH ≥ 4tcy/9, both measured from STSTB↓ (p8), so the sample point is p8 + 4 = p3 of the next Φ cycle (setup 50 ns, hold 0); the output: tDR ≥ 4tcy/9 - 25 ns ("READY or RESET to Φ2 delay", 192 ns at 488 ns) measured in the waveform from the RESET / READY change to the *falling* edge of Φ2, so the output changes ≤ 25 ns after p3. Result: the flip-flop is clocked at p3, one oscillator period after Φ2↑ (not at Φ2↓ = p7). [R86] p. 31 says the same in words: RDYIN and RESIN, applied at arbitrary moments, "are stored in the internal flip-flops of the clock generator and passed to the outputs RDY and RES on the leading edge of the Φ2 pulse train"; "RES can also be formed by the Schmitt trigger in the clock generator"; RESIN comes from C1, C2, R1, R2, R3, VD1 and the СБРОС key, which also limit the reset length. Every 8080 sampler of RESET / READY (READY setup tRS 120 ns before Φ2↓ of T2 / TW, [C78] 11-15) sees the new value in the same Φ cycle | [D8224] 1-50 Fig. 1, 1-51 (DC), 1-52, 1-53, 1-54 Waveforms; [C78] 11-26, 11-27; [R86] p. 31 (render `Radio_Magazine-1986-05-page-31_p01.png`) |
| CLK-6 | READY synchroniser | RDYIN (pin 3) → D of a second flip-flop on the same "Φ2 D" clock; READY (pin 4) = Q. Same timing as CLK-5 (tDRS, tDRH, tDR): sampled and changed at p3. "RDYIN Setup Time to Status Strobe" is the only RDYIN reference in the table; the block diagram shows no STSTB input to the flip-flop, so STSTB is only the timing reference, not the clock | [D8224] 1-50 Fig. 1, 1-52, 1-54; [C78] 11-26, 11-27 |
| CLK-7 | STSTB | STSTB (pin 7, active low) = NOR (SYNC AND "Φ1 A", RESET) (Fig. 1). tDSS = 6tcy/9 - 30 .. 6tcy/9 ns after Φ2↑ → falls at p8; tPW ≥ tcy/9 - 15 ns → low for one period (p8), when SYNC (pin 5, from the 8080) is high | [D8224] 1-50 Fig. 1, 1-52; [C78] 11-26, 11-27 |
| CLK-8 | STSTB during RESET | By the NOR of Fig. 1, STSTB is also low for as long as RESET is high | [D8224] 1-50 Fig. 1 |
| CLK-9 | OSC, Φ2 (TTL) | OSC (pin 12): the oscillator output, TTL; Φ2 (TTL) (pin 6): Φ2 at TTL level, tDΦ2 = -5 .. +15 ns from Φ2 (both edges) | [D8224] 1-50, 1-52; [C78] 11-26 |
| CLK-10 | Limits | fMAX 27 MHz (formulas), 18.432 MHz in the tested table; crystal: series resonance, fundamental | [D8224] 1-51, 1-52, 1-53; [ГФ24] p. 2 |

## Edition differences (CLK-Dn)

None recorded.

## SILENT (CLK)

- CLK-1: on which oscillator edge the ÷9 counter steps, so the phase of the SN7492 transitions (CKA↓) against Φ1 / Φ2 within a period is open; and the power-up phase of the ÷9 counter against the SN7492 (neither has a reset on the boards): searched [D8224] 1-50..1-54, [C78] 11-24..11-27, [ГФ24]. The model's checks list it as SILENT.
- CLK-5/6: the exact delay of the internal "Φ2 D" edge after Φ2↑ (derived as one oscillator period from the formulas; Fig. 1 does not define "Φ2 D").

## Assumptions checked

Model assumptions (CLK):

- Clock block: the RESET and READY flip-flops: the 8224 clocks both at its internal "Φ2 D", whose edge is p3 by the AC table (tDRH = 4tcy/9 after STSTB↓ at p8; tDR = 4tcy/9 - 25 ns before Φ2↓) and the waveform figure (tDR drawn to the *falling* edge of Φ2); [R86] p. 31: "on the leading edge of the Φ2 pulse train". `rk86_clocks16.v` clocks them at p3 (`step == F2_STEP + 1`). A reading of tDR as "p7 to the next p2" (Φ2↓) would have no effect on any input sampled at p0 or p2 (the 8080's samples, and the 8257's READY sample at θ↑, which is p2): a change at p3 or at p7 is seen at the same following p0 / p2. On the RK86 READY is constant high.
- Clock block: STSTB low for the period p8 when SYNC is high: confirmed ([D8224] 1-52 tDSS, tPW; Fig. 1). STSTB is also low while RESET is high (Fig. 1 NOR); `rk86_clocks16.v` has that term (`ststb_n = !(ststb_sync || reset)`). STSTB is not connected on either board.
- [C78] 11-26 also times RDYIN against STSTB: resolved: STSTB is the timing reference only; Fig. 1 has no STSTB input to the READY flip-flop; both flip-flops share the "Φ2 D" clock.

## Timing reference

Timing checks a-d of the machine. Every value carries its source. a is this section; b and d are in the chips' records in `retroICs` (`ics/intel/8257/record.md`, "Timing (data sheet)"; `ics/intel/8275/record.md`, "Timing (data sheet)"), their 16 MHz values in `machines/rk86/ics/timing-16mhz.md`; c (the 8275 pins on the boards) is board wiring: `retroComputersDocs/computers/rk86/board.md`, "The 8275 pins on the boards".

### a. 8224 clock generator

| Item | Data sheet | In oscillator periods | Source |
|---|---|---|---|
| Φ cycle | tCLK = tCY / 9 | 9 periods, 562.5 ns at 16 MHz | [C78] 11-26 |
| Φ1 high | tΦ1 ≥ 2tCY/9 - 20 ns | p0-p1 (2 periods) | [C78] 11-26, waveform 11-27 |
| Φ1 to Φ2 | tD1 ≥ 0 ns; leading edges tD3 = 2tCY/9 .. 2tCY/9 + 20 ns | Φ2 rises at p2, when Φ1 falls | [C78] 11-26 |
| Φ2 high | tΦ2 ≥ 5tCY/9 - 35 ns | p2-p6 (5 periods) | [C78] 11-26 |
| Φ2 to Φ1 | tD2 ≥ 2tCY/9 - 14 ns | both low p7-p8 (2 periods) | [C78] 11-26 |
| Φ2 (TTL) | tDΦ2 = -5 .. +15 ns after Φ2 | the 8257 CLK edges are the Φ2 edges | [C78] 11-26 |
| Example tCY = 488.28 ns | tΦ1 89, tΦ2 236, tD2 95, tD3 109-129 ns | 2 / 5 / 2 / 2 periods of 54.25 ns | [C78] 11-27 |

Result: Φ1 rises at 0 (high 0-1), Φ2 rises at 2 (high 2-6), both low 7-8: `F2_STEP = 2`, as the model assumes.

## Hardware checks

None planned.
