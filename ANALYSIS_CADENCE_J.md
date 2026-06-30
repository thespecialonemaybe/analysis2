# Task J: TRON/Aptos Channel Update Cadence Snapshot

**Date:** 2026-06-30 (updated)  
**Task:** Monitor W1/W2/W3 update cadence; check for new payloads since last scan

---

## Status Snapshot (as of 2026-06-30)

| Channel | Last update | Days since | BSC TX |
|---------|------------|-----------|--------|
| W1 / A1 | 2026-06-23 | **7 days** | `0x18a8420f727f2405f9...` |
| W2 / A2 | 2026-06-25 | **5 days** | `0x622bcfd4538f7e6877...` |
| W3 / A3 | 2026-06-08 | **22 days** | `0xb6c725890be6890fd2...` |

No new updates on any channel since the Jun 28 snapshot.

### Previous snapshot (2026-06-28)

| Channel | Last update | Days since | BSC TX |
|---------|------------|-----------|--------|
| W1 / A1 | 2026-06-23 | 5 days | `0x18a8420f727f2405f9...` |
| W2 / A2 | 2026-06-25 | 3 days | `0x622bcfd4538f7e6877...` |
| W3 / A3 | 2026-06-08 | 20 days | `0xb6c725890be6890fd2...` |

---

## W3 True History — Nov 2025 to Jun 2026

W3 (`TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v`) has **69 total TXs** going back to
**November 13, 2025** — four months earlier than previously thought.

### Full Update Timeline

| Period | Activity | Notes |
|--------|----------|-------|
| 2025-11-13 | Account setup (no memo) | W3 wallet created |
| 2025-11-14, 18, 19 | 3 payload TXs | First Stage 2 dead-drop deployments |
| 2025-12-16 | 4 TXs (14:48–16:53) | Batch rotation |
| 2025-12-17 | 2 TXs | Followup |
| 2025-12-19, 22 | 1 TX each | Minor updates |
| 2026-01-06 | 1 TX | New year update |
| 2026-01-23 | 3 TXs (15:35–15:49) | Batch |
| 2026-01-24, 30 | 1–2 TXs each | |
| 2026-02-10 | 2 TXs | |
| 2026-02-11 | 4 TXs (14:14–15:05) | Batch |
| 2026-02-12 | 1 TX | |
| 2026-02-25 | **12 TXs** (18:01–21:07) | Largest single-day batch |
| 2026-03-03 | 4 TXs (3 no-memo + 1 payload) | Cashout + update |
| 2026-03-18 | 1 TX | |
| *(2-month gap)* | | No W3 activity Mar 19 – May 16 |
| 2026-05-17 | 1 cashout TX | Account maintenance |
| 2026-05-19 | 3 TXs (16:13–17:32) | Pre-JFrog package upload burst |
| 2026-05-20 | 3 TXs (15:05–15:59) | Batch |
| 2026-05-21 | **6 TXs** (12:38–13:20) | **Function wrapper introduced mid-session** |
| 2026-05-22 | 1 TX | |
| 2026-05-23 | 1 TX | |
| 2026-06-02 | 5 TXs (16:01–16:54) | Batch |
| 2026-06-03 | 2 TXs (1 cashout, 1 payload) | |
| 2026-06-05 | 1 TX | |
| 2026-06-08 | 1 TX | **Last update — 20 days quiet** |

### The 2-Month Gap (Mar 19 – May 16)

W3 was completely silent for 59 days while W1 continued updating (Mar 26, Mar 31, May 20, May 23
are all known W1 updates). During this period, Stage 2 was likely served directly from the C2
(`198.105.127.210`) rather than via the blockchain dead-drop — the dead-drop adds resilience
but is not strictly required if victims can reach the C2 directly.

The gap coincides with the `_$_913e` → `_$_b229` cipher transition (response to OSM's Mar 7 YARA
rule). The actor may have been rebuilding the Stage 2 payload before resuming W3 updates.

---

## Stage 2 Payload Evolution (W3)

Decoded a sample of BSC TXs to map payload growth over time:

| Date | Chars | Function wrapper | Notes |
|------|-------|-----------------|-------|
| 2026-05-20 | ~65,657–67,778 | **None** | Plain LZString IIFE |
| 2026-05-21 (early) | ~66,820–71,376 | **None** | Still no wrapper |
| 2026-05-21 (late) | 70,251 | **`Function("uzvbiIG", ...)`** | Wrapper introduced |
| 2026-05-22 | 71,848 | `Function("gIWDUzx", ...)` | |
| 2026-05-23 | 70,120 | `Function("jgkHqCt", ...)` | |
| 2026-06-02 (early) | 71,095 | `Function("f6ohOMl", ...)` | |
| 2026-06-02 (late) | 72,569 | `Function("c1HTBI", ...)` | |
| 2026-06-03 | 72,897 | `Function("qzv69ys", ...)` | |
| 2026-06-05 | 77,365 | `Function("IW39dX", ...)` | |
| **2026-06-08** | **77,279** | **`Function("oTNBm2c", ...)`** | **Current — 20 days stable** |

Key observations:
- The `Function("param", body)(moduleProxy)` UMD wrapper was introduced on **May 21, 2026**
  at some point between the 13:09 and 13:20 TXs — the actor pushed multiple variants within
  minutes before settling on the wrapper approach
- Payload size grew from ~65KB → ~77KB (+18%) between May 20 and Jun 8
- The Jun 5 payload (77,365 chars) is slightly larger than Jun 8 (77,279 chars) — 86 chars
  were trimmed in the final version, suggesting minor code cleanup
- Jun 8 has been stable for 20 days — the longest pause in W3's history

**Function parameter names are randomly generated each deployment:** `uzvbiIG`, `gIWDUzx`,
`jgkHqCt`, `f6ohOMl`, `c1HTBI`, `qzv69ys`, `IW39dX`, `oTNBm2c` — all different.
The parameter is used as the UMD module proxy (intercepts `define`, `module`, `angular`
references), not as the compressed data argument.

---

## Architectural Implication

The W3 dead-drop (Stage 2 delivery) started **November 2025**, five months after W1/W2 went
live in June 2025. This means:

```
Jun 2025 – Oct 2025:    W1/W2 → Stage 1 → Stage 2 served DIRECTLY from C2
Nov 2025 – present:     W1/W2 → Stage 1 → W3 dead-drop → Stage 2
```

Adding the W3 blockchain layer gave the actor a resilient Stage 2 delivery channel immune to
C2 takedowns. The pre-November 2025 Stage 1 payloads presumably had a hardcoded BSC TX or
C2 URL for Stage 2 rather than pointing to W3.

---

## New BSC TXs (W3, not previously catalogued)

16 new W3 BSC transaction hashes identified (May 20 – Jun 2 2026, plus older pre-May history):

```
# Jun 2 batch (5 TXs, 16:01–16:54)
0xa1eeb9dc3b5c4ae0f8c292c14ed9cfb50bdb4586ad01ada719bff648b89dfd51
0x55574a62c1f2afbe528834f96ed44bca7d0a2ba151d8e4b177a31646cc415c7d
0x3bb80ebaa4ac38dd1c90a1689d3f2148d801225894a95e1b7757ea94429be198
0x8ba882519e64756d4c5ecb19bffc0cf65704956f73a0c984c16f6fdc9569c26a
0xa7de3a7764f31866c15a2b4075b381f9cedeb5bd9f27d7621eee3e1b7b59f36f

# May 23
0xfad600a962daefebe456f96989bfe5ec65ab4438e48fb788e1b9b59000d2cec9

# May 22
0xf188850b746bc8c467e95e7c3d2a6a47eb92211ab3cc69355e88d4f7375e31c5

# May 21 (6 TXs, 12:38–13:20)
0x571ca79be71260296e9d67fb2bebf5f4d314b9df2b461e2ab9eaece1a484f23c
0xceb3b0e24555c59415382d18a18a4839b50ed341e7d1568f8d095df3a4245531
0xc43f48f34d6937626370962b155e7e1cca4a76e118df11c2fec57eb8c70624a7
0x1588991e1a5049b3a77305a9a09779d7a588686373a1436ebd56f30fe4d7be44
0xe7058ec299469f48bb38aac5b97f288139b89ff0e47b48fd98da4fa817df9c71
0x615e2bd0fa06dfd8947aac85e09b672628c15d8cb276e808b72b297b626544e3

# May 20 (3 TXs, 15:05–15:59)
0xd865c32814b1323355cd0925ef5c939737dbdbc2dad272e54dbb96842727fbd6
0x126a8942a6058fc7ce883e322059d76b7615094e2d5c115991676cdbc3959695
0x815a712af5b51226035493a75551d1379422ef3918ca4998b7d85dfd9dcfd5b7
```

Additionally: 19 W3 TXs from Nov 2025 – Mar 2026 carry payload memos not yet decoded.
The pre-Function-wrapper payloads (~65KB, no UMD shim) may be easier to decode for Task T.

---

## Monitoring Recommendation

---

## Jun 23 A2 Payload Decoded (2026-06-30)

The Jun 23 Aptos A2 TX (seq=8) points to BSC `0x76a7ae331269603bd690d2d9d810393b42d0c324acf1eacdf5a5258dfd3a6761`.
This was previously undecoded; the Jun 25 payload (seq=9) was decoded in Task R as `_$_f5f0`.

### Jun 23 A2 payload details

| Field | Value |
|-------|-------|
| Outer cipher | `_$_f5f0`, string `"mctjncr%uioonf%et%b"`, seed `1003076` |
| Outer table | `['function','r','object','m']` — same 4-entry table as Jun 25 |
| Inner cipher | `SgH`, seed `570964` |
| `Hvn` | `'constructor'` (11-char prefix of decoded string) |
| Activation code | **`5842`** |
| Return code | **`8711`** |

### Activation/return code progression (_$_f5f0 W2 channel)

| Date | Deployment | Activation | Return | Source |
|------|-----------|-----------|--------|--------|
| 2026-06-20 | W2 TRON direct | `8063` | `8223` | Task B |
| 2026-06-23 | A2 Aptos | **`5842`** | **`8711`** | This check |
| 2026-06-25 | A2 Aptos | `1218` | `2021` | Task R |

The activation and return codes change with every deployment. These values are likely
session/version identifiers used to verify Stage 2 → C2 handshake integrity.

---

## Monitoring Recommendation

| Channel | Next expected update | Action |
|---------|---------------------|--------|
| W1 | Overdue (7d; avg 5-14d cadence) | **Check now — may have updated** |
| W2 | 5d; normal | Monitor |
| W3 | 22d quiet — approaching prior 2-month gap | Check weekly; may signal transition |

**W3 hypothesis (as of Jun 30):** The 22-day silence mirrors the Mar 19 – May 16 gap
(59 days). During that gap, Stage 2 was served directly from C2 rather than via blockchain
dead-drop. Task AB confirmed the C2 servers now deliver `RS260605` Stage 2 format
(generator-function obfuscated, XOR key `ThZG+0jfXE6VAGOJ`) instead of the LZString Beavertail
blob. If W3 remains silent indefinitely, the actor may have permanently transitioned Stage 2
delivery to the RS260605 C2-direct model — the blockchain dead-drop W3 link is no longer needed.

W1/W2 (Stage 1 loaders) continue updating normally — the dead-drop loader chain is unchanged.
Only Stage 2 delivery mode may be shifting.

The W3 silence is the most notable: with 69 TXs over 7.5 months the average cadence was
<3 days between updates. A 22-day gap is the longest on record and warrants continued monitoring.
