# Task AP: `11-#` Atob Dropper — GitHub Scan

## Objective

Search GitHub for victims of the base64-wrapped `eval(atob(...))` dropper variant, which
hardcodes campaign ID `11-#` rather than a victim-specific ID. This variant evades text-based
code search because all recognizable PolinRider strings are inside a base64 blob.

---

## Payload Anatomy

### Atob Dropper (8080 bytes, SHA `81b3b0ab`)

```
[1688 bytes whitespace padding]
eval(atob('Z2xvYmFsWychJ109JzExLSMn...'))  ← 6376-char base64 string
```

Decoding the base64 (4781 bytes):
```javascript
global['!']='11-#';var _$_1e42=(function(l,e){...})("rmcej%otb%",2857687);
global[_$_1e42[0]]= require;
if( typeof module=== _$_1e42[1]){global[_$_1e42[2]]= module};
(function(){
  var LQI='',TUU=401-390;
  function sfL(w){ var n=2667686; ... }
  // Stage 1 → TRON dead-drop chain (W1/W2/W3)
})();
```

Key differences from the standard 5102-byte variant:
- **Outer wrapper**: `eval(atob('...'))` hides all PolinRider strings from code search
- **Outer cipher seed**: 2857687 (vs 2667686 in standard variant)
- **Campaign ID**: `11-#` — hardcoded literal, not victim-specific
- **Inner sfL**: still uses seed 2667686 (same TRON URL shuffle)

### Campaign ID Routing

```
global['!'] = '11-#'
         ↓
global['_V'] = 'A11-#'
         ↓
_V[0] == 'A' → old: 23.27.13.43 (dead); current Jun 25 Stage 2: SILENT DROP
```

Victims with `11-#` receive no C2 beacon. They are not being actively exfiltrated.

### Payload Size Taxonomy (Full Picture)

| Size | SHA (prefix) | Variant | Campaign | Cipher seed | Victims |
|------|-------------|---------|----------|-------------|---------|
| 5102B | `b4aa3256`/varies | Plaintext `_$_1e42` | 8-765, 10-010 | 2667686 | saif72437 (old), madeeldev, SajidAfridi, birajdiyora |
| 5103B | `7efcfb2b` | Plaintext `_$_1e42` | 10-010 | 2667686 | hoangnv170752 (StudyNest) |
| 5533B | `8e14837c` | Plaintext `_$_1e42` | `8-**` | 2857687 | saif72437 (Jun-15 sweep), Nigerian HNG/DSC-Unilag cluster |
| 8080B | `81b3b0ab` | **Atob dropper** | `11-#` | 2857687 (inner) | NikhilGupta777, Rafijohari18 |

---

## Victims Identified

### Victim 1: `NikhilGupta777` — Indian developer (TypeScript/AI/web projects)

**Sweep date**: 2026-06-15T00:24–00:32 UTC (8-minute window)
**Repos infected**: 31 (all byte-identical, SHA `81b3b0ab`)

| Repo | Forged commit date | pushed_at |
|------|--------------------|-----------|
| Gemini-Clone | 2026-05-25T22:59:21Z | 2026-06-15T00:26:23Z |
| asd | 2025-09-08T21:18:49Z | 2026-06-15T00:24:00Z |
| Email-Harvestor | (varies) | 2026-06-15T00:25:04Z |
| Nikhil-Gupta | (varies) | 2026-06-15T00:32:04Z |
| (27 more repos) | (varies per repo) | 2026-06-15T00:xx:xxZ |

**Detection of injection commit** (Gemini-Clone): The injection commit SHA `0cbc3be0` was
forged to match the date and message of the developer's final legitimate commit
(`2026-05-25T22:59:21Z`, "revert(video): play video immediately on start"). Files added in the
injection commit:

```
.vscode/tasks.json            ← injection trigger
public/fonts/fa-solid-400.woff2  ← atob dropper payload (8080B)
public/fonts/fa-brands-400.woff2 ← cover (real FontAwesome)
public/fonts/fa-regular-400.woff2 ← cover
public/fonts/fa-solid-900.woff2  ← cover
public/fonts/README.md           ← cover
.vscode/extensions.json          ← cover
.vscode/launch.json              ← cover
.vscode/settings.json            ← cover
.vscode/spellright.dict          ← cover
```

The actor added an entire legitimate FontAwesome font set alongside the payload to make the
commit appear routine. This is more sophisticated than earlier batches (madeeldev, SajidAfridi)
which added only the tasks.json + woff2.

**Complete list of 31 infected repos**: `-DungeonSystemProject`, `AIIMAGE`, `asd`, `Claude-fork-new`,
`COM-611_2022A1R090`, `Datastructure`, `Datastructures-in-C`, `dusra-wala`, `Email-Harvestor`,
`Email1oct`, `email23sep`, `email2oct-2`, `EMAILKARYA2OCT`, `Gemini-Clone`, `Image-gen-ai`,
`imagegenerator`, `INTERNSHIP-JULY-MIET-2024`, `Mini-Project-Lab`, `Narayani-Sena-Email`,
`NarayaniSenaNewWebsite`, `Nikhil-Gupta`, `OpenSwarm-agent-terminal-coder-best-not-coding-but-we-can.modify-`,
`project-1-videodownload-`, `RailwayEmailRepoFInal`, `repo-root`, `runware-temp-pls-delete-`,
`system_prompts_leaks`, `terax-ai-best`, `test`, `testrailway-replit`, `testrailwaydeploy2oct`,
`video-clipper`

The victim sweeps ALL repo types indiscriminately — C code, Python, email harvesters, data
structures, university coursework, nothing excluded.

---

### Victim 2: `Rafijohari18` — Indonesian developer (PHP/Astro/Laravel/web)

**Sweep dates**: 2026-06-19 (astro-speed) and 2026-06-21 (birthday-imelda, learn-git)

This victim has **two infection vectors** in the same batch:

#### Vector A: `astro.config.mjs` injection (Rafijohari18/astro-speed)

File size: 13,696 bytes. Legitimate Astro config is only ~180 bytes:

```javascript
import { defineConfig } from 'astro/config';
import preact from '@astrojs/preact';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
export default defineConfig({
  output: 'static', compressHTML: true, integrations: [preact()],
  build: { inlineStylesheets: 'always' },
});
```

After the legitimate export (byte ~820), the actor appended **two payloads at module scope**:

```
Byte   832:  global['!']='8-4081'; var _$_1e42=...  ← Payload 1 (plaintext, seed 2667686, 5102-style)
Byte  7303:  eval(atob('Z2xvYmFsWychJ109JzExLSMn...')) ← Payload 2 (atob dropper, 11-#)
```

Both payloads execute when Node.js imports this module (e.g., on `astro build` or `astro dev`).
Campaign `8-4081` uses the old sfL seed (2667686), indicating it targets a different Stage 1
dead-drop than the `11-#` atob dropper. The dual-payload structure may serve as a fallback: if
one cipher/XOR key fails, the other executes.

#### Vector B: `public/fonts/fa-solid-400.woff2` injection (standard path)

| Repo | Size | SHA | Forged date | pushed_at |
|------|------|-----|-------------|-----------|
| birthday-imelda | 8080B | `81b3b0ab` | 2024-06-04 | 2026-06-21T02:36:50Z |
| learn-git | 8080B | `81b3b0ab` | (varies) | 2026-06-21 |

The `birthday-imelda` injection forged to 2024-06-04 — a 2-year gap with the `pushed_at` of
2026-06-21. The most extreme timestamp forgery gap documented across all victims.

---

### Victim 3: `saif72437` — Pakistani developer (JS/CSS/Flutter) — second infection wave

**Prior infection** (documented in Task N): campaign `8-765`, 5102-byte standard variant.

**Second sweep** (2026-06-15): 64 repos re-swept with the **5533-byte `8-**` variant**
(SHA `8e14837c`). The actor returned to this machine and either updated or added to the payload.

Also present: `temp_auto_push.bat` (1036 bytes) found in at least 5 repos
(`Email-Layout-Builder`, `cool-sketch`, `full-stack-medium-clone`, `saif72437`,
`real-estate-app`). The bat file was committed accidentally during the Jun-15 sweep — this is
the first documented case of the actor's infection tool appearing in a victim repo.

---

## Additional Victims (5533-byte `8-**` variant)

The 5533-byte payload (SHA `8e14837c`) appears in a large cluster of Nigerian developer repos,
primarily from the HNG (HNG Tech) internship ecosystem and University of Lagos tech community.
These repos share the byte-identical `8-**` template:

| Account cluster | Sample repos | Payload |
|----------------|-------------|---------|
| DSC-Unilag | dsc-unilag-app, Code-Workshop-Mobile-Project, ecx_mobile | 5533B `8-**` |
| hngx-org | mirage-kotlin-auth-library, financial-planner-ai-app, openai-api-library | 5533B `8-**` |
| hngi | Team-Geras-Solar-Calculator, Team-storm-mobile- | 5533B `8-**` |
| devcareer | fiverly-flutter | 5533B `8-**` |
| KIHM-02 | SilverCare, SoundScape | 5533B `8-**` |
| devlopersabbir | new_android_application, randomiser | 5533B `8-**` |

The `8-**` campaign ID contains literal asterisks — not a placeholder for a victim-specific ID.
All `8-**` victims are silently dropped by the current Stage 2, same as `11-#`.

---

## Other Victims Confirmed (5102-byte standard variant)

Additional victims beyond previously documented saif72437/madeeldev clusters:

| Account | Sweep date | Repos | Campaign | Size |
|---------|-----------|-------|----------|------|
| `SajidAfridi` | 2026-06-08 | 14 Dart repos | 10-010 | 5102B |
| `hoangnv170752` | (unknown) | StudyNest | 10-010 | 5103B |
| `birajdiyora` | (unknown) | CabbashHotel | (unknown) | 5102B |
| `kishan-ck` | (unknown) | compose-pixelperfectdesign | (unknown) | 5102B |
| `FarazRashid` | (unknown) | FintechAdvise | (unknown) | 5102B |

`SajidAfridi` and `madeeldev` both have campaign `10-010` and were swept on consecutive days
(Jun 7–8, 2026), suggesting they are in the same campaign batch.

---

## Search Methodology

GitHub code search for `fa-solid-400.woff2 filename:tasks.json` returned **125 results** —
the full victim surface for the `public/fonts/` delivery path. After filtering out legitimate
FontAwesome installs (>30KB) and research tools (Ndevu12/stayAwakeBot, amir-mostafa-hs, etc.),
the infected repos fall into three size buckets: 5102–5103B, 5533B, 8080B.

The `eval+atob` pattern is invisible to `filename:*.woff2` text search — GitHub does not index
binary file content for code search. The atob dropper evades this search vector entirely;
discovery required size analysis of all woff2 files returned by the tasks.json search.

---

## IOCs

| Type | Value |
|------|-------|
| Atob dropper payload | SHA `81b3b0ab65e6f8ab5f4fcb31a5049a41c3a73398` (8080 bytes) |
| Atob dropper SHA (decoded) | inner payload 4781 bytes, campaign `11-#` |
| 5533-byte template | SHA `8e14837c2c9eb2fd21e15ddbd40b267491764593`, campaign `8-**` |
| Victim: NikhilGupta777 | 31 repos infected 2026-06-15, `public/fonts/fa-solid-400.woff2` |
| Victim: Rafijohari18 | `astro-speed` (astro.config.mjs, dual payload), `birthday-imelda`, `learn-git` |
| Victim: saif72437 (wave 2) | 64 repos swept 2026-06-15, now 5533B (`8-**`) |
| Infection tool leak | `temp_auto_push.bat` (1036B) in saif72437 repos |
| Dual-payload file | `Rafijohari18/astro-speed/astro.config.mjs` (13696B): campaigns `8-4081` + `11-#` |
| Cipher outer seed (atob) | 2857687 (differs from standard 5102-byte seed 2667686) |

---

## Assessment

**The atob dropper (`11-#`) was deployed to at least 2 identified victims**: `NikhilGupta777`
(31 repos, Jun 15) and `Rafijohari18` (3 repos, Jun 19–21), with a combined 34 infected
repositories all carrying SHA `81b3b0ab`. Given the GitHub code search returns 0 hits for
the inner strings (`11-#`, `_$_1e42`, `sfL`), additional victims are likely undetected —
the atob wrapper makes text-based discovery infeasible without inspecting every woff2 blob.

**The injection is becoming more sophisticated**: the NikhilGupta777 batch includes a full
FontAwesome cover set and copies the developer's exact last commit message and timestamp. Earlier
batches (madeeldev, SajidAfridi) used only "Update README.md" as the forged message. The actor
is improving the forgery to resist visual inspection of git log.

**The `astro.config.mjs` dual-payload** in `Rafijohari18/astro-speed` is a new delivery surface
not previously documented. It executes at `astro build/dev` runtime, not just at VSCode open
time. This broadens the trigger surface: both CI/CD pipelines and local dev would activate the
payload.

**The `temp_auto_push.bat` exposure** in saif72437 repos is an OPSEC failure by the actor —
the infection tool was accidentally committed to the victim's repos. This file (1036 bytes)
should be retrieved and analyzed for actor infrastructure details.

**Recommended follow-on tasks**:
- **AU**: Retrieve and reverse `temp_auto_push.bat` from saif72437 repos
- **AV**: Search for `astro.config.mjs` injections beyond Rafijohari18 (GitHub code search for oversized astro configs)
- **AW**: Determine if any atob dropper victims have the Stage 2 Beavertail loader (do they have a W4/W5 TRON wallet mapping?)
