# CTI Report: PolinRider Supply-Chain Campaign
### DPRK-Aligned Threat Actor — Developer Targeting via Blockchain Dead-Drops

**TLP: WHITE — Approved for unrestricted distribution**  
**Report date:** 2026-07-23  
**Confidence:** High  
**Distribution:** SOC · Threat Detection · Threat Hunting · IR  
**Classification:** DPRK-nexus / Supply-chain / Full-RAT + Infostealer

---

## Executive Summary

A sophisticated DPRK-aligned threat actor has been conducting an ongoing supply-chain campaign
targeting software developers since at least early 2025. The actor compromises developer machines
through infected open-source repositories, then uses the initial foothold to inject malicious code
into the victim's own repositories — propagating the campaign automatically to anyone who clones
those repos and opens them in VS Code.

**What makes this campaign unusual:**
- Uses **live blockchain transactions** (TRON, Aptos, Binance Smart Chain) as encrypted payload
  dead-drops — no traditional C2 domain that can be sinkholed
- Delivers a **full-featured Node.js RAT** with socket.io WebSocket C2, remote shell, clipboard
  capture, and persistence injection into VS Code, Cursor, GitHub Desktop, and npm
- Follows with a **Python infostealer** targeting browser credentials, wallets, SSH keys,
  environment secrets, and developer tool configs
- Actively maintained: actor updated blockchain dead-drops and C2 routing through June 2026

**Scale:** 750+ infected public repositories (Trend Micro, March 2026); 33+ framework config
files; 9 malicious npm packages; 16 malicious Go packages. Confirmed compromise of repositories
belonging to DataStax, Neutralinojs, ZurichJS, and many independent developers.

**Current status:** Blockchain dead-drop wallets went silent in June 2026 (W1 last active
Jun 23, W2 Jun 20, W3 Jun 8). Production C2 `198.105.127.210` may still respond. The actor
has not been observed deploying new infrastructure as of 2026-07-23; the ZurichJS re-infection
(21 days after first remediation) shows this group re-engages confirmed victims, and
reactivation on new infrastructure cannot be ruled out.

---

## 1. Threat Actor

| Field | Value |
|-------|-------|
| **Actor names** | PolinRider (this investigation), DEV#POPPER (Securonix), Void Dokkaebi (Trend Micro TRU) |
| **Cluster** | Famous Chollima / Contagious Interview (CrowdStrike); Lazarus Group (broader attribution) |
| **Attribution** | DPRK — high confidence (TTPs, infrastructure, targeting, financial motivation) |
| **Motivation** | Financial (crypto theft from developer wallets, credential theft) + intelligence collection |
| **Targeting** | Software developers — primarily JavaScript/TypeScript, Node.js, React, Python ecosystem |
| **Lure** | Fake technical job interviews; recruiters on LinkedIn/Telegram offering coding challenges |
| **Infra creation** | 2025-11-13 (confirmed first blockchain activity); some infected repo commit timestamps date to 2023, but the actor's own commit-backdating TTP (`temp_auto_push.bat`) makes those dates unverifiable |
| **Campaign active** | 2025-11 through 2026-06 (wind-down indicators); potentially resuming |

**Fake job interview lure:** The actor poses as a technical recruiter, invites developers to
a live coding challenge, and asks them to clone a repository and run code locally. The
repository contains the Stage 0 payload — execution begins as soon as the victim opens the
folder in VS Code.

---

## 2. Origin Case: ZurichJS (Campaign 5-3-298)

ZurichJS (`zurich-js/zurichjs-website`) was the investigation entry point. It demonstrates
all primary TTPs in a contained single-org incident.

**Timeline:**
```
2026-02-19  First ZurichJS infection (5-3-161): next.config.mjs injected
2026-05-04  5-3-161 remediated (74-day dwell time)
2026-05-19  W1/W3 blockchain dead-drops pre-staged for next wave (6 days before injection)
2026-05-25  Second injection (5-3-298): postcss.config.mjs injected, commit "fix twint"
            — via compromised developer account farisaziz12 (GH ID 53216647)
            — active window: 21 hours 14 minutes
2026-05-26  5-3-298 remediated
```

**Initial access mechanism:** The initial access vector for `farisaziz12` is **not confirmed**.
The actor had persistent remote access to the developer's machine — evidenced by the use of
`temp_auto_push.bat` and the two separate injection events 21 days apart. How the machine was
first compromised is unknown; candidates include the fake job interview lure (the documented
primary vector for this campaign), infection via cloning another compromised repository, or
phishing/credential theft. The actor retained that access and used the `temp_auto_push.bat`
commit-tampering tool to re-inject the second payload:

1. Script extracts original commit metadata (author, email, timestamp, message)
2. System clock is temporarily altered to match the original commit date
3. Commit is amended with the malicious payload (payload hidden after 2,700 trailing spaces)
4. Pushes with `--no-verify` (bypasses pre-commit hooks) and `--force`

The result is a commit indistinguishable from the legitimate developer's work in `git log`.

**Why ZurichJS matters as an origin case:**
- Two re-infections of the same org (21 days apart) shows actor persistence after detection
- 6-day pre-staging of blockchain dead-drops before injection shows planned operations
- Confirmed attacker had persistent remote access (not just one-time payload drop)
- Infrastructure overlap between campaigns 5-3-161 and 5-3-298 is 100% (same C2, same wallets)

---

## 3. Attack Chain (Stage 0 → 5)

```
DEVELOPER OPENS REPO IN VS CODE
         │
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 0 — Trigger                                                   │
│  Files: astro.config.mjs / postcss.config.mjs / next.config.mjs    │
│         fa-solid-400.woff2 (fake font) / package.json postinstall   │
│  Trigger: build/dev run, or VSCode folderOpen task                  │
│  Action: sets global['!'] = campaign ID; spawns detached node       │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 1 — Blockchain Loader (~4–5 KB obfuscated JS)                 │
│  Calls TRON → Aptos fallback → BSC to retrieve encrypted Stage 2    │
│                                                                     │
│  TRON:  GET api.trongrid.io/v1/accounts/<wallet>/transactions       │
│         ↳ raw_data.data (hex) → reverse UTF-8 → BSC TX hash        │
│  Aptos: GET fullnode.mainnet.aptoslabs.com/v1/accounts/<addr>/txns  │
│         ↳ payload.arguments[0] → BSC TX hash (direct)              │
│  BSC:   eth_getTransactionByHash(hash)                              │
│         ↳ result.input → split('?.?')[1] → XOR decrypt → Stage 2   │
│                                                                     │
│  Rate-limit guard: 30-second cooldown via global['_p_t']            │
│  Two paths: eval() + child_process.spawn (detached, windowsHide)   │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 2 — Boot Payload                                              │
│  Routes to C2 HTTP server based on campaign ID prefix:             │
│  Fetches Stage 3 via GET <C2>/$/boot (not blockchain)              │
│  C2 routing by campaign prefix:                                     │
│    'A...'  → 166.88.134.62 (admin pool) [or 23.27.13.43 Jun 20-25] │
│    '5-...' → 198.105.127.210 (production)                           │
│    numeric → 198.105.127.210                                        │
│  GET <C2>/$/boot  with header  Sec-V: <campaign_id>                 │
│  Response XOR key: ThZG+0jfXE6VAGOJ → eval(Stage 3)                │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 3 — Socket.io RAT Loader                                      │
│  Installs: socket.io-client, axios, form-data → ~/.node_modules     │
│  Persistence injection into (if present):                           │
│    VS Code / Cursor / Antigravity:                                  │
│      <app>/resources/app/node_modules/@vscode/deviceid/dist/index.js│
│    GitHub Desktop: <app>/resources/app/main.js                      │
│    Discord: discord_desktop_core/index.js                           │
│    npm CLI: npm/lib/cli.js                                          │
│  Sandbox/CI check: blocks on AWS/Azure/GCP/Kali/GitHub runner hints │
│  Reports env vars to C2 /snv                                        │
│  Connects WebSocket to 166.88.54.158                                │
│  Marker: /*RS260605*/ or /*C25...*/ appended to injected files      │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 4 — socket.io WebSocket RAT (77 KB JS)                        │
│  Commands supported:                                                │
│    Remote shell (any OS command), directory change                  │
│    File upload (single file or recursive directory)                 │
│    Clipboard read, public IP lookup                                 │
│    Arbitrary JS eval (ss_eval: / ss_eval64:)                        │
│    Forced process exit                                               │
│  Victim registration: hostname, PID, OS type, campaign ID,          │
│                       first/current timestamps                       │
│  Installs Python runtime if missing (Windows: python.zip/7z;        │
│    Linux/macOS: pip via bootstrap.pypa.io)                          │
│  Requests Stage 5: GET <C2>/$/<id>  (Sec-V: campaign_id)            │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 5 — Python Infostealer (Beavertail/OmniStealer variant)       │
│  Targets: browser credentials (Chrome, Firefox, Safari, Brave)      │
│           crypto wallets (MetaMask, Phantom, etc.)                  │
│           SSH private keys (~/.ssh/)                                │
│           GPG keys                                                  │
│           Shell history (bash, zsh)                                 │
│           .env files (all directories)                               │
│           AWS / GCP / Azure credentials (~/.aws, ~/.config)         │
│           npm tokens (~/.npmrc)                                     │
│           Kubernetes configs (~/.kube)                              │
│  Exfil: ZIP archive → <hostname>$<username>.zip                     │
│         Telegram bot (token prefix 7870147428:AAGbYG...,            │
│                       chat ID 7699029999)                           │
│         Upload to C2 /u/e and /u/f                                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Delivery Vectors

| Vector | Trigger | Target audience |
|--------|---------|-----------------|
| `astro.config.mjs` injection | `npm run dev/build` (Astro framework) | Frontend/full-stack devs |
| `postcss.config.mjs` injection | Any PostCSS-using build | React/Next.js devs |
| `next.config.mjs` injection | `npm run dev/build` (Next.js) | Next.js devs |
| `.vscode/tasks.json` + `fa-solid-400.woff2` | VS Code folderOpen (trusted workspace) | Any VS Code user |
| npm package (postinstall / side-effect import) | `npm install` | Any npm user |
| Go module | `go get` / module import | Go developers |
| atob dropper | eval(atob(...)) in build config | JavaScript/Node.js/React developers |

**Key insight:** The `.vscode/tasks.json` vector is self-propagating — once a developer is
infected, the actor plants the `tasks.json` in their other repositories, infecting anyone
who later clones those repos and opens them in VS Code.

---

## 5. Persistence Mechanisms

After Stage 3 runs, the malware persists by modifying application files. Detection markers:

| Application | Injected file | Search string |
|-------------|--------------|---------------|
| VS Code / Cursor / Antigravity | `<app>/resources/app/node_modules/@vscode/deviceid/dist/index.js` | `/*RS260605*/` or `/*C25` |
| GitHub Desktop | `<app>/resources/app/main.js` | `/*RS260605*/` |
| Discord | `<discord>/modules/discord_desktop_core[-1]/discord_desktop_core/index.js` | `/*RS260605*/` |
| npm CLI | `<npm root -g>/npm/lib/cli.js` | `/*RS260605*/` |

**This means every npm install or VS Code session re-executes the malware.**

---

## 6. Host-Based Detection

### 6.1 Suspicious filesystem artifacts

```
~/.node_modules/               — npm package dir planted by Stage 3 (legitimate path is
                                 ~/.npm, not ~/.node_modules)
~/.local/bin/node20            — planted Node.js binary (Linux/macOS)
%LOCALAPPDATA%\Programs\Python\Python3127\  — Python runtime planted by Stage 4 (Windows)
/tmp/.npm                      — exfil staging directory (Linux/macOS)
%USERPROFILE%\.npm             — NOTE: legitimate npm cache dir; suspicious only if it
                                 contains a file matching <hostname>$<username>.zip
*.zip matching <hostname>$<username>.zip  — exfil archive (look in /tmp/.npm or %USERPROFILE%\.npm)
```

### 6.2 File content search (all platforms)

Hunt for these exact strings in source files and build configs:

```
# Campaign ID marker in JS files
global\['!'\]\s*=\s*'[0-9A]

# Variant 2 marker
global\[['"]_V['"]\]

# TRON dead-drop lookup (Stage 1)
api\.trongrid\.io

# Aptos dead-drop lookup (Stage 1)
fullnode\.mainnet\.aptoslabs\.com

# BSC payload separator
\?\.?\?

# XOR key strings (both known keys)
2\[gWfGj;<:-93Z\^C
m6:tTh\^D\)cBz\?NM\]

# Known TRON wallet addresses
TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP
TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG
TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v

# Persistence marker in app files
/\*RS260605\*/
```

### 6.3 YARA rules

```yara
rule PolinRider_Stage1_Loader {
    meta:
        description = "PolinRider Stage 1 blockchain loader — detects XOR keys and dead-drop strings"
        tlp = "WHITE"
        confidence = "high"
    strings:
        $xor1 = "2[gWfGj;<:-93Z^C" ascii
        $xor2 = "m6:tTh^D)cBz?NM]" ascii
        $tron = "api.trongrid.io" ascii
        $aptos = "fullnode.mainnet.aptoslabs.com" ascii
        $wallet_w1 = "TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP" ascii
        $wallet_w2 = "TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG" ascii
        $wallet_w3 = "TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v" ascii
        $marker_v = "global['_V']" ascii
        $marker_bang = "global['!']" ascii
    condition:
        any of ($xor1, $xor2) or
        (2 of ($tron, $aptos, $wallet_w1, $wallet_w2, $wallet_w3)) or
        ($marker_v and ($tron or $aptos))
}

rule PolinRider_Persistence_Marker {
    meta:
        description = "PolinRider Stage 3 persistence injection marker in app files"
        tlp = "WHITE"
        confidence = "high"
    strings:
        $marker1 = "/*RS260605*/" ascii
        $marker2 = "/*C25" ascii
        $anchor1 = "socket.io-client" ascii
        $anchor2 = "global['_p_t']" ascii
        $anchor3 = "ThZG+0jfXE6VAGOJ" ascii
    condition:
        $marker1 or $anchor3 or
        (2 of ($anchor1, $anchor2)) or
        ($marker2 and any of ($anchor1, $anchor2, $anchor3))
}

rule PolinRider_Stage0_FakeFont {
    meta:
        description = "PolinRider fake font file containing JavaScript payload"
        tlp = "WHITE"
        confidence = "high"
    strings:
        $js_sig1 = "global['!']" ascii
        $js_sig2 = "global['_V']" ascii
        $spaces = { 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 }  // 16+ spaces (padding pattern)
    condition:
        (uint32be(0) != 0x774F4632) and  // not real WOFF2 magic (big-endian: 77 4F 46 32)
        ($spaces and ($js_sig1 or $js_sig2)) and
        (filename matches /\.woff2$/ or filename matches /astro\.config/ or
         filename matches /postcss\.config/ or filename matches /next\.config/)
}

rule PolinRider_VSCode_TasksJson {
    meta:
        description = "PolinRider malicious VSCode tasks.json with folderOpen autorun"
        tlp = "WHITE"
        confidence = "high"
    strings:
        $runo = "\"runOn\": \"folderOpen\"" ascii
        $hide = "\"hide\": true" ascii
        $woff = ".woff2" ascii
        $node = "node " ascii
    condition:
        filename matches /tasks\.json$/ and
        $runo and ($hide or ($woff and $node))
}
```

---

## 7. Network-Based Detection

### 7.1 C2 IP addresses

All campaign C2 infrastructure is hosted on **AS149440 Evoxt Sdn. Bhd.**

| IP | Role | Status | Ports |
|----|------|--------|-------|
| `198.105.127.210` | Primary production C2 | **Active** (last checked 2026-07-18) | 80, 443, 5985, 27017 |
| `166.88.134.62` | Admin C2 (A-prefix victims) | Unverified (port 5985 confirmed; HTTP not probed) | 5985 |
| `166.88.54.158` | Stage 3 socket.io WebSocket C2 | Unknown | — |
| `23.27.202.27` | Secondary C2 / WebSocket | Unverified (port 5985 confirmed; HTTP not probed) | 5985 |
| `23.27.13.43` | A6-prefix victim C2 (Jun 20–25 only) | Offline | — |
| `136.0.9.8` | Former C2 | Dead (since 2026-06-18) | — |

**Block all of the above at perimeter.** Any outbound connection to these IPs from a developer
workstation is a high-confidence indicator of compromise.

### 7.2 Blockchain dead-drop domains

These are legitimate public blockchain APIs being abused. Blocking them outright may
impact legitimate cryptocurrency usage — prefer alerting and investigating hits:

```
api.trongrid.io
fullnode.mainnet.aptoslabs.com
bsc-dataseed.binance.org
bsc-rpc.publicnode.com
```

**Context:** PolinRider is the only known malware family that queries `api.trongrid.io`
and `fullnode.mainnet.aptoslabs.com` from developer workstations. Any Node.js process
making HTTPS requests to both of these domains is highly suspicious.

### 7.3 Sigma detection rules

```yaml
# Rule 1: PolinRider C2 beacon (Sec-V header)
title: PolinRider C2 Boot Beacon
id: a1b2c3d4-e5f6-7890-abcd-ef1234567890
status: stable
description: Detects the PolinRider Stage 2 /$/boot beacon with campaign ID header
tlp: WHITE
logsource:
  category: proxy
  product: any
detection:
  selection:
    cs-uri-path|contains: '/$/boot'
    cs-headers|contains: 'Sec-V:'
  condition: selection
falsepositives:
  - None known; path and header combination is highly specific
level: high
tags:
  - attack.command_and_control
  - attack.t1071.001

---
# Rule 2: Node.js blockchain API access (Stage 1 dead-drop)
title: PolinRider Blockchain Dead-Drop Fetch
id: b2c3d4e5-f6a7-8901-bcde-f01234567891
status: stable
description: >
  Detects Node.js processes querying TRON or Aptos APIs — the signature
  dead-drop pattern of PolinRider Stage 1 loaders.
tlp: WHITE
logsource:
  category: dns
detection:
  selection_tron:
    dns.question.name: 'api.trongrid.io'
  selection_aptos:
    dns.question.name: 'fullnode.mainnet.aptoslabs.com'
  condition: selection_tron or selection_aptos
falsepositives:
  - Legitimate blockchain developers querying these APIs directly
level: medium
tags:
  - attack.command_and_control
  - attack.t1102.001

---
# Rule 3: Detached Node.js process with -e flag (Stage 1 spawn path)
title: PolinRider Detached Node Eval Spawn
id: c3d4e5f6-a7b8-9012-cdef-012345678902
status: stable
description: >
  Detects child_process.spawn of node with -e (eval) flag in detached mode —
  the Stage 1 spawn execution path used by PolinRider to deliver Stage 2.
tlp: WHITE
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    ParentImage|endswith:
      - '\node.exe'
      - '\node'
    Image|endswith:
      - '\node.exe'
      - '\node'
    CommandLine|contains:
      - ' -e '
      - ' --eval '
  filter_devtools:
    CommandLine|contains:
      - 'jest'
      - 'mocha'
      - 'webpack'
  condition: selection and not filter_devtools
falsepositives:
  - Some build tools spawn node -e for inline scripts
level: medium
tags:
  - attack.execution
  - attack.t1059.007

---
# Rule 4: WinRM connection to known PolinRider C2 IPs
title: PolinRider WinRM C2 Connection
id: d4e5f6a7-b8c9-0123-defa-123456789013
status: stable
description: >
  Detects outbound WinRM (TCP 5985) connections to known PolinRider C2 IPs.
  WinRM is used by the actor for remote administration of their Windows C2 servers.
tlp: WHITE
logsource:
  category: network_connection
detection:
  selection:
    dst_port: 5985
    dst_ip:
      - '198.105.127.210'
      - '166.88.134.62'
      - '23.27.202.27'
      - '23.27.13.43'
  condition: selection
falsepositives:
  - None expected; these IPs are confirmed malicious
level: critical
tags:
  - attack.command_and_control
  - attack.t1021.006

---
# Rule 5: VS Code / npm file modification (Stage 3 persistence)
title: PolinRider Persistence Injection into Developer Tools
id: e5f6a7b8-c9d0-1234-efab-234567890124
status: experimental
description: >
  Detects modification of VS Code, npm, or Discord application files by a
  non-installer process — consistent with PolinRider Stage 3 persistence.
tlp: WHITE
logsource:
  category: file_event
  product: windows
detection:
  selection_paths:
    TargetFilename|contains:
      - '\resources\app\node_modules\@vscode\deviceid\dist\index.js'
      - '\resources\app\main.js'
      - '\discord_desktop_core\index.js'
      - '\npm\lib\cli.js'
  filter_installer:
    Image|contains:
      - '\Update.exe'
      - '\installer'
      - '\setup'
  condition: selection_paths and not filter_installer
falsepositives:
  - Application updates — tune the installer filter
level: high
tags:
  - attack.persistence
  - attack.t1554
```

---

## 8. Blockchain IOCs

These are permanent, immutable on-chain records and cannot be "taken down."

### TRON Dead-Drop Wallets

| Wallet | Canonical name | Role | Status (2026-07-18) |
|--------|---------------|------|---------------------|
| `TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP` | W1 | Stage 1 primary loader | Silent 25 days (last TX Jun 23) |
| `TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG` | W2 | Stage 1 spawn path | Silent 28 days (last TX Jun 20) |
| `TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v` | W3 | Stage 2 dead-drop | Silent 40 days (last TX Jun 8) |
| `TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF` | W4 | Unknown variant | Silent 60+ days |
| `TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH` | W5 | Dormant | Silent 141+ days |

**Detection:** Any internal asset querying the TRON blockchain for transactions from these
wallet addresses should be treated as an active Stage 1 infection.

### Aptos Fallback Addresses

| Address | Wallet pair | Role |
|---------|------------|------|
| `0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e` | W1 | Stage 1 fallback |
| `0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3` | W2 | Stage 1 fallback |
| `0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1` | W3 | Stage 2 fallback |

**Note:** If W1/W2/W3 resume sending new TRON transactions, the campaign has reactivated.
Monitor these addresses.

---

## 9. File Hashes

| Hash (SHA-256) | File | Stage |
|---------------|------|-------|
| `53abf37710d6f2e35694fbe7cfaf1108127cbc001ce3e6bf994d0486cae5a0e8` | `fa-solid-400.woff2` (html-to-gutenberg npm) | Stage 0 |
| `13e9a3c41e038bf9d8fcb0831305819819e4f7f4452bc20a04b9bf2756ee22e8` | `fa-solid-400.woff2` (fetch-page-assets npm) | Stage 0 |
| `d017fe6e8e138630575050902acde5a41a4d676f73eace64ecc47d49262e2330` | Stage 1 decrypted payload (5-3-298) | Stage 1 |
| `c74e11f97168d9f1f3a434248c9d875b0012cca23e90a5940b7bd4a61063172d` | Stage 4 live RAT (2026-06-05) | Stage 4 |
| `1a6283f5fd8fadf6ed71558c31c6ecc2e392ba9e4915201c2c9557b7e7b94a9d` | `lib.min.js` (tailwindcss-merge npm, malicious) | Stage 0/1 |
| `cc074a2f99e5bdfa7acde7d9dd6620771a3d6c9a71e023e50c1853df8681a43d` | `lib.min.js` (typeorm-encrypt npm, v1.0.2) | Stage 0/1 |
| `b373c2d8b6479a9acdb2fadbd35d312e8bd70975c8a3a3247b2aa9df6c3ef0e4` | `lib.min.js` (sass-formats npm) | Stage 0/1 |

---

## 10. Malicious npm Packages (removed but known)

All removed from npm on 2026-06-11. Presence in `package.json` or `package-lock.json` is
an indicator of past exposure.

| Package | Impersonates | Campaign series | Removed |
|---------|-------------|-----------------|---------|
| `tailwindcss-merge` | `tailwind-merge` | A6 | 2026-06-11 |
| `sass-formats` | `sass-formatter` | A6 (A6-519-79 confirmed) | 2026-06-11 |
| `sass-format` | `sass-formatter` | A6 | 2026-06-11 |
| `tailwindcss-animates-kit` | `tailwindcss-animate` | A6 | 2026-06-11 |
| `tailwindcss-animatics` | `tailwindcss-animate` | A6 | 2026-06-11 |
| `clsx-tailwind` | `clsx` users | A6 | 2026-06-11 |
| `rate-limit-flexible` | `rate-limiter-flexible` | A6 | 2026-06-11 |
| `rate-limits-flexible` | `rate-limiter-flexible` | A6 | 2026-06-11 |
| `typeorm-encrypt` | `typeorm-encrypted-column` | A6 | 2026-06-11 |
| `html-to-gutenberg` | `html-to-gutenberg` (hijacked) | A8 | 2026-06 |
| `fetch-page-assets` | `fetch-page-assets` (hijacked) | A8 | 2026-06 |

**Hunt action:** Search internal artifact repositories (Nexus, Artifactory, npm caches)
and developer workstation `package-lock.json` files for any of these package names.

---

## 11. Threat Hunting Queries

### 11.1 Hunt: Blockchain dead-drop API calls from developer machines

```
# Splunk / Elastic (proxy logs)
(dest_host="api.trongrid.io" OR dest_host="fullnode.mainnet.aptoslabs.com")
AND src_category="workstation"
| stats count by src_ip, user, dest_host, _time
```

```
# EDR process network — look for node.exe calling these hosts
process_name IN ("node.exe", "node")
AND dest_host IN ("api.trongrid.io", "fullnode.mainnet.aptoslabs.com",
                  "bsc-dataseed.binance.org", "bsc-rpc.publicnode.com")
```

### 11.2 Hunt: /$/boot beacon

```
# Proxy / firewall logs
uri_path CONTAINS "/$/boot"

# Or by header
request_headers CONTAINS "Sec-V:"
AND dst_ip IN ("198.105.127.210", "166.88.134.62", "166.88.54.158",
               "23.27.202.27", "23.27.13.43")
```

### 11.3 Hunt: Detached node -e processes

```
# Windows (Sysmon EventID 1)
ParentImage: "node.exe"
Image: "node.exe"
CommandLine|contains: " -e "
NOT CommandLine|contains: "jest|mocha|webpack|ts-node"
```

### 11.4 Hunt: Malicious package in lockfiles (retroactive exposure)

Search all developer workstations and CI environments for `package-lock.json` or
`yarn.lock` files containing any of the malicious package names listed in Section 10.

```bash
# Find on Linux/macOS
find / -name "package-lock.json" -exec grep -l \
  "tailwindcss-merge\|sass-formats\|typeorm-encrypt\|rate-limit-flexible\|clsx-tailwind" {} \;
```

### 11.5 Hunt: VS Code / app file modification markers

```bash
# Grep for persistence markers in VS Code installation
grep -r "RS260605\|_p_t\|ThZG+0jfXE6VAGOJ" \
  "/Applications/Visual Studio Code.app" \
  "$HOME/.vscode" \
  "$(npm root -g)/npm/lib/" 2>/dev/null
```

### 11.6 Hunt: Malicious ~/.node_modules directory

```bash
# Flag — this directory should not exist for normal users
ls -la ~/.node_modules 2>/dev/null && echo "SUSPICIOUS: ~/.node_modules exists"
```

### 11.7 Hunt: Exfil archive pattern

```
# File creation events — hostname$username.zip pattern
file.name MATCHES ".*\$.*\.zip$"
AND file.directory IN ("/tmp/.npm", "%USERPROFILE%\.npm")
```

---

## 12. Incident Response Checklist

If PolinRider is detected on a workstation:

**Immediate containment:**
- [ ] Isolate the workstation from the network (but preserve for forensics)
- [ ] Revoke all tokens/secrets accessible from that machine:
  - GitHub / GitLab / Bitbucket personal access tokens
  - npm auth tokens (`~/.npmrc`)
  - AWS/GCP/Azure credentials (`~/.aws/credentials`, `~/.config/gcloud`)
  - SSH private keys (generate new keypairs)
  - Browser-saved passwords (treat all as compromised)
  - Crypto wallet seed phrases / private keys
- [ ] Notify any organizations whose repositories the developer has push access to

**Assess propagation:**
- [ ] Review all repositories the developer has committed to in the past 6 months
      (ZurichJS dwell was 74 days on first infection; assume multi-month access)
- [ ] Check each for `.vscode/tasks.json` with `runOn: folderOpen`
- [ ] Check each for suspicious injections in `astro.config.mjs`, `postcss.config.mjs`,
  `next.config.mjs`, or unexpected binary files (`.woff2`) in source directories
- [ ] Alert collaborators who may have cloned those repositories

**Remove persistence:**
- [ ] Search for and remove `/*RS260605*/` markers from application files (see Section 5)
- [ ] Check `~/.node_modules` and remove if present
- [ ] Remove `~/.local/bin/node20` if present
- [ ] Review VS Code, Cursor, GitHub Desktop, Discord, npm for injected code

**Re-image decision:**
Given Stage 4's full remote shell capability, assume the attacker had unrestricted access.
Re-image is recommended for any workstation where Stage 3 or later was reached.

---

## 13. Actor OPSEC Notes

- **Infrastructure provider:** 100% Evoxt Sdn. Bhd. (AS149440) — any new Evoxt IP used
  in developer-targeting attacks should be treated as potential PolinRider infrastructure
- **WinRM fleet signature:** 4 of 6 confirmed C2 IPs have port 5985 (WinRM) open
  (`198.105.127.210`, `166.88.134.62`, `23.27.202.27`, `23.27.13.43`) — the actor
  manages their Windows C2 infrastructure via PowerShell Remoting
- **Campaign wind-down indicators:** Wallet silence precedes public disclosure by weeks
  (W3 silent 16 days before JFrog Jun 24 post; W2 4 days before; W1 1 day before).
  The actor monitors threat intel feeds and proactively retires infrastructure.
- **No infrastructure rotation:** The five TRON wallet addresses and two XOR keys have
  never been rotated across the confirmed campaign lifetime (2025-11-13 to 2026-06). Only the obfuscation
  wrapper changed when detected.
- **Commit backdating:** `temp_auto_push.bat` forgeries match original commit timestamps
  exactly. Do not rely on commit dates for triage — use file content, not metadata.
- **6-day pre-staging:** W1/W3 dead-drop payloads for campaign 5-3-298 were written
  6 days before the ZurichJS injection — the actor plans injections in advance.
- **Self-exclusion:** Stage 3 contains a blocklist of actor test hostnames:
  `EV-CHQG3L42MMQ`, `EV-4A6OE6M0E2D`. Decoys or honeypots using these names will
  not be infected.

---

## 14. IOC Summary (Machine-Readable)

```
# NETWORK — C2 IPs (block/alert)
198.105.127.210
166.88.134.62
166.88.54.158
23.27.202.27
23.27.13.43
136.0.9.8

# NETWORK — C2 ports
5985/tcp (WinRM — fleet management signature)
27017/tcp (MongoDB — C2 backend)
443/tcp (HTTPS C2)
80/tcp (HTTP C2)

# NETWORK — Abused legitimate domains (alert, do not block without investigation)
api.trongrid.io
fullnode.mainnet.aptoslabs.com
bsc-dataseed.binance.org
bsc-rpc.publicnode.com

# NETWORK — C2 paths
/$/boot
/$/{id}
/u/e
/u/f
/snv
/verify-human/{channel}
/socket.io/

# NETWORK — C2 HTTP headers
Sec-V: <value>    (Stage 2/3/4 requests; value = campaign ID)

# FILE — XOR keys (binary or string match)
2[gWfGj;<:-93Z^C
m6:tTh^D)cBz?NM]
ThZG+0jfXE6VAGOJ

# FILE — Wallet strings
TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP
TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG
TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v
TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF
TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH

# FILE — Persistence marker
/*RS260605*/

# FILE — Suspicious directories
~/.node_modules
%LOCALAPPDATA%\Programs\Python\Python3127\

# HASH — SHA-256
53abf37710d6f2e35694fbe7cfaf1108127cbc001ce3e6bf994d0486cae5a0e8
13e9a3c41e038bf9d8fcb0831305819819e4f7f4452bc20a04b9bf2756ee22e8
d017fe6e8e138630575050902acde5a41a4d676f73eace64ecc47d49262e2330
c74e11f97168d9f1f3a434248c9d875b0012cca23e90a5940b7bd4a61063172d
1a6283f5fd8fadf6ed71558c31c6ecc2e392ba9e4915201c2c9557b7e7b94a9d
cc074a2f99e5bdfa7acde7d9dd6620771a3d6c9a71e023e50c1853df8681a43d
b373c2d8b6479a9acdb2fadbd35d312e8bd70975c8a3a3247b2aa9df6c3ef0e4

# BLOCKCHAIN — TRON wallets (monitor for new transactions = campaign reactivation)
TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP    W1
TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG    W2
TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v    W3
TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF    W4
TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH    W5

# BLOCKCHAIN — Aptos addresses
0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e
0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3
0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1

# EXFIL — Telegram
Bot token prefix: 7870147428:AAGbYG
Chat ID: 7699029999
```

---

## 15. References and Further Reading

| Source | Date | Notes |
|--------|------|-------|
| Trend Micro TRU — Void Dokkaebi | Apr 2026 | `temp_auto_push.bat` analysis; 750+ repo scale |
| Securonix — DEV#POPPER | 2025–2026 | Stage 3–5 RAT/infostealer detail |
| JFrog Security Research — ChainVeil | 2026-06-24 | npm packages; full 5-stage chain; VSCode task vector |
| Nextron Research | 2026-06-25 | 16 Go packages (update to JFrog post) |
| Amazon Inspector | 2026-06-11 | 9 ChainVeil A6-series npm packages; OSV MAL-2026-5625 through 5633 |

**Internal investigation documents:** `CAMPAIGN_MASTER.md` (synthesis); `ANALYSIS_REPORT.md`
(ZurichJS case study); `OVERVIEW_C2_INFRASTRUCTURE.md` (full C2 registry);
`ANALYSIS_BA_CHAINVEIL_NPM.md` (A6 npm packages); `ANALYSIS_AZ_A6_SCOPE_C2.md` (C2 analysis).
