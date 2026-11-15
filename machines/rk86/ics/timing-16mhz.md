# rk86: the chip timing in the 16 MHz timebase

The `retroICs` records give the 8257 timing in data sheet units: the edges of the 8257 clock θ (θ↑,
θ↓) in its states, TCY (one clock period) and Tθ (the clock high time); the 8275 timing in CCLK
units (`ics/intel/8257/record.md`, "Timing (data sheet)" with "Transfer states" and "HOLD overhead
with an 8080A"; `ics/intel/8275/record.md`, "Timing (data sheet)"). This machine runs every chip on
one 16 MHz timebase (`ce16`, one oscillator period), and its RTL comments and TBs count in it. This
file keeps that mapping: the rule, and the 8257 transfer and HOLD rows in oscillator periods.
The 8275 record was already in CCLK units; at 16 MHz one CCLK is 12 oscillator periods (750 ns,
`machines/rk86/ics/ti-sn7492/record.md`, IE4-1; the board wiring: IE4-4).

## The mapping

One Φ cycle = 9 periods of 62.5 ns, p0..p8 from Φ1↑ (`machines/rk86/ics/intel-8224/record.md`,
CLK-1..CLK-4 and timing reference a). The 8257 CLK = Φ2 (TTL): θ↑ = p2, θ↓ = p7. One 8257 state =
9 periods, from one θ↓ to the next. `rel N` = periods from the θ↓ that starts S1:

| Edge | rel |
|---|---|
| θ↓(S1) | 0 |
| θ↑(S1) | 4 |
| θ↓(S2) | 9 |
| θ↑(S2) | 13 |
| θ↓(S3) | 18 |
| θ↑(S3) | 22 |
| θ↓(S4) | 27 |
| θ↑(S4) | 31 |
| next θ↓ (the next S1 or SI) | 36 |
| θ↑(SI) | 40 |
| θ↓ that ends the first SI | 45 |
| θ↑ of the second SI | 49 |
| θ↓ that ends the second SI | 54 |

Tθ = 5 periods (p2..p7), TCY - Tθ = 4 periods. In the RTL body comments and the TBs `rel N` is
the clock-enable count of the TB harness from the θ↓ that starts S1 (each TB header defines it); in
this machine that count is `ce16`.

## The 8257 rows in oscillator periods

The 8257 transfer in oscillator periods (`rel N`), as this machine's RTL comments and TBs count it;
the data sheet units are in the retroICs record.

States (Fig. 6, [C78] 12-104): SI idle; S0 with HRQ high until HLDA; S1, S2, S3, (SW), S4 per transfer. S4 goes to S1 directly (no S0) when HRQ and HLDA are both still high; HRQ is reset in S4 when the DRQ is not active, and S4 then goes to SI. READY is tied high on both boards (8224 RDYIN pulled up), so SW never occurs.

The RK86 programs a DMA write cycle (count bits 15:14 = 01, [C78] 12-100): the 8257 drives IOR (8275 WR) and MEMW (memory read strobe ЧТЕНИЕ); MEMR and IOW stay inactive ([C78] 12-105). Times in oscillator periods from the start of S1 (S1 starts at 0 = p7 of a Φ cycle; one state = 9 periods):

| State (start) | AEN | ADSTB | DACK2 | IOR (Rd) | MEMW, mode bit 5 = 0 | MEMW, extended write (A4h) | Other |
|---|---|---|---|---|---|---|---|
| SI | falls at θ↑(SI), TAET ≤ 200 ns | low | high | high | high | high | DRQ sampled at θ↓ (TQS ≥ 120 ns setup); HRQ rises at θ↑(SI), TDQ ≤ 160 ns |
| S0 | low | low | high | high | high | high | HRQ high; HLDA sampled at the θ↓ that ends S0 (THS ≥ 100 ns) |
| S1 (0) | rises at θ↓(S1) = 0, TAEL ≤ 300 ns | high from θ↑(S1) = 4 (TSTL) to θ↑(S2) = 13 (TSTT) | high | high | high | high | A0-A7 driven from 4 (TFAAB, TASM ≤ 250 ns); A8-A15 on D0-D7 from 4 to 13 |
| S2 (9) | high | falls at 13 | falls at θ↓(S2) = 9, TAK ≤ 250 ns | falls at θ↑(S2) = 13, TDCL ≤ 200 ns | high | falls at 13 | |
| S3 (18) | high | low | low | low | falls at θ↑(S3) = 22 | low | TC (count = 0) rises at 22; READY sampled at 22 |
| S4 (27) | high | low | low | low | rises at θ↑(S4) = 31, TDCT ≤ 200 ns | rises at 31 | DRQ sampled at θ↓(S4) = 27; HRQ falls at 31 if DRQ is not active; TC falls at 31 |
| next S1 or SI (36) | stays high (S1) / falls at 40 (SI) | | rises at 36 | rises at 36, TDCT ≤ 200 ns | | | A0-A7 change at 40 (S1) or float at 40 (SI) |

Sources: AC table [C78] 12-109 (TQS, TDQ, THS, TAEL, TAET, TFAAB, TASM, TAH, TAHR, TAHW, TSTL, TSTT, TAK, TDCL, TDCT, TRWM, TWWM, TWWME), DMA mode waveforms 12-110, text 12-105 ("IOR at the beginning of S2, MEMW at the beginning of S3 ... Extended WR ... generated in S2"), 12-103 (extended write).

- Widths: IOR 23 periods (TRWM ≥ 2TCY + Tθ - 50 ns); MEMW 9 periods normal (TWWM ≥ TCY - 50 ns), 18 periods extended (TWWME ≥ 2TCY - 50 ns). With A4h the memory read strobe of the board is S2-S4, 1125 ns.
- The memory read strobe (MEMW) ends at 31, the 8275 takes the byte at IOR↑ (36; tDW ≥ 150 ns, [D79] p. 1-185): the byte must stay at the 8275 for 5 periods (312.5 ns) after the read strobe ends, while the address is still valid (until 40). DACK↑ and IOR↑ come from the same edge (TAK ≤ 250 ns, TDCT ≤ 200 ns, no minimums), so the 8275's "WR↑ to DACK↑ ≥ 0" is not guaranteed by the 8257's numbers; a model should keep DACK active at the IOR rising edge.

HOLD overhead (8080A: [C78] 11-12 pin description, 11-14 tDC, 11-15 tHS; [UM83] 4-12, 4-13):

| Step | Timing | Source |
|---|---|---|
| 8080 samples HOLD | at Φ2↑ (p2) of T2 or TW, READY high; tHS ≥ 140 ns | [C78] 11-12, 11-15 (note 12); [UM83] 4-13, Fig. 4-9 |
| HLDA rises | at Φ1↑ (p0) of T3 for memory read, input (also the M1 fetch and INTA); at Φ1↑ of the state after T3 for write, output and the other cycles (DAD's bus-idle M2, M3); tDC ≤ 120 ns | [C78] 11-12, 11-14; [UM83] 4-13, Fig. 4-9, 4-10 |
| 8257 sees HLDA | at θ↓ (p7) of the same Φ cycle (317 ns ≥ THS 100 ns): S1 starts at p7 of the hold-acknowledge state | [C78] 12-109, 12-110 |
| Latency | DRQ sampled at θ↓ of cycle a; HRQ at θ↑ of a + 1; first HOLD sample at Φ2↑ of a + 2 (402 ns ≥ tHS); w = Φ cycles from a + 2 to the next T2: 0..4 (longest: a + 2 = T3 of a 5-state M1, then T4, T5, T1, T2) | derived |
| DRQ sample to S1 | read-type 3 + w = 3..7 Φ; write-type 4 + w = 4..8 Φ; S0 states 2..7. DRQ↑ to its sampling edge 0..1 Φ more; AEN↑ ≤ 300 ns after S1 starts | derived |
| End of HOLD | last S4 starts at p7 of cycle k; HRQ↓ at θ↑ of k + 1; the 8080 samples HOLD low at Φ2↑ of k + 2; HLDA↓ and T1 of the next machine cycle at Φ1↑ of k + 3; AEN↓ at p2 of k + 2 + ≤ 200 ns. From the end of the last S4 to T1: 11 periods; from its start, 20 | [C78] 12-109; [UM83] 4-13 ("HLDA returns to a low level following the leading edge of the next Φ1") |
| Per HOLD period of N transfers | AEN high 36N + 4 periods (4N Φ + 4/9 Φ) plus TAEL / TAET; HLDA high 4N + 2 Φ cycles; CPU states not executed: write-type 4N + 2, read-type 4N - 1 .. 4N + 1 (T3, and T4 / T5 of an M1, run inside HLDA) | derived |

## The RK86 case: one HOLD period per character

The machine's DMA cadence (the board side: `retroComputersDocs/computers/rk86/board.md`, "The 8257
on the board (GLUE)", "The DMA cadence"), with the 8257 record's HOLD overhead:

The RK86 case: the 8275 drops DRQ at each DMA WR↓ (tRQ ≤ 200 ns [D79], 250 ns [D84]) and raises it again tWQ ≤ 250 / 275 ns after WR↑ while the burst lasts ([D79] Fig. 30 p. 1-184, table p. 1-182). Its WR is the 8257 IOR, low from θ↑(S2) to θ↓ of the next state. So DRQ is low when the 8257 samples it at θ↓(S4) of every transfer: HRQ falls after every character and the 8257 returns to SI. The DRQ comes back ≤ 450 / 475 ns after that SI starts and is normally taken at the next θ↓ (562.5 ns later; it misses only with both TDCT and tWQ near their maxima). Within an 8275 burst each character is then its own HOLD period: SI, SI, S0, S0, S1-S4 = 8 Φ per character when the 8080's resumed machine cycle is read-type (HOLD is sampled at its T2), 9 Φ when it is write-type, 11-14 Φ when the DRQ misses the SI sample (one more machine cycle). The 8080 runs one machine cycle between two characters. The first character of a burst follows the latency row above.

## Machine notes on the 8257 record items

- DMA-29 (HRQ after an S4 → SI exit: the DRQ is taken at the θ↓ that ends the first SI, HRQ↑ at θ↑
  of the second SI): the machine TB's S1_SI = 45 (the HRQ rise after an S4 → SI exit, rel 49).
- The upper address byte (with DMA-33, the lower address pins): the RK86 machine takes
  `a_o[15:8]` instead of the board latch at ADSTB, the same at the pins (the latch is transparent
  from rel 4; `a_o` changes at rel 40 = θ↑ of the next S1).
- The data sheet review of 2026-11-11 (two blind readers): no machine number changed (AEN 40 ce16
  per transfer, one HOLD period per character, HLDA 4N + 2 Φ, the per-3-frame totals).
