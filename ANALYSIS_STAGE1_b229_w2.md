# Stage 1 Analysis: Live W2 Payload (`_$_16d1` cipher)

**Retrieved:** 2026-06-27  
**BSC TX source:** `0x7ffb4efddd96e20aec90724be2ac9a71c138a9af697b9fb8224bbf80ea4f22be`  
**TRON wallet (W2):** `TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG` — updated 2026-06-20T13:37Z  
**XOR key (delivery):** `m6:tTh^D)cBz?NM]` (key2)  
**Payload size:** 3,524 chars (3,528 with `\r\n` line endings)  
**Public documentation status:** Zero GitHub results for `_$_16d1`

---

## Summary

The W2 Stage 1 is a significantly simpler payload than W1 Stage 1 (3,524 vs 5,849 chars). Its
`_$_16d1` cipher decodes only **2 strings** — a minimal bootstrap to set `global['r'] = require`.
All Stage 2 fetch logic is compressed inside the inner IIFE.

**W2 Stage 1 is an older, lighter version of the W1 Stage 1.** The W1 (deployed Jun 23) added
IP-based C2 routing, filesystem capture, source storage, and a secondary cipher blob — all absent
from W2 (deployed Jun 20). The actor is iteratively upgrading Stage 1 capability while keeping
both chains running in parallel.

---

## Cipher: `_$_16d1`

**Parameters:** offsets 488/538, mods 34187/48866, modulus 4728540, seed 1147810

**Encoded string (10 chars):** `"ou%trinncf"`  
**Decoded strings (2 entries):**

| Index | Value | Role |
|-------|-------|------|
| [0] | `'function'` | typeof check — `typeof require === 'function'` |
| [1] | `'r'` | global key — `global['r'] = require` |

**Usage:**
```javascript
var _$_16d1 = (function(k,a){
    // offsets 488/538, mods 34187/48866, modulus 4728540
})("ou%trinncf", 1147810);

if (typeof require === _$_16d1[0]) {   // if typeof require === 'function'
    global[_$_16d1[1]] = require       // global['r'] = require
}
```

This is the entirety of `_$_16d1`'s role. Unlike W1's `_$_9f51` (17-entry routing table with
C2 IPs, TRON wallets, and BSC TX hashes), W2's `_$_16d1` is a pure bootstrap shim — it only
makes `require` available globally so the inner IIFE can use it to load modules.

---

## Inner IIFE: `Wrm` Cipher (3-Layer, same pattern as W1/Stage 0)

The inner IIFE follows the same 3-layer structure as `_$_b229` Stage 0 and W1 Stage 1's
`NVu` cipher:

**`Wrm` cipher parameters:**
- Seed: `2296496`
- Offsets: `213` / `407`
- Mods: `18466` / `32620`
- Modulus: `3485560`

**Layer 1 — 'constructor' accessor:**
```javascript
var VkC = Wrm('hmrcqulkvtuatjoocswicsdynongpezfrtxbr').substr(0, 11);
// VkC = 'constructor'
var POz = Wrm[VkC];  // POz = Function
```

**Layer 2 — `Function` constructor via property:**
`Wrm['constructor']` accesses the built-in `Function` constructor through a decoded property name.
Avoids the literal string `"Function"` appearing in source.

**Layer 3 — Dynamic decompressor:**
```javascript
var uEC = POz(lMN, Wrm(ptU));     // Function("", decompressor_code)
var JfM = uEC(Wrm(':PfihP$...'));  // decoded Stage 2 fetch function  
var WEz = OTJ(WUG, JfM);          // compiled
WEz(8063);                         // execute with activation code 8063
return 8223;                       // sentinel
```

- Activation code: **8063** (W1 uses 9608; `_$_b229` Stage 0 uses 1632)
- Return sentinel: **8223** (W1 uses 2776; `_$_b229` Stage 0 uses 2952)

These per-stage constants are distinct across all three stages, suggesting they may serve as
anti-analysis sentinels or version identifiers.

---

## W2 vs W1 Stage 1 — Feature Comparison

| Feature | W2 Stage 1 (`_$_16d1`) | W1 Stage 1 (`_$_9f51`) |
|---------|------------------------|------------------------|
| **Cipher entry count** | **2 strings** | 17 strings |
| Payload size | 3,524 chars | 5,849 chars |
| Deployed | 2026-06-20 | 2026-06-23 |
| Guard key check | No | `global["_t_t"]` |
| `__dirname` capture | No | `global["___dirname"]` |
| `__filename` capture | No | `global["___filename"]` |
| Stage 1 source stored | No | `global["_t_c"]` |
| Secondary cipher blob | No | `global["_t_0"]` (`_$_96c7`) |
| Direct IP C2 routing | **No** | 3 IP pools |
| Stage 2 TRON wallet | Compressed inside `WEz` | `TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v` |
| Error reporting | No | `global._R` |
| Activation code | **8063** | 9608 |
| Return sentinel | **8223** | 2776 |
| Inner cipher name | `Wrm` (seed 2296496) | `NVu` (seed 6964224) |
| Bootstrap shim | `global['r'] = require` | (none — uses existing global) |

**The 3-day gap between W2 (Jun 20) and W1 (Jun 23) represents the actor's development cadence.** 
W1 is the upgraded Stage 1; W2 is the older baseline still running. The actor has not yet pushed
an updated W2 Stage 1 with the new features, suggesting either:
1. The two chains serve different victim segments and W2 victims get the older payload
2. W2 is being phased out — its TRON wallet has fewer recent TXs than W3 (the Stage 2 wallet)

---

## XOR Delivery Observation

The raw BSC TX for the W2 Stage 1 is 3,531 bytes:
- First 3 bytes: `?.?` (the standard actor delimiter, `0x3f 0x2e 0x3f`)
- Next 3,528 bytes: XOR-encrypted W2 Stage 1 (key2: `m6:tTh^D)cBz?NM]`)

Artifact: the last 3 bytes of the encrypted payload (`0x3f 0x2e 0x3f`) happen to be the same
as the `?.?` delimiter bytes. XOR-decrypted they produce `Wp{` — a truncated identifier
(`W`=wallet?, `p`=?, `{`=JSON open?) or purely coincidental noise. The valid JS ends at
`})()` before the `Wp{` tail.

---

## Complete Cipher Parameter Registry

All shuffle ciphers confirmed across the PolinRider campaign, as of 2026-06-27:

| Cipher | Layer | Campaign | Offsets | Mods | Modulus | Seed |
|--------|-------|----------|---------|------|---------|------|
| `_$_46e0` | Stage 0 | 5-3-161 | 508/318 | 22828/38027 | 3080816 | — |
| `_$_913e` | Stage 0 | 5-3-225/252/296/298/341, 5-2-328 | 508/318 | 12693/42331 | 4827673 | 36301 |
| `_$_b229` | Stage 0 | 5-4-39, 5-167 | 226/515 | 13874/23159 | 6342606 | 3590695 |
| `_$_4445` | Stage 0 | 5-2-319 | unknown | unknown | unknown | unknown |
| `_$_16d1` | **W2 Stage 1** | W2 chain (Jun 20) | 488/538 | 34187/48866 | 4728540 | 1147810 |
| `_$_9f51` | W1 Stage 1 (outer) | W1 chain (Jun 23) | 102/92 | 20113/48803 | 4969312 | 3654926 |
| `_$_96c7` | W1 Stage 1 (atob) | W1 chain (Jun 23) | 80/210 | 31099/45223 | 6108610 | 5914652 |
| `NVu` | W1 Stage 1 (inner `c()`) | W1 chain (Jun 23) | 122/89 | 16975/35503 | 7635721 | 6964224 |
| `Wrm` | **W2 Stage 1 (inner IIFE)** | W2 chain (Jun 20) | 213/407 | 18466/32620 | 3485560 | 2296496 |

**No two ciphers share the same modulus.** Each generation uses a unique modulus, making
the modulus alone a reliable per-cipher IOC for YARA targeting decoded payloads.

---

## YARA Rules (Task B additions)

```yara
rule PolinRider_Stage1_W2_CipherConstants {
    meta:
        description = "PolinRider Stage 1 W2 — _$_16d1 and Wrm cipher numeric constants"
        author = "analysis2"
        date = "2026-06-27"
        note = "Applies to decoded/decrypted W2 Stage 1 JS source (after XOR with key2)"
    strings:
        // _$_16d1 specific constants
        $mod_16d1   = "4728540" ascii   // modulus
        $seed_16d1  = "1147810" ascii   // seed
        // Wrm inner cipher constants
        $mod_Wrm    = "3485560" ascii   // modulus
        $seed_Wrm   = "2296496" ascii   // seed
        // Activation/return sentinels (both appear together in W2 Stage 1)
        $act_8063   = "8063" ascii
        $ret_8223   = "8223" ascii
    condition:
        ($mod_16d1 and $seed_16d1) or ($mod_Wrm and $seed_Wrm) or ($act_8063 and $ret_8223)
}

rule PolinRider_Stage1_W2_InRepo_ForwardLooking {
    meta:
        description = "PolinRider Stage 0 using _$_16d1 cipher — FORWARD LOOKING"
        author = "analysis2"
        date = "2026-06-27"
        note = "Not yet found in infected repos; rule for when it appears"
    strings:
        $cipher = "_$_16d1" ascii
        $seed   = "1147810" ascii
        $global_i  = "global.i='" ascii
        $eval_atob = "eval(atob(" ascii
    condition:
        $cipher and $seed and ($global_i or $eval_atob)
}
```

**Detection note for W2:** The `_$_16d1` cipher string would only appear in infected repo files
if Stage 0 for W2-targeted victims starts using this cipher name. Currently the cipher name
only appears inside the decoded W2 Stage 1 payload (from BSC TX). The cipher constants are
the reliable Tier 2 target for sandbox/decoded-payload scanning.
