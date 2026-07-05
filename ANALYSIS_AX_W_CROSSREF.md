# AX-W: W5/W6 Wallet Cross-Reference

**Date:** 2026-07-05  
**Task:** Cross-reference AX "W5/W6" wallet pairs against existing wallet tracking docs.

---

## Finding: No New Infrastructure

The two TRON wallets introduced in the AX analysis (as "W5" and "W6") are **identical to
canonical W1 and W2** — already fully documented in `ANALYSIS_TRON_WALLETS_FULL.md`,
`ANALYSIS_APTOS_WALLETS.md`, and `ANALYSIS_AM_CASHOUT_WALLETS.md`. The obfuscator.io
delivery format deploys the same Stage 1 infrastructure as all other _$_b229-era payloads.

---

## Naming Collision — Reconciliation Table

| AX label | Canonical name | TRON address | Documented in |
|----------|---------------|-------------|---------------|
| W5 | **W1** | `TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP` | TRON wallets full, AM cashout, AT enumeration |
| W6 | **W2** | `TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG` | TRON wallets full, AM cashout, AT enumeration |
| AX Aptos W5 | **A1** | `0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e` | Aptos wallets |
| AX Aptos W6 | **A2** | `0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3` | Aptos wallets |

**Why the AX naming was "W5/W6"**: The `_$_ccfc` payload string table has 58 entries; the
wallet pairs appear at indices 46–51 (XOR key, TRON, Aptos for each). The AX analysis
session referred to them as "W5/W6" based on their position in that table, not the
canonical dead-drop wallet numbering established in Task AM.

---

## XOR Key Confirmation

| Source | Label | XOR key |
|--------|-------|---------|
| AX `_$_ccfc[46]` | AX "W5 key" | `2[gWfGj;<:-93Z^C` |
| ANALYSIS_AT_WALLET_ENUMERATION.md, W1 row | Canonical W1 cipher | `2[gWfGj;<:-93Z^C` |

| Source | Label | XOR key |
|--------|-------|---------|
| AX `_$_ccfc[49]` | AX "W6 key" | `m6:tTh^D)cBz?NM]` |
| ANALYSIS_AT_WALLET_ENUMERATION.md, W2 row | Canonical W2 cipher | `m6:tTh^D)cBz?NM]` |

Both XOR keys match exactly. Task AT independently determined these keys from the AT wallet
enumeration; AX recovered them by decoding the obfuscator.io inner payload. Consistent.

---

## Transaction History (Already Fully Documented)

### Canonical W1 (`TMfKQEd7...`) — 37 total TXs

- **Funded**: 2025-06-06 by Operator Master (`TQdwohPCWqqfCUaCispyV1NaUZ1HgiJPUy`)
- **First dead-drop TX**: 2025-06-13 (campaign go-live)
- **Latest TX**: 2026-06-23 02:35 UTC — BSC `0x18a8420f727f2405f9d1805ad887b31029b584b2ff5a7ec0f57c72635183e99d`
- **Silence as of 2026-07-05**: 12 days (⚠️ approaching outer edge of 5–14 day cadence)

The Jun 23 TX is exactly the TX decoded in the AX-Live pull (confirmed).

### Canonical W2 (`TXfxHUet...`) — 11 total TXs

- **Funded**: 2025-06-13 by Operator Master
- **First dead-drop TX**: 2025-06-13
- **Latest TX**: 2026-06-20 13:37 UTC — BSC `0x7ffb4efddd96e20aec90724be2ac9a71c138a9af697b9fb8224bbf80ea4f22be`
- **Silence as of 2026-07-05**: 15 days

The Jun 20 TX is the AX-Live W6 pull (confirmed).

### Aptos A1 (`0xbe037400...`) — 22 total TXs

- Mirrors W1 TRON channel. Latest TX 2026-06-23 → same BSC hash as W1 Jun 23.
- Jun 23 Aptos TX `0xc422e4bb...` → `0x18a8420f...` (= W1 BSC, AX-Live confirmed ✓)

### Aptos A2 (`0x3f0e5781...`) — 10 total TXs

- Mirrors W2 TRON channel. Latest Jun 25 `_$_f5f0` payload (differs from W2 Jun 20 payload).
- Jun 23/25 A2 TXs carry `_$_f5f0` cipher — **NOT** the `_$_1e42`/AX outer wrapper format.
- A2 is pushing a newer cipher format in parallel to the AX obfuscator.io variant.

---

## Complete Dead-Drop Wallet Map (Post-AX)

From Task AT (`ANALYSIS_AT_WALLET_ENUMERATION.md`), the full enumeration is **closed** —
no wallets beyond W5 exist in either operator funding wallet's outgoing TX set:

| Wallet | TRON Address | XOR key | Stage | Active period |
|--------|-------------|---------|-------|---------------|
| W1 | `TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP` | `2[gWfGj;<:-93Z^C` | Stage 1 | Jun 2025 – Jun 2026 |
| W2 | `TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG` | `m6:tTh^D)cBz?NM]` | Stage 1 | Jun 2025 – Jun 2026 |
| W3 | `TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v` | `2[gWfGj;<:-93Z^C` | Stage 2 (Beavertail) | Nov 2025 – Jun 2026 |
| W4 | `TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF` | **Unknown** | Unknown Stage 1 variant | Nov 2025 – May 2026 |
| W5 | `TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH` | **Unknown** | Unknown dead-drop | Nov 2025 – Feb 2026 |

AX "W5"/"W6" names do NOT introduce new wallet slots. The total dead-drop count remains 5.

---

## Parallel Cipher Activity on W2/A2

While the AX obfuscator.io format uses the established `_$_1e42` inner cipher, A2 is
simultaneously serving a newer format (`_$_f5f0`) as of Jun 23–25 2026:

| Channel | Jun 20 payload | Jun 23 payload | Jun 25 payload |
|---------|---------------|---------------|---------------|
| W2 TRON | `_$_f5f0` / `_$_16d1` (W2 Stage 1) | — | — |
| A2 Aptos | — | `_$_f5f0` / `SgH` | `_$_f5f0` / `cdi` |

The `_$_f5f0` Jun 25 variant adds `global['m'] = module` — a new capability not present in
the AX obfuscator.io payloads. The obfuscator.io format (AX) and the newer `_$_f5f0` format
are running concurrently on the **same W1/W2 infrastructure**, indicating the actor is
deploying multiple Stage 1 variants simultaneously to different victim pools.

---

## Assessment

**The AX obfuscator.io wrapper uses the established W1/W2 infrastructure with no new wallets.**
The actor added the obfuscator.io delivery layer on top of the existing `_$_1e42` chain without
changing the underlying blockchain dead-drop or XOR key infrastructure.

The naming inconsistency in `ANALYSIS_AX_OBFUSCATOR.md` and `ANALYSIS_AX_STAGE2_LIVE.md`
("W5"/"W6") refers to canonical W1/W2. Future analysis should use W1/W2 for these addresses.

**Open gap (unchanged from Task AT):** W4 and canonical W5 ciphers remain unknown — BSC
archive access required to retrieve their payloads.

---

## Related Documents

- `ANALYSIS_TRON_WALLETS_FULL.md` — W1/W2 complete TX history (37 + 11 TXs)
- `ANALYSIS_APTOS_WALLETS.md` — A1/A2 full TX history; `_$_f5f0` new cipher
- `ANALYSIS_AM_CASHOUT_WALLETS.md` — Operator cluster; W3/W4/W5 funder wallet
- `ANALYSIS_AT_WALLET_ENUMERATION.md` — Full enumeration; W4/W5 cipher gap
- `ANALYSIS_AX_OBFUSCATOR.md` — Stage 1 decode (note: "W5/W6" = canonical W1/W2)
- `ANALYSIS_AX_STAGE2_LIVE.md` — Live Stage 2 pull via W1 Jun 23 TX
