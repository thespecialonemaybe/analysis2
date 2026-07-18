# Task AX-AV: Obfuscator.io Victim Wallet Extraction — CharlieJT, itzvin19 ×2

**Date:** 2026-07-18  
**Repos:** `CharlieJT/cleric-homepage`, `itzvin19/dance-studio`, `itzvin19/03-blog`  
**Reference:** `ANALYSIS_AV_ASTRO_SCAN.md` (victim discovery), `ANALYSIS_AX_OBFUSCATOR.md` (blob decode)

---

## Summary

All three remaining obfuscator.io-wrapped victims use **W1/W2 (canonical wallets)** — no new
infrastructure. The actor was still deploying to the old W1/W2 dead-drop pair as late as
**2026-06-26**, three days after W1's last dead-drop TX (Jun 23) and six days after W2's (Jun 20).
No replacement wallet infrastructure has appeared in any GitHub-discoverable repo.

---

## Repo Status (as of 2026-07-18)

| Repo | Status | push_at | Size |
|------|--------|---------|------|
| `CharlieJT/cleric-homepage` | **EXISTS** (not deleted) | 2026-06-26T06:44:25Z | 5,320 KB |
| `itzvin19/dance-studio` | **EXISTS** (not deleted) | 2026-06-25T11:50:00Z | 51,535 KB |
| `itzvin19/03-blog` | **EXISTS** (not deleted) | 2026-06-25T11:49:53Z | 2,712 KB |

All three repos remain live and unmodified since the June 2026 injection. No remediation.

---

## Payload Verification

| Repo | Total size | Campaign ID | Blob offset | Blob size | SHA-256[:16] |
|------|-----------|-------------|-------------|-----------|-------------|
| `aegre/damian` (reference) | 20,836 B | `9-7298` | 745 | 20,091 B | `eed6279da7999913` |
| `CharlieJT/cleric-homepage` | 20,932 B | `9-7172` | 841 | 20,091 B | `eed6279da7999913` |
| `itzvin19/dance-studio` | 21,025 B | `8-4435-1` | 935 | 20,090 B | `be16808dae74465f` |
| `itzvin19/03-blog` | 20,979 B | `8-4435-1` | 889 | 20,090 B | `be16808dae74465f` |

Two blob hashes appear: `eed6279d` (series 9) and `be16808d` (series 8). Byte-level diff
of the two blobs reveals **exactly one difference at position 20,089**: `\r\n` vs `\n`
(CRLF vs LF line ending at the final character of the file). This is a git line-ending
normalization artifact — the payloads are cryptographically and functionally identical.

The wallet addresses, XOR keys, cipher constants, and all payload logic are in the inner
compressed blob, well ahead of the final character. The AV doc's claim of byte-identity
is confirmed: the obfuscator.io template was deployed once, with only the campaign ID
substituted per victim.

---

## Wallet Extraction

The inner `_$_ccfc` string table (decoded in `ANALYSIS_AX_OBFUSCATOR.md`) applies to all
four victims:

| Index | Value | Role |
|-------|-------|------|
| 46 | `2[gWfGj;<:-93Z^C` | **W1 XOR key** (16 chars) |
| 47 | `TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP` | **W1 TRON wallet** |
| 48 | `0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e` | W1 Aptos fallback |
| 49 | `m6:tTh^D)cBz?NM]` | **W2 XOR key** (16 chars) |
| 50 | `TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG` | **W2 TRON wallet** |
| 51 | `0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3` | W2 Aptos fallback |

(Note: AX analysis used W5/W6 names for these; AX-W crossref confirmed W5=W1, W6=W2 canonical.)

**Result: all four obfuscator.io victims use W1/W2. No new wallet infrastructure.**

---

## Operational Implication: Victims Deployed After Wallets Went Silent

The deployment timeline relative to wallet silence is significant:

| Date | Event |
|------|-------|
| 2026-06-08 | W3 last dead-drop TX (Stage 2 channel silenced) |
| 2026-06-20 | W2 last dead-drop TX; `aegre/damian` swept (same day) |
| 2026-06-23 | W1 last dead-drop TX |
| 2026-06-24 | JFrog blog post published |
| 2026-06-25 | `itzvin19/dance-studio` and `itzvin19/03-blog` swept |
| 2026-06-26 | `CharlieJT/cleric-homepage` swept — **3 days after W1's last TX** |

The `itzvin19` and `CharlieJT` victims were infected **after** W2 and W1 respectively had
already posted their last dead-drop payloads. These victims' Stage 1 loaders would fetch
the most recent (and now final) BSC TX hash from W1/W2. For CharlieJT (infected Jun 26),
the W1 dead-drop from Jun 23 was only 3 days stale — likely still available on BSC nodes
at that time, meaning the Stage 1 would have successfully fetched Stage 2. By Jul 18 (25
days later), the Jun 23 BSC TX is almost certainly pruned from all public BSC RPC nodes,
so CharlieJT's payload is now non-functional.

This timing suggests the actor's sweeping automation continued running **after the actor
manually stopped updating the dead-drop wallets**, either because:
1. The sweep tooling runs on a schedule independent of wallet management, or
2. The actor was already in wind-down, letting existing wallet state coast while sweeping continued

---

## No New Infrastructure Found

The primary motivation for AX-AV was to check whether the Jun 20–26 deployment wave might
reference new wallets (actor potentially rotating infrastructure as W1–W3 were wound down).
The answer is no: the entire wave reuses W1/W2. Combined with the wallet silence check
(2026-07-18: W1 25d, W2 28d, W3 40d), there is **no visible evidence of replacement
blockchain dead-drop infrastructure** in any GitHub-discoverable repository.

If the actor has stood up new wallets, they have not yet appeared in public GitHub repos.
The actor may be:
1. In a full operational pause post-JFrog disclosure
2. Using a new delivery vector not yet detected (different file types, different platforms)
3. Deploying to private/invitation-only repositories not indexed by GitHub

---

## Related Documents

- `ANALYSIS_AV_ASTRO_SCAN.md` — victim discovery and AX decode summary
- `ANALYSIS_AX_OBFUSCATOR.md` — full obfuscator.io decode; complete `_$_ccfc` string table
- `ANALYSIS_AX_W_CROSSREF.md` — AX W5/W6 = canonical W1/W2 confirmation
- `ANALYSIS_AX_STAGE2_LIVE.md` — live Stage 2 fetch and C2 routing table
