# Task BA: ChainVeil npm Packages — A6 Series Analysis

**Date:** 2026-07-23  
**Packages:** tailwindcss-merge, sass-format, tailwindcss-animates-kit, sass-formats,
clsx-tailwind, tailwindcss-animatics, typeorm-encrypt, rate-limits-flexible, rate-limit-flexible  
**Reference:** Dragon-Lady CHAINVEIL_TEXT_INDICATORS; `ANALYSIS_CIPHER_SCAN_P.md`

---

## Summary

All 9 ChainVeil packages are confirmed PolinRider malware in the **A6 campaign series**. Campaign
ID `A6-519-79` is directly confirmed in one advisory; Dragon-Lady independently tracked
A6-317, A6-318, A6-420, A6-420-#, and A6-519-79/81/83/85 — these IDs likely map to the 5
version slots of `sass-formats` (1.0.1–1.0.5) and the two earliest packages
(`tailwindcss-animatics` + `tailwindcss-animates-kit`). All packages share the canonical
PolinRider TRON/Aptos/BSC dead-drop infrastructure. A new cipher seed (`2540575`) is documented
for `tailwindcss-merge`; wallet addresses remain unrecovered (tarballs and version manifests
fully deleted by npm). `typeorm-encrypt` represents the first confirmed expansion beyond
CSS/frontend tooling into the TypeORM/NestJS/Express backend ecosystem.

**All packages taken down Jun 11, 2026** — 13 days before the JFrog disclosure (Jun 24). Amazon
Inspector was the reporting entity.

---

## Package Status

All 9 packages are fully removed from npm. npm replaced each with a `0.0.1-security` holding
package on **2026-06-11 09:33–09:34 UTC** (43-second automated batch window):

| Package | Versions | OSV ID | GHSA ID | First Published |
|---------|----------|--------|---------|-----------------|
| tailwindcss-merge | 1.0.1–1.0.4 + 0.0.1, 0.0.2 (Jan 2024) | MAL-2026-5632 | GHSA-m2xh-rw7p-69rx | 2024-01-17 |
| sass-formats | 1.0.1–1.0.5 | MAL-2026-5629 | GHSA-pvrm-39m5-j3c4 | 2026-06-07 |
| typeorm-encrypt | 1.0.1–1.0.2 | MAL-2026-5633 | GHSA-f7h6-4xj8-8qh7 | 2026-06-07 |
| rate-limit-flexible | 1.0.1–1.0.2 | MAL-2026-5626 | GHSA-v7vx-48xw-jwm8 | 2026-06-07 |
| clsx-tailwind | 1.0.1 | MAL-2026-5625 | GHSA-373j-j35f-q4gx | 2026-06-07 |
| rate-limits-flexible | 1.0.1 | MAL-2026-5627 | GHSA-hg8j-2wmv-w4v6 | 2026-06-10 |
| sass-format | 1.0.1 | MAL-2026-5628 | GHSA-m8x4-pc4m-p5gv | 2026-06-10 |
| tailwindcss-animatics | 1.0.1 | MAL-2026-5631 | GHSA-mp9h-24x9-xc7r | 2026-05-19 |
| tailwindcss-animates-kit | 1.0.1 | MAL-2026-5630 | GHSA-v4xp-qgj3-gphm | 2026-05-19 |

Tarballs: CDN 404 (fully deleted, not just registry-suppressed).  
Version manifests: registry 404 (npm purged individual version entries).  
Publisher info: scrubbed (all versions show `npm <npm@npmjs.com>` after takeover).

---

## Typosquatting Targets

| Malicious Package | Legitimate Target | Attack |
|-------------------|------------------|--------|
| `tailwindcss-merge` | `tailwind-merge` | 1-char insert (`tailwindcss` vs `tailwind`) |
| `sass-formats` | `sass-formatter` | 1-char swap (`formats` vs `formatter`) |
| `sass-format` | `sass-formatter` | Truncation (`format` vs `formatter`) |
| `tailwindcss-animates-kit` | `tailwindcss-animate` | Suffix addition (`-kit`) |
| `tailwindcss-animatics` | `tailwindcss-animate` | Suffix swap (`-atics` vs `e`) |
| `clsx-tailwind` | `clsx` + `tailwindcss` users | Combinator squatting |
| `rate-limit-flexible` | `rate-limiter-flexible` | 1-char drop (`limiter` vs `limit`) |
| `rate-limits-flexible` | `rate-limiter-flexible` | Plural variant |
| `typeorm-encrypt` | `typeorm-encrypted-column` or similar | Truncation |

---

## Publish Timeline

Three publishing sessions, all UTC:

**Session 1 — May 19, 2026** (earmark: 6 minutes between packages)
```
07:18:19  tailwindcss-animatics  1.0.1
07:24:50  tailwindcss-animates-kit  1.0.1
```

**Session 2 — Jun 7, 2026** (~7.5 hours, rapid version iteration per package)
```
02:43  sass-formats 1.0.1
03:09  sass-formats 1.0.2
03:26  sass-formats 1.0.3
03:34  sass-formats 1.0.4
05:19  sass-formats 1.0.5
06:28  tailwindcss-merge 1.0.1
06:36  tailwindcss-merge 1.0.2
06:49  tailwindcss-merge 1.0.3
07:09  tailwindcss-merge 1.0.4
07:47  clsx-tailwind 1.0.1
08:32  rate-limit-flexible 1.0.1
09:07  rate-limit-flexible 1.0.2
09:33  typeorm-encrypt 1.0.1
10:00  typeorm-encrypt 1.0.2
```

**Session 3 — Jun 10, 2026** (~1 minute apart)
```
10:50:49  sass-format 1.0.1
10:51:41  rate-limits-flexible 1.0.1
```

**Takedown — Jun 11, 2026** (43-second batch, Amazon Inspector report)
```
09:33:50  clsx-tailwind → 0.0.1-security
09:33:55  rate-limit-flexible → 0.0.1-security
09:33:59  rate-limits-flexible → 0.0.1-security
09:34:05  sass-format → 0.0.1-security
09:34:10  sass-formats → 0.0.1-security
09:34:14  tailwindcss-animates-kit → 0.0.1-security
09:34:20  tailwindcss-animatics → 0.0.1-security
09:34:25  tailwindcss-merge → 0.0.1-security
09:34:30  typeorm-encrypt → 0.0.1-security
```

---

## Campaign ID Evidence

**Direct confirmation:** `sass-formats` 1.0.2 advisory (MAL-2026-5629) quotes:
> `global['_V']='A6-519-79'`

This is an A6-series victim ID, routing prefix `'A'` (→ admin C2 `166.88.134.62`).

**Dragon-Lady cross-reference:** `ANALYSIS_CIPHER_SCAN_P.md` records Dragon-Lady's
CHAINVEIL_NETWORK_INDICATORS tracking these IDs: A6-317, A6-318, A6-420, A6-420-#,
A6-519-79, A6-519-81, A6-519-83, A6-519-85.

**Hypothesized mapping** (victim IDs per publish batch, based on timing):
```
A6-317           ← tailwindcss-animatics 1.0.1    (May 19, session 1, pkg 1)
A6-318           ← tailwindcss-animates-kit 1.0.1  (May 19, session 1, pkg 2)
A6-420           ← clsx-tailwind or tailwindcss-merge earliest (Jun 7)
A6-420-#         ← a version suffix variant of same package
A6-519-79        ← sass-formats 1.0.2  (confirmed)
A6-519-81/83/85  ← sass-formats 1.0.3/4/5  (unconfirmed but consistent)
```

The ID structure follows the PolinRider series-victim convention: `6` = series 6, `317`/`318`/
`420`/`519` = victim group, suffix = sub-variant (matching observed pattern in series 8 and 9).

---

## Technical Details

### Payload location per package

| Package | Malicious file | Entry reference |
|---------|---------------|-----------------|
| `tailwindcss-merge` | `src/lib/lib.min.js` | `src/index.ts` line 13: `import './lib/lib.min.js'` (side-effect import despite `sideEffects:false`) |
| `sass-formats` | `dist/lib/lib.min.js` | Loaded from dist entry |
| `clsx-tailwind` | `dist/lib/lib.min.js` | `dist/index.js` unconditionally requires it |
| `typeorm-encrypt` | `lib/lib.min.js` | **NOT referenced from `lib/index.js`** — requires postinstall or separate execution |
| others | `dist/lib/lib.min.js` | Standard dist entry |

All files are ~4 KB, heavily obfuscated.

### PolinRider execution pattern (shared by all 9)

```javascript
// Step 1: Stash Node intrinsics globally
global['r'] = require;
global['m'] = module;

// Step 2: Set campaign ID
global['_V'] = 'A' + global['!'];   // e.g. 'A6-519-79'

// Step 3: Permutation-decoder reconstructs 'constructor'
// Different function name per package variant:
//   tailwindcss-merge: unnamed (inline)
//   clsx-tailwind: YWG

// Step 4: Function.constructor eval
YWG[OSN]('', decoded_blob)(compressed_payload)  // or equivalent

// Step 5: Dead-drop fetch (TRON → Aptos fallback → BSC)
async function loadPayload(xorKey, tronAccount, aptosAccount) { ... }
```

This matches the canonical PolinRider Stage 1 loader shape documented in `ANALYSIS_1E42_C2.md`.

### New cipher variant: seed 2540575

`tailwindcss-merge` uses a Knuth-style string-shuffle seeded with **`2540575`** to reconstruct
the string `'constructor'` from the scrambled literal `'axhscuutcrogycrneotisjlnkdpfqmzovtrwb'`
(38 chars containing all letters of 'constructor' plus noise/padding).

Known cipher seeds across all PolinRider variants:

| Seed | Where seen | Source |
|------|-----------|--------|
| `2667686` | Standard `_$_1e42` (JudeTejada and most npm/astro loaders) | ANALYSIS_AJ |
| `2857687` | Outer obfuscator.io wrapper (aegre/damian AX) | ANALYSIS_AX_OBFUSCATOR |
| `1812138` | Inner `_$af163278` (obfuscator.io inner, same AX payload) | ANALYSIS_AX_OBFUSCATOR |
| **`2540575`** | **A6-series tailwindcss-merge** | This document |

The A6-series seed is distinct, confirming these packages use a separate obfuscation template
from the series 8/9 npm packages.

### Dead-drop infrastructure (confirmed by Amazon Inspector)

All 9 packages contact the same three endpoints:
- `api.trongrid.io` — TRON dead-drop resolver (Step 1 primary)
- `fullnode.mainnet.aptoslabs.com` — Aptos dead-drop resolver (Step 1 fallback)  
- `bsc-dataseed.binance.org` — BSC RPC, payload retrieval (Step 2)
- `bsc-rpc.publicnode.com` — BSC RPC fallback (inferred from standard PolinRider pattern)

`bootstrap.pypa.io` also appears in Amazon Inspector IOCs: this is legitimate PyPA
infrastructure (hosts `get-pip.py`). It is contacted by the Stage 4 Python bootstrapper
to install missing pip dependencies on Linux/macOS — not a C2 server. This is the same
Stage 4 behavior documented by JFrog for the A8 packages (`ANALYSIS_CIPHER_SCAN_P.md`).

### Wallet addresses (UNRECOVERED)

The specific TRON wallet addresses for A6-series cannot be recovered: tarballs are
fully deleted and the OSV advisories do not include wallet addresses in their IOC lists.
The infrastructure IOCs confirm PolinRider dead-drop architecture but not which of W1–W5
(or a new wallet) serves the A6 series.

**Best guess:** A6-series packages with `'A'` prefix routing go to admin C2 `166.88.134.62`
for Stage 2. A8-series packages also use `'A'` prefix and confirmed W1 (`TMfKQEd7...`) as
Stage 1 dead-drop. If A6 follows the same wallet assignment as A8, they use W1/W2. However,
the different cipher seed (`2540575`) could indicate a separate obfuscation template associated
with a different wallet pair (e.g. W4 or an unidentified wallet).

**This remains an open intelligence gap.**

---

## Notable Artifacts

### tailwindcss-merge: 17-month pre-positioning

`tailwindcss-merge` published placeholder versions in January 2024 — 17 months before the
campaign's active phase:

```
0.0.1  published 2024-01-17T23:15:58Z
0.0.2  published 2024-01-18T04:12:06Z
         [17-month gap]
1.0.1  published 2026-06-07T06:28:25Z  ← malicious
1.0.2  published 2026-06-07T06:36:28Z  ← malicious
1.0.3  published 2026-06-07T06:49:14Z  ← malicious
1.0.4  published 2026-06-07T07:09:43Z  ← malicious
```

The 0.0.x versions are prior to the campaign's earliest known activity (infra creation
2025-11-13). This suggests either: (a) the actor squatted the `tailwindcss-merge` namespace
in early 2024 as pre-campaign positioning, or (b) a legitimate early owner published 0.0.x
and the actor later hijacked the package name. No 0.0.x code is recoverable for analysis.

### sass-formats: fake developer attribution

`dist/cli.js` in `sass-formats` contains a modified-by header:
```
// Modified by https://github.com/maaratum... Marat Arzymatov 2025
```

The GitHub account `maaratum` does not exist (verified: 404 from GitHub API, 2026-07-23).
The `sass-formatter` legitimate package uses `"author": "Syler"` — `sass-formats` copies
this field to appear authentic while attributing modifications to a fabricated developer.

### typeorm-encrypt: orphaned malicious file

The advisory notes that `lib/lib.min.js` is **not referenced** from `lib/index.js` (the
package main) or any other clean module. The package's legitimate stated purpose is a
TypeORM column encryption transformer, with clean source in `lib/crypto.js`, `lib/entity.js`,
and `lib/transformer.js`. The malicious file would require a `postinstall` script or similar
mechanism to execute — this execution path is not confirmed from the advisory. This is an
unusual loader variant that differs from other packages where the main entry directly imports
the malicious file.

### New targeting vector: TypeORM/Express backend

All prior PolinRider npm packages targeted frontend tooling (Astro, Vite, PostCSS, Tailwind,
clsx). `typeorm-encrypt` and `rate-limit-flexible`/`rate-limits-flexible` are the first
confirmed packages targeting the Node.js backend ecosystem:

- `typeorm-encrypt`: TypeORM is the most-used ORM for NestJS applications; TypeORM column
  encryption packages are commonly added to database models handling PII/credentials.
- `rate-limit-flexible`/`rate-limits-flexible`: typosquatting `rate-limiter-flexible`, an
  Express/Koa/NestJS rate-limiting middleware with 2M+ weekly downloads. Developers adding
  rate-limiting to APIs would be targeted.

This broadens the PolinRider victim profile from frontend/Astro developers to anyone building
Node.js backend services.

---

## IOC Summary

### Network / Blockchain (shared with all PolinRider packages)

| Indicator | Type | Role |
|-----------|------|------|
| `api.trongrid.io` | Domain | TRON dead-drop resolver |
| `fullnode.mainnet.aptoslabs.com` | Domain | Aptos dead-drop fallback |
| `bsc-dataseed.binance.org` | Domain | BSC RPC payload delivery |
| `bsc-rpc.publicnode.com` | Domain | BSC RPC fallback |
| `166.88.134.62` | IP | A-prefix C2 (admin; Stage 2 eval) |
| `bootstrap.pypa.io` | Domain | PyPA (legitimate; Stage 4 pip bootstrap) |

### Cipher fingerprint

| Field | Value |
|-------|-------|
| Cipher seed (tailwindcss-merge) | `2540575` |
| Anagram literal | `'axhscuutcrogycrneotisjlnkdpfqmzovtrwb'` |
| Reconstructed string | `'constructor'` |
| Decoder function (clsx-tailwind) | `YWG` |

### Campaign IDs

| ID | Package | Version | Confirmed |
|----|---------|---------|-----------|
| A6-519-79 | sass-formats | 1.0.2 | Direct (OSV advisory) |
| A6-317 | tailwindcss-animatics | 1.0.1 | Dragon-Lady (inferred) |
| A6-318 | tailwindcss-animates-kit | 1.0.1 | Dragon-Lady (inferred) |
| A6-420 | unknown (Jun 7 batch) | 1.0.1 | Dragon-Lady (inferred) |
| A6-519-81/83/85 | sass-formats | 1.0.3/4/5 | Dragon-Lady (inferred) |

### File hashes (from advisories — partial)

| Package | File | SHA256 |
|---------|------|--------|
| tailwindcss-merge | src/index.ts | 87bf1942492d077d43efc57b03dd5cc54a1f4d61fe687c05edfe86a18e33a226 |
| tailwindcss-merge | src/lib/lib.min.js | 1a6283f5fd8fadf6ed71558c31c6ecc2e392ba9e4915201c2c9557b7e7b94a9d |
| typeorm-encrypt (v1.0.2) | lib/lib.min.js | cc074a2f99e5bdfa7acde7d9dd6620771a3d6c9a71e023e50c1853df8681a43d |
| typeorm-encrypt (v1.0.2) | package.json | 61de2a0fdb31eca99c6a6e22aef56df1e2aa663ef8f6e5f2b63c61037973fbf6 |
| sass-formats | dist/lib/lib.min.js | b373c2d8b6479a9acdb2fadbd35d312e8bd70975c8a3a3247b2aa9df6c3ef0e4 |
| clsx-tailwind | dist/lib/lib.min.js | 294f1d358f4ec049372757af801789c84c43ff2d758f55a6eeadcab3a6fb05f5 |
| rate-limit-flexible | (package) | 166436585b1666871717d2202a01b64cfc580432ad36d90fa05903daf050d8f7 |
| rate-limits-flexible | (package, v1.0.1) | 809e7f8796ee45bb12d644bd48e71cbfca430e22d40b06ea0e0437097d131068 |
| tailwindcss-animatics | (package) | b874b5b9324f64b8a30a60f2c89c8ea75dd40de7503a678c9d0e1829e53e8f01 |
| tailwindcss-animates-kit | (package) | 36f982d7c842137890d743938442fe409fd41a786fe5727bcd77277406b2a189 |

---

## Open Intelligence Gaps

1. **A6-series wallet addresses** — tarballs deleted, no wallet extraction possible. Cannot
   confirm W1/W2 vs alternative wallet pair for A6. Archive investigation (per task AY
   methodology) would require the actual npm tarballs from a pre-deletion mirror.

2. **A6-420 and A6-420-# mapping** — which package(s) carry these IDs is unconfirmed.
   `tailwindcss-merge` and `clsx-tailwind` are candidates (Jun 7 batch, `4xx` ID range
   fits between the May 19 `3xx` and Jun 7 `5xx` groups).

3. **typeorm-encrypt execution path** — malicious file is orphaned (not imported from main).
   Whether it used `postinstall`, `prepare`, or another hook is unknown.

4. **tailwindcss-merge 0.0.1/0.0.2 (Jan 2024)** — legitimate placeholder or early actor
   namespace grab? No code recoverable.

---

## Relation to Known Campaign Timeline

```
2026-05-19  Session 1: tailwindcss-animatics + tailwindcss-animates-kit (A6-317/318)
2026-05-25  JFrog npm packages (html-to-gutenberg + fetch-page-assets) uploaded — A8 series
2026-06-07  Session 2: sass-formats + tailwindcss-merge + clsx-tailwind + rate-limit* + typeorm-encrypt
2026-06-08  W3 last dead-drop TX (Stage 2/Stage 3 channel begins wind-down)
2026-06-10  Session 3: sass-format + rate-limits-flexible
2026-06-11  Amazon Inspector report → npm batch takedown of all 9 in 43 seconds
2026-06-20  W2 last dead-drop TX; aegre/damian astro victim swept
2026-06-23  W1 last dead-drop TX  
2026-06-24  JFrog blog post published (public disclosure)
2026-06-25  itzvin19 astro victims swept
2026-06-26  CharlieJT astro victim swept
```

The npm packages were taken down 13 days before the JFrog disclosure — but notably *after*
the first wallet wind-down began (W3 silent Jun 8, W2 silent Jun 20). This timeline is
consistent with the actor already transitioning away from W1/W2/W3 when Amazon Inspector
flagged the npm packages on Jun 11.

---

## Related Documents

- `ANALYSIS_CIPHER_SCAN_P.md` — JFrog post full summary; Dragon-Lady cross-ref; first
  enumeration of these 9 packages
- `ANALYSIS_AN_GO_PACKAGES.md` — Go package campaign (same period, A8 series, W1 cipher)
- `CAMPAIGN_MASTER.md` §7 — Campaign ID taxonomy and A-prefix routing
- `ANALYSIS_AX_OBFUSCATOR.md` — Cipher variant comparison (obfuscator.io seed 2857687)
- `ANALYSIS_AJ_JUDETEJADA.md` — Standard seed 2667686 reference
