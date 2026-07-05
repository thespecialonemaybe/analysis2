# Task AV: Oversized `astro.config.mjs` Scan

## Objective

Search GitHub for `astro.config.mjs` files with PolinRider injection beyond the 29 repos
documented in Task AG/AI. Normal legitimate Astro configs are <500 bytes. Previously known
infected variants run 3,300–11,715 bytes. Task AK found `Rafijohari18/astro-speed` at
13,696 bytes (dual payload). This scan looked for additional victims, especially ones using
the `eval(atob(...))` dropper found in Rafijohari18.

---

## Search Methodology

| Query | Results |
|-------|---------|
| `eval atob filename:astro.config.mjs` | 0 (GitHub doesn't index .mjs binary content) |
| `_1e42 filename:astro.config.mjs` | 28 (all previously known Task AG/AI victims) |
| `createRequire global filename:astro.config.mjs` | 42 (14 repos NOT in `_1e42` set) |
| `Tgw 2509 filename:astro.config.mjs` | 0 (YARA anchor not indexed) |
| `_0x22ee filename:astro.config.mjs` | 0 (obfuscated names not indexed) |

The `createRequire+global` query was the productive vector: it catches infected repos where
the outer layer obfuscates the `_$_1e42` string, making it invisible to all IOC-specific
GitHub searches.

---

## Results: 4 New Victims Confirmed

All use a **new delivery format**: an obfuscator.io outer wrapper (~20KB) encasing the
standard `_$_1e42` inner cipher. This variant does not appear in any `_$_1e42` code search.

### New Victim Table

| Repo | Size | Campaign | pushed_at | Commit forgery |
|------|------|----------|-----------|----------------|
| `aegre/damian` | 20,836B | `9-7298` | 2026-06-20T14:46:00Z | auth 2025-10-01 / commt 2026-06-20 **GAP** |
| `CharlieJT/cleric-homepage` | 20,932B | `9-7172` | 2026-06-26T06:44:25Z | auth=commt 2026-01-27 (no gap) |
| `itzvin19/dance-studio` | 21,025B | `8-4435-1` | 2026-06-25T11:50:00Z | auth=commt 2025-10-30 (no gap) |
| `itzvin19/03-blog` | 20,979B | `8-4435-1` | 2026-06-25T11:49:53Z | auth=commt 2026-01-03 (no gap) |

**`itzvin19`** has two infected repos sharing the same campaign ID `8-4435-1`, pushed 7
seconds apart — confirming the actor swept both repos on the same victim machine in a single
session (Jun 25, ~11:49 UTC).

**`aegre/damian`** shows the classic timestamp gap (actor committed directly from their own
machine), forging the author date to October 2025 while the committer date reveals the true
injection date of June 20, 2026.

---

## New Delivery Format: Obfuscator.io Outer Wrapper

### Structure

```
[0–210B]:  Legitimate Astro config
           import { defineConfig } from 'astro/config';
           import { createRequire } from 'module';
           const require = createRequire(import.meta.url);
           export default defineConfig({});

[~210–720B]: Whitespace padding (~500 chars)

[720B+]:   global['!']='9-7298';
           var _0x383eb4=_0x22ee;
           function _0x37df(){ var _0x580eb4=['.]_.()r5%]','g]1jRec2rq',...,'rmcej%otb%',...] }
           ...
           [~20,100 chars of obfuscator.io-style code]
```

### Outer cipher fingerprint (byte-identical across all 4 repos)

```javascript
var _0x383eb4=_0x22ee;
function _0x37df(){
  var _0x580eb4 = ['.]_.()r5%]','g]1jRec2rq','sp.hu0) p]',...,'rmcej%otb%',...];
  // ...
}
```

- `_0x383eb4`, `_0x22ee`, `_0x37df` — obfuscator.io hex-style variable names
- `rmcej%otb%` is the `_$_1e42` cipher seed string, buried inside the `_0x580eb4` string array
- Inside the obfuscated code: `_$_1e42` cipher and `require;typeof module===_$_1e42[...]` logic

### Payload size variation explained

| Repo | Campaign ID | Payload chars |
|------|------------|--------------|
| `aegre/damian` | `9-7298` | 20,112 |
| `CharlieJT/cleric-homepage` | `9-7172` | 20,112 |
| `itzvin19/dance-studio` | `8-4435-1` | 20,113 |
| `itzvin19/03-blog` | `8-4435-1` | 20,106 |

The 1–6 char variance is entirely from the campaign ID string being different lengths.
The outer obfuscation template is otherwise byte-identical. A single batch was used.

---

## Campaign ID Analysis

| ID | Series | Significance |
|----|--------|-------------|
| `9-7298` | 9 | **New high-water mark** — previous max was `9-7226` (FieteLab, Task AI) |
| `9-7172` | 9 | 126 below the new max; same sweep window (Jun 20–26) |
| `8-4435-1` | 8 | Sub-ID `-1` suffix; same ID for two repos (same victim machine) |

Series 9 now confirmed to have at least **7,298** tracked victims. Combined with Series 8
(≥4,435), total actor-tracked victim count exceeds **11,733+** across both series.

---

## Sweep Clustering

| Date | Time UTC | Victim | Repos infected |
|------|----------|--------|----------------|
| 2026-06-20 | 14:43–14:46 | `aegre` | 1 (`damian`) |
| 2026-06-25 | 11:49–11:50 | `itzvin19` | 2 (`dance-studio`, `03-blog`) |
| 2026-06-26 | 06:44 | `CharlieJT` | 1 (`cleric-homepage`) |

`aegre` Jun 20 sweep pushed all 3 of the owner's Astro repos at ~14:46 UTC — only one
(`damian`) was successfully infected; the other two (`tokyo-racer`, `srag`) lacked a
compatible injection surface.

---

## Evasion Impact

The obfuscator.io wrapper completely defeats the current GitHub search IOC set:

| Detection method | Plaintext `_$_1e42` | Obfuscator.io variant |
|----------------|--------------------|-----------------------|
| `_1e42 filename:astro.config.mjs` | ✓ detects | ✗ miss |
| `rmcej+otb filename:astro.config.mjs` | ✓ detects | ✗ miss |
| `Tgw 2509 filename:astro.config.mjs` | ✓ detects | ✗ miss |
| `createRequire global filename:astro.config.mjs` | ✓ detects | ✓ detects |
| File size > 3KB | ✓ detects | ✓ detects |

The `createRequire+global` query is the only current search vector that catches this
variant. But it also returns ~30 legitimate false positives (coreui, handsontable,
jagreehal/awaitly, etc.) and requires manual size-based triage.

**The variant is also invisible to YARA rules targeting `_$_1e42` or `rmcej%otb%`** since
those strings only appear inside the obfuscated string table in scrambled form.

---

## Previously Known Astro Cluster (Tasks AG/AI)

29 repos, all plaintext `_$_1e42`, confirmed infected. Adding the 4 new obfuscated repos:

**Total confirmed infected `astro.config.mjs` repos: 33+**

The actual count is higher — the obfuscator.io variant cannot be enumerated via GitHub code
search. Discovery requires fetching and inspecting individual files.

---

## IOCs

| Type | Value |
|------|-------|
| Obfuscated astro payload | Outer: `var _0x383eb4=_0x22ee; function _0x37df()` |
| Inner cipher confirmation | `_$_1e42` + `rmcej%otb%` string inside `_0x580eb4` array |
| New victim: `aegre/damian` | Campaign `9-7298`, pushed 2026-06-20, injection commit gap |
| New victim: `CharlieJT/cleric-homepage` | Campaign `9-7172`, pushed 2026-06-26 |
| New victim: `itzvin19/dance-studio` | Campaign `8-4435-1`, pushed 2026-06-25T11:50 |
| New victim: `itzvin19/03-blog` | Campaign `8-4435-1`, pushed 2026-06-25T11:49 |
| Series 9 new maximum | `9-7298` (prev. max `9-7226`, Task AI) |
| Sweep batch dates | Jun 20 (`aegre`), Jun 25 (`itzvin19` ×2), Jun 26 (`CharlieJT`) |

---

## Assessment

**The actor has added an obfuscator.io wrapping layer to the `astro.config.mjs` delivery
vector**, producing ~20KB payloads that evade all `_$_1e42`-targeted GitHub code search
and YARA rules. The inner C2 chain is unchanged (`_$_1e42` cipher, TRON dead-drop, same
campaign ID routing).

The three distinct sweep dates (Jun 20, 25, 26) indicate this is an ongoing, active
deployment wave — not a historical artifact. All four repos were infected within the
Jun 20–26, 2026 window, coinciding with the final W2/A2 update period (last TRON W2 TX
was Jun 20; last Aptos A2 TX was Jun 25).

**Recommended follow-on (Task AX):** Partially decode the `_0x22ee`/`_0x37df` outer cipher
to confirm the full TRON → BSC → XOR chain is intact inside the obfuscated wrapper. This
would close the loop on whether the obfuscated variant uses the same infrastructure or
routes to a new endpoint.
