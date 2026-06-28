# Task Z: Dragon-Lady sources.md Review

**Date:** 2026-06-28  
**Task:** Read Dragon-Lady `docs/sources.md` (18KB) and `docs/advisory.md` (25KB) to extract
new intel on ChainVeil/PolinRider not already in our analysis.

---

## Summary

The Dragon-Lady advisory references three critical new findings for this investigation:
1. **npm publisher identity confirmed: `successkeyteck`** (Checkmarx report)
2. **New XOR key: `ThZG+0jfXE6VAGOJ`** — HTTP C2 response decryption key (SafeDep report)
3. **Malicious PR attack on `Egonex-AI/Understand-Anything`** (57K+ stars) — first documented
   PolinRider supply-chain attack via GitHub PR, not npm (SafeDep report)
4. **Two additional hijacked npm packages**: `html-to-gutenberg@4.2.11` and
   `fetch-page-assets@1.2.9` (both 2026-05-25, now removed)
5. **Stage 4/5 Linux persistence paths** documented by Dragon-Lady (new IOCs)
6. **Additional new DPRK npm packages** from OX Security (separate campaign track)

---

## Key Finding 1: npm Publisher — `successkeyteck`

Source: Checkmarx "ChainVeil: A Malicious npm Supply Chain Attack by SuccessKey"

All 9 Dragon-Lady packages (Task W) were published by npm account **`successkeyteck`**.
The account has been suspended/cleared — search returns 0 packages as of 2026-06-28.
Total downloads across the 9 packages: **3,293** (Checkmarx figure, vs our ~3,100 estimate).

This resolves Task W's unknown publisher question.

---

## Key Finding 2: Third XOR Key — `ThZG+0jfXE6VAGOJ`

Source: SafeDep "Supply Chain Attack Analysis: astro.config.mjs Malware"

Known XOR keys for this campaign:

| Key | Role | Channel |
|-----|------|---------|
| `2[gWfGj;<:-93Z^C` | Blockchain payload decryption | W1, W3 (current) |
| `m6:tTh^D)cBz?NM]` | Blockchain payload decryption | W2 (current) |
| `cA]2!+37v,-szeU}` | Blockchain payload decryption | W3 (historical, pre-Feb 25 2026) |
| **`ThZG+0jfXE6VAGOJ`** | **HTTP C2 response decryption** | Stage 1 → C2 HTTP response |

`ThZG+0jfXE6VAGOJ` is a **fourth key**, used to decrypt the HTTP response body when Stage 1
beacons to the C2 (not the blockchain payload). The SafeDep report describes two separate XOR
operations in one Stage 1 variant:
1. XOR with `ThZG+0jfXE6VAGOJ` to decrypt the C2 HTTP response
2. XOR with `2[gWfGj;<:-93Z^C` to decrypt the blockchain-fetched Stage 2

This suggests the C2 HTTP response is itself XOR-encrypted — a layer not previously documented
in our analysis of the `/0x/js` endpoint (which returned plaintext `/*RS260605*/` JS). Either:
- The `ThZG+0jfXE6VAGOJ` layer was used in an older Stage 1 variant before the `/*RS260605*/` format
- Or the XOR step applies to a different C2 endpoint/response than `/0x/js`

**This key is not in any prior public PolinRider report.** New IOC.

---

## Key Finding 3: Malicious PR Attack — `Egonex-AI/Understand-Anything`

Source: SafeDep "Supply Chain Attack Analysis: astro.config.mjs Malware"

PolinRider's first documented **malicious pull request** attack against a large open-source project:

- **Target**: `Egonex-AI/Understand-Anything` — 57,000+ GitHub stars
- **PRs**: #198, #206, #261 — all authored by actor account `AsimRaza10` (now suspended)
- **Payload location**: `homepage/astro.config.mjs` — JavaScript build config file, not a package
- **Delivery**: Stage 1 loader embedded in Astro config, executes on `npm install` or build

The infrastructure is **identical** to all other PolinRider variants:
- TRON W1 (`TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP`) → BSC → XOR → Stage 2
- C2: `166.88.54.158` (prefix "A"), `198.105.127.210` (numeric), `23.27.202.27:27017` (fallback)
- Cipher: `_$_1e42`, shuffle marker `rmcej%otb%`, seed `2857687`

**Significance:** The actor is not limiting attacks to npm packages or fake job repos. Any popular
open-source project that accepts PRs from unknown contributors is a potential delivery vehicle.
A maintainer merging PR #206 would have distributed the payload to all downstream users.

---

## Key Finding 4: Two Additional Hijacked npm Packages

Source: Dragon-Lady advisory.md (referencing JFrog report)

| Package | Malicious version | Published | Status |
|---------|------------------|-----------|--------|
| `html-to-gutenberg` | **v4.2.11** | 2026-05-25 | Removed — `latest` still at v4.2.10 |
| `fetch-page-assets` | **v1.2.9** | 2026-05-25 | Removed — `latest` still at v1.2.8 |

Both were published on the **same day (2026-05-25)** — 6 days after Wave 1 (May 19) packages and
13 days before Wave 2 (June 7). This is a mid-campaign addition not in Dragon-Lady's or the
Checkmarx package list.

Both are legitimate packages with long histories (2024+) that were **account-hijacked** to insert
a malicious version bump. The package names do not match the PolinRider CSS-tool naming pattern —
these are generic utility packages with established user bases, making them higher-impact hijacks.
Version metadata for the malicious versions has been purged from the CDN.

---

## Key Finding 5: Stage 4/5 Linux Persistence Paths

Source: Dragon-Lady `docs/advisory.md` — supply-chain persistence checks section

New persistence IOCs not previously documented in our analysis:

```
/tmp/transformers.pyz                                     ← Stage 4 Python bootstrapper artifact
~/.config/systemd/user/gh-token-monitor.service          ← Stage 5 persistence (systemd user)
~/.local/bin/gh-token-monitor.sh                          ← Stage 5 shell launcher
~/.config/gh-token-monitor/                               ← Stage 5 config directory
~/.config/systemd/user/pgsql-monitor.service              ← Stage 5 persistence (variant)
/etc/systemd/system/pgsql-monitor.service                 ← Stage 5 persistence (system-wide)
~/.local/bin/pgmonitor.py                                  ← Stage 5 Python infostealer
/usr/bin/pgmonitor.py                                      ← Stage 5 Python infostealer (system)
```

The service names (`gh-token-monitor`, `pgsql-monitor`) are chosen to blend in with developer
tooling. `gh-token-monitor` implies it watches for GitHub tokens (credential theft). `pgsql-monitor`
implies database monitoring — both are plausible service names a developer might not question.

`/tmp/transformers.pyz` is the Python bootstrapper (Stage 4 in JFrog's terminology) — a zipapp
that installs and runs the Python infostealer (Stage 5).

---

## Key Finding 6: OX Security DPRK npm RAT Packages (separate track)

Source: Dragon-Lady advisory.md — "DPRK npm RAT dependency indicators"

These packages are attributed to DPRK/Famous Chollima but use **different C2 infrastructure**
from PolinRider — no blockchain dead-drop, different beacon path:

| Package | Published | Revoked | Notes |
|---------|-----------|---------|-------|
| `terminal-logger-utils` | 2026-05-20 | 2026-05-22 | v0.1.0–v1.1.2 |
| `ts-logger-pack` | 2026-04-01 | 2026-05-22 | v0.0.1–v1.1.3 |
| `pretty-logger-utils` | — | — | Not found in registry |
| `pinno-loggers` | — | — | Not found in registry |

C2 indicators (different from PolinRider):
- Beacon path: `/api/validate/keyboard-events` (not `/0x/js` or `/$/boot`)
- Exfil artifact: `pwdKeyString` (password keylogger)
- Second C2: Telegram Bot API (not socket.io WebSocket)
- Payload file: `utils.cjs`

This is a **separate DPRK/Famous Chollima sub-campaign** — same threat actor group but different
implant architecture. Likely a parallel operation by a different sub-team.

---

## New IOCs Summary

| IOC | Type | Notes |
|-----|------|-------|
| `ThZG+0jfXE6VAGOJ` | XOR key | HTTP C2 response decryption — 4th campaign key |
| `successkeyteck` | npm account | Publisher of all 9 Dragon-Lady packages — suspended |
| `AsimRaza10` | GitHub account | Actor-controlled PR account — suspended |
| `html-to-gutenberg@4.2.11` | npm version | Malicious hijack (pub 2026-05-25, removed) |
| `fetch-page-assets@1.2.9` | npm version | Malicious hijack (pub 2026-05-25, removed) |
| `/tmp/transformers.pyz` | Filesystem path | Stage 4 Python bootstrapper artifact |
| `gh-token-monitor.service` | Systemd service | Stage 5 persistence (GitHub token harvester) |
| `pgsql-monitor.service` | Systemd service | Stage 5 persistence variant (database monitor) |
| `~/.local/bin/pgmonitor.py` | Filesystem path | Stage 5 Python infostealer |
| `Egonex-AI/Understand-Anything` | GitHub repo | 57K-star repo targeted via malicious PRs |
| `/api/validate/keyboard-events` | HTTP path | OX Security RAT C2 beacon (separate campaign) |
| `terminal-logger-utils` | npm package | OX Security DPRK RAT (revoked 2026-05-22) |
| `ts-logger-pack` | npm package | OX Security DPRK RAT (revoked 2026-05-22) |

---

## New Sources

| Source | URL | Relevance |
|--------|-----|-----------|
| Checkmarx ChainVeil | checkmarx.com/zero-post/chainveil-a-malicious-npm-supply-chain-attack-by-successkey/ | Publisher `successkeyteck`, full package list, C2/wallet IOCs |
| SafeDep Astro C2 | safedep.io/astro-config-blockchain-c2-supply-chain/ | `ThZG+0jfXE6VAGOJ` key, `Egonex-AI` PR attack, astro.config.mjs vector |
| OX Security DPRK RAT | ox.security/blog/north-korean-npm-infostealer-rat/ | Separate DPRK npm RAT packages, `/api/validate/keyboard-events` C2 |

---

## New Tasks Spawned

- **AG**: Investigate `Egonex-AI/Understand-Anything` PR attack — check if PRs were merged,
  whether the 57K-star project's users were exposed, and whether `AsimRaza10` has other
  actor-controlled PR submissions across GitHub
- **AH**: Decode `ThZG+0jfXE6VAGOJ` key usage — find the Stage 1 variant that uses this key,
  determine which channel/response it decrypts, and confirm whether it's still in use
