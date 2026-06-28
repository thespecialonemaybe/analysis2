# Task S: TRON W1/W2 Full Transaction History

**Date:** 2026-06-28  
**Task:** Re-query TRON W2 for Jun 23/25 updates; compare to Aptos A2 timeline

---

## Key Findings

1. **Jun 23/25 Aptos A2 updates are confirmed Aptos-only** — TRON W2 has NO transactions on those dates. The actor updated the Aptos fallback without touching TRON.

2. **True operation start: June 6, 2025** — W1 wallet has TXs going back to Jun 6, 2025. The "Myx custom memo text" test TXs on that date show the actor manually testing the TRON memo field 7 days before the first real BSC TX pointer was deployed.

3. **No-memo TXs are cashout transactions** — `TransferContract` and `TransferAssetContract` TXs with no `raw_data.data` field are the actor moving TRX/TRC-10 tokens to secondary wallets. Two actor cashout wallet addresses identified.

4. **Actor cashout wallets discovered:**
   - W1 cashout: `41803f5d3cc635e5ac3c96c86a6cbe98c9eda82e66`
   - W2 cashout: `41ee0f692be2f1e405b35b027260ba696de90a43dd`

5. **W1 has 37 total TXs** (vs W2's 11) — W1 is the primary channel, W2 is lighter-use.

6. **One new W2 Jun 13 2025 BSC TX found** (`0x1a323149...`) — pruned from BSC archive, payload unrecoverable.

---

## TRON W2 Full Transaction Map

`TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG` — 11 total TXs:

| Date (UTC) | TRON TX | Type | BSC TX / Notes |
|-----------|---------|------|----------------|
| 2026-06-20 13:37 | `3a2b5067...` | Dead-drop | `0x7ffb4efddd96e20aec...` (known) |
| 2026-06-14 17:06 | `239b0e89...` | **Cashout** | TRC-10 amount=970000 to W2 cashout wallet |
| 2026-03-26 15:13 | `fc005f15...` | Dead-drop | `0xa896af4f2876df59af...` (known) |
| 2026-03-26 14:53 | `acc53081...` | Dead-drop | `0xea7e97b13fc70642ed...` (known) |
| 2026-03-04 16:27 | `47f808cc...` | Dead-drop | `0x60537dcbb1ad6a1fdd...` (known) |
| 2025-08-13 14:06 | `1264bb24...` | Dead-drop | `0xd33f78662df123adf2...` (known) |
| 2025-06-18 08:28 | `5bb93a04...` | Dead-drop | `0x13e3ce3aefc019258c...` (known) |
| 2025-06-13 05:55 | `e0d9ac0d...` | Dead-drop | `0xc83de8720855a6b207...` (known) |
| 2025-06-13 05:54 | `4dd04cbb...` | Dead-drop | `0x919911669b003d263c...` (garbled) |
| 2025-06-13 05:50 | `f394244b...` | Dead-drop | `0x1a323149a56ac6a1ca...` (**new** — BSC pruned) |
| 2025-06-13 05:45 | `ea27f4c9...` | **Cashout** | TransferContract to W2 cashout wallet |

**Jun 23/25 confirmed absent** — TRON W2 last updated Jun 20. Aptos A2 was updated directly.

---

## TRON W1 Full Transaction Map

`TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP` — 37 total TXs:

| Date (UTC) | TRON TX | Type | BSC TX / Notes |
|-----------|---------|------|----------------|
| 2026-06-23 02:35 | `baf00565...` | Dead-drop | `0x18a8420f727f2405f9...` (known) |
| 2026-06-18 13:09 | `ff86aec0...` | Dead-drop | `0xb73920732115ab3a0a...` (known) |
| 2026-06-15 01:05 | `bf6af17f...` | **Cashout** | TRC-10 amount=970000 to W1 cashout wallet |
| 2026-05-23 16:16 | `914e5e07...` | Dead-drop | `0x80a1148ee589125bc1...` (known) |
| 2026-05-23 15:01 | `5818540d...` | Dead-drop | `0x7d726de66b27361943...` (known) |
| 2026-05-20 19:32 | `88a61bb9...` | **Cashout** | TRC-10 amount=8888 to W1 cashout wallet |
| 2026-05-20 15:16 | `288ab333...` | Dead-drop | `0x7c1c8ad22f95491daa...` (known) |
| 2026-03-31 14:20 | `d991242176...` | Dead-drop | `0x64286dc9d288cca084...` (known) |
| 2026-03-26 15:59 | `f8cf4cb1...` | Dead-drop | `0xbe22e3626ef8ca4f84...` (known) |
| 2026-03-26 15:10 | `d4a11408...` | **Cashout** | TRX amount=6 to W1 cashout wallet |
| 2026-03-26 15:10 | `05f244e2...` | **Cashout** | TRX amount=15000000 sun (=15 TRX) to W1 cashout wallet |
| 2026-03-04 17:03 | `87b7e4d0...` | Dead-drop | `0xc06e1b8427d699d2cc...` (known) |
| 2025-12-01 14:09 | `2480c7d7...` | Dead-drop | `0xec567681e8c98d694e...` (known) |
| 2025-10-01 17:26 | `f3c46284...` | Dead-drop | `0xf46c86c886bbf9915f...` (known) |
| 2025-10-01 17:01 | `e2604d06...` | Dead-drop | `0xb980676a283234de8a...` (known) |
| 2025-10-01 16:56 | `beccc95a...` | Dead-drop | `0x1ad0dd0135fe084e57...` (**TEST** `_V='9-test'`) |
| 2025-08-19 16:46 | `1dfb1569...` | Dead-drop | `0xa2ffa9b0ec69869ccb...` (`RVj` cipher) |
| 2025-07-23 16:28 | `b1681edf...` | Dead-drop | `0x51a46279be66265b3e...` (`GAR` cipher) |
| 2025-06-24 05:23 | `3a599d0d...` | Dead-drop | `0xe40a40c6cef6461da5...` (`AOv` cipher) |
| 2025-06-24 05:14 | `c416fea9...` | Dead-drop | `0x67e43df37ecad064d6...` (`DML` cipher) |
| 2025-06-13 06:25 | `8467773b...` | Dead-drop | `0xe5a0cff72c7529b1d8...` (`uap` cipher) |
| 2025-06-13 05:19 | `e4d94eb7...` | Dead-drop | `0x1293aa8f691e49ba26...` (`BIY` cipher) |
| 2025-06-13 05:06 | `52d3d1f7...` | Dead-drop | `0x14e7b64b5369fc74b0...` (garbled W1 key) |
| 2025-06-11 16:58 | `2bafedee...` | **Failed encoding** | Binary memo (not valid BSC TX hash) |
| 2025-06-11 16:57 | `40ee0738...` | **Failed encoding** | Binary memo (same content — repeated attempt) |
| 2025-06-10 07:06 | `63dc4d88...` | Infrastructure | TRX 1 sun to W1 cashout wallet |
| 2025-06-10 07:05 | `de2dbd47...` | Infrastructure | TRX 2 sun to W1 cashout wallet |
| 2025-06-10 07:05 | `625a1f2c...` | Infrastructure | TRX 70000000 sun (=70 TRX) to new address |
| 2025-06-06 15:34 | `38515cd9...` | **Test** | Memo: `"Mxy custom memo text"` |
| 2025-06-06 14:45 | `3fa56cbb...` | **Test** | Memo: `"Mxy custom memo text"` |
| 2025-06-06 14:30 | `3443dbdc...` | Infrastructure | TRX 1 sun to funding address |
| 2025-06-06 14:19 | `bc2f72bc...` | Infrastructure | TRX 1 sun to funding address |
| 2025-06-06 14:17 | `fa2831520...` | Infrastructure | TRX 1 sun to funding address |
| 2025-06-06 14:08 | `1ec33afe...` | Infrastructure | TRC-10 amount=800 to W1 cashout wallet |
| 2025-06-06 14:06 | `ade80528...` | Infrastructure | TRX 8 to W1 cashout wallet |
| 2025-06-06 14:06 | `11e1c22b...` | Infrastructure | TRX 1 to W1 cashout wallet |
| 2025-06-06 14:06 | `72ea9405...` | Infrastructure | TRX 100000000 sun (=100 TRX) to W1 cashout wallet |

---

## Infrastructure Setup Timeline (June 6–13, 2025)

```
2025-06-06 14:06  W1 funded: 100 TRX to W1 cashout wallet (initial setup)
2025-06-06 14:06  Small TRX transfers (account activation test)
2025-06-06 14:08  TRC-10 token transfers to cashout
2025-06-06 14:17–30  TRX to funding address (unknown third party — possibly exchange?)
2025-06-06 14:45  TEST memo: "Mxy custom memo text"
2025-06-06 15:34  TEST memo: "Mxy custom memo text" (second test)
2025-06-10 07:05  Fund TRX transfers (testing continuation)
2025-06-11 16:57  Failed binary memo attempt #1 (raw binary in data field)
2025-06-11 16:58  Failed binary memo attempt #2 (same binary content)
            ↑ Actor discovers binary encoding doesn't work — switches to hex-encoded UTF-8
2025-06-13 05:06  FIRST LIVE BSC TX POINTER deployed (W1 goes operational)
2025-06-13 05:45  W2 funded (TRX transfer to W2 cashout wallet)
2025-06-13 05:50  W2 first live BSC TX pointer (3 attempts on same day)
2025-06-13 05:54–55  W2 second and third attempts
2025-06-13 05:12–06:25  Aptos A1 and A2 set up as fallbacks (Aptos TXs begin)
```

The Jun 11 failed binary memos are particularly revealing: the actor tried to embed the BSC TX hash as raw binary bytes (not hex-encoded), which the malware's `bytes.fromhex().decode()` pipeline could not parse. They corrected this on Jun 13 by hex-encoding the hash first.

---

## Actor Cashout Wallets

| Wallet (hex) | Used by | Transactions |
|-------------|---------|-------------|
| `41803f5d3cc635e5ac3c96c86a6cbe98c9eda82e66` | W1 cashout | Multiple TRX/TRC-10 transfers from W1, dating to Jun 6 2025 |
| `41ee0f692be2f1e405b35b027260ba696de90a43dd` | W2 cashout | Jun 13 2025 initial, Jun 14 2026 TRC-10 transfer |

These addresses receive periodic TRX and TRC-10 token transfers from the dead-drop wallets.
The Jun 15 2026 W1 cashout (TRC-10 amount=970000) and Jun 14 2026 W2 cashout (TRC-10 amount=970000)
are interesting: both are the same TRC-10 amount on consecutive days — likely routine cashout
of earnings from C2 operations (ransoms, stolen credentials, crypto keys).

---

## Aptos vs TRON Update Synchronization

Cross-referencing all known updates across channels:

| Date | TRON W1 | TRON W2 | Aptos A1 | Aptos A2 | Notes |
|------|---------|---------|----------|----------|-------|
| 2025-06-13 | ✓ (3 TXs) | ✓ (3 TXs) | ✓ (4 TXs) | ✓ (2 TXs) | Go-live day |
| 2025-06-18 | — | ✓ | — | ✓ | W2 update only |
| 2025-06-24 | ✓ (2 TXs) | — | ✓ (2 TXs) | — | W1 update only |
| 2025-07-23 | ✓ | — | ✓ | — | W1 update only |
| 2025-08-13 | — | ✓ | — | ✓ | W2 update only |
| 2025-08-19 | ✓ | — | ✓ | — | W1 update only |
| 2025-10-01 | ✓ (3 TXs) | — | ✓ (3 TXs) | — | W1 test+fix+rotate |
| 2025-12-01 | ✓ | — | ✓ | — | W1 update only |
| 2026-03-04 | ✓ | ✓ | ✓ | ✓ | Both channels updated |
| 2026-03-26 | ✓ (3 TXs) | ✓ (2 TXs) | ✓ (4 TXs) | ✓ (2 TXs) | Major update day |
| 2026-03-31 | ✓ | — | ✓ | — | W1 update only |
| 2026-05-20 | ✓ | — | ✓ | — | W1 update only |
| 2026-05-23 | ✓ (2 TXs) | — | ✓ (2 TXs) | — | W1 update only |
| 2026-06-18 | ✓ | — | ✓ | — | W1 update only |
| 2026-06-20 | — | ✓ | — | ✓ | W2 update only |
| 2026-06-23 | ✓ | — | ✓ | ✓ | **W1 TRON + A1 + A2** (A2 Aptos-only!) |
| 2026-06-25 | — | — | — | ✓ | **Aptos A2 only — no TRON update** |

The Jun 23 and Jun 25 A2 updates had no TRON counterpart — confirmed Aptos-only deployments.
Notably, Jun 23 W1 TRON DID update (BSC `0x18a8420f...`) and A1 Aptos also updated — only A2
received a different payload that day (the new `_$_f5f0` cipher).

---

## New IOCs

```
# Actor cashout wallet addresses (TRON)
41803f5d3cc635e5ac3c96c86a6cbe98c9eda82e66   ← W1 cashout (TRON hex format)
41ee0f692be2f1e405b35b027260ba696de90a43dd   ← W2 cashout (TRON hex format)

# New TRON W2 TX (Jun 14 2026 cashout)
239b0e89cda4308942c9f994a804474fc6f9bfbd4feac7a10d17226c47ee0a19

# New BSC TX (W2 Jun 13 2025 — payload pruned)
0x1a323149a56ac6a1caa1f804c2a26c5ff7b36820023b0ab2a0c44de06d30cf01

# Operation timeline
True start:       2025-06-06 (TRON W1 setup and testing)
First live deploy: 2025-06-13 (both TRON channels + Aptos fallbacks go live)
```
