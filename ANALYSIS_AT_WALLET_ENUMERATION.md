# Task AT: Complete Control Wallet Enumeration

## Objective

Enumerate all wallets funded by the two operator infrastructure wallets (Operator Master and
W3/W4/W5 Funder) to find any undiscovered dead-drop wallets (W6+). Also attempt to recover
W4's XOR cipher by fetching its BSC dead-drop payloads.

---

## Methodology

For each outgoing TX from both operator wallets, convert the recipient hex address to base58,
query TRON Grid API with `only_from=true`, and classify the wallet:

- **DEAD-DROP**: all outgoing TXs send 1 sun to `41000...0` (null address) with BSC TX hash in memo
- **MIXED**: some dead-drop + some other
- **NOT-DD / EMPTY**: non-dead-drop or no outgoing TXs (receiver-only, DEX, P2P exchange)

---

## Operator Master — `TQdwohPCWqqfCUaCispyV1NaUZ1HgiJPUy`

All outgoing recipients checked:

| Recipient | Amount | Date | Classification |
|-----------|--------|------|----------------|
| `TMfKQEd7...` (W1) | 100 TRX | 2025-06-06 | **DEAD-DROP** ✓ |
| `TXfxHUet...` (W2) | 10 TRX | 2025-06-13 | **DEAD-DROP** ✓ |
| `TLmj13VL...` | 10–20 TRX × 4 | Jun 2025 | EMPTY (receiver-only) |
| `TPDBqDKA...` | 100 TRX | 2026-03-09 | EMPTY (receiver-only) |
| `TYUJ8XWG...` | 80 TRX | 2024-12-27 | EMPTY (receiver-only) |
| `TFxcpVEY...` | 100 TRX | 2024-11-19 | EMPTY (receiver-only) |
| `TXhMYPCQ...` | 250 TRX | 2024-11-19 | EMPTY (receiver-only) |
| `TPayment5v6...` | 2.04 TRX | 2025-05-01 | NOT-DD (P2P exchange) |
| `TPaymentz2F...` | 2.04 TRX | 2025-05-01 | NOT-DD (P2P exchange) |
| `TPaymentk Ti...` | 2.04 TRX | 2025-05-01 | NOT-DD (P2P exchange) |

**Result: W1 and W2 are the only dead-drop wallets funded by Operator Master. No W6+.**

The large non-dead-drop recipients (250/100/80 TRX, Nov–Dec 2024) are receiver-only — they
accepted TRX but never sent anything out. These are likely exchange deposit addresses or
trusted counterparty wallets used before the campaign launched.

The `TPayment*` addresses (created Mar 2024, 340–490 TRX balance + USDT) are P2P OTC exchange
service wallets. The actor paid them 2.04 TRX each in May 2025 — likely energy/bandwidth
rental fees for the TRON network.

---

## W3/W4/W5 Funder — `TGJ1YJJNkFYLZKU4ZGqJfS6dU2cvGac7pS`

All outgoing recipients checked:

| Recipient | Amount | Date | Classification |
|-----------|--------|------|----------------|
| `TA48dct6...` (W3) | 50 TRX + 100 TRX | Nov 2025, Mar 2026 | **DEAD-DROP** ✓ |
| `TCqf6Zka...` (W4) | 50 TRX | 2025-11-13 | **DEAD-DROP** ✓ |
| `TFMryB9m...` (W5) | 50 TRX | 2025-11-13 | **DEAD-DROP** ✓ |
| `TLmj13VL...` | 50 TRX | 2025-10-30 | EMPTY (receiver-only) |
| `TJWkatg8...` | 7 TRX | 2025-11-17 | EMPTY (receiver-only) |
| `TUnui18w...` | 10 TRX | 2025-10-03 | NOT-DD (P2P, sent back 10.98 TRX same day) |
| `TNWEkue6...` | 101 TRX | 2025-05-08 | EMPTY (receiver-only) |
| `TDNA5Ghr...` | 50 TRX | 2025-04-14 | EMPTY (receiver-only) |

**Result: W3, W4, W5 are the only dead-drop wallets funded by W3/W4/W5 Funder. No W6+.**

`TLmj13VL4p6NQ7jpxz8d9uYY6FUKCYatSe` (created Jun 12, 2025; 40 TRX balance) receives TRX
from both the Operator Master and the W3/W4/W5 Funder — the only wallet funded by both. Its
role is unclear: no outgoing TXs visible via TRON API. It may be a second-tier operational
wallet not yet activated, or an intermediary for TRC-10 token operations.

---

## Operator Cluster Funding Chain

Tracing WHERE the two operator wallets receive their TRX from:

### W3/W4/W5 Funder Inflows

| Date | From | Amount | Source type |
|------|------|--------|-------------|
| 2024-11-02 | `TWDw3oWRhX3BXgFkvnBSgioKtpJ6pJoBqn` | 55 TRX | Initial funding |
| 2024-11-28 | `412f6eb6...` | 169 TRX | Large inflow |
| 2025-04-11 | `41af52d1...` | 152 TRX | Large inflow |
| 2025-07-14 | `TQSrBJjbzgTPKWQp49JtN84rxdiDTww8Za` | 542 TRX | **Largest single inflow** |
| 2025-07-14 | `TMthe9mu2x6RM7j8D3aPug9TCSuEXFSMA6` | 24 TRX | Same session |

The 542 TRX sender (`TQSrBJjbzgTPKWQp49JtN84rxdiDTww8Za`) sent this amount 4 months before
W3/W4/W5 were activated (Nov 2025) — likely an operational capital reserve. Multiple smaller
senders (1–10 TRX) in the same session are consistent with TRON energy rental (staked TRX
lent to cover TX fees).

**Pattern**: Large-value inflows (50–542 TRX) from distinct addresses on each session, each
with multiple small accompanying TXs (1–10 TRX from 3–7 different addresses). This is the
standard TRON P2P OTC exchange pattern: buyer pays, multiple energy providers cover fees.

No actor-controlled "upstream" wallet found — the operator cluster receives TRX from what
appears to be multiple independent P2P OTC market sellers.

### TRC-10 Token Initialization (Nov 5, 2024)

Three sources sent custom TRC-10 tokens to the W3/W4/W5 Funder on Nov 5 2024 (3 days after wallet creation):

| From | Token ID | Amount |
|------|----------|--------|
| `TETtEjAoVnfgqKqJxAHpFbVcWduujrZWjJ` | (same as 1005026) | 8,888,880,000 |
| `TWqWMsHFX3tFbvvcLG3bL5LoCfWMnwXwdt` | (same as 1005027) | 8,888,880,000 |
| `TMZC3XytUdnpemMZ8Mt3xQLDpGkzLs9KM2` | (same as 1005041) | 10,000 |

These three wallets are the token creation/distribution sources. The `8888` denominator is
consistent across all TRC-10 token transfers in the actor cluster (W3 received 8888 from two
senders in May/Jun 2026). These custom tokens may serve as internal "campaign tokens" or
operational markers passed between actor wallets.

---

## W4 Cipher — Not Recoverable

Attempted W4 BSC TX fetch via:
- Multiple BSC full-node RPC endpoints (bsc-dataseed.binance.org, bsc-rpc.publicnode.com, bsc.meowrpc.com, rpc.ankr.com/bsc)
- BSCScan API (eth_getTransactionByHash)

All W4 dead-drop BSC TXs (Nov 2025 – May 2026) return null — pruned from all available nodes.
BSCScan API requires authentication for this endpoint.

**W4 cipher is unknown.** BSC archive access (Quicknode, Alchemy, or Chainstack full-archive node)
would be required to retrieve W4 payloads. Given W4 was active through the Feb 25 2026 key rotation
event (10 TXs that day, matching W1/W2/W3 rotation activity), W4 likely uses the same W1 XOR key
`2[gWfGj;<:-93Z^C` deployed post-rotation, but this is unconfirmed.

---

## Complete Wallet Map

```
                     ┌─── TRC-10 token senders (Nov 2024) ──┐
                     │                                        │
            Operator Master         W3/W4/W5 Funder
          TQdwohPCWqq... (Oct 28)  TGJ1YJJNkFY... (Nov 2)
               │                        │
          ┌────┤                    ┌───┼────┬──────┐
          │    └── TLmj13VL ────────┘   │    │      │
          │         (shared ops)        │    │      │
          ▼                             ▼    ▼      ▼
    W1 dead-drop              W3 dead-drop  W4    W5
  TMfKQEd7... (W1)           TA48dct6...   TCqf  TFMr
          │                             (Stage 2)  (23 TXs, NEW)  (3 TXs, NEW)
          ▼
   Cash-out hub
  TGg8q6d... → DEX (TRX→USDT) → TTQydud... (trading partner)

  W2 dead-drop: TXfxHUet...  [funded separately by Operator Master]
  W4 → W1 (15 TRX fee replenishment, Mar 2026)
```

---

## Final Wallet Inventory

| Wallet | Address | Role | TXs | Cipher |
|--------|---------|------|-----|--------|
| Operator Master | `TQdwohPCWqqfCUaCispyV1NaUZ1HgiJPUy` | Infrastructure funding | — | — |
| W3/W4/W5 Funder | `TGJ1YJJNkFYLZKU4ZGqJfS6dU2cvGac7pS` | Infrastructure funding | — | — |
| W1 | `TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP` | Stage 1 dead-drop | 21 | `2[gWfGj;<:-93Z^C` (known) |
| W2 | `TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG` | Stage 1 dead-drop | 9 | `m6:tTh^D)cBz?NM]` (known) |
| W3 | `TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v` | Stage 2 dead-drop | 69+ | `2[gWfGj;<:-93Z^C` (known) |
| W4 | `TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF` | Unknown dead-drop channel | 23 | **Unknown** |
| W5 | `TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH` | Unknown dead-drop channel | 3 | **Unknown** |
| Cash-out hub | `TGg8q6dWKSNbCszZk6egLR8t8teZ411gkh` | TRX→USDT conversion | — | — |
| TLmj13VL | `TLmj13VL4p6NQ7jpxz8d9uYY6FUKCYatSe` | Shared ops (unfunded) | 0 | — |

**Total dead-drop wallets: 5 (W1–W5). No W6+ found.**

---

## Assessment

**The actor runs a 5-wallet dead-drop cluster. Enumeration is complete.**

No additional dead-drop wallets were found among any recipient of either operator funding
wallet. The cluster boundary is W1–W5, with W4 and W5 having unknown ciphers/XOR keys.

**W4 is the most significant gap.** 23 TXs over 6 months, including 10 during the Feb 25 key
rotation event, indicates a non-trivial victim pool using W4 as their Stage 1 source. These
victims are currently unreachable — their infected repos aren't detectable via GitHub code search
(BSC payloads don't appear in repo files), and their campaign IDs are unknown.

**W4/W5 cipher recovery requires a BSC full-archive node.** All public RPC endpoints have
pruned the relevant transactions. Quicknode or Alchemy archive node API would retrieve them.

**The operator cluster is funded from TRON P2P OTC markets**, not a higher-level actor wallet.
The funding trail ends at P2P exchange sellers. No upstream operator wallet exists in on-chain
data — either the actor converts fiat/other crypto at an exchange and sends TRX to P2P sellers,
or the P2P OTC is the terminal point.
