# Task O: `_$_1e42` 2509/1358 Cluster — C2 Mapping

**Date:** 2026-06-27  
**Task:** Decode Stage 2 from `_$_1e42` activation 2509 / return 1358 cluster  
**Source:** `saif72437/medium-clone/tailwind.config.js` (live sample)

---

## Summary

The `_$_1e42` 2509/1358 cluster uses **identical C2 infrastructure** to every other
PolinRider wave documented in this investigation. Same TRON wallets, same Aptos fallbacks,
same BSC endpoints, same XOR campaign keys, same `?.?` payload separator — confirmed across
Jan 2026 (`_$_1e42` 1632/2952), Mar-Apr 2026 (`Cot%3t=shtP` 5471/3456), and now the bat-file
cluster (`_$_1e42` 2509/1358). Six months of continuous operation on a single C2 backend.

---

## Decoding Chain

The payload has a **two-layer structure**: an outer Stage 0 IIFE and an inner atob-encoded layer.

```
tailwind.config.js line 9:
  global['!'] = '8-765'                    ← Stage 0: set campaign routing key
  var _$_1e42 = (fn)(enc, seed)             ← outer cipher (placeholder / YARA target)
  eval(atob('BASE64'))                      ← decode inner layer (4,781 bytes)

  atob-decoded inner layer:
    global['!'] = '11-#'                   ← override campaign key (Stage 2 reads this)
    var _$_1e42 = (fn)("rmcej%otb%", 2857687)   ← mini-cipher (3-entry table for keys)
    global[_$_1e42[0]] = require            ← store require in global key
    (function(){
      var LQI='', TUU=11
      function sfL(w){                      ← Stage 2 bootstrap cipher
        seed=2667686, off1=228, mod1=50332
        off2=128, mod2=52119, modulus=4289487
      }
      var EKc = sfL('wuqktamce...').substr(0,11)  → 'constructor'
      var joW = '...890-char encoded decompressor...'
      var dgC = sfL[EKc]                    ← Function constructor
      var xBg = dgC('', sfL(joW))          ← build decompressor fn
      var pYd = xBg(sfL('o B%v[...2824-char stage2_enc...'))
                                            ← decompress → Stage 2 body (3,858 chars)
      var Tgw = Function('', pYd)
      Tgw(2509); return 1358               ← run Stage 2
    })()
```

**Stage 2 cipher** (`_$af163278`): seed=**1812138**, off1=139, mod1=20044, off2=473,
mod2=41543, modulus=5446973. Distinct parameters from all other documented cipher instances.

---

## Stage 2 String Table — `_$_ccfc` Decoded

58-entry string table from `_$af163278("be_Vo%0l81ldJ1%...", 1812138)`:

```
[0]:  "r"                               ← global key for require()
[1]:  "_V"                              ← campaign ID global key
[2]:  "A"                               ← campaign ID prefix
[3]:  "!"                               ← old global key (Stage 0 set this)
[4]:  "end"
[5]:  "error"
[6]:  "on"
[7]:  ""
[8]:  "data"
[9]:  "parse"
[10]: "JSON"
[11]: "get"
[12]: "https"
[13]: "Promise"
[14]: "2.0"
[15]: "stringify"
[16]: "POST"
[17]: "request"
[18]: "write"
[19]: "join"
[20]: "reverse"
[21]: "split"
[22]: "utf8"
[23]: "toString"
[24]: "raw_data"
[25]: "/transactions?only_confirmed=true&only_from=true&limit=1"
[26]: "hex"
[27]: "from"
[28]: "Buffer"
[29]: "arguments"
[30]: "payload"
[31]: "/transactions?limit=1"
[32]: "?.?"                             ← BSC payload separator IOC
[33]: "substring"
[34]: "input"
[35]: "result"
[36]: "eth_getTransactionByHash"        ← BSC RPC method
[37]: "bsc-dataseed.binance.org"        ← BSC RPC primary
[38]: "bsc-rpc.publicnode.com"          ← BSC RPC fallback
[39]: "length"
[40]: "charCodeAt"
[41]: "fromCharCode"
[42]: "String"
[43]: "getTime"                         ← new: timestamp tracking
[44]: "Date"                            ← new: Date object
[45]: "_p_t"                            ← new: global['_p_t'] = infection timestamp
[46]: "2[gWfGj;<:-93Z^C"               ← Campaign XOR key 1 (W1 channel)
[47]: "TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP"   ← TRON wallet W1
[48]: "0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e"  ← Aptos 1
[49]: "m6:tTh^D)cBz?NM]"               ← Campaign XOR key 2 (W2 channel)
[50]: "TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG"   ← TRON wallet W2
[51]: "0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3"  ← Aptos 2
[52]: "node"
[53]: "-e"
[54]: "';"
[55]: "ignore"
[56]: "spawn"
[57]: "child_process"
```

---

## Cross-Wave Infrastructure Comparison — Complete

All confirmed Stage 2 string tables now decoded:

| Field | `_$_1e42` 2509/1358 | `Cot%3t=shtP` 5471/3456 | `_$_b229` Jun 2026 |
|-------|---------------------|--------------------------|---------------------|
| W1 TRON | `TMfKQEd7...` ✓ | `TMfKQEd7...` ✓ | `TMfKQEd7...` ✓ |
| W2 TRON | `TXfxHUet...` ✓ | `TXfxHUet...` ✓ | `TXfxHUet...` ✓ |
| Aptos 1 | `0xbe037400...` ✓ | `0xbe037400...` ✓ | `0xbe037400...` ✓ |
| Aptos 2 | `0x3f0e5781...` ✓ | `0x3f0e5781...` ✓ | `0x3f0e5781...` ✓ |
| BSC primary | bsc-dataseed.binance.org | bsc-dataseed.binance.org | bsc-dataseed.binance.org |
| BSC fallback | bsc-rpc.publicnode.com | bsc-rpc.publicnode.com | bsc-rpc.publicnode.com |
| Separator | `?.?` | `?.?` | `?.?` |
| XOR key 1 | `2[gWfGj;<:-93Z^C` | `2[gWfGj;<:-93Z^C` | `2[gWfGj;<:-93Z^C` |
| XOR key 2 | `m6:tTh^D)cBz?NM]` | `m6:tTh^D)cBz?NM]` | `m6:tTh^D)cBz?NM]` |
| require key | `global['r']` | `global['r']` | `global['r']` |
| campaign ID key | `global['_V']` | `global['_V']` | `global['_V']` |

**Every single field is identical.** A single C2 backend has operated without change across
at least 6 months of PolinRider activity (January 2026 through June 2026).

---

## Campaign ID Architecture — Clarified

The two-layer payload reveals how campaign IDs propagate through the execution chain:

```
Stage 0 (tailwind.config.js):
  global['!'] = '8-765'          ← raw victim ID set by Stage 0

Stage 2 reads it and sets:
  global['_V'] = "A" + global['!']
             = "A" + "8-765"
             = "A8-765"          ← campaign ID used for C2 routing

Stage 2 also sets:
  global['_p_t'] = new Date().getTime()   ← infection timestamp (new in this cluster)
```

The `"A"` prefix added by Stage 2 distinguishes this from the newer `_$_b229` era format
(`"5-3-161"`). The `_$_1e42` 2509/1358 batch uses `"A8-765"` format, suggesting `8` is the
batch number and `765` is the victim sequence number within that batch.

The inner atob layer sets `global['!'] = '11-#'` BEFORE running Stage 2 — Stage 2 reads
`global['!']` = `'11-#'` and sets `global['_V'] = "A11-#"`. The `#` character suggests this
is a template placeholder that normally gets filled with a victim number at injection time;
in this sample it was left as `#`.

**Infection timestamp tracking** (`global['_p_t']`): the `_$_1e42` 2509/1358 Stage 2
records `new Date().getTime()` at execution. This was NOT present in the Cot wave's Stage 2
(53 entries vs 58). The actor added infection-time tracking between the Cot wave and this
cluster — possibly to deduplicate re-infections or to time-gate payloads.

---

## New Cipher Registry Entry

| Wave | Stage 2 Cipher | Seed | off1 | mod1 | off2 | mod2 | Modulus |
|------|----------------|------|------|------|------|------|---------|
| Cot%3t=shtP | `_$af402005` | 1111436 | 119 | 13553 | 615 | 37182 | 3896884 |
| `_$_1e42` 2509/1358 | `_$af163278` | **1812138** | 139 | 20044 | 473 | 41543 | 5446973 |

These are DIFFERENT cipher instances with the same structural pattern — each deployment wave
uses a freshly-generated cipher with unique parameters.

---

## Updated Complete Cipher Registry

| Stage | Cipher/var | Act | Ret | Wave | Seed |
|-------|-----------|-----|-----|------|------|
| Stage 0 | `_$_1e42` (jFD/LQI) | 1632 | 2952 | Earliest | (not decoded) |
| Stage 0 | `_$_1e42` (jFD/LQI) | **2509** | **1358** | Bat-file cluster | sfL seed 2667686 |
| Stage 0 | `Cot%3t=shtP` (MDy) | 5471 | 3456 | Mar–Apr 2026 | MDy seed 1111436 |
| Stage 0 | `_$_913e` | ? | ? | May 2026 | (not decoded) |
| Stage 0 | `_$_b229` | 1632 | 2952 | Jun 2026 | (decoded in prior tasks) |
| Stage 0 | `_$_4445` | ? | ? | Jun 26 2026 | (not decoded) |
| Stage 1 | `NVu` (inner) | 9608 | 2776 | W1 Jun 23 | (decoded in Task A) |
| Stage 1 | `Wrm` (inner) | 8063 | 8223 | W2 Jun 20 | (decoded in prior tasks) |
| Stage 2 | `_$af163278` | — | — | `_$_1e42` 2509/1358 | **1812138** |
| Stage 2 | `_$af402005` | — | — | `Cot%3t=shtP` | 1111436 |

---

## IOCs (new from Task O)

```
# Stage 2 cipher (_$_1e42 bat-file cluster)
Cipher: _$af163278
Seed: 1812138
Offsets: 139 / 473
Mods: 20044 / 41543
Modulus: 5446973

# Campaign ID format (_$_1e42 era)
global['!'] = '{N}-{NNN}'   (e.g. '8-765', set by Stage 0)
global['_V'] = 'A' + global['!']   (e.g. 'A8-765', set by Stage 2)

# Infection timestamp (new in _$_1e42 2509/1358 cluster)
global['_p_t'] = new Date().getTime()

# Confirmed: all waves share these (final confirmation)
TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP   (TRON W1, all waves)
TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG   (TRON W2, all waves)
0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e  (Aptos 1, all waves)
0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3  (Aptos 2, all waves)
"2[gWfGj;<:-93Z^C"   (XOR key W1 channel, all waves)
"m6:tTh^D)cBz?NM]"  (XOR key W2 channel, all waves)
"?.?"                (BSC payload separator, all waves)
bsc-dataseed.binance.org   (BSC RPC, all waves)
bsc-rpc.publicnode.com     (BSC RPC fallback, all waves)
```
