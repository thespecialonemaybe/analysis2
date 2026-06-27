# Stage 1 Analysis: Live W1 Payload (`_$_9f51` cipher)

**Retrieved:** 2026-06-27  
**BSC TX source:** `0x18a8420f727f2405f9d1805ad887b31029b584b2ff5a7ec0f57c72635183e99d`  
**TRON wallet (W1):** `TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP` — updated 2026-06-23T02:35Z  
**Payload size:** 5,849 chars  
**Guard key (new):** `global["_t_t"]`  
**Public documentation status:** Zero GitHub results for `_$_9f51`, `_$_96c7`, `_t_t`

---

## Architecture Overview

The W1 Stage 1 is a significant upgrade from the Stage 0 payload. While Stage 0 (`_$_b229`) is 4–5 KB and delivers the C2 lookup chain, Stage 1 is a layered, multi-cipher orchestrator that:

1. Captures the local filesystem path of the running Node.js process
2. Stores itself in a global variable for introspection by later stages
3. Decodes a secondary cipher block to bootstrap the next chain
4. Performs campaign-ID-based IP routing to three distinct C2 server pools
5. Fetches and executes Stage 2 (77 KB compressed Beavertail RAT) from a new blockchain dead-drop
6. Provides error reporting back to the actor via `global._R`

### Full Execution Flow

```
Stage 0 (_$_b229)
  └─ TRON W1 → BSC TX → XOR decrypt → Stage 1 [5,849 chars]

Stage 1 (_$_9f51):
  ├─ guard check: global["_t_t"] exists? → exit if already running
  ├─ capture: global["___dirname"] = __dirname
  ├─ capture: global["___filename"] = __filename
  ├─ define c() [inner async function, 3-layer NVu cipher]
  ├─ global["_t_c"] = c.toString()       ← stores Stage 1 source
  ├─ global["_t_0"] = atob("...")         ← stores _$_96c7 cipher code string
  ├─ decode _$_9f51 string table [17 entries]
  ├─ route by _V (campaign ID):
  │    _V[0]=='A' or _V=='0' → C2 IP pool 1 (166.88.134.62)
  │    parseInt(_V) is numeric → C2 IP pool 2 (198.105.127.210)
  │    else → C2 IP pool 3 (23.27.202.27, port 27017 MongoDB)
  ├─ set global["_t_1"] = TA48dct6... [new Stage 2 TRON wallet]
  ├─ set global["_t_2"] = 0x533b2d... [Stage 2 BSC TX fallback]
  └─ await c()
       └─ NVu inner cipher → Function constructor → decompressor
            └─ decode Stage 2 payload → eval → Beavertail RAT
```

---

## New vs Previous Campaign Features

| Feature | `_$_913e` campaigns | `_$_b229` Stage 0 | W1 Stage 1 (new) |
|---------|--------------------|--------------------|-----------------|
| Guard key | `_p_t` | `_p_t` | **`_t_t`** |
| `__dirname` capture | No | No | **Yes** |
| `__filename` capture | No | No | **Yes** |
| Stage source stored | No | No | **`global["_t_c"]`** |
| Secondary cipher blob | No | No | **`global["_t_0"]`** |
| IP-based C2 routing | No | No | **Yes (3 pools)** |
| Direct IP C2 targets | Not in Stage 0 | Not in Stage 0 | **Exposed in Stage 1** |
| Error reporting | No | No | **`global._R`** |
| Activation code | None | 1632 | **9608** |
| Return sentinel | None | 2952 | **2776** |

---

## Cipher 1: `_$_9f51` — Stage 2 Routing Table (17 entries)

**Parameters:** offsets 102/92, mods 20113/48803, modulus 4969312, seed 3654926

**Encoded string (289 chars):**
```
2j220.a_%/4%50/h3./r3s1302t74p44.1_7%_7oc_h5t308_:c9.9%VV3ts6012%17:ID501c3d8pa4.Bi.
/8%7p.84se7:82n17/Xht84f/a.d61_66chp12t8t99101143//:662p8__41dL.6::%/tt%.Ff.i1tWd4.t72
/7::05j77:d.%T126tFt6%a.8vrAt42tt1t122rAeyap2t3%2N%37fbu07/b2t0/es32h%3%p1u3141N25%3t.
:hA4%8af5.9Sabx2F1e0M81322b._0.b2
```

**Decoded strings:**
| Index | Value | Role |
|-------|-------|------|
| [0] | `'_V'` | global key → read campaign ID set by Stage 0 |
| [1] | `'A'` | check: no-campaign marker (first char of `_V`) |
| [2] | `'0'` | check: uninitialized `_V` value |
| [3] | `'_t_s'` | global key → Stage 2 server URL with port |
| [4] | `'http://166.88.134.62:443'` | **C2 IP #1** (admin / no-campaign mode) |
| [5] | `'_t_u'` | global key → Stage 2 server URL base |
| [6] | `'http://166.88.134.62'` | **C2 IP #1 base** |
| [7] | `'parseInt'` | builtin for campaign ID numeric check |
| [8] | `'isNaN'` | builtin for campaign ID numeric check |
| [9] | `'http://198.105.127.210:443'` | **C2 IP #2** (numeric campaign IDs like `5-167`) |
| [10] | `'http://198.105.127.210'` | **C2 IP #2 base** |
| [11] | `'http://23.27.202.27:443'` | **C2 IP #3** (non-numeric `_V`) |
| [12] | `'http://23.27.202.27:27017'` | **C2 IP #3 base — port 27017 (MongoDB)** |
| [13] | `'_t_1'` | global key → Stage 2 TRON wallet |
| [14] | `'TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v'` | **NEW TRON wallet (Stage 2 dead-drop)** |
| [15] | `'_t_2'` | global key → Stage 2 BSC TX (fallback) |
| [16] | `'0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1'` | **Stage 2 BSC TX fallback** |

### Routing Logic

```javascript
_V = global['_V'] || 0;                       // campaign ID from Stage 0
if (_V[0] == 'A' || _V == '0') {
    // Admin/unconfigured mode — direct to IP #1
    global['_t_s'] = 'http://166.88.134.62:443';
    global['_t_u'] = 'http://166.88.134.62';
} else {
    if (!isNaN(parseInt(_V))) {
        // Numeric campaign ID (e.g. '5-167' → parseInt = 5)
        global['_t_s'] = 'http://198.105.127.210:443';
        global['_t_u'] = 'http://198.105.127.210';
    } else {
        // Non-numeric _V
        global['_t_s'] = 'http://23.27.202.27:443';
        global['_t_u'] = 'http://23.27.202.27:27017';  // MongoDB
    }
    global['_t_1'] = 'TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v';  // Stage 2 TRON wallet
}
global['_t_2'] = '0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1';
```

**Significance of IP routing:** Stage 2 uses the C2 IPs for direct communication (not blockchain). The three-pool routing based on campaign ID suggests different server pools may be allocated per campaign batch. Port 27017 (MongoDB) on `23.27.202.27` indicates the actor's C2 backend uses MongoDB for victim data storage.

---

## Cipher 2: `_$_96c7` — Secondary Bootstrap (from `global["_t_0"]`)

**Parameters:** offsets 80/210, mods 31099/45223, modulus 6108610, seed 5914652

**Encoded string (111 chars):**
```
3t_66TbftK8cdT7mP367Z4770cN3_c7c49srA1%Jf4xz%2xbe_f19ZM0dLv3ber721eb%32JJf1606de8375330a5_2a9f28e500ed07Ep8887Q
```

**Decoded strings (4 entries):**
| Index | Value | Role |
|-------|-------|------|
| [0] | `'_t_1'` | global key → TRON wallet reference |
| [1] | `'TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP'` | W1 TRON wallet (same as Stage 0!) |
| [2] | `'_t_2'` | global key → Aptos fallback reference |
| [3] | `'0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e'` | Aptos W1 fallback (same as Stage 0!) |

**How it's used:** Stage 1 stores the `_$_96c7` cipher definition as a code string in `global["_t_0"]`. When Stage 2 evals `global["_t_0"]`, it sets `global['_t_1']` and `global['_t_2']` back to the W1 TRON wallet and Aptos fallback — enabling Stage 2 to re-enter the same blockchain lookup chain for Stage 3 delivery. This is a staged C2 bootstrap: Stage 1 provides Stage 2 with the code to locate Stage 3.

There is a naming conflict by design: `_$_9f51` sets `_t_1` to the NEW wallet `TA48dct6...` for immediate Stage 2 fetch; once Stage 2 is running, it evals `_t_0` to reset `_t_1` to the original W1 TRON wallet (`TMfKQEd7...`) for Stage 3.

---

## Cipher 3: `NVu` — Inner IIFE (3-layer, inside `c()`)

**Parameters:** seed 6964224, offsets 122/89, mods 16975/35503, modulus 7635721

This cipher is the same 3-layer structure as `_$_b229` Stage 0:

1. **Layer 1 (NVu bootstrap):** `NVu("wanfojclgdrhucpkcmrsvbtuzsotnytoqxeri").substr(0,11)` → `'constructor'`
2. **Layer 2 (Function constructor via property):** `NVu['constructor']` → `Function`; avoids literal `"Function"` string
3. **Layer 3 (dynamic decompressor):** `Function(Mys, NVu(cWL))` creates a decompressor; runs it with activation code `9608`; returns `2776`

The inner `c()` function uses `_t_1`, `_t_2`, `_t_s`, `_t_u` (set by `_$_9f51`) to fetch and execute Stage 2.

---

## New Stage 2 Dead-Drop Chain

Stage 2 is delivered through a **third TRON wallet** (not seen in Stage 0):

| IOC | Value |
|-----|-------|
| Stage 2 TRON wallet | `TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v` |
| Stage 2 fallback BSC TX | `0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1` |
| Live Stage 2 BSC TX (Jun 8 2026) | `0xb6c725890be6890fd2c735eedc47e24b85a350301f6c19a3864e43c35e470968` |
| Stage 2 XOR key | `2[gWfGj;<:-93Z^C` (unchanged from Stage 0) |
| Stage 2 payload size | **77,279 chars** |

**TRON wallet `TA48dct6...` transaction history (confirmed active):**
| TX hash (truncated) | Timestamp (approx) | BSC TX (reversed) |
|--------------------|--------------------|-------------------|
| `08685820...` | ~2026-06-08 | `0xb6c725890be6890fd2c735eedc47e24b85a350301f6c19a3864e43c35e470968` |
| `f16931ee...` | ~2026-06-04 | `0x23fea476d18039a65bd438a4a071c2feb1530592b96ddf15c6ffb93acc03cd3f` |
| `8b2c39c6...` | ~2026-06-02 | `0x54b8bde10ea26d9ae0702e6e590f0af3e500cb14fda876e908620760ac32b76c` |

The Stage 2 wallet has been active since at least June 2, 2026, updating roughly every 3–6 days.

---

## Live Stage 2 Structure

The decrypted 77,279-char Stage 2 begins:
```javascript
Function("oTNBm2c","var lQlUCC=function(){var otJYbl=String.fromCharCode,
KWyyol=\"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=\",
XSqXuwG=\"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-$\",
DF5r02={};...
```

Structure:
- `Function("oTNBm2c", decompressor_code)` — same `Function` constructor pattern as previous stages
- Activation parameter: `oTNBm2c` (new, vs `1632`/`9608` in earlier stages)
- Decompressor: LZString/LZW variant with base64 and custom base91 alphabets
- The decompressor decodes the embedded compressed payload → Stage 3 (Beavertail RAT)
- Ends with UMD wrapper: `module`, `angular`, `define` environment detection

Stage 2 is the decompressor + compressed Beavertail RAT combined into one XOR-encrypted blob. Stage 3 execution happens entirely in-memory via `Function` constructor without writing to disk.

---

## Complete New IOC Set (Task A — previously unpublished)

### Direct C2 Infrastructure (first seen in any payload)
| IP | Port(s) | Routing condition |
|----|---------|-------------------|
| `166.88.134.62` | 443 | `_V` unset / `_V[0]=='A'` (admin/test mode) |
| `198.105.127.210` | 443 | Numeric campaign ID (all `5-X-YYY` victims) |
| `23.27.202.27` | 443, **27017** | Non-numeric `_V` |

**Port 27017 = MongoDB.** The actor's C2 backend exposes MongoDB directly.

### Blockchain IOCs (Stage 2 chain)
| IOC | Value |
|-----|-------|
| TRON wallet (Stage 2) | `TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v` |
| BSC TX fallback (Stage 2) | `0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1` |
| BSC TX live (Stage 2, Jun 8) | `0xb6c725890be6890fd2c735eedc47e24b85a350301f6c19a3864e43c35e470968` |

### Global Variable Namespace (Stage 1 signals in memory)
| Variable | Content | New |
|----------|---------|-----|
| `global["_t_t"]` | guard key — presence means Stage 1 already ran | **New** |
| `global["___dirname"]` | absolute path of running script | **New** |
| `global["___filename"]` | absolute filename of running script | **New** |
| `global["_t_c"]` | Stage 1 source code as string | **New** |
| `global["_t_0"]` | `_$_96c7` cipher code string for Stage 2 bootstrap | **New** |
| `global["_t_s"]` | Stage 2 C2 server URL with port | **New** |
| `global["_t_u"]` | Stage 2 C2 server URL base | **New** |
| `global["_t_1"]` | Stage 2 TRON wallet / W1 TRON (after Stage 2 runs `_t_0`) | Changed |
| `global["_t_2"]` | Stage 2 BSC TX / Aptos fallback (after Stage 2 runs `_t_0`) | Changed |
| `global._R` | error reporting callback (set by Stage 0 or caller) | **New** |

---

## C2 Architecture Implications

**The direct IP connection is new.** All previous documented stages used only blockchain for payload delivery. Stage 1 introduces three hardcoded IP addresses for C2 callbacks — the MongoDB port suggests the actor's backend stores victim reports in a MongoDB instance, with Stage 2/3 doing callbacks to `_t_s`/`_t_u`.

**The `___dirname`/`___filename` capture** tells the actor which file on the victim's machine ran the Stage 1. Combined with `global["_t_c"]` (Stage 1 source stored for inspection by later stages), the actor has full visibility into where the payload is executing.

**The `global._R` error callback** means Stage 0 or Stage 1 can report failures back to the actor's infrastructure. If Stage 2 fetch fails, the error string (`"failed to run clientCode: ${err}"`) is transmitted — giving the actor live telemetry on injection success rates.

**The three-pool IP routing** is a capacity/segmentation design. Victims in "admin mode" (no campaign ID) go to IP #1, real campaign victims go to IP #2, and a third pool handles edge cases. This suggests the actor is routing a large victim pool across multiple C2 servers.

---

## Cipher Parameter Reference

| Cipher | Location | Offsets | Mods | Modulus | Seed |
|--------|----------|---------|------|---------|------|
| `_$_9f51` | W1 Stage 1 outer | 102/92 | 20113/48803 | 4969312 | 3654926 |
| `_$_96c7` | W1 Stage 1 atob block | 80/210 | 31099/45223 | 6108610 | 5914652 |
| `NVu` | Inside `c()` | 122/89 | 16975/35503 | 7635721 | 6964224 |
| `_$_16d1` | W2 Stage 1 | 488/538 | 34187/48866 | 4728540 | (see W2 analysis) |
| `_$_b229` | Stage 0 (June 2026) | 226/515 | 13874/23159 | 6342606 | 3590695 |
| `_$_913e` | Stage 0 (May 2026) | 508/318 | 12693/42331 | 4827673 | 36301 |

---

## YARA Detection Rules

**Critical caveat: the IPs, wallets, and TRON addresses in `_$_9f51` are obfuscated** — they only exist as plaintext after the shuffle cipher runs at runtime. The encoded payload in the BSC TX is XOR-encrypted, and the decoded Stage 1 source contains those values only inside the encoded cipher string. YARA rules therefore target different detection surfaces:

| Surface | What's visible in plaintext | Rule tier |
|---------|----------------------------|-----------|
| **Infected repo file** (Stage 0 in git) | `_$_b229` cipher name, encoded cipher string, `eval(atob(`, `global.i=` | Tier 1 — repo scanning |
| **BSC TX after XOR decryption** (Stage 1 JS source) | Cipher function code with `4969312`, `3654926` etc. as JS literals | Tier 2 — decoded payload / sandbox |
| **Memory after Stage 1 runs** | Decoded strings including IPs, wallets | Tier 3 — EDR / memory forensics |

### Tier 1 — Infected Repository Files (Stage 0)

```yara
rule PolinRider_Stage0_b229_InRepo {
    meta:
        description = "PolinRider Stage 0 _$_b229 — infected JS/TS source file in repo"
        author = "analysis2"
        date = "2026-06-27"
        reference = "thespecialonemaybe/analysis2"
        note = "The _$_b229 cipher name appears in plaintext in infected repo files"
    strings:
        // Cipher function name is in cleartext in Stage 0
        $cipher = "_$_b229" ascii
        // Standard injection patterns
        $global_i = "global.i='" ascii
        $eval_atob = "eval(atob(" ascii
        // Large trailing space blocks before payload
        $trail = "                                                            " ascii  // 60+ spaces
    condition:
        $cipher and ($global_i or $eval_atob or $trail)
}

rule PolinRider_Stage0_9f51_ForwardLooking {
    meta:
        description = "PolinRider Stage 0 using _$_9f51 cipher — FORWARD LOOKING"
        author = "analysis2"
        date = "2026-06-27"
        note = "Not yet found in infected repos as of 2026-06-27; rule for when it appears"
    strings:
        $cipher = "_$_9f51" ascii
        $seed   = "3654926" ascii
        $global_i  = "global.i='" ascii
        $eval_atob = "eval(atob(" ascii
    condition:
        $cipher and $seed and ($global_i or $eval_atob)
}
```

### Tier 2 — Decoded Stage 1 Payload (BSC TX after XOR decrypt)

The cipher constants appear as JavaScript numeric literals in the Stage 1 source. These are plaintext in the decoded payload and would be visible to a sandbox or anyone who has decrypted the BSC TX.

```yara
rule PolinRider_Stage1_W1_CipherConstants {
    meta:
        description = "PolinRider Stage 1 W1 — _$_9f51 and _$_96c7 cipher numeric constants"
        author = "analysis2"
        date = "2026-06-27"
        note = "Applies to decoded/decrypted Stage 1 JS source (after XOR)"
    strings:
        // _$_9f51 specific constants
        $mod1  = "4969312" ascii   // _$_9f51 modulus
        $seed1 = "3654926" ascii   // _$_9f51 seed
        // _$_96c7 specific constants (co-occurs in same payload)
        $mod2  = "6108610" ascii   // _$_96c7 modulus
        $seed2 = "5914652" ascii   // _$_96c7 seed
        // Inner NVu cipher (also present)
        $mod3  = "7635721" ascii   // NVu modulus
        $seed3 = "6964224" ascii   // NVu seed
    condition:
        // Require 4 of 6 — three ciphers co-occur in the same payload
        4 of them
}
```

### Tier 3 — Memory Forensics (after Stage 1 executes)

After `_$_9f51` runs, the decoded strings exist in the Node.js heap. These rules apply to memory dumps or EDR memory scanning.

```yara
rule PolinRider_Stage1_W1_Memory_IPs {
    meta:
        description = "PolinRider Stage 1 W1 — decoded C2 IPs in process memory"
        author = "analysis2"
        date = "2026-06-27"
        note = "Memory forensics only — strings are obfuscated before runtime"
    strings:
        // All three IPs co-occur only in PolinRider Stage 1 W1
        $ip1 = "166.88.134.62" ascii
        $ip2 = "198.105.127.210" ascii
        $ip3_mongo = "23.27.202.27:27017" ascii   // MongoDB port in URL is near-unique
    condition:
        all of ($ip*)
}

rule PolinRider_Stage2_TRON_Wallet_Memory {
    meta:
        description = "PolinRider Stage 2 TRON wallet — in memory after Stage 1 decodes"
        author = "analysis2"
        date = "2026-06-27"
        note = "Memory forensics only"
    strings:
        $tron = "TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v" ascii   // 34-char base58, unique
    condition:
        $tron
}
```

**Detection note:** For proactive defense without memory forensics, Tier 1 (infected repo scanning) is the most actionable — it catches the injected Stage 0 before it ever runs. The `_$_b229` cipher name in source files is a reliable indicator. For SOC/EDR detection of active infections, Tier 2 (sandbox detonation catching the decoded Stage 1) and Tier 3 (memory scanning for IPs after execution) are the right approaches.
