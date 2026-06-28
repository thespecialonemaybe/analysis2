# Task T: Stage 2 Beavertail RAT — Full Decode

**Date:** 2026-06-28  
**Artifact:** `/tmp/b229_stage2_live.js` (77,279 chars, SHA-256 `f9dcca3ea7d32189ff2bc69e46abff78447f7538952e6b7efc511ffa0bfdde4b`)  
**Source:** W3 TRON wallet → BSC `0xb6c725890be6890fd2c735eedc47e24b85a350301f6c19a3864e43c35e470968`, XOR key `2[gWfGj;<:-93Z^C`

---

## Summary

Stage 2 IS Beavertail — not a loader for a separate RAT, but the complete implant. It decodes to
a 337-entry string table and a 65KB JavaScript RAT that performs IDE/tool persistence injection,
socket.io C2 beaconing, clipboard theft, file upload, and arbitrary command execution. A Python
stage launcher is embedded for escalation to Stages 4–5.

String table decompressed: 337 entries, 4,896 chars (UTF-16 LZString compressed to 1,708 chars /
~3,416 raw bytes). Full table at `/tmp/stage2_string_table.json`.

---

## Blob Structure

```
Function("oTNBm2c", "<body>")({UMD module proxy})
```

The body (77,005 raw chars / 74,642 after JSON unescape) contains:

1. **LZString decompressor** (positions 0–9,165): Self-contained LZString library assigned to `lQlUCC`
2. **UMD module proxy boilerplate** (positions 9,165–9,480): AMD/CommonJS/Angular environment check
3. **String table setup** (positions 9,480–20,050): Shuffled IIFE that decompresses `P3NTXh.TL9CGmn`
   (UTF-16 LZString) → `P3NTXh.E72zId` array (337 strings) → `otJYbl(n)` lookup function
4. **RAT code** (positions 20,050–74,642): 337 `otJYbl(0xN)` calls replaced by the string table

---

## Build Stamps

```
VERSION:         260605           (June 5, 2026 — release date of this blob)
Injection stamp: /*RS260605*/     (verified on server; marks current injection as live)

Module compile dates embedded as constants:
  WW8Rik = /*C250617A*/    (June 17, 2025 — original injection module)
  rYg576 = /*C250618A*/    (June 18, 2025)
  PnUMs0D= /*C250619A*/    (June 19, 2025)
  H6zz7vN= /*C250620A*/    (June 20, 2025)
  Hohg484= /*C260511A*/    (May 11, 2026 — newer module)
  NA_5ar = /*C260512A*/    (May 12, 2026)
```

The oldest injection module dates to **June 17, 2025** — one week after the operation launched
(Jun 13 go-live). The actor has been injecting into IDEs from day one. The May 2026 modules
correspond to the `_$_913e`/`_$_b229` cipher transition period.

---

## Boot Sequence

1. Read `global['_H2']` (C2 base URL, set by Stage 1) → stored as `_mMJxE`
2. Read `global['_t_c']` (Stage 1 source), `global['_t_0']` (secondary cipher), `global['_V']` (campaign ID)
3. Fingerprint device:
   - OS info (platform, hostname, username, version)
   - Compute device UUID by hashing the fingerprint
   - `STARTUP_TIME`, `FIRST_VISIT_TIME` recorded
4. **Boot beacon**: `GET _mMJxE/0x/js?_V=<campaign_id>&id=<uuid>$<version>`
   - Response = JS injection payload (checked for `/*RS260605*/` to confirm current version)
5. **Sandbox check** (see below) — if sandbox detected, abort
6. **Inject into all targets** (see below) using the /0x/js response payload
7. **Install socket.io-client + axios** via npm if not already present
8. **Connect to socket.io C2** at `_mMJxE` (same base URL)

---

## C2 Endpoints

All relative to `_H2` (base URL from Stage 1):

| Endpoint | Method | Purpose |
|---------|--------|---------|
| `/0x/js?_V=<campaign_id>&id=<uuid>$<version>` | GET | Boot beacon; returns JS injection payload |
| `/verify-human/<path>` | POST | Human verification gate (unknown exact behavior) |
| `/u/f` | POST (form-data) | File upload — files sent as multipart form |

**External services:**
- `http://ip-api.com/json` — Victim IP/geo data (used by `ss_ip` command)

**Socket.io connection**: Same base URL as `_H2`. The C2 can send `ss_connect:<ip>` to redirect
to a new socket server. Example: `ss_connect:166.88.54.158` → sets `_H2 = http://166.88.54.158:443`.

---

## Persistence: IDE/Tool Injection Targets

The function `sNXeNn(path, appname, overwrite, callback)` injects the `/0x/js` payload into
target files. The injection checks for existing markers before overwriting.

**Injection code format:**
```javascript
global.i='<campaign_id>';global.j=1;<injection_payload>
// then appended to target file
global['r']=require;global['m']=module;
```

### IDEs / Code Editors

| Target | Tag | Windows Path | macOS Path | Linux Path |
|--------|-----|-------------|-----------|-----------|
| VSCode | `app-vscode` | `%LOCALAPPDATA%\Programs\Microsoft VS Code\resources\app\node_modules\@vscode\deviceid\dist\index.js` | `/Applications/Visual Studio Code.app/Contents/Resources/app/node_modules/@vscode/deviceid/dist/index.js` | `/usr/share/code/resources/app/node_modules/@vscode/deviceid/dist/index.js` |
| Cursor | `app-cursor` | `%LOCALAPPDATA%\Programs\cursor\resources\app\node_modules\@vscode\deviceid\dist\index.js` | `/Applications/Cursor.app/Contents/Resources/app/node_modules/@vscode/deviceid/dist/index.js` | `/usr/share/cursor/resources/app/node_modules/@vscode/deviceid/dist/index.js` |
| **Antigravity** | `app-antigravity` | `%LOCALAPPDATA%\Programs\Antigravity\resources\app\node_modules\@vscode\deviceid\dist\index.js` | `/Applications/Antigravity.app/Contents/Resources/app/node_modules/@vscode/deviceid/dist/index.js` | `/usr/share/antigravity/resources/app/node_modules/@vscode/deviceid/dist/index.js` |

**Antigravity** is an AI coding assistant not previously documented in any PolinRider report.
All three IDEs share the same injection point (`@vscode/deviceid/dist/index.js`) because Cursor
and Antigravity are VSCode forks that use the same internal module structure.

### Communication Tools

| Target | Tag | Windows Path | macOS Path | Linux Path |
|--------|-----|-------------|-----------|-----------|
| Discord | `app-discord` | `%AppData%\discord\<ver>\modules\discord_desktop_core-1\discord_desktop_core\index.js` | `~/Library/Application Support/discord/<ver>/modules/discord_desktop_core/index.js` | `/usr/share/discord/modules/discord_desktop_core/index.js` |
| GitHub Desktop | `app-GitHubDesktop` | `%LOCALAPPDATA%\GitHubDesktop\resources\app\main.js` | `/Applications/GitHub Desktop.app/Contents/Resources/app/main.js` | `/usr/share/GitHub Desktop/Contents/Resources/app/main.js` |

### Package Manager

| Target | Tag | Path |
|--------|-----|------|
| npm CLI | `NPM` | `$(npm root -g)/npm/lib/cli.js` |

**npm CLI injection is the supply chain multiplier**: any future `npm install` or `npm publish`
by the victim runs the injected code. This is how the actor silently spreads to new victim
packages without any additional exploit.

---

## Sandbox Detection

Multi-layer evasion checked before injection:

**Environment variables:**
- `process.env['jsbot']` — analysis environment marker
- Device UUID = `EV-CHQG3L42MMQ` or `EV-4A6OE6M0E2D` — known analysis agent IDs

**Hostname patterns:**
- `192.168.*` — private IP (NAT'd lab)
- `Mac-`, `Mac`, `darwin` hostname prefix/suffix
- `.lan` suffix
- Exact strings: `microsoft-standard-WSL2`, `github-runner`, `buildbot`, `build-`, `sandbox-pool-`, `buildkitsandbox`, `cloudchamber`, `(none)`

**User context:**
- Username: `root` → abort

**Windows process check:**
- Runs `tasklist /FO CSV /NH`, extracts process names
- MD5-hashes each process name, checks for `9a47bb48b7b8ca41fc138fd3372e8cc0`
  - This is the MD5 of a specific sandbox monitoring process name (not yet identified — reverse the hash)
- If found: silently exits

---

## Socket.io Command Set

Commands received over socket.io as string `BrWPG5j`:

| Command | Action |
|---------|--------|
| `ss_info` | System report: campaign ID, version, session, OS, C2 URL, upload URL, Node path/version, startup path/time, first visit, connected time, `__dirname`, `__filename` |
| `ss_ip` | Fetch `http://ip-api.com/json` and return victim's IP, ISP, geo |
| `ss_cb` | Steal clipboard content (all platforms) |
| `ss_upf` | Upload file(s) to `/u/f` via axios multipart POST |
| `ss_upd` | Upload entire directory to `/u/f` |
| `ss_dir` | Directory listing |
| `ss_fcd` | File + change directory |
| `ss_stop` | Stop active upload |
| `ss_inz:<appname>` | Re-inject into named app (e.g. `ss_inz:vscode`) |
| `ss_inzx:<path>` | Inject into arbitrary file path |
| `ss_connect:<ip>` | Reconnect socket.io to new IP (sets `_H2=http://<ip>:443`) |
| `ss_eval:<code>` | Evaluate arbitrary JavaScript in-process |
| `ss_eval64:<b64>` | Evaluate base64-decoded JavaScript |
| `ss_exit` | Graceful exit (only if `ilsgb0j` flag set) |
| `ss_exit_f` | Force exit (unconditional) |
| `cd <path>` | Change working directory |
| (any other) | Execute as shell command; return output |

The `ss_eval`/`ss_eval64` commands give the actor unlimited in-process code execution for
escalation — they can deploy Stage 4 (Python bootstrapper) or any new capability without
updating the blockchain dead-drop.

---

## Clipboard Theft (All Platforms)

```javascript
// Windows
powershell -NoProfile -Command "Get-Clipboard"
// macOS
pbpaste
// Linux (with fallback)
xclip -selection clipboard -o
xsel --clipboard --output
```

Clipboard is retrieved via `ss_cb` command or possibly at boot. Cross-platform coverage is complete.

---

## Python Stage Launcher

The Python bootstrapper (Stage 4) is spawned via shell command routing. On Windows, the
`PATH` is modified to prepend `%LOCALAPPDATA%\Programs\Python\Python3127` before execution,
ensuring the actor-installed Python is used. Special command prefix `node **0` spawns a
detached, stdio-ignored child process (for background persistence).

---

## Sandbox ID `9a47bb48b7b8ca41fc138fd3372e8cc0`

The MD5 hash being checked against all running process names is a specific sandbox artifact
process. The hash `9a47bb48b7b8ca41fc138fd3372e8cc0` is not publicly documented. Potential
reverse candidates include VM guest agent processes or analysis environment tools.

This check is platform-specific (Windows only — uses `tasklist`).

---

## Attribution to Beavertail

**Confirmed Beavertail indicators present:**

| Indicator | Source | Present in Stage 2? |
|-----------|--------|---------------------|
| VSCode `@vscode/deviceid` injection | Trend Micro Beavertail report | ✓ |
| socket.io C2 backdoor | JFrog Stage 3 description | ✓ |
| `ss_*` socket command format | Dragon-Lady ChainVeil | ✓ |
| `/u/f` file upload endpoint | JFrog report | ✓ |
| `/verify-human/` endpoint | Dragon-Lady report | ✓ |
| npm CLI injection | Not previously documented | ✓ (new) |
| Antigravity IDE targeting | Not previously documented | ✓ (new) |
| `global['_V']`, `global['_H2']` globals | Our Stage 1 analysis | ✓ |
| `EV-CHQG3L42MMQ`/`EV-4A6OE6M0E2D` sandbox IDs | Not previously documented | ✓ (new) |

**Stage 2 = Stage 3 (unified)**: JFrog described Stage 2 and Stage 3 as separate (Stage 2 beacons to
`/$/boot`, Stage 3 is the socket.io backdoor). In this blob, both functions are unified in the same
77KB payload. The boot beacon is `/0x/js` (not `/$/boot`). Either JFrog analyzed a different version
with separate stages, or the actor merged them after that analysis.

---

## New IOCs

```
# C2 endpoint (relative to _H2 base URL from Stage 1)
/0x/js?_V=<campaign_id>&id=<fingerprint>    ← boot beacon + injection payload fetch
/verify-human/<path>                         ← verification gate
/u/f                                         ← file upload (POST multipart)

# External
http://ip-api.com/json                       ← IP geolocation (victim profiling)

# Injection targets (cross-platform — Windows/macOS/Linux)
@vscode/deviceid/dist/index.js  (VSCode, Cursor, Antigravity)
discord_desktop_core/index.js   (Discord)
main.js                         (GitHub Desktop)
npm/lib/cli.js                  (npm global CLI)

# Previously undocumented application target
Antigravity AI coding assistant (all platforms)

# Sandbox evasion
9a47bb48b7b8ca41fc138fd3372e8cc0   ← MD5 of monitored process name (Windows)
EV-CHQG3L42MMQ                     ← known analysis environment UUID
EV-4A6OE6M0E2D                     ← known analysis environment UUID

# Build version
260605   (Stage 2 version — June 5, 2026)
/*RS260605*/   (injection payload release stamp)

# Socket.io C2 reconnect command format
ss_connect:<ip>   → binds new C2 to http://<ip>:443
```

---

## Relationship to zurichjs Investigation

The zurichjs campaigns delivered Stage 0 (infected `package.json`/`webpack.config.js` files with
embedded `_$_913e`/`_$_b229` cipher). Stage 0 executed Stage 1 (blockchain dead-drop loader), which
fetched this Stage 2 payload via W3 → BSC TX → XOR decrypt → eval.

Any developer who opened an infected zurichjs repository in VSCode (or ran `npm install` on an
infected package) and had network access to the C2 would have had this payload execute. The payload
would then attempt to:
1. Inject itself into their local VSCode installation
2. Connect to the actor's socket.io C2
3. Await commands (file exfil, eval, clipboard theft, Python stage escalation)

The zurichjs infections were **the entry point**; Stage 2 is what executed on each victim's machine.
