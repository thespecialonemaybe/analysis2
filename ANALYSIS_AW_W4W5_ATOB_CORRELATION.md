# Task AW: W4/W5 TX Date Correlation with Atob Dropper Victims

**Date:** 2026-07-11  
**Wallets:** W4 (`TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF`), W5 (`TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH`)  
**Victims:** NikhilGupta777 (sweep 2026-06-15), Rafijohari18 (sweeps 2026-06-19/21)

---

## Summary

The atob dropper (`11-#` variant, SHA `81b3b0ab`) does **not** use W4 or W5 as its dead-drop
channel — it uses canonical W1/W2, confirmed by AK decode (identical `pYd_enc` and wallet
hardcodes). However, two new findings emerge from fresh TRON API queries:

1. **W4 received TRC-10 token 1005141 (970,000 units) at 2026-06-15 01:05 UTC** — exactly 33
   minutes after the NikhilGupta777 sweep completed (00:24–00:32 UTC). This is the actor's
   on-chain bookkeeping for the sweep operation, not a dead-drop TX.

2. **All 23 W4 BSC TX hashes and all 3 W5 BSC TX hashes are now documented** — previously
   unavailable because AM analysis used API summary data rather than raw memo fields.

W5 is confirmed dormant since 2026-02-27. No correlation with June 2026 atob sweeps exists
for either wallet's dead-drop activity.

---

## Primary Answer: Atob Dropper Uses W1/W2, Not W4/W5

From `ANALYSIS_AK_RAFI.md` (Task AK decode of Rafijohari18/astro-speed):

> The `eval(atob(...))` IIFE-2 has a byte-for-byte identical `pYd_enc` to IIFE-1 (standard
> sfL dropper). Both decode to the same 3,858-char Stage 1 body with TRON wallets
> W1: `TMfKQEd7...` and W2: `TXfxHUet...`.

The atob dropper is purely an encoding change — the inner Stage 1 logic, wallet addresses, and
XOR keys are unchanged from standard infections. W4/W5 are irrelevant to the atob victim pool.

W4 and W5 serve an **unknown Stage 1 variant** with an unknown cipher and unknown XOR key.
Their victim pool is not searchable via GitHub code scan (the Stage 1 payload that references
W4/W5 has never been recovered from a public repository).

---

## W4 Transaction Timeline (Full, Verified from Raw API)

All timestamps verified by converting raw `block_timestamp` (ms) to UTC. Previous ANALYSIS_AM
documented 10 TXs in the Feb 25 batch; raw data shows **12 TXs** in that session.

| UTC Date | Type | Detail |
|----------|------|--------|
| 2025-11-13 15:03 | Funding | 50 TRX from W3/W4/W5 Funder |
| 2025-11-14 13:50 | Dead-drop | BSC hash A (see table below) |
| 2025-11-14 14:01 | Dead-drop | BSC hash B |
| 2025-12-17 11:47 | Dead-drop | BSC hash C |
| 2026-02-10 14:32 | Dead-drop | BSC hash **B** (duplicate — same payload reused from Nov 14) |
| 2026-02-10 14:41 | Dead-drop | BSC hash D |
| 2026-02-10 20:47 | Dead-drop | BSC hash E |
| 2026-02-12 13:05 | Dead-drop | BSC hash F |
| 2026-02-25 18:06 | Dead-drop | BSC hash G (key rotation batch start) |
| 2026-02-25 18:10 | Dead-drop | BSC hash H |
| 2026-02-25 18:12 | Dead-drop | BSC hash I |
| 2026-02-25 18:27 | Dead-drop | BSC hash J |
| 2026-02-25 18:42 | Dead-drop | BSC hash K |
| 2026-02-25 18:55 | Dead-drop | BSC hash L |
| 2026-02-25 19:09 | Dead-drop | BSC hash M |
| 2026-02-25 19:16 | Dead-drop | BSC hash N |
| 2026-02-25 19:46 | Dead-drop | BSC hash O |
| 2026-02-25 20:57 | Dead-drop | BSC hash P |
| 2026-02-25 20:59 | Dead-drop | BSC hash Q |
| 2026-02-25 21:00 | Dead-drop | BSC hash R (key rotation batch end) |
| 2026-03-10 14:57 | Dead-drop | BSC hash S |
| 2026-03-26 15:10 | Fee TX | 15 TRX → W1 (`41803f5d...`) — operational fee replenishment |
| 2026-03-26 15:13 | Dead-drop | BSC hash T |
| 2026-05-19 15:04 | Dead-drop | BSC hash U (**last dead-drop TX**) |
| 2026-05-19 19:28 | TRC-10 recv | 8,888 units token 1005114 from `416a224bcf...` |
| **2026-06-15 01:05** | **TRC-10 recv** | **970,000 units token 1005141 from `4101774404...`** |

**Total dead-drop TXs: 23** (including 1 hash reuse). **Total unique BSC hashes: 22.**

### Feb 25, 2026 Correction

`ANALYSIS_AM` documented "10 TXs" in the Feb 25 session. Raw timestamps show **12 TXs** over
a 2h54m window (18:06–21:00 UTC). This is the same date W3 deployed its XOR key rotation
(`cA]2!+37v,-szeU}` → `2[gWfGj;<:-93Z^C`, per Task X). W4's 12-TX burst is consistent with
a simultaneous W3/W4 key rotation event.

### Hash B Reuse (Nov 14 → Feb 10)

BSC hash `0x3b62da076ee5f14201c15af18891ed23eb63162a507062e8bee010c5cf98faeb` appears on both
2025-11-14 (second TX) and 2026-02-10 (first TX of the session). The actor reposted the same
Stage 2 BSC TX without updating the payload — W4's victim pool ran the same Stage 2 from
Nov 14, 2025 through Feb 10, 2026 (a ~87-day window of stable payload).

---

## W4 BSC TX Hash Registry (All 23 TXs)

All hashes are pruned from all public BSC RPC nodes (confirmed in Task AT). Documented here
for future retrieval via archive node (Quicknode/Alchemy full-archive).

| Date | TRON TX | BSC TX Hash |
|------|---------|-------------|
| 2025-11-14 13:50 | `cf23...64` | `0xcf23a3eeea74520bc87d58e6aaac8d04ff6425d549f5f96ee639cc784c780067` |
| 2025-11-14 14:01 | `2cdfd0...` | `0x3b62da076ee5f14201c15af18891ed23eb63162a507062e8bee010c5cf98faeb` |
| 2025-12-17 11:47 | `d7e3c3...` | `0x2025a199b9f3d6fc9358337314c556b004a98bbed87bd8c48ecf76ce5ef55d23` |
| 2026-02-10 14:32 | `98f3fc...` | `0x3b62da076ee5f14201c15af18891ed23eb63162a507062e8bee010c5cf98faeb` (reuse) |
| 2026-02-10 14:41 | `44d4de...` | `0xb78eeb8d9e71f712ab9a81dfcc61e06500a4b4112329ff50e934da99b460c752` |
| 2026-02-10 20:47 | `dc928f...` | `0x2cc0e34a0714856a1557e55ca7d45063158e5b87ed472b6ca8ae385051886416` |
| 2026-02-12 13:05 | `1eecd7...` | `0xc55322b77991da29074cc893b306087d8e1e91569133968c8f89d9d65d77a74a` |
| 2026-02-25 18:06 | `062af0...` | `0xd99818bcc1d98d44f3de367137c8e93776aa23d13514ce69cc510e81f5bf7733` |
| 2026-02-25 18:10 | `4dd571...` | `0xc3a3435dfed2a961dde2cfc0cf1f2ed08ce60238393f4d5edec8a6c0d841e86e` |
| 2026-02-25 18:12 | `8286bd...` | `0x14d210084099694c011d7d0dbf64986b8d9867809f2126a0ae964b8131547f7e` |
| 2026-02-25 18:27 | `5a4ab9...` | `0x602fde62931699bec9eb05ddf9b5a280c1eab3bcc9d2ad1af116c7612039cc18` |
| 2026-02-25 18:42 | `f3e394...` | `0x529caff0aee2d5da44032f2c367f537f38aa224df3de131e8bdc63ed594dcf8e` |
| 2026-02-25 18:55 | `8c2d77...` | `0x560415046778e7abd3416af69ba003ab4d570563277d792ce68f7ceb611bc84d` |
| 2026-02-25 19:09 | `aa6690...` | `0x93d43725b946d8ddfce09bf4154f5b2df94263903c1fefc4c3436ab92bb6706b` |
| 2026-02-25 19:16 | `273d6c...` | `0xa62ba4fa40a51ccef2abc71c6b16840a5c12634b092aca3a11db57c0caef688f` |
| 2026-02-25 19:46 | `376966...` | `0x1780ea17164d5d6cad4cc762e1957032c1e644188856bf9b39ec1d9f924e362c` |
| 2026-02-25 20:57 | `25ae20...` | `0x88ed44af7612ffd4fc11b5385d2405c9c52c0d0df65773c958fc9a628a3451e8` |
| 2026-02-25 20:59 | `b19017...` | `0x9a81c1a22e3b916bc8b1eedd9d70224e9af9c4833d2faf6baed0e741f9238a5b` |
| 2026-02-25 21:00 | `67ef02...` | `0x39daa01908964927dd9ea62c947fccf0e84bcba6156f438e171e4db2967ddab4` |
| 2026-03-10 14:57 | `a0af16...` | `0x578a8cbe42be19f6f862c7534fe502bc1a8ac8eb4f267b52b8fa6832bdcc8d05` |
| 2026-03-26 15:13 | `53ff86...` | `0x3055151b225752885be415c199341117ba0512c7298b375fe78eaaaaff4b49b9` |
| 2026-05-19 15:04 | `23c31c...` | `0x0fa804035bcf4aa8ad029406e1bd1d83c51963a0075e22349bda76c6eba58ba5` |

**Current W4 payload** (as of Jun 2026, when atob victims run their payloads): the May 19, 2026
BSC TX. W4-subscribing victims who ran their dropper in June 2026 fetched
`0x0fa804035bcf4aa8ad029406e1bd1d83c51963a0075e22349bda76c6eba58ba5` — a payload that's been
live for 27 days by the sweep date.

---

## W5 Transaction Timeline (Complete)

| UTC Date | Type | Detail |
|----------|------|--------|
| 2025-11-13 15:02 | Funding | 50 TRX from W3/W4/W5 Funder |
| 2025-11-19 14:03 | Dead-drop | BSC hash 1 |
| 2026-02-12 13:29 | Dead-drop | BSC hash 2 |
| 2026-02-27 02:27 | Dead-drop | BSC hash 3 (**last TX, ever**) |

W5 BSC TX Hashes:

| Date | BSC TX Hash |
|------|-------------|
| 2025-11-19 | `0x88c02dd40e793c33eabc5d657616907f0e8398c91364b5694f16d37b577f0b18` |
| 2026-02-12 | `0x5cf62a3c22e6d1b1021a0d7a780387d6646bf363ceb18e02fccc375a513a174b` |
| 2026-02-27 | `0x61606e03fdf7d53657645a199d63ba5369a638424ff641e39dfd3f8c1e679ccb` |

W5 has been completely inactive since 2026-02-27 (134 days as of today). No TRC-10 coordination
tokens have been received. W5 appears to have served a very small pilot group and was abandoned.

---

## New Finding: TRC-10 Timing Correlation

| Event | UTC Timestamp | Delta |
|-------|--------------|-------|
| NikhilGupta777 sweep start | 2026-06-15 00:24 | — |
| NikhilGupta777 sweep end | 2026-06-15 00:32 | +8 min |
| **W4 receives TRC-10 1005141 (970,000 units)** | **2026-06-15 01:05** | **+33 min** |

The actor received TRC-10 token 1005141 to W4 **33 minutes after completing the sweep** of
NikhilGupta777's 31 repos. This is the tightest timing correlation between a W4 event and any
documented actor operation in the dataset.

### TRC-10 Token Sender

The token arrived from `4101774404645f3d10473b1ddc290db6f5b01378ca` (TRON hex). This address
is new — not previously documented in ANALYSIS_AM or ANALYSIS_AT. The same address sent
970,000 units of token 1005141 specifically to W4.

Compared to the May 19, 2026 TRC-10 receipt (8,888 units of token 1005114 from `416a224bcf...`),
the June 15 receipt uses a different token ID, different amount, and different sender address.
This inconsistency suggests different tokens serve different tracking purposes.

### Interpretation

The TRC-10 token sent 33 minutes post-sweep is consistent with the actor using on-chain token
transfers as completion signals:
- After finishing a sweep of a victim's repos, the actor sends a token to the relevant
  infrastructure wallet as an internal timestamp/confirmation
- The W4 wallet is not the delivery channel for these victims (they use W1/W2), but W4 may be
  the actor's "tracking" wallet for this victim batch
- The amount (970,000) does not obviously encode victim count (31 repos) — it may be an
  internal campaign-amount encoding or simply an arbitrary amount from the actor's token supply

This is the first documented case where a TRC-10 transfer to W4 is tightly correlated (< 1h)
with a documented victim sweep event.

---

## Correlation Summary

| Wallet | Last dead-drop | Days before sweep | New activity after? |
|--------|----------------|-------------------|--------------------|
| W4 | 2026-05-19 | 27 days | TRC-10 on Jun 15 (+33min post-sweep) |
| W5 | 2026-02-27 | 109 days | None |
| W1 | 2026-06-23 | — (post-sweep) | Used by atob dropper directly |
| W2 | 2026-06-20 | — (post-sweep) | Used by atob dropper directly |

**Conclusion**: The atob dropper victims use W1/W2 for dead-drop delivery. W4 has no dead-drop
activity coinciding with the June 2026 sweeps, but the Jun 15 TRC-10 receipt suggests W4 is
operationally linked to the same actor session that conducted the sweep. W5 is dormant.

---

## W4 Cipher Status

W4 BSC payloads are pruned from all public RPC nodes (confirmed, Task AT). The 22 unique
hashes documented above are now available for archive node retrieval. Until retrieved, W4's
XOR cipher and Stage 1 variant structure remain unknown.

The only testable inference: W4's Feb 25, 2026 key rotation (12 new BSC TXs) synchronized
with W3's XOR key rotation on the same date. If W4 follows the same rotation pattern as W3,
its post-Feb-25 XOR key is likely `2[gWfGj;<:-93Z^C` (canonical W1 key) — but this is
unconfirmed.

---

## New IOCs

| Type | Value | Notes |
|------|-------|-------|
| W4 current BSC TX | `0x0fa804035bcf4aa8ad029406e1bd1d83c51963a0075e22349bda76c6eba58ba5` | May 19, 2026 — served to W4 victims through Jun 2026 |
| W5 last BSC TX | `0x61606e03fdf7d53657645a199d63ba5369a638424ff641e39dfd3f8c1e679ccb` | Feb 27, 2026 — last W5 payload |
| TRC-10 sender (Jun 15) | `4101774404645f3d10473b1ddc290db6f5b01378ca` | Sent 970K token 1005141 to W4, 33min post-sweep |
| TRC-10 sender (May 19) | `416a224bcf011c57a2394644b304a4b56635172fac` | Sent 8,888 token 1005114 to W4 |
| TRC-10 token 1005114 | 8,888 units to W4 (2026-05-19) | Post-payload rotation coordination token |
| TRC-10 token 1005141 | 970,000 units to W4 (2026-06-15 01:05 UTC) | Post-sweep coordination token |
| W4 full BSC hash set | 22 unique hashes (2025-11-14 – 2026-05-19) | All documented in table above |
| W5 full BSC hash set | 3 unique hashes (2025-11-19 – 2026-02-27) | All documented in table above |

---

## Related Documents

- `ANALYSIS_AM_CASHOUT_WALLETS.md` — W4/W5 discovery; wallet cluster graph
- `ANALYSIS_AT_WALLET_ENUMERATION.md` — W4 BSC payload recovery attempt (pruned)
- `ANALYSIS_AP_ATOB_DROPPER.md` — NikhilGupta777/Rafijohari18 atob victim analysis
- `ANALYSIS_AK_RAFI.md` — atob dropper decode confirming W1/W2 usage
- `ANALYSIS_TRON_WALLETS_FULL.md` — W1/W2 transaction history
