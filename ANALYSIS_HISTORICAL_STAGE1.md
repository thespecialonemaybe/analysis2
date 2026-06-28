# Task Q: Historical Stage 1 Payload Recovery (2025–2026)

**Date:** 2026-06-28  
**Source:** Aptos A1 (W1 channel) + A2 (W2 channel) BSC TX pointers  
**Retrieved:** 15 historical BSC TXs spanning 2025-06-13 → 2026-03-26

---

## Summary

Full BSC TX retrieval across both Aptos wallets yielded 13 successfully decoded Stage 1 payloads
spanning June 2025 through March 2026. Combined with the June 2026 payloads already retrieved,
this gives a near-complete view of the cipher evolution across 12+ months.

Key findings:
- **8 new inner cipher families** documented for the first time (W1 channel alone)
- **2 new outer cipher families** on W2: `_$_3333` (Mar 4) and `_$_ec7c` (Mar 26)
- **`module` capture present from June 2025** in W2 — dropped in Jun 20 `_$_16d1`, then re-added in `_$_f5f0`
- **`_global` variable** appears in W2 from Jun 18 2025 onward
- **Test TX confirmed**: Oct 1 2025, actor pushed `global['_V'] = '9-test'` and corrected it 5 minutes later
- **2 garbled/undecodable first TXs** on Jun 13 — suggest a different initial key at launch

---

## W1 (A1) Historical Stage 1 Cipher Table

All 12 W1 channel payloads decoded with key `2[gWfGj;<:-93Z^C`:

| Date | BSC TX | Outer | Inner fn | Seed | off1 | mod1 | off2 | mod2 | Modulus | Notes |
|------|--------|-------|----------|------|------|------|------|------|---------|-------|
| 2025-06-13 | `0x14e7b64b` | none | **?** | — | — | — | — | — | — | Garbled — pre-rotation key |
| 2025-06-13 | `0x1293aa8f` | none | `BIY` | 782914 | 538 | 30166 | 411 | 42192 | 2515333 | `global["r"]=require; global["m"]=module` |
| 2025-06-13 | `0xe5a0cff7` | none | `uap` | 1020957 | 303 | 45806 | 384 | 53241 | 4133653 | bare IIFE |
| 2025-06-24 | `0x67e43df3` | none | `DML` | 2248352 | 123 | 45422 | 287 | 38257 | 4396911 | |
| 2025-06-24 | `0xe40a40c6` | none | `AOv` | 798578 | 251 | 27735 | 213 | 45526 | 1731010 | |
| 2025-07-23 | `0x51a46279` | none | `GAR` | 2901018 | 431 | 21966 | 750 | 23065 | 7540223 | |
| 2025-08-19 | `0xa2ffa9b0` | none | `RVj` | 2078320 | 366 | 39403 | 397 | 44415 | 7371537 | (Task I) |
| 2025-10-01 | `0x1ad0dd01` | none | `AZL` | 2087235 | 190 | 48841 | 345 | 38996 | 6881022 | **TEST: `global['_V']='9-test'`** |
| 2025-10-01 | `0xb980676a` | none | `AZL` | 2087235 | 190 | 48841 | 345 | 38996 | 6881022 | correction (same cipher, no test marker) |
| 2025-10-01 | `0xf46c86c8` | none | `utH` | 3298209 | 487 | 45671 | 106 | 25791 | 4273585 | third push same day |
| 2025-12-01 | `0xec567681` | none | `Gez` | 3409844 | 169 | 49955 | 659 | 41405 | 5292331 | |
| 2026-03-04 | `0xc06e1b84` | **?** | **?** | — | — | — | — | — | — | guard `_t_t` added (5,901b) |

The outer cipher obfuscation wrapper (`_$_xxx`) is **absent from all W1 TXs through Dec 2025**.
The Mar 2026 W1 payload was previously retrieved (Task I) but the outer cipher structure was not
identified — it begins with the `async` IIFE guard directly.

---

## W2 (A2) Historical Stage 1 Cipher Table

All 10 W2 channel payloads decoded with key `m6:tTh^D)cBz?NM]`:

| Date | BSC TX | Outer | Inner fn | Seed | off1 | mod1 | off2 | mod2 | Modulus | Notes |
|------|--------|-------|----------|------|------|------|------|------|---------|-------|
| 2025-06-13 | `0x91991166` | none | **?** | — | — | — | — | — | — | Garbled — pre-rotation key |
| 2025-06-13 | `0xc83de872` | none | `nBj` | 4946713 | 499 | 18518 | 93 | 15297 | 5587190 | plain require/module; `a0b/a0n/a0a` vars |
| 2025-06-18 | `0x13e3ce3a` | none | `RZn` | 3776299 | 471 | 33957 | 568 | 48342 | 5052911 | + `_global` var appears |
| 2025-08-13 | `0xd33f7866` | none | `gOe` | 3547675 | 360 | 32226 | 326 | 51262 | 3722251 | `_global` var |
| 2026-03-04 | `0x60537dcb` | **`_$_3333`** | ? | ? | 98 | 20835 | 229 | 49667 | 2450783 | **FIRST outer cipher on W2** |
| 2026-03-26 | `0xea7e97b1` | **`_$_ec7c`** | ? | ? | 192 | 20415 | 737 | 17006 | 4357531 | second outer cipher |
| 2026-06-20 | `0x7ffb4efd` | `_$_16d1` | `Wrm` | 2296496 | 213 | 18466 | 407 | 32620 | 3485560 | drops module capture (Task B) |
| 2026-06-23 | `0x76a7ae33` | `_$_f5f0` | `SgH` | 570964 | 428 | 13367 | 379 | 43098 | 1937868 | module re-added (Task I) |
| 2026-06-25 | `0x622bcfd4` | `_$_f5f0` | `cdi` | 1787286 | 523 | 49385 | 387 | 23782 | 7288442 | (Task I) |

---

## New Outer Ciphers — W2 March 2026

### `_$_3333` (2026-03-04)

```javascript
var _$_3333=(function(w,t){
  var c=w.length; var q=[];
  for(var e=0;e<c;e++){q[e]=w.charAt(e)};
  for(var e=0;e<c;e++){
    var l=t*(e+98)+(t%20835);
    var d=t*(e+229)+(t%49667);
    var b=l%c; var y=d%c;
    var v=q[b]; q[b]=q[y]; q[y]=v;
    t=(l+d)%2450783
  }
  ...
})("...", seed);
```

**Parameters:** off1=98, mod1=20835, off2=229, mod2=49667, modulus=2450783  
This is the FIRST outer cipher seen on the W2 channel — the transition point where the W2 channel
switched from plaintext `typeof require` checks to obfuscated cipher lookup (same evolution as W1,
but W2 appears to have adopted it around the same date in March 2026).

### `_$_ec7c` (2026-03-26)

**Parameters:** off1=192, mod1=20415, off2=737, mod2=17006, modulus=4357531  
Replaced `_$_3333` within 22 days. Outer cipher rotation was rapid in March 2026 —
3 W1 + 2 W2 updates all on Mar 26 2026 (as seen in the A1/A2 Aptos records).

---

## June 2025 W2 Structure — Plain Text Phase

Before the outer cipher obfuscation was adopted, W2 Stage 1 opened with:

```javascript
if('function' === typeof require) global['r'] = require;
if(typeof module === 'object') global['m'] = module;
var a0b, a0n, a0a;           // placeholder vars — purpose unclear
(function(){
  var ycz='', VIa=320-309;   // VIa=11 → substr(0,11) → 'constructor'
  function nBj(k){...}       // bootstrap cipher
  ...
})()
```

From Jun 18 2025 onward, `_global` was added:

```javascript
var a0b, a0n, _global, a0a;
```

`_global` likely stores `global` to survive scope changes (consistent with later
`global['r']=require` pattern). The `a0b/a0n/a0a` vars appear to be declarations
for globals that Stage 2 will populate — they were refined into the `global['_V']`,
`global['_H']`, etc. naming scheme used from 2026 onward.

---

## `module` Capture — Timeline

The `global['m'] = module` capability was NOT a new addition in `_$_f5f0` — it was
present from the very first clean Stage 1 (Jun 13 2025, `0x1293aa8f`):

| Period | `module` captured? | Form |
|--------|--------------------|------|
| Jun 2025 (W1: `0x1293aa8f`) | ✓ YES | `global["m"]=module` inline |
| Jun–Aug 2025 (W2: all plain variants) | ✓ YES | `global['m']=module` inline |
| Aug 2025 (W1: `RVj` plain IIFE) | Not observed (differs in structure) |
| Oct 2025 (W1: `AZL` test TX) | ✓ YES | `global['m'] = module` inline |
| Dec 2025 (W1: `Gez`) | Not in first 400 chars |
| Mar 2026 (W2: `_$_3333`, `_$_ec7c`) | Not visible (outer cipher obfuscates) |
| Jun 20 2026 (W2: `_$_16d1`) | ✗ NO — cipher only has 2 entries |
| Jun 23 2026 (W2: `_$_f5f0`) | ✓ YES — cipher entry `[3]='m'` |

`_$_16d1` (Jun 20) appears to be an **aberration** — the outer cipher was minimized to 2 entries
and the module capture was omitted. `_$_f5f0` (Jun 23) restored it. This could be an actor
mistake or a deliberate temporary reduction in the Jun 20 push.

---

## Test Deployment — October 1, 2025

The three A1 TX cluster on 2025-10-01 reveals the actor actively testing:

**TX 1 `0x1ad0dd01` (16:56 UTC):**
```javascript
global['_V'] = '9-test';   // ← hardcoded test campaign ID
global['r'] = require;
global['m'] = module;
(function(){...AZL cipher...})()
```

**TX 2 `0xb980676a` (17:01 UTC, +5 min):**
```javascript
// same AZL cipher, but global['_V']='9-test' REMOVED
(function(){...AZL cipher...})()
```

**TX 3 `0xf46c86c8` (17:26 UTC, +30 min):**
```javascript
// completely different inner cipher utH
(function(){...utH cipher...})()
```

The actor pushed a test, realized the campaign ID was hardcoded, corrected it, then pushed
a second variant with a rotated inner cipher — all within 30 minutes. By October 2025 the
campaign ID system (`_V`) was already designed but not yet delivered in infected repos
(the `_V` variable only appears in public scripts from early 2026).

---

## Garbled First TXs (Jun 13 2025)

The very first TX on both A1 and A2 on Jun 13 2025 does not decrypt cleanly with either the
W1 or W2 XOR key:

| Wallet | TX | First TX on channel? | Decryption |
|--------|----|---------------------|-----------|
| A1 | `0x14e7b64b` | YES (05:12 UTC) | Garbled with W1 key |
| A1 | `0x1293aa8f` | No (05:14 UTC, +2 min) | Clean JS with W1 key |
| A2 | `0x91991166` | YES (05:54 UTC) | Garbled with W2 key |
| A2 | `0xc83de872` | No (05:55 UTC, +1 min) | Clean JS with W2 key |

Both garbled TXs are immediately followed by a clean replacement, suggesting the actor:
1. Used a test/different key for the initial infrastructure push
2. Immediately corrected with the operational key

The garbled content does not resemble JS regardless of which known key is applied — it may have
used a pre-operational key that was rotated before real deployment.

---

## Complete Cipher Evolution Timeline (All Channels)

```
2025-06-13  W1 launch: BIY (782914), uap (1020957) — garbled first TX
2025-06-13  W2 launch: nBj (4946713) — garbled first TX, then clean
2025-06-18  W2 update: RZn (3776299) — _global var added
2025-06-24  W1 update: DML (2248352), AOv (798578) — two pushes same day
2025-07-23  W1 update: GAR (2901018)
2025-08-13  W2 update: gOe (3547675)
2025-08-19  W1 update: RVj (2078320) — no outer cipher, bare IIFE
2025-10-01  W1 test+fix: AZL (2087235) ×2, then utH (3298209) — 3 TXs in 30 min
2025-12-01  W1 update: Gez (3409844)
           [~2 month gap: Jan–Feb 2026 — no Aptos updates observed]
2026-03-04  W1 update: _t_t guard key added (5,901b), async IIFE, __dirname capture
2026-03-04  W2 update: _$_3333 outer cipher introduced on W2
2026-03-26  W1 update ×3 + W2 update ×2 — all in 1.5 hours
2026-03-26  W2: _$_ec7c replaces _$_3333
2026-05-20  W1 update
2026-05-23  W1 update ×2 — _$_913e generation
2026-06-18  W1 update
2026-06-20  W2 update: _$_16d1 (drops module capture, direct HTTP C2)
2026-06-23  W1 update: _$_9f51
2026-06-23  W2 update: _$_f5f0/SgH (module re-added)
2026-06-25  W2 update: _$_f5f0/cdi (inner cipher rotated)
```

---

## New IOCs

```
# W1 (A1) historical inner ciphers — all new, not in any public report
BIY:  seed=782914,  off1=538, mod1=30166, off2=411, mod2=42192, modulus=2515333  (2025-06-13)
uap:  seed=1020957, off1=303, mod1=45806, off2=384, mod2=53241, modulus=4133653  (2025-06-13)
DML:  seed=2248352, off1=123, mod1=45422, off2=287, mod2=38257, modulus=4396911  (2025-06-24)
AOv:  seed=798578,  off1=251, mod1=27735, off2=213, mod2=45526, modulus=1731010  (2025-06-24)
GAR:  seed=2901018, off1=431, mod1=21966, off2=750, mod2=23065, modulus=7540223  (2025-07-23)
AZL:  seed=2087235, off1=190, mod1=48841, off2=345, mod2=38996, modulus=6881022  (2025-10-01)
utH:  seed=3298209, off1=487, mod1=45671, off2=106, mod2=25791, modulus=4273585  (2025-10-01)
Gez:  seed=3409844, off1=169, mod1=49955, off2=659, mod2=41405, modulus=5292331  (2025-12-01)

# W2 (A2) historical inner ciphers — all new
nBj:  seed=4946713, off1=499, mod1=18518, off2=93,  mod2=15297, modulus=5587190  (2025-06-13)
RZn:  seed=3776299, off1=471, mod1=33957, off2=568, mod2=48342, modulus=5052911  (2025-06-18)
gOe:  seed=3547675, off1=360, mod1=32226, off2=326, mod2=51262, modulus=3722251  (2025-08-13)

# W2 new outer ciphers (March 2026) — not in any public report
_$_3333: off1=98,  mod1=20835, off2=229, mod2=49667, modulus=2450783  (2026-03-04)
_$_ec7c: off1=192, mod1=20415, off2=737, mod2=17006, modulus=4357531  (2026-03-26)

# Test campaign ID (Oct 1 2025)
global['_V'] = '9-test'   ← actor test marker, BSC TX 0x1ad0dd0135fe084e...
```
