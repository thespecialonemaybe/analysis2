# Task AM: Actor Cashout Wallet Tracing

## Summary

Systematic tracing of all non-dead-drop TRON transactions from W1, W2, and W3 revealed the
actor's complete on-chain infrastructure cluster: two operator funding wallets, five confirmed
dead-drop wallets (W1–W5), and a TRX→USDT cash-out pathway. Two previously unknown dead-drop
wallets (W4, W5) are now documented.

The `ANALYSIS_TRON_WALLETS_FULL.md` "cashout wallet" hex labels were a documentation error —
those hex values decoded to the W1/W2 operational wallets themselves. This task corrects that
record and extends the wallet map.

---

## Methodology

Queried TRON Grid API for all outgoing and incoming transactions on W1, W2, W3, and their
connected addresses. Pattern for dead-drop wallets: all outgoing TXs send 1 sun to
`41000...000` (null address) with BSC TX hash encoded in the `data` (memo) field. This
distinguishes them from funding/cash-out wallets immediately.

---

## Operator Infrastructure Cluster

### Operator Master Wallet — `TQdwohPCWqqfCUaCispyV1NaUZ1HgiJPUy`
**Created: 2024-10-28** | Balance: 146 TRX | TRC-10 tokens: 1005050, 1005027, 1005028

This is the primary operator funding wallet. It directly funded W1 and W2:

| Date | Action | To | Amount |
|------|--------|-----|--------|
| 2025-06-06 | Fund W1 | `TMfKQEd7...` (W1) | 100 TRX |
| 2025-06-13 | Fund W2 | `TXfxHUet...` (W2) | 10 TRX |
| 2025-06-12–20 | Fund `TLmj13VL...` | Recurring operational | 10–20 TRX × 4 |
| 2024-11-19 | Large send | `TXhMYPCQ...` | 250 TRX |
| 2024-11-19 | Large send | `TFxcpVEY...` | 100 TRX |
| 2024-12-27 | Large send | `TYUJ8XWG...` | 80 TRX |
| 2025-03-09 | Large send | `TPDBqDKA...` | 100 TRX |

The Nov-Dec 2024 and Mar 2026 large sends predate and postdate W1/W2 activation — this
wallet is used for broader operational finance, not just C2 wallet funding. Multiple
`TriggerSmartContract` TXs (Jun 2025, Jan 2025, Nov 2024) indicate DEX operations.

Received large inflows:
- 35 TRX from `TVxW8vnh...` (May 2025)
- 93 TRX from `TDoXUNZ6...` (Jan 2025)

These inflows suggest the operator is being supplied TRX from other operational accounts
that receive revenue (possibly exchange cashouts from other campaigns).

### W3/W4/W5 Funder — `TGJ1YJJNkFYLZKU4ZGqJfS6dU2cvGac7pS`
**Created: 2024-11-02** (5 days after Operator Master) | Balance: 352 TRX + 543 USDT | TRC-10: 1005026, 1005027

Funded W3, W4, and W5 in two batches:

| Date | Action | To | Amount |
|------|--------|-----|--------|
| 2025-11-13 | Fund W3 (initial) | `TA48dct6...` | 50 TRX |
| 2025-11-13 | Fund W4 (initial) | `TCqf6Zka...` | 50 TRX |
| 2025-11-13 | Fund W5 (initial) | `TFMryB9m...` | 50 TRX |
| 2026-03-03 | Fund W3 (replenish) | `TA48dct6...` | 100 TRX |
| 2025-10-30 | Fund `TLmj13VL...` | Recurring operational | 50 TRX |
| 2025-05-08 | Send to `41897fde...` | Unknown | 101 TRX |
| 2025-04-14 | Send to `41253f80...` | Unknown | 50 TRX |

**The Nov 13, 2025 batch** is significant: W3, W4, and W5 were all created and funded in the
same 2-minute window. This is the same date W3 first started making dead-drop TXs.

The creation of `TGJ1YJJNkFYLZKU4ZGqJfS6dU2cvGac7pS` just 5 days after the Operator Master
strongly suggests these two wallets are held by the same operator and set up together in a
pre-operation infrastructure preparation session.

---

## Dead-Drop Wallet Map (Complete)

All 5 confirmed dead-drop wallets:

| Wallet | Address | Dead-drop TXs | Active period | Notes |
|--------|---------|--------------|---------------|-------|
| W1 | `TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP` | 21 | Jun 2025 – Jun 2026 | W1 Stage 1 channel; publicly known |
| W2 | `TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG` | 9 | Jun 2025 – Jun 2026 | W2 Stage 1 channel; publicly known |
| W3 | `TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v` | 69+ | Nov 2025 – Jun 2026 | Stage 2 Beavertail; partially known |
| W4 | `TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF` | 23 | Nov 2025 – May 2026 | **NEW — not documented** |
| W5 | `TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH` | 3 | Nov 2025 – Feb 2026 | **NEW — not documented** |

### W4 — `TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF`

Funded Nov 13, 2025 (50 TRX from W3/W4/W5 funder). 23 dead-drop TXs total.

Activity timeline:
- **Nov 14, 2025**: First two dead-drop TXs (day after funding)
- **Dec 17, 2025**: Single TX
- **Feb 10–12, 2026**: 4 TXs (ramping up)
- **Feb 25, 2026**: 10 TXs in a single session (13:00–21:00 UTC) — **coincides with W3 key rotation event**
- **Mar 10, 2026**: 1 TX
- **Mar 26, 2026**: 1 TX (same date as W1 and W2 TXs)
- **May 19, 2026**: 1 TX (last known)

Additionally: W4 sent **15 TRX to W1** on 2026-03-26 (`to=41803f5d...`) — replenishing W1's TRX
balance for dead-drop TX fees. This cross-wallet operational TRX supply confirms W4 is managed
by the same actor who controls W1.

**The Feb 25 batch (10 TXs)** is highly significant: this is the date of the W3 XOR key rotation
(`cA]2!+37v,-szeU}` → `2[gWfGj;<:-93Z^C`, documented in Task X). W4's 10-TX spike on the same
day suggests W4 was also pushing a new payload to its subscriber base simultaneously.

BSC payloads from all W4 TXs are unavailable — all nodes returned null (pruned from BSC archive).
W4's cipher variant and XOR key are unknown. This is a gap for future investigation (see Task AT).

### W5 — `TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH`

Funded Nov 13, 2025 (50 TRX from W3/W4/W5 funder). Only 3 dead-drop TXs:
- 2025-11-19
- 2026-02-12
- 2026-02-27

W5 appears to be a low-usage or test channel. It may have been provisioned for a third Stage 1
variant that was never widely deployed, or it is a backup channel with a very small victim pool.

---

## Cash-Out Pathway

W1 sent 70 TRX to `TGg8q6dWKSNbCszZk6egLR8t8teZ411gkh` on **2025-06-10** — the same day W1
first went live (its earliest dead-drop TX is Jun 13, suggesting this 70 TRX was operational
seed capital).

`TGg8q6dWKSNbCszZk6egLR8t8teZ411gkh` (created Jun 10, 2025):
- Balance: 10.84 TRX + 4.29 USDT (TRC-20)
- Performed multiple `TriggerSmartContract` TXs (Jun 10) = DEX swaps (JustSwap / SunSwap)
- Recurring TRX transfers with `TTQydud22nZZGQy9Gnebs2168g6wukB4eC` (trading partner)
- The TRC-20 USDT balance (`TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` = USDT contract) confirms
  the hub converted actor-held TRX to USDT for exfil/cashout

```
W1 (70 TRX) → TGg8q6d... → DEX swap → USDT → TTQydud... (trading partner)
```

---

## TRC-10 Custom Token Cluster

Multiple operator-linked wallets hold TRC-10 tokens in the ID range `1005022–1005141`.
These are custom tokens issued on the TRON network:

| Token ID | Held by | Balance (units) |
|----------|---------|-----------------|
| 1005026 | W3/W4/W5 funder | 8,888,880,000 |
| 1005027 | W3/W4/W5 funder + Operator Master | 8,888,880,000 |
| 1005041 | W3/W4/W5 funder | 10,000 |
| 1005050 | Operator Master | 10,000 |
| 1005122 | W2 TRC-10 sender (`TPg56mPQ...`) | 4,999,940,600,000 |
| 1005141 | W2 TRC-10 sender | 1,049,795,330,000 |

The `8888` denomination (8,888 with implied decimal places) recurs across multiple transfers:
W3 received 8,888 on May 19 and Jun 3 2026. The number 8888 is auspicious in Korean/Chinese
numerology — potentially a cultural marker for the North Korean actor.

These tokens are sent between operator wallets in small batches and have no public market
listing. They function as an internal accounting or coordination mechanism across the operator
cluster.

---

## Wallet Cluster Graph

```
Operator Master (Oct 2024)     W3/W4/W5 Funder (Nov 2024)
 TQdwohPCWqq...                 TGJ1YJJNkFY...
  |                               |
  ├→ W1 (Jun 2025) ─────────────────────────────┐
  ├→ W2 (Jun 2025)               ├→ W3 (Nov 2025) [Stage 2 dead-drop]
  └→ TLmj13VL... (Jun 2025) ←───├→ W4 (Nov 2025) [Stage 1 dead-drop?] ─→ W1 (fee refill)
                                 └→ W5 (Nov 2025) [low-use channel]

W1 ──70 TRX──→ TGg8q6d... (cash-out hub) ──DEX──→ USDT ──→ TTQydud... (trading partner)
```

---

## IOCs

| Type | Value |
|------|-------|
| Operator Master | `TQdwohPCWqqfCUaCispyV1NaUZ1HgiJPUy` (TRON, created Oct 28, 2024) |
| W3/W4/W5 Funder | `TGJ1YJJNkFYLZKU4ZGqJfS6dU2cvGac7pS` (TRON, created Nov 2, 2024) |
| W4 dead-drop | `TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF` (TRON, Nov 2025 – May 2026) |
| W5 dead-drop | `TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH` (TRON, Nov 2025 – Feb 2026) |
| Cash-out hub | `TGg8q6dWKSNbCszZk6egLR8t8teZ411gkh` (TRON, Jun 2025) |
| DEX trading partner | `TTQydud22nZZGQy9Gnebs2168g6wukB4eC` (TRON) |
| Operational wallet | `TLmj13VL4p6NQ7jpxz8d9uYY6FUKCYatSe` (TRON, Jun 12 2025, 40 TRX) |
| TRC-10 tokens | IDs 1005026, 1005027, 1005041, 1005050, 1005122, 1005141 |

---

## Assessment

**The wallet cluster is a 5-dead-drop operation controlled by 2 funding wallets**, both created
in the same 5-day window (Oct 28 – Nov 2, 2024) — 8 months before W1/W2 went live. The actor
prepared the full infrastructure cluster before starting the campaign.

**W4 is the most significant new finding.** 23 dead-drop TXs over 6 months suggests a
meaningful victim pool using W4 as their Stage 1 source. The Feb 25 spike (10 TXs = key rotation
event) indicates W4 deploys updates in sync with W1/W2/W3, implying it is managed from the same
control plane. W4's cipher variant is unknown — BSC payloads are pruned. This is the highest
priority gap.

**W5 is likely a test or low-deployment channel.** 3 TXs over 4 months is minimal compared to
W4's 23. It may have been provisioned for a sub-variant that was abandoned.

**Cash-out is via DEX (TRX→USDT)**, not direct exchange deposit. This adds one hop of
obfuscation before fiat conversion. The USDT trading partner `TTQydud...` is not immediately
identifiable as a known exchange, suggesting either a P2P exchange or a further intermediate.

**Task AT recommended**: Enumerate all wallets funded by Operator Master and W3/W4/W5 Funder
to find any additional dead-drop wallets not yet identified. The funding graphs are shallow
enough (13 total outgoing TXs from W3 funder, ~50 from op master) to enumerate fully.
