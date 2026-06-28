# Task I: Aptos Fallback Address Transaction History

**Date:** 2026-06-28  
**Task:** Query Aptos fallback addresses for transaction history  
**Addresses:**
- A1: `0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e`
- A2: `0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3`

---

## Key Findings

1. **Aptos dead-drop mechanism confirmed**: All transactions are `0x1::aptos_account::transfer` with amount `'0'`. The RECIPIENT address field holds the BSC transaction hash — zero-value transfers to a BSC TX address encode the dead-drop pointer.

2. **Operation dates to at least June 13, 2025** — both A1 and A2 have transactions from that date. The campaign has been running for at minimum **12 months**, not 6 months as implied by public reporting.

3. **A1 tracks the W1 TRON channel** (`TMfKQEd7...`), A2 tracks the W2 TRON channel** (`TXfxHUet...`) — confirmed by cross-matching Aptos transfer recipients with known TRON→BSC TX pairs.

4. **NEW: Two deployments of new cipher `_$_f5f0` found** (Jun 23 and Jun 25, 2026) via A2 — not yet seen in any public GitHub repo. New capability added: `global['m'] = module`.

5. **Historical Stage 1 from August 2025 recovered** via A1 — uses cipher `RVj` with NO outer `_$_xxx` wrapper. This is the earliest Stage 1 variant retrieved.

---

## Dead-Drop Mechanism

The Aptos fallback works identically to the TRON primary:

```
Stage 0 malware:
  1. Try TRON wallet (TMfKQEd7... or TXfxHUet...)
     → Get latest TX → raw_data.data hex → UTF-8 → BSC TX hash
  2. Fallback: Try Aptos wallet (A1 or A2)
     → Get latest transfer TX → look at recipient address → that IS the BSC TX hash
  3. Hit BSC: eth_getTransactionByHash(bsc_tx_hash)
     → input field → hex→UTF-8 → split '?.?' → [1] → XOR → Stage 1
```

Evidence: every Aptos TX in both A1 and A2 has:
- `function`: `0x1::aptos_account::transfer`
- `arguments[1]` = `'0'` (zero APT transferred)
- `arguments[0]` = BSC TX hash (32-byte hex address)

The last 3 A1 transfers point to EXACTLY the same BSC TXs as the last 3 W1 TRON TXs.
The last 2 A2 transfers point to EXACTLY the same BSC TXs as the last 2 W2 TRON TXs.

---

## A1 Full Transaction History

`0xbe037400...` — W1 channel fallback. 22 total transactions.

| Date (UTC) | Aptos TX (short) | → BSC TX (recipient) | Note |
|-----------|-----------------|---------------------|------|
| 2025-06-13 05:12 | `0xf5bbb9c2...` | `0x14e7b64b5369fc74b0f3ef6f5de3ed6892786238c1f4172e6f465ac5558e5f04` | earliest |
| 2025-06-13 05:14 | `0xc3f2da1a...` | `0x14e7b64b...` (same) | duplicate |
| 2025-06-13 05:19 | `0xb54cf234...` | `0x1293aa8f691e49ba265ee19ae202061aa562f20fa158081618bf93f9be2d440b` | |
| 2025-06-13 06:25 | `0x63abb532...` | `0xe5a0cff72c7529b1d832a5d87872784ce50d480e59b464aa50bf75e5cdb86fac` | |
| 2025-06-24 05:14 | `0xe2a0459c...` | `0x67e43df37ecad064d6a66695ca4e9c8a7f0c00ed46afe1b77c780bb6b407ade8` | |
| 2025-06-24 05:23 | `0x9481e46c...` | `0xe40a40c6cef6461da5bb582f6da177b3197225dc4ea307414cde232ad9bb2054` | |
| 2025-07-23 16:28 | `0x448df8b4...` | `0x51a46279be66265b3eb660f4ebe71397d1f4714c5993c9a00a73e990bbfffb5c` | |
| 2025-08-19 16:45 | `0x8729b391...` | `0xa2ffa9b0ec69869ccba2c828a682c29fcd08a331d77550b3f2ca089ec25b8669` | **W1 Aug 2025 Stage 1 retrieved** |
| 2025-10-01 16:56 | `0x14fe1df5...` | `0x1ad0dd0135fe084e579aa67bfc3f0d2696ae451c0f1e7ea551c8b9613deb6eb1` | |
| 2025-10-01 17:01 | `0xe46b6c8c...` | `0xb980676a283234de8abb91a9ecfd1ca5055ab1119492f08bc31711d8ef48cb21` | |
| 2025-10-01 17:26 | `0x07b7ce01...` | `0xf46c86c886bbf9915f4841a8c27b38c519fe3ce54ba69c98d233d0ffc94d19fc` | |
| 2025-12-01 14:09 | `0x479e75d3...` | `0xec567681e8c98d694ef6f10303ac37da8cec0180da4c4be4c54e47a0bf31c436` | |
| 2026-03-04 17:03 | `0x0999330c...` | `0xc06e1b8427d699d2cc1caca174e70a19f13d6945b855a9655869a3c0ec26d4b0` | **W1 Mar 2026 retrieved, guard `_t_t` confirmed** |
| 2026-03-26 15:07 | `0x89b0fb19...` | `0xcfac95acd72844fa934c0de2aca3c208f532476c6a5d146b0a9333782f3aa550` | |
| 2026-03-26 15:08 | `0xc10e890b...` | `0xddad4f634fb787133cf4ed0b71f87cd1a354f70b0b47ba2b3469dc6574332932` | |
| 2026-03-26 15:59 | `0x95433ea7...` | `0xbe22e3626ef8ca4f84f7843163e35c8ebb5a889d0810bd1b501967f757cbc8a1` | |
| 2026-03-31 14:20 | `0x5e8f7828...` | `0x64286dc9d288cca084d3697237ad8e22573181b5b7a3ac8f0289a0369c28b6c9` | |
| 2026-05-20 15:16 | `0xaa54bc0b...` | `0x7c1c8ad22f95491daa62a11df1d5ff5c687a6491ff5d70409c8c2cbde3190f39` | |
| 2026-05-23 15:01 | `0x600289b2...` | `0x7d726de66b2736194395f37ccd3463ae7891ac13573d1ece7b315794633d03e4` | |
| 2026-05-23 16:16 | `0x4ae98212...` | `0x80a1148ee589125bc1e57d36abac9f08089b2990d9372be3a33a1f057ad1ef89` | = W1 BSC May 23 (known) ✓ |
| 2026-06-18 13:09 | `0xcbfdd577...` | `0xb73920732115ab3a0ae8d9ecd28666670d271bee77d29692ff29505fd9a1a6b2` | = W1 BSC Jun 18 (known) ✓ |
| 2026-06-23 02:35 | `0xc422e4bb...` | `0x18a8420f727f2405f9d1805ad887b31029b584b2ff5a7ec0f57c72635183e99d` | = W1 BSC Jun 23 (known) ✓ |

A1 update cadence: dense activity in Jun–Oct 2025 (actor was active all summer 2025),
quiet Nov 2025 – Feb 2026, then resumed Mar 2026.

---

## A2 Full Transaction History

`0x3f0e5781...` — W2 channel fallback. 10 total transactions.

| Date (UTC) | Aptos TX (short) | → BSC TX (recipient) | Note |
|-----------|-----------------|---------------------|------|
| 2025-06-13 05:54 | `0x73d3b033...` | `0x919911669b003d263c1f2a606100f27f7c11e2ef5287a50499f576fc13f500ab` | earliest |
| 2025-06-13 05:55 | `0x6c53e621...` | `0xc83de8720855a6b20761c15585c1273ce082a003ed67aaef5b4de443591e5021` | |
| 2025-06-18 08:28 | `0x384016de...` | `0x13e3ce3aefc019258c618265241ec1c51d858e6e5457a48ea5e38820fc4ba9a1` | |
| 2025-08-13 14:06 | `0xae9cb668...` | `0xd33f78662df123adf2a178628980b605a0026c0d8c4f4e87e43e724cda258fef` | |
| 2026-03-04 16:27 | `0x88982ee4...` | `0x60537dcbb1ad6a1fdd393c21eb7d38bcebad64de37eb23cde9a13df6f4926152` | |
| 2026-03-26 14:53 | `0xb2be93d0...` | `0xea7e97b13fc70642ed984d5d04d7a9d26dddd98bd17c7620b90821a837fea3be` | |
| 2026-03-26 15:13 | `0xa6a84c3c...` | `0xa896af4f2876df59af1e705fb75031630ebd37fa89659a9896be4d3da8c87f02` | = W2 BSC Mar 26 (known) ✓ |
| 2026-06-20 13:37 | `0x1e9d76a6...` | `0x7ffb4efddd96e20aec90724be2ac9a71c138a9af697b9fb8224bbf80ea4f22be` | = W2 BSC Jun 20 (known) ✓ |
| 2026-06-23 02:33 | `0xff88ac59...` | `0x76a7ae331269603bd690d2d9d810393b42d0c324acf1eacdf5a5258dfd3a6761` | **NEW — `_$_f5f0` Jun 23 deployment** |
| 2026-06-25 06:41 | `0xdf67b13a...` | `0x622bcfd4538f7e68772a1d5a08a48f9f8db82b2ca1babc8d45dba538c6a10e2e` | **NEW — `_$_f5f0` Jun 25 deployment** |

Jun 23 and Jun 25 updates on A2 have NO corresponding TRON W2 transactions in our TRON data —
the actor pushed these through Aptos-only. Either the TRON wallet was also updated and we missed
it, or the actor is using Aptos as a faster/parallel update channel.

---

## New Cipher: `_$_f5f0` (June 23–25, 2026)

Both Jun 23 and Jun 25 BSC TXs decrypt to W2 Stage 1 with the same outer cipher `_$_f5f0`
but different inner bootstrap cipher parameters.

### `_$_f5f0` outer cipher (identical in both)

| Parameter | Value |
|-----------|-------|
| Encoded string | `"mctjncr%uioonf%et%b"` |
| Seed | 1003076 |
| off1 | 272 |
| mod1 | 17454 |
| off2 | 349 |
| mod2 | 53273 |
| Modulus | 1523580 |

Decoded table (4 entries):

| Index | Value | Purpose |
|-------|-------|---------|
| `[0]` | `'function'` | `typeof require === 'function'` |
| `[1]` | `'r'` | `global['r'] = require` |
| `[2]` | `'object'` | `typeof module === 'object'` |
| `[3]` | `'m'` | **`global['m'] = module`** ← NEW |

**New capability**: `_$_f5f0` stores the CommonJS `module` object in `global['m']`. Prior
Stage 1 variants (`_$_16d1`, `_$_9f51`) only stored `require`. Access to the `module` object
gives Stage 2+ visibility into:
- `module.filename` — path of the infected config file on victim's machine
- `module.parent` — what required this module (reveals IDE/tooling context)
- `module.paths` — Node.js search paths (reveals project structure)
- `module.exports` — could be tampered to poison downstream require() callers

### Inner cipher — Jun 23 deployment: `SgH`

| Parameter | Value |
|-----------|-------|
| Cipher name | `SgH` |
| Seed | 570964 |
| off1 | 428 |
| mod1 | 13367 |
| off2 | 379 |
| mod2 | 43098 |
| Modulus | 1937868 |
| Stage 1 size | 3,612 chars |

### Inner cipher — Jun 25 deployment: `cdi`

| Parameter | Value |
|-----------|-------|
| Cipher name | `cdi` |
| Seed | 1787286 |
| off1 | 523 |
| mod1 | 49385 |
| off2 | 387 |
| mod2 | 23782 |
| Modulus | 7288442 |
| Stage 1 size | 3,530 chars |

The outer `_$_f5f0` cipher is shared (same seed/params). The inner bootstrap cipher rotated
between deployments. This pattern — stable outer + rotating inner — is consistent with the
actor reusing an outer wrapper while changing the decompressor obfuscation between pushes.

---

## Historical Stage 1: August 2025 — Cipher `RVj`

BSC TX `0xa2ffa9b0...` (A1, 2025-08-19) → W1 Stage 1, 3,688 chars.

This is the **earliest Stage 1 variant retrieved**, predating all previously documented ciphers.

```javascript
(function(){
  var Euo='', YYk=859-848;   // YYk=11

  function RVj(u){
    var j=2078320;
    // off1=366, mod1=39403, off2=397, mod2=44415, modulus=7371537
    ...
  }

  var xgI = RVj('ctduvckwoostulciftbxsgrrqoparjnezmynh').substr(0,YYk);  // → 'constructor'
  var mMO = '...decompressor...';
  var oOz = RVj[xgI];         // Function constructor
  var iJV = oOz(Zmm, RVj(mMO));  // decompressor fn
  var LHZ = iJV(RVj('ZdZs}...'));  // Stage 2 body
  ...
})()
```

**Key structural difference from 2026 variants:**

| | Aug 2025 | Jun 2026 |
|-|----------|---------|
| Outer `_$_xxx` cipher | **None** — raw IIFE | Present (`_$_f5f0`, `_$_16d1`, `_$_9f51`) |
| `require` storage | Not observed | `global['r'] = require` |
| `module` storage | Not observed | `global['m'] = module` (new, Jun 25+) |
| Guard key | Not confirmed | `global['_t_t']` (confirmed Mar 2026+) |
| Stage 2 encoded string | Starts with `Z` padding chars | Standard base chars |

The outer cipher wrapper was added between August 2025 and March 2026 — likely as an evasion
improvement after early detection attempts. The bare IIFE structure was the original form.

Inner cipher `RVj` parameters:

| Parameter | Value |
|-----------|-------|
| Seed | 2078320 |
| off1 | 366 |
| mod1 | 39403 |
| off2 | 397 |
| mod2 | 44415 |
| Modulus | 7371537 |

---

## Historical Stage 1: March 2026 — Guard Key Confirmed

BSC TX `0xc06e1b84...` (A1, 2026-03-04) → W1 Stage 1, 5,901 chars.

```javascript
(async()=>{
  if(global["_t_t"]) return;                          // guard: already infected?
  global["_t_t"] = (new global.Date).getTime();       // set guard
  if(typeof __dirname !== "undefined") global[...     // capture __dirname
  ...
```

This is structurally identical to the current June 2026 W1 Stage 1 — the guard key `_t_t`,
`__dirname`/`__filename` capture, and `async` IIFE wrapper were all present by March 4, 2026.
The guard mechanism has been stable for 4 months.

---

## Cipher Evolution Timeline (Updated)

| Period | Stage 1 variant | Key addition |
|--------|----------------|--------------|
| 2025-06-13 | Unknown (first A1/A2 TXs) | Infrastructure stood up |
| 2025-08-19 | `RVj` (seed 2078320) | Raw IIFE, no outer cipher |
| 2026-03-04 | Guard `_t_t`, `async` IIFE, 5,901 chars | Outer cipher added, `__dirname` capture |
| 2026-03-26 | Multiple W1+W2 updates same day | 3 W1 + 2 W2 updates in 1.5h |
| 2026-05-23 | W1 update | `_$_913e` generation in use |
| 2026-06-20 | W2 `_$_16d1` | W2 switches to direct HTTP C2 (Task B) |
| 2026-06-23 | W2 `_$_f5f0` / `SgH` | New outer cipher, adds `global['m'] = module` |
| 2026-06-25 | W2 `_$_f5f0` / `cdi` | Same outer, rotated inner |

---

## Unretrieved Historical Payloads (A1)

The following A1 BSC TXs from 2025 likely contain earlier Stage 1 variants. Most may still
be in BSC archive nodes. Worth retrieving to complete cipher timeline:

```
0x14e7b64b5369fc74b0f3ef6f5de3ed6892786238c1f4172e6f465ac5558e5f04  (2025-06-13)
0x1293aa8f691e49ba265ee19ae202061aa562f20fa158081618bf93f9be2d440b  (2025-06-13)
0xe5a0cff72c7529b1d832a5d87872784ce50d480e59b464aa50bf75e5cdb86fac  (2025-06-13)
0x67e43df37ecad064d6a66695ca4e9c8a7f0c00ed46afe1b77c780bb6b407ade8  (2025-06-24)
0xe40a40c6cef6461da5bb582f6da177b3197225dc4ea307414cde232ad9bb2054  (2025-06-24)
0x51a46279be66265b3eb660f4ebe71397d1f4714c5993c9a00a73e990bbfffb5c  (2025-07-23)
0x1ad0dd0135fe084e579aa67bfc3f0d2696ae451c0f1e7ea551c8b9613deb6eb1  (2025-10-01)
0xb980676a283234de8abb91a9ecfd1ca5055ab1119492f08bc31711d8ef48cb21  (2025-10-01)
0xf46c86c886bbf9915f4841a8c27b38c519fe3ce54ba69c98d233d0ffc94d19fc  (2025-10-01)
0xec567681e8c98d694ef6f10303ac37da8cec0180da4c4be4c54e47a0bf31c436  (2025-12-01)
```

---

## New IOCs

```
# New cipher (not in any public report)
_$_f5f0
Seed: 1003076 | off1: 272 | mod1: 17454 | off2: 349 | mod2: 53273 | Modulus: 1523580
Encoded: "mctjncr%uioonf%et%b" → ['function','r','object','m']

# _$_f5f0 inner cipher (Jun 23 deployment)
SgH: seed=570964, off1=428, mod1=13367, off2=379, mod2=43098, modulus=1937868

# _$_f5f0 inner cipher (Jun 25 deployment)
cdi: seed=1787286, off1=523, mod1=49385, off2=387, mod2=23782, modulus=7288442

# Historical cipher (Aug 2025)
RVj: seed=2078320, off1=366, mod1=39403, off2=397, mod2=44415, modulus=7371537

# New BSC TXs containing live Stage 1 payloads
0x76a7ae331269603bd690d2d9d810393b42d0c324acf1eacdf5a5258dfd3a6761  (W2, 2026-06-23)
0x622bcfd4538f7e68772a1d5a08a48f9f8db82b2ca1babc8d45dba538c6a10e2e  (W2, 2026-06-25)

# New capability (Stage 1, Jun 25+)
global['m'] = module    ← CommonJS module object now exfiltrated to Stage 2
```
