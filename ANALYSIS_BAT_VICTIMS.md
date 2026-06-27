# Task L: Bat-File Victim Repo Investigation

**Date:** 2026-06-27  
**Scope:** 8 repos with `config.bat` committed + sample of 30 from 102 repos with `temp_interactive_push.bat`

---

## Summary

29 repos scanned across both bat-file groups. **7 have live JS payloads** in config files, all
using the `_$_1e42` cipher with a previously undocumented activation/return pair (**2509/1358**).
The payload is YARA-detectable via the existing `rmcej_otb_payload` rule, but these repos have
not been cleaned despite being months old.

A Cursor IDE plugin repo (`dryhurstdigital/invoice-my-clients-cursor-plugin`) has
`temp_interactive_push.bat` committed but no JS payload in standard config files — the bat
file was placed but the injection step did not complete, or targets an unconventional file path.

---

## config.bat Repos: Scan Results (8/8 checked)

| Repo | JS Payload | File | Notes |
|------|-----------|------|-------|
| `fahad-khan11/auth-app-with-nestjs-api` | **INFECTED** | `eslint.config.mjs` | 6,277 chars |
| `one-project-one-month/Easy-Trip-Python` | Clean | — | Python repo — no JS config files |
| `farahos/Point-of-sale-management-system` | Clean | — | No standard config files |
| `Sohaib909/E-comm-Backend` | Clean | — | No standard config files |
| `Saarcasmic/BulkEmailCampaignManager` | Clean | — | No standard config files |
| `fahad-khan11/image-generate-SaaS_App-using-Next-Mern-` | Clean | — | No payload found |
| `srushtibhilare/women` | Clean | — | No standard config files |
| `HUZAIFASAJJAD012/Job_protal` | Clean | — | No standard config files |

7 of 8 config.bat repos have no JS payload — the bat file was committed but the injection either
didn't fire (perhaps the repo had no matching config file), or the payload was cleaned after
commit.

---

## temp_interactive_push.bat Repos: Scan Results (29 sampled from 102)

### Live infections found

| Repo | File | Size | Notes |
|------|------|------|-------|
| `fahad-khan11/auth-app-with-nestjs-api` | `eslint.config.mjs` | 6,277b | (also in config.bat group) |
| `Iambilalfaisal/glow-aim-tools` | `postcss.config.js` | 5,462b | — |
| `ArturSargsyan1995/one-click-hugo-cms` | `postcss.config.js` | 5,478b | — |
| `Vladyslav0060/budget-app` | `postcss.config.js` | 5,374b | — |
| `cto-varun/frontend-design-dashboard-test` | `tailwind.config.js` | 5,412b | High-value: CTO username |
| `Jaskaran2701/Test-1` | `postcss.config.mjs` | 5,516b | — |
| `Harsimran-Nugen/assignment` | `postcss.config.mjs` | 5,516b | — |

**Hit rate: 7 of 29 sampled repos infected (24%).** Extrapolating to all 102 `temp_interactive_push.bat`
repos, approximately **25 repos** likely have live payloads.

### Notable clean repos

| Repo | Bat file present | Payload | Notes |
|------|-----------------|---------|-------|
| `dryhurstdigital/invoice-my-clients-cursor-plugin` | Yes | **None found** | Cursor IDE plugin — unconventional file layout |
| `new-computers/seeder` | Yes | None found | OSM-tracked, bat-only |
| `new-computers/arena-toolkit` | Yes | None found | OSM-tracked, bat-only |
| `Reactongraph/digital-signature-pad` | Yes | None found | No standard config files |
| `GrootNet-Software-Solutions-Pvt-Ltd/memory_game` | Yes | None found | — |

---

## Cipher Profile: New Activation/Return Pair

All 7 live infections share identical cipher characteristics:

| Field | Value |
|-------|-------|
| Cipher variable | `_$_1e42` |
| Encoded string | `rmcej%otb%...` (matches OSM YARA rule) |
| Global marker | `global['!']` |
| **Activation code** | **2509** |
| **Return sentinel** | **1358** |

The activation code **2509** and return sentinel **1358** are **not previously documented**
for `_$_1e42`. The only other `_$_1e42` activation/return pair in our records is from the
earliest Stage 0 analysis (1632/2952). The actor is running multiple `_$_1e42` variants with
different activation codes — likely corresponding to different deployment batches or operator
sessions. Each activation code uniquely identifies a deployment run.

These repos are detectable by OSM's `rmcej_otb_payload` YARA rule (the `rmcej%otb%` encoded
string is present in plaintext inside the infected config file) but have not been cleaned —
suggesting the repo owners are unaware, or OSM's notification process did not reach them.

---

## The Cursor Plugin Finding

`dryhurstdigital/invoice-my-clients-cursor-plugin` is a Cursor IDE plugin repository. It has:
- `temp_interactive_push.bat` committed at root
- No JS payload in any standard config file location
- `vitest.config.js` is clean (128 bytes, legitimate config)
- `package.json` has no malicious dependencies

Two explanations:
1. The bat file was placed during the infection setup phase, but the injection step targeted a
   config file that doesn't exist in this repo (`postcss.config.*`, `tailwind.config.*`, etc.
   are typical targets but this is a Cursor plugin project, not a Next.js/Tailwind app)
2. The payload was injected somewhere non-standard (e.g., inside `scripts/` or a skill file)
   and wasn't caught by the standard config-file scan

The fact that this is a **Cursor IDE plugin** is notable. If Stage 4 achieved persistence on
the developer's machine and `config.bat` ran, any repo the developer has push access to could
have been modified — including this plugin. Anyone who installs this plugin from source would
then clone an infected developer's tooling environment.

---

## Extrapolation and Scale

| Group | Total repos | Sampled | Live infections found | Est. total live |
|-------|-------------|---------|----------------------|----------------|
| config.bat | 8 | 8 (100%) | 1 | 1 |
| temp_interactive_push.bat | 102 | 29 (28%) | 6 | ~21 |
| **Combined** | **110** | **37** | **7** | **~22** |

These ~22 repos represent infections from the `_$_1e42` wave (the OLD cipher, YARA-detectable)
that remain live as of June 2026 — months after OSM's first public documentation in March.

---

## New IOCs

```
# New activation/return pair for _$_1e42 (Stage 0, previously undocumented)
Activation: 2509
Return:     1358

# Live infected repos (config file infections, _$_1e42 cipher)
fahad-khan11/auth-app-with-nestjs-api       — eslint.config.mjs
Iambilalfaisal/glow-aim-tools               — postcss.config.js
ArturSargsyan1995/one-click-hugo-cms        — postcss.config.js
Vladyslav0060/budget-app                    — postcss.config.js
cto-varun/frontend-design-dashboard-test    — tailwind.config.js
Jaskaran2701/Test-1                         — postcss.config.mjs
Harsimran-Nugen/assignment                  — postcss.config.mjs

# Cursor plugin repo with bat artifact (payload location unknown)
dryhurstdigital/invoice-my-clients-cursor-plugin
```
