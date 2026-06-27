# Task G: New Cipher GitHub Scan + Side Discoveries

**Date:** 2026-06-27  
**Task:** Search GitHub for `_$_16d1`, `_$_9f51`, `_$_96c7`, `_$_4445` in infected repos

---

## Result: All Four New Ciphers — Zero Results

| Cipher | GitHub results | Modulus search | Status |
|--------|---------------|----------------|--------|
| `_$_16d1` | **0** | 0 | Not yet in any public repo |
| `_$_9f51` | **0** | 0 | Not yet in any public repo |
| `_$_96c7` | **0** | 0 | Not yet in any public repo |
| `_$_4445` | **0** | 0 | Not yet in any public repo |

**The new-generation ciphers have not yet appeared in any publicly indexed GitHub repo.** This
is the expected state for ciphers that exist only in the blockchain-delivered Stage 1 payload
— they would appear in GitHub code search only if a new Stage 0 injection used them as the
in-repo cipher name.

The only confirmed Stage 0 use of `_$_4445` was in `zurichjs-conf` PR#199 (June 26), which
was remediated 6 hours later — before GitHub's indexer processed the change.

**This establishes a monitoring baseline.** When any of these four strings appear in GitHub
code search results, it will be the earliest public signal of new Stage 0 deployments using
the next-generation cipher family.

---

## Side Discoveries from Recon

Running Task G surfaced two unplanned but significant findings.

---

### 1. `Cot%3t=shtP` Cipher — Still Live, New Act/Ret Pair

**5 of 8 sampled** `Cot%3t=shtP-sg` repos (from OSM's April 11 list) have live payloads as of
June 27, 2026 — 2.5 months after OSM first tracked them.

| Repo | File | Size | Notes |
|------|------|------|-------|
| `herasoftlabs/ChainLab` | `postcss.config.mjs` | 5,966b | Blockchain dev platform |
| `herasoftlabs/ChainLab` | `next.config.mjs` | 7,105b | **Dual injection** |
| `herasoftlabs/Dappify` | `postcss.config.mjs` | 5,682b | Decentralized app platform |
| `raiv200/Tic-Tac-Toe-Game` | `tailwind.config.js` | 5,438b | — |
| `sanketnighot/sat-token-deployer-ui` | `postcss.config.js` | 6,018b | Token deployer UI |

**New activation/return pair documented: 5471 / 3456**

This is the first time the `Cot%3t=shtP` cipher's execution constants have been confirmed from
a live sample. The `Cot%3t=shtP` marker differs from the `_$_1e42` variants:

| Field | `_$_1e42` (2509/1358 cluster) | `Cot%3t=shtP` (5471/3456) |
|-------|-------------------------------|---------------------------|
| Cipher variable | `_$_1e42` (explicit var name) | None (anonymous) |
| Encoded string start | `rmcej%otb%...` | `Cot%3t=shtP)4k]os4@...` |
| Campaign ID global | `global['!']` | `global['_V']` |
| Extra globals | — | `global['r']`, `global['m']` |
| Cipher function | varies (`jFD`, `LQI`) | `AoT` (seen in ChainLab) |
| Activation | 2509 | **5471** |
| Return | 1358 | **3456** |

The shift from `global['!']` to `global['_V']` aligns with W1 Stage 1, which reads
`_V = global[_$_9f51[0]]` — the campaign ID key was renamed from `'!'` to `'_V'` between
the `_$_1e42` wave and the `Cot%3t=shtP` wave, and that naming persisted through the W1
Stage 1 build.

**`herasoftlabs/ChainLab` has a dual injection** — both `postcss.config.mjs` AND
`next.config.mjs` contain the payload. This is a technique seen in other campaigns where
the actor injects multiple config files to increase persistence (cleaning one doesn't clean
the other).

**Encoded string recovered:** `'Cot%3t=shtP)4k]os4@(\/1d189s6<m_0P](;T95'` (41 chars)  
This is the Stage 0 IIFE's outer cipher string — the `Cot%3t=shtP` prefix is exactly where
OSM derived the cipher family name.

---

### 2. `saif72437` — Mass Infection, 30 Repos Updated Same Day

`saif72437` has 30 GitHub repos, **all updated 2026-06-15** — an actor sweep on a single day.
`saif72437/medium-clone/tailwind.config.js` confirmed infected with `_$_1e42`, act 2509/ret
1358. The `saif72437` profile repo and `WebSockets` repo are listed as "Batchfile" language —
these contain `temp_auto_push.bat` / `config.bat`.

A mass same-day update across all repos of a developer is the fingerprint of `config.bat`
running on the developer's machine and iterating across every local git repo with push access.
The `branch_structure.json` artifact (from Innovative-VAS signatures) likely enumerated all
30 repos as targets. The actor's sweep hit all of them in sequence on June 15.

---

## Complete Activation/Return Registry (updated)

All confirmed Stage 0 execution constants as of 2026-06-27:

| Cipher | Act | Return | Wave | Notes |
|--------|-----|--------|------|-------|
| `_$_1e42` | 1632 | 2952 | Earliest (`rmcej%otb%`) | OSM YARA baseline |
| `_$_1e42` | **2509** | **1358** | Bat-file cluster | Task L discovery |
| `Cot%3t=shtP` | **5471** | **3456** | Mar–Apr 2026 interim | Task G discovery |
| `_$_913e` | ? | ? | May 2026 | Zurichjs 5-3-298, external victims |
| `_$_b229` | 1632 | 2952 | Jun 2026 | Zurichjs 5-4-39, 5-167 (same as _$_1e42 ?) |
| `_$_4445` | ? | ? | Jun 26 2026 | Zurichjs 5-2-319 |
| `NVu` (Stage 1 inner) | 9608 | 2776 | W1 Stage 1 | Inside c() function |
| `Wrm` (Stage 1 inner) | 8063 | 8223 | W2 Stage 1 | Inside IIFE |

The activation code is the **most reliable per-deployment IOC** — it appears as a plain
integer in the payload tail (`var tzo=AoT(VRG,quw);tzo(5471);return 3456`) and cannot be
obfuscated without changing the execution flow.

---

## Proposed New Tasks

Based on Task G recon, three new tasks are recommended:

**M — Decode `Cot%3t=shtP` cipher from live samples**  
Live encoded string recovered: `'Cot%3t=shtP)4k]os4@(\/1d189s6<m_0P](;T95'` (41 chars).
Decode to extract: full string table, TRON wallet addresses, Aptos fallback, campaign ID
format change (`global['_V']` vs `global['!']`). Would complete the cipher registry for
the March–April wave and confirm whether the C2 wallets changed between `_$_1e42` and
`Cot%3t=shtP`.

**N — `saif72437` full sweep**  
30 repos all updated 2026-06-15, one confirmed infected. Check all for live payloads, extract
campaign IDs, determine whether a second C2 chain was used for this developer's machine
(the June 15 date is AFTER `_$_b229` appeared, so campaign IDs may be from the June wave).

**O — `_$_1e42` 2509/1358 cluster C2 mapping**  
Multiple live repos using this undocumented activation/return pair. Decode one payload fully
to extract the TRON wallet address. This may reveal a third `_$_1e42`-era C2 chain distinct
from the OSM-tracked `TMfKQEd7...` / `TXfxHUet...` wallets.

---

## IOCs (new from Task G)

```
# New activation/return pair — Cot%3t=shtP cipher (Stage 0)
Activation: 5471
Return:     3456

# Cot encoded string (recovered from live sample)
'Cot%3t=shtP)4k]os4@(\/1d189s6<m_0P](;T95'   (41 chars)

# Live infected repos — Cot%3t=shtP cipher (still unpatched as of 2026-06-27)
herasoftlabs/ChainLab         — postcss.config.mjs + next.config.mjs (dual)
herasoftlabs/Dappify          — postcss.config.mjs
raiv200/Tic-Tac-Toe-Game      — tailwind.config.js
sanketnighot/sat-token-deployer-ui — postcss.config.js

# saif72437 — mass infection June 15, 2026
saif72437/medium-clone        — tailwind.config.js (confirmed, _$_1e42, 2509/1358)
saif72437/* (29 others)        — likely infected, not yet scanned
```
