# PolinRider / DEV#POPPER / Void Dokkaebi — Campaign Master Reference

**Classification:** TLP:WHITE  
**Last updated:** 2026-07-18  
**Confidence:** High  
**Attribution:** Lazarus Group / Famous Chollima / DPRK-nexus

This document is the single authoritative reference for the full investigation. Individual
analysis documents are linked throughout; this is the synthesis layer — architecture,
registry tables, taxonomy, and current status in one place.

---

## 1. Campaign Identity

| Name | Source |
|------|--------|
| **PolinRider** | Community / this investigation |
| **DEV#POPPER** | Securonix |
| **Void Dokkaebi** | Trend Micro TRU |
| **Contagious Interview** | CrowdStrike (sub-cluster) |
| **Famous Chollima** | CrowdStrike (actor group) |
| **ChainVeil** | Dragon-Lady/linux-supply-chain-guard |

All names refer to the same DPRK-aligned intrusion set. "Contagious Interview" / "Famous
Chollima" refers specifically to the fake job-interview pretext sub-cluster. "BestCity
cluster" (see §11) is a separate actor sharing the VSCode delivery vector but with no
infrastructure overlap.

---

## 2. Dead-Drop Architecture

This is the campaign's defining technical characteristic. Understanding it is a prerequisite
for every other section.

### 2.1 Three-Chain Pointer-Payload Split

The malware does **not** store payloads on TRON or Aptos. Those chains store *pointers only*.
The payload lives exclusively on BSC.

```
Step 1 — Pointer resolution (TRON OR Aptos, one fallback for the other):
  ┌─ TRON wallet  ──► raw_data.data (hex) → reverse UTF-8 → BSC TX hash ─┐
  └─ Aptos wallet ──► payload.arguments[0] = BSC TX hash (direct)        ─┴─► hash

Step 2 — Payload delivery (BSC only, no fallback):
  hash ──► eth_getTransactionByHash(hash) ──► result.input
        ──► hex decode → UTF-8 → split('?.?')[1]
        ──► XOR decrypt (wallet-specific key)
        ──► eval(Stage N payload)
```

**Critical failure-mode note:** TRON and Aptos are redundant resolvers for step 1 only.
Both chains store the *same BSC TX hash*. If a public BSC RPC node has pruned that
transaction from its index, falling back from TRON to Aptos still returns the same
unresolvable hash. The payload chain breaks at step 2 regardless. Recovery requires a BSC
full-archive node (Quicknode/Alchemy archive), not a chain fallback.

### 2.2 TRON Encoding

Each TRON dead-drop wallet's most recent outbound `TransferContract` carries the BSC hash
in its `raw_data.data` memo field. Decode:

```
hex(raw_data.data) → UTF-8 string → reverse entire string → 0x-prefixed BSC TX hash
```

The actor appends a trailing `x0` to the hash before writing; reversal converts it to a
leading `0x` prefix. This also serves as a simple integrity marker.

### 2.3 Aptos Encoding

Each Aptos address makes a 0-APT `0x1::aptos_account::transfer` transaction where the
*recipient address* is the BSC TX hash directly (Aptos addresses = 32-byte hex = same
space as BSC TX hashes). No decoding required; the malware reads
`transactions[0].payload.arguments[0]`.

### 2.4 BSC Delimiter

All BSC transactions containing payloads use `?.?` as a delimiter in the hex input field:
```
<prefix hex>?.?<XOR-encrypted payload>
```
The malware splits on `?.?` and takes `[1]`.

### 2.5 Public BSC RPC Endpoints Used

| Endpoint | Role |
|----------|------|
| `bsc-dataseed.binance.org` | Primary BSC RPC |
| `bsc-rpc.publicnode.com` | Fallback BSC RPC |

Both are public pruned nodes; transactions older than ~2–4 weeks become inaccessible.

---

## 3. Wallet Registry

### 3.1 Canonical Naming

The wallets have acquired multiple names across documents. Canonical names are defined here.

| Canonical | TRON address | Aptos address | Role | XOR key |
|-----------|-------------|---------------|------|---------|
| **W1** | `TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP` | `0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e` | Stage 1 primary (eval path) | `2[gWfGj;<:-93Z^C` |
| **W2** | `TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG` | `0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3` | Stage 1 spawn path | `m6:tTh^D)cBz?NM]` |
| **W3** | `TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v` | `0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1` | Stage 2 dead-drop | `2[gWfGj;<:-93Z^C` |
| **W4** | `TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF` | `0x9d202c824402ca89e9aaccd2390b6f8b332ae743caa1469c695feb2781d56519` | Unknown variant (Stage 1?) | Unknown |
| **W5** | `TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH` | `0x3d2075f97b7b1e3234bd653779d21c605d7d8c6ec9c98d983880be5c7f4f9471` | Unknown variant (low-use) | Unknown |

**Naming collision warning:** Early analysis documents (ANALYSIS_REPORT.md, Task AX) use
W1–W3 for what are now W4/W5/W3 respectively. The AX-W crossref (ANALYSIS_AX_W_CROSSREF.md)
resolved this. Always use canonical names above. When reading older docs: AX "W5" = canonical
W1, AX "W6" = canonical W2.

### 3.2 Wallet Status (as of 2026-07-18)

| Wallet | Last dead-drop TX | Days silent | Notes |
|--------|-------------------|-------------|-------|
| W1 | 2026-06-23 02:35 UTC | **25d** | Last ever; JFrog disclosure Jun 24 |
| W2 | 2026-06-20 13:37 UTC | **28d** | Last ever |
| W3 | 2026-06-08 21:29 UTC | **40d** | Last ever |
| W4 | 2026-05-19 15:04 UTC | **60d** (dead-drop) | Any activity: Jun 15 (TRC-10 token receipt) |
| W5 | 2026-02-27 02:27 UTC | **141d** | Confirmed dormant |

All five wallets are silent. Silence pre-dates JFrog disclosure (Jun 24): W3 dark Jun 8
(16d before), W2 dark Jun 20 (4d before), W1 dark Jun 23 (1d before). This is a planned
wind-down, not an emergency shutdown in response to disclosure.

### 3.3 Infrastructure Creation Date

All wallets and Aptos addresses were funded on **2025-11-13** — the actor's infrastructure
setup date, approximately 3 months before the first known victim injection (2026-02-19).

---

## 4. Stage Chain

```
Stage 0 ── Trigger
│  Delivery: astro.config.mjs / postcss.config.mjs / package.json / fa-solid-400.woff2
│  Method: trailing whitespace hiding (>500 chars) OR VSCode folderOpen task
│  Cipher: varies by victim (shuffle cipher seed, or obfuscator.io wrapper)
│  Action: sets global['_V'] = campaign ID; spawns detached node -e Stage 1
│
Stage 1 ── Blockchain Loader
│  Dead-drop: W1 TRON → Aptos A1 fallback → BSC TX → XOR('2[gWfGj;<:-93Z^C')
│  Spawn path: W2 TRON → Aptos A2 fallback → BSC TX → XOR('m6:tTh^D)cBz?NM]')
│  Action: sets C2 globals (_t_s, _t_u, _t_1, _t_2); proceeds to Stage 2
│
Stage 2 ── Boot Payload
│  Dead-drop: W3 TRON → Aptos A3 fallback → BSC TX → XOR('2[gWfGj;<:-93Z^C')
│  OR: direct delivery via C2 /$/boot with Sec-V: <campaign_id> header
│  Action: C2 selection by campaign prefix; requests Stage 3
│  C2 routing: _V[0]=='A' → 166.88.134.62 | numeric → 198.105.127.210
│  Stage 2 XOR key (boot response): ThZG+0jfXE6VAGOJ
│
Stage 3 ── Socket.io RAT Loader
│  Size: ~70–77KB (XOR + LZString UTF16 compressed)
│  Action: installs socket.io-client/axios; injects persistence into apps;
│          sandbox/CI detection; connects to C2 WebSocket
│  Persistence targets: VS Code, Cursor, Antigravity, Discord, GitHub Desktop, npm CLI
│  Injection path: node_modules/@vscode/deviceid/dist/index.js (IDE apps)
│
Stage 4 ── Socket.io WebSocket RAT
│  Served live from C2 (/0x/js or /$/{id})
│  Commands: shell, ss_eval, ss_cb, ss_upf, ss_dir, ss_inz, ss_connect, ss_exit…
│  Build markers: /*RS260605*/, /*C25XXXX*/, /*C26XXXX*/
│
Stage 5 ── Python Infostealer
   Served via /$/{id} after Stage 4 bootstrap
   Targets: browsers, crypto wallet extensions, password managers,
            git credentials, GitHub Desktop, VS Code storage, desktop wallets
   Staging: /tmp/.npm (Linux/macOS) or %USERPROFILE%\.npm (Windows)
   Exfil: POST /u/f + Telegram (token from /u/e endpoint)
   Archive name: <hostname>$<username>.zip
```

---

## 5. C2 Infrastructure

### 5.1 Known C2 IPs

| IP | Location | ASN | Role | Status (2026-07-18) |
|----|----------|-----|------|---------------------|
| `198.105.127.210` | London, GB | AS149440 Evoxt | Primary C2 | Unknown (last confirmed alive 2026-06-18) |
| `166.88.134.62` | — | — | Admin C2 (`_V[0]=='A'` victims) | Unknown |
| `198.105.127.210` port 80 | — | — | C2 fallback | Was DOWN as of 2026-06-18 |
| `166.88.54.158` | — | — | Stage 3 socket.io WebSocket | Unknown |
| `23.27.202.27` | New York, US | AS149440 Evoxt | Secondary C2 (WebSocket only) | Unknown |
| `23.27.13.43` | — | — | A6-prefix victim C2 (Jun 20 Stage 2 only) | Unknown; silently dropped by Jun 25 |
| `136.0.9.8` | — | — | Former C2 (_V=A campaigns) | DEAD as of 2026-06-18 |

All confirmed Evoxt (AS149440) nodes are deliberate — the actor consistently uses this
budget Malaysian VPS provider across all campaigns.

### 5.2 C2 Paths

| Path | Purpose |
|------|---------|
| `/$/boot` | Stage 2 boot beacon (Sec-V: campaign_id header required) |
| `/$/{id}` | Stage 4 / Python payload delivery |
| `/0x/js?_V=...&id=...` | Stage 4 delivery (earlier format) |
| `/u/e` | Telegram token retrieval |
| `/u/f` | File/exfil upload (POST) |
| `/snv` | Environment variable exfil (Stage 4) |
| `/verify-human/{channel}` | Operator status reporting |
| `/d/python.zip`, `/d/python.7z`, `/d/7zr.exe` | Python runtime download |
| `/socket.io/` | WebSocket C2 (Stage 3/4) |
| `/upload` | Data receipt (older C2, 166.88.54.158) |

---

## 6. Cipher and Key Registry

| Key / Seed | Role | Source |
|-----------|------|--------|
| `2[gWfGj;<:-93Z^C` | W1 XOR / W3 XOR / Stage 1 primary | All major variants |
| `m6:tTh^D)cBz?NM]` | W2 XOR / Stage 1 spawn path | All major variants |
| `ThZG+0jfXE6VAGOJ` | Stage 2 boot response XOR | JFrog post; ANALYSIS_CIPHER_SCAN_P.md |
| seed `2667686` | `sfL` cipher (JudeTejada double-IIFE) | ANALYSIS_AJ_JUDETEJADA.md |
| seed `2857687` | `_$_1e42` outer (obfuscator.io wrapper) | ANALYSIS_AX_OBFUSCATOR.md |
| seed `1812138` | `_$af163278` inner (obfuscator.io wrapper) | ANALYSIS_AX_OBFUSCATOR.md |
| seed `36301` | Stage 0 shuffle cipher (5-3-298 postcss) | ANALYSIS_REPORT.md |
| seed `1347634` | Stage 2 shuffle cipher (5-3-298) | ANALYSIS_REPORT.md |
| `_$_1e42` name + seed `2857687` | Standard astro.config.mjs Stage 1 outer cipher | ANALYSIS_AV_ASTRO_SCAN.md |
| `_$af163278` name + seed `1812138` | Inner payload cipher | ANALYSIS_AX_OBFUSCATOR.md |

**Key rotation event (confirmed):** W3 rotated from `cA]2!+37v,-szeU}` to `2[gWfGj;<:-93Z^C`
at the same time W1 rotated (Task X). Current `2[gWfGj;<:-93Z^C` is the live key for both
W1 and W3 channels.

---

## 7. Campaign ID Taxonomy

Campaign IDs are set in Stage 0 as `global['!'] = '<series>-<victim>'`, then prepended
with `'A'` to form `global['_V'] = 'A' + global['!']`. The `_V` value is sent in the
`Sec-V` HTTP header on C2 requests.

### 7.1 Series structure

| Series | Format | Example | C2 routing | Notes |
|--------|--------|---------|-----------|-------|
| 5 | `5-X-Y` | `5-3-298` | `198.105.127.210` | ZurichJS campaigns; X=batch, Y=victim# |
| 8 | `8-NNNN` or `8-NNNN-1` | `8-4435-1` | `198.105.127.210` | Nigerian HNG/DSC-Unilag cluster; `-1` = sub-session |
| 9 | `9-NNNN` | `9-7298` | `198.105.127.210` | Large series; ≥7,298 victims confirmed |
| A6 | `A6-NNN` or `A6-NNN-NN` | `A6-519-79` | `23.27.13.43` (Jun 20) → abandoned | A-prefix batch 6; abandoned in Jun 25 Stage 2 |
| A8 | `A8-**` | `A8-**` | `166.88.134.62` | Literal `**` (not victim-specific); JFrog npm/Go packages |
| 11 | `11-#` | `11-#` | Silently dropped | Literal `#`; atob dropper variant; W1/W2 infrastructure |

`_V[0]` (first char after prepending 'A') determines C2 routing:
- `'A'` → `166.88.134.62` (admin/high-value server)
- Any digit → `198.105.127.210` (production server)

The `A6-` series previously routed to `23.27.13.43`; those victims are now silently dropped
(the Jun 25 Stage 2 removed that routing entry).

### 7.2 Victim scale

| Series | Known max victim# | Source |
|--------|-----------------|--------|
| 9 | 7,298 | `aegre/damian` (`9-7298`), Task AV |
| 8 (sub-series) | 4,435 | `itzvin19` (`8-4435-1`), Task AV |
| 5 | ~298+ | ZurichJS range |
| A6 | 519-85 | Dragon-Lady/linux-supply-chain-guard |
| A8 | (not enumerated — `**` literal) | JFrog post |

Total actor-tracked victims across series 9+8: **≥11,733**.

---

## 8. Delivery Vectors

| Vector | File | Trigger | Obfuscation | Notes |
|--------|------|---------|-------------|-------|
| Build config inject | `astro.config.mjs` | npm build/dev | shuffle cipher or obfuscator.io wrapper | Primary vector; 33+ repos confirmed |
| Build config inject | `postcss.config.mjs` | npm build/dev | shuffle cipher | ZurichJS campaigns |
| Build config inject | `next.config.mjs` | npm build/dev | shuffle cipher | Campaign 5-3-161 |
| Build config inject | `vitest.config.js` | npm test | shuffle cipher | DryhurstDigital |
| Git history rewrite | any | passive | `temp_auto_push.bat` | Actor's OPSEC tool; backdates commits |
| VSCode task | `.vscode/tasks.json` + fake font | folderOpen | WJS IIFE or obfuscator.io | npm/Go package vector; BestCity cluster |
| npm package | `public/fonts/fa-solid-400.woff2` | VSCode task | same | html-to-gutenberg, fetch-page-assets |
| Go module | fake font in repo | VSCode task | same | 16 Nextron-identified packages |
| atob dropper | `eval(atob(...))` wrapper | build hook | wraps Stage 1 | `11-#` campaign; W1/W2 infrastructure |

---

## 9. Known Victim / Infection Clusters

| Cluster | Repos | Campaign IDs | Key doc |
|---------|-------|-------------|---------|
| ZurichJS (farisaziz12) | zurichjs-website | 5-3-161, 5-3-298 | ANALYSIS_REPORT.md |
| Astro cluster (AG/AI) | 33+ astro.config.mjs repos | 5-X-Y, 8-XXXX, 9-XXXX | ANALYSIS_ASTRO_CLUSTER_AI.md |
| Obfuscator.io astro | 4 repos (aegre, CharlieJT, itzvin19 ×2) | 9-7298, 9-7172, 8-4435-1 | ANALYSIS_AV_ASTRO_SCAN.md, ANALYSIS_AX_AV_VICTIMS.md |
| Nigerian HNG/DSC-Unilag | DSC-Unilag, hngx-org, hngi, devcareer, KIHM-02 | 8-**, 8-NNNN | ANALYSIS_AP_ATOB_DROPPER.md |
| JudeTejada | jude-portfolio-v3 | 9-1330-1 + 8 | ANALYSIS_AJ_JUDETEJADA.md |
| Saif72437 | 64 repos swept 2026-06-15 | 8-** (wave 2) | ANALYSIS_SAIF72437.md |
| DryhurstDigital | dryhurstdigital.com | 8-** | ANALYSIS_AQ_DRYHURSTDIGITAL.md |
| atob dropper victims | NikhilGupta777 (13 repos), Rafijohari18 | 11-# | ANALYSIS_AP_ATOB_DROPPER.md, ANALYSIS_AK_RAFI.md |
| npm packages | html-to-gutenberg@4.2.11, fetch-page-assets@1.2.9 | A8-** | JFrog; ANALYSIS_CIPHER_SCAN_P.md |
| Go packages (Nextron) | 16 packages, all repos deleted | A8-** (inferred) | ANALYSIS_AN_GO_PACKAGES.md |

---

## 10. Payload Size / Variant Registry

| SHA (partial) | Size | Campaign | Cipher seed | Notes |
|--------------|------|----------|------------|-------|
| `8e14837c` | 5,533B | `8-**` | `_$_1e42` seed `2857687` | Bulk-deploy; HNG cluster, npm/Go packages |
| `81b3b0ab` | varies | `11-#` | wraps W1/W2 | atob dropper variant; NikhilGupta777, Rafijohari18 |
| — | 5,102–5,103B | `5-X-Y` | shuffle cipher | Early ZurichJS-adjacent payloads |
| — | 8,080B | varies | shuffle cipher | Intermediate variant |
| — | 20,836–21,025B | `8-**`, `9-XXXX` | obfuscator.io outer + `_$_1e42` inner | Latest wave (Jun 2026) |

---

## 11. Separate Actor: BestCity Cluster

**Not PolinRider.** The BestCity cluster shares the VSCode `folderOpen` delivery vector
but has zero infrastructure overlap (different C2, no TRON/BSC, different staging paths).
Attributed to **Contagious Interview / Famous Chollima** sub-cluster.

| Indicator | BestCity | PolinRider |
|-----------|---------|-----------|
| C2 | jsonkeeper.com / api-server-mocha.vercel.app | 198.105.127.210 / 166.88.134.62 |
| Dead-drop | None | TRON + Aptos + BSC |
| Staging | `/tmp/programx64/` or `~/Programs_X64/` | (in-memory eval) |
| Status | Fully decommissioned (2026-07-11, both C2s dead) | Wallets silent; C2 unknown |

See ANALYSIS_AC_BESTCITY_CLUSTER.md and ANALYSIS_AS_BESTCITY_OBFUSCATOR.md.

---

## 12. Operational Timeline

| Date | Event |
|------|-------|
| 2025-11-13 | All wallets (W1–W5) and Aptos addresses funded — infrastructure setup date |
| 2025-11-14 | First Stage 3 RAT payload written to W3 BSC (v1, 71,882B) |
| 2026-02-19 | Campaign 5-3-161 launches (zurich-js/zurichjs-website) |
| 2026-02-25 | 13 W1 + 6 Aptos-only W3 dead-drop updates in 174 min — live debugging against victims |
| 2026-05-04 | Campaign 5-3-161 remediated |
| 2026-05-19 | Campaign 5-3-298 payload pre-staged on W1/W3 (6 days before injection) |
| 2026-05-25 | Campaign 5-3-298 injection; npm packages html-to-gutenberg / fetch-page-assets uploaded |
| 2026-05-26 | Campaign 5-3-298 remediated (21-hour window) |
| 2026-06-08 | W3 last dead-drop TX — Stage 2 channel goes silent |
| 2026-06-15 | W4 receives TRC-10 token (1005141, 970K units) — 33min after NikhilGupta777 sweep |
| 2026-06-20 | W2 last dead-drop TX; `aegre/damian` swept (same day) |
| 2026-06-23 | W1 last dead-drop TX |
| 2026-06-24 | JFrog blog post published (full 5-stage chain, Stage 5 infostealer) |
| 2026-06-25 | Nextron Research: 16 infected Go packages identified; `itzvin19` swept |
| 2026-06-26 | `CharlieJT` swept — last known victim injection |
| 2026-07-03 | `lambda-platform` GitHub org ToS-blocked by GitHub |
| 2026-07-11 | BestCity cluster confirmed fully decommissioned |
| 2026-07-18 | All wallets silent (W1: 25d, W2: 28d, W3: 40d, W4: 60d dead-drop, W5: 141d) |

---

## 13. Actor OPSEC Indicators

| Indicator | Notes |
|-----------|-------|
| `temp_auto_push.bat` | Commit-timestamp-spoofing tool; its presence = prior remote access confirmed |
| Actor test hostnames | `EV-CHQG3L42MMQ`, `EV-4A6OE6M0E2D` (Stage 3 self-exclusion blocklist) |
| Aptos as staging chain | Experimental payloads appear on Aptos before TRON; Aptos-only entries = actor testing |
| BSC TX reversal | `x0` trailer reverses to `0x` prefix — deliberate encoding; not an accident |
| 6-day pre-staging | W1/W3 payload for 5-3-298 written May 19, injection May 25 — planned operations |
| Backdated Go commits | 14 of 16 Go packages have backdated commit timestamps to blend into archival noise |
| Process blocklist MD5 | `9a47bb48b7b8ca41fc138fd3372e8cc0` — MD5 of unknown process name (O-prefix, unidentified) |

---

## 14. IOC Master List

### TRON Wallets
```
TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP   W1 — Stage 1 primary
TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG   W2 — Stage 1 spawn
TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v   W3 — Stage 2
TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF   W4 — unknown variant
TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH   W5 — unknown variant (dormant)
```

### Aptos Addresses
```
0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e   A1 (W1)
0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3   A2 (W2)
0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1   A3 (W3)
0x9d202c824402ca89e9aaccd2390b6f8b332ae743caa1469c695feb2781d56519   (W4)
0x3d2075f97b7b1e3234bd653779d21c605d7d8c6ec9c98d983880be5c7f4f9471   (W5)
```

### C2 IPs
```
198.105.127.210    Primary C2 (AS149440 Evoxt, London)
166.88.134.62      Admin C2 (A-prefix victims)
166.88.54.158      Stage 3 socket.io WebSocket C2
23.27.202.27       Secondary C2 / WebSocket listener (AS149440 Evoxt, New York)
23.27.13.43        A6-prefix victim C2 (Jun 20 Stage 2 only; abandoned Jun 25)
136.0.9.8          Former C2 (DEAD as of 2026-06-18)
```

### XOR Keys
```
2[gWfGj;<:-93Z^C   W1 / W3 / Stage 1-2 primary
m6:tTh^D)cBz?NM]   W2 / Stage 1 spawn
ThZG+0jfXE6VAGOJ   Stage 2 boot response
```

### Blockchain APIs (abused as dead-drop infrastructure)
```
api.trongrid.io
fullnode.mainnet.aptoslabs.com
bsc-dataseed.binance.org
bsc-rpc.publicnode.com
```

### Host Artifacts
```
~/.node_modules                            npm dep install dir (Stage 3)
%LOCALAPPDATA%\Programs\Python\Python3127\ Python runtime (Stage 4, Windows)
/tmp/.npm                                  Exfil staging (Linux/macOS)
%USERPROFILE%\.npm                         Exfil staging (Windows)
<hostname>$<username>.zip                  Exfil archive naming pattern
~/.local/bin/node20                        Planted Node binary (Linux/macOS)
```

### Injected App File Paths (check for build markers `/*RS260605*/` / `/*C25...*/`)
```
<app>/resources/app/node_modules/@vscode/deviceid/dist/index.js   VS Code, Cursor, Antigravity
<app>/resources/app/main.js                                         GitHub Desktop
<discord>/modules/discord_desktop_core[-1]/discord_desktop_core/index.js
<npm root -g>/npm/lib/cli.js
```

### File Hashes
```
# Stage 0 font file (JFrog npm packages)
53abf37710d6f2e35694fbe7cfaf1108127cbc001ce3e6bf994d0486cae5a0e8   fa-solid-400.woff2 (html-to-gutenberg)
13e9a3c41e038bf9d8fcb0831305819819e4f7f4452bc20a04b9bf2756ee22e8   fa-solid-400.woff2 (fetch-page-assets)

# Stage 1 payload (campaign 5-3-298)
d017fe6e8e138630575050902acde5a41a4d676f73eace64ecc47d49262e2330   stage1_decrypted.js

# Stage 4 live payload
c74e11f97168d9f1f3a434248c9d875b0012cca23e90a5940b7bd4a61063172d   stage4_live.js (2026-06-05)
```

### Telegram Exfil
```
Token prefix: 7870147428:AAGbYG...
Chat ID:       7699029999
```

---

## 15. Pending Investigation Items

| Task | Description |
|------|-------------|
| **AO** | W3 silence monitoring — poll for activity break |
| **AY** | W4 payload recovery via BSC archive node (23 TX hashes documented in ANALYSIS_AW_W4W5_ATOB_CORRELATION.md) |
| **AZ** | A6 campaign victim repo hunt + `23.27.13.43` C2 analysis |
| **BA** | Dragon-Lady ChainVeil npm packages — 9 packages (incl. typeorm-encrypt) status + cipher |
| **AA** | MD5 `9a47bb48b7b8ca41fc138fd3372e8cc0` — blocked; needs vendor intel (ANY.RUN/Mandiant) |

---

## 16. Document Index

| Document | Topic |
|----------|-------|
| `ANALYSIS_REPORT.md` | ZurichJS 5-3-298 full incident report (Stage 0–4 decode, liveness) |
| `ANALYSIS_ASTRO_CLUSTER_AI.md` | Full astro.config.mjs infection cluster (29+ repos) |
| `ANALYSIS_AV_ASTRO_SCAN.md` | Obfuscator.io astro variant discovery (4 new victims) |
| `ANALYSIS_AX_OBFUSCATOR.md` | Full obfuscator.io wrapper decode (aegre/damian) |
| `ANALYSIS_AX_STAGE2_LIVE.md` | Live Stage 2/3 pull; C2 routing table |
| `ANALYSIS_AX_W_CROSSREF.md` | AX wallet naming → canonical W1/W2 reconciliation |
| `ANALYSIS_AX_AV_VICTIMS.md` | AX-AV: remaining 3 obfuscator.io victims confirmed W1/W2 |
| `ANALYSIS_AW_W4W5_ATOB_CORRELATION.md` | W4/W5 TX timeline; atob dropper uses W1/W2; 22+3 BSC hashes |
| `ANALYSIS_AP_ATOB_DROPPER.md` | atob dropper anatomy; Nigerian HNG/DSC-Unilag cluster; 8-** payload |
| `ANALYSIS_AK_RAFI.md` | Rafijohari18 atob dropper decode |
| `ANALYSIS_AJ_JUDETEJADA.md` | Double-IIFE; sfL cipher seed 2667686 |
| `ANALYSIS_AQ_DRYHURSTDIGITAL.md` | DryhurstDigital; bat file git timestamp spoofing |
| `ANALYSIS_AR_STAGE5_SCAN.md` | Stage 5 process name hunt; Shai-Hulud/durabletask cluster |
| `ANALYSIS_AN_GO_PACKAGES.md` | 16 Nextron Go packages; all deleted; W1 cipher confirmed |
| `ANALYSIS_CIPHER_SCAN_P.md` | JFrog post full summary; Dragon-Lady cross-ref; all new IOCs |
| `ANALYSIS_AC_BESTCITY_CLUSTER.md` | BestCity cluster overview (separate actor) |
| `ANALYSIS_AS_BESTCITY_OBFUSCATOR.md` | BestCity obfuscator.io variant decode |
| `ANALYSIS_AM_CASHOUT_WALLETS.md` | Cashout wallet analysis |
| `ANALYSIS_AT_WALLET_ENUMERATION.md` | Full wallet enumeration |
| `ANALYSIS_AU_BAT_FILE.md` | temp_auto_push.bat analysis |
| `ANALYSIS_TRON_WALLETS_FULL.md` | Complete TRON wallet transaction history |
| `ANALYSIS_SAIF72437.md` | Saif72437 victim analysis |
