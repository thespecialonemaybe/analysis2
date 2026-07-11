# Task AR: Stage 5 Persistence Path Scan — GitHub Search Results

**Date:** 2026-07-11  
**Method:** GitHub code search for `gh-token-monitor.service`, `pgmonitor.py`, `/tmp/transformers.pyz`

---

## Summary

All three IOCs are publicly documented under the "Shai-Hulud" / "Mini Shai-Hulud" / "TanStack
supply chain" campaign cluster (DPRK / Sapphire Sleet / BlueNoroff, May 2026). They originate
from a **separate DPRK cluster** with different C2 infrastructure than PolinRider — no IP or
domain overlap with `166.88.134.62`, `198.105.127.210`, or `23.27.202.27`.

No actual Stage 5 persistence artifacts from real infections were found on GitHub. All 600+
search hits across the three terms are security detection scripts, advisories, or IOC feeds.

---

## Search Results

| IOC | GitHub hits | Real artifact hits | Assessment |
|-----|------------|---------------------|------------|
| `gh-token-monitor.service` | 187 | 0 | Detection docs only |
| `pgmonitor.py` | 127 | 0 | Detection docs + PostgreSQL FP |
| `transformers.pyz` | 280 | 0 | Detection docs only |

**Real artifact search (filename-exact)**: `gh-token-monitor.service` as filename → 0 results.
Stage 5 artifacts live on victims' filesystems; they aren't committed to repos.

---

## Public Campaign Attribution

### Mini Shai-Hulud (TanStack npm, May 11, 2026)

| IOC | Value |
|-----|-------|
| C2 | `git-tanstack.com`, `api.masscan.cloud`, `filev2.getsession.org`, `seed1.getsession.org` |
| Payload files | `router_init.js`, `tanstack_runner.js` |
| Persistence (Linux) | `gh-token-monitor.service` → `~/.config/systemd/user/gh-token-monitor.service` |
| Persistence (macOS) | `com.user.gh-token-monitor.plist` → `~/Library/LaunchAgents/` |
| Persistence binary | `~/.local/bin/gh-token-monitor.sh` |
| Token file | `~/.config/gh-token-monitor/token` |
| Claude Code target | `~/.claude/router_runtime.js` |
| VS Code target | `~/.vscode/router_runtime.js` |
| Sigma rule | `SigmaHQ/sigma` rules-emerging-threats (2026-05-12) |

The Claude Code-specific path (`~/.claude/router_runtime.js`) is notable: the actor is
explicitly targeting Claude Code users, consistent with the PolinRider victim profile
(developers using Claude Code to work on Astro/Node.js projects).

### durabletask PyPI (May 19, 2026)

| IOC | Value |
|-----|-------|
| C2 (primary) | `check.git-service.com` → `160.119.64.3` |
| C2 (secondary) | `t.m-kosche.com` → `185.95.159.32` |
| Package | `durabletask` 1.4.1 / 1.4.2 / 1.4.3 (PyPI maintainer account takeover) |
| Stage 2 payload | `rope.pyz` (fetched from C2, 28,703 bytes, SHA256: `069ac1dc...`) |
| Persistence binary (root) | `/usr/bin/pgmonitor.py` |
| Persistence binary (user) | `~/.local/bin/pgmonitor.py` |
| Persistence service | `pgsql-monitor.service` |
| OSSF ID | MAL-2026-4174 |
| Capabilities | Multi-cloud cred theft (AWS/GCP/Azure/K8s/Vault), 85 credential paths, GitHub dead-drop C2 (FIRESCALE pattern), geotargeted wiper (Israel/Iran), Russia locale exclusion |

`/tmp/transformers.pyz` — search results include this in Shai-Hulud/durabletask IOC lists but
the OSSF entry confirms the actual dropped file is `rope.pyz`. `transformers.pyz` may refer to
a variant or a misattributed IOC.

---

## Infrastructure Comparison

| Field | PolinRider | Mini Shai-Hulud | durabletask |
|-------|-----------|-----------------|-------------|
| C2 IPs | `166.88.134.62` / `198.105.127.210` / `23.27.202.27` | `git-tanstack.com` / `api.masscan.cloud` | `160.119.64.3` / `185.95.159.32` |
| Blockchain dead-drop | TRON + Aptos (W1–W5) | None documented | GitHub commits (FIRESCALE) |
| Stage 4 | Beavertail RAT | Unknown | Credential stealer (rope.pyz) |
| Persistence name | Unknown (not documented) | `gh-token-monitor` | `pgsql-monitor` / `pgmonitor.py` |
| Attribution | DPRK / Lazarus / Moonstone Sleet | DPRK / Sapphire Sleet / BlueNoroff | DPRK / Sapphire Sleet / BlueNoroff |
| IP overlap | — | None | None |

PolinRider uses TRON blockchain dead-drops (unique to this cluster); the Shai-Hulud clusters
use domain-based C2. Same actor group (DPRK), different operational units or toolkits.

---

## Why These IOCs Were in the Task Queue

The `gh-token-monitor.service`, `pgmonitor.py`, and `transformers.pyz` artifacts were likely
identified as known DPRK Stage 5 indicators from the public Shai-Hulud reports, and added to
the scan queue to check whether any PolinRider victims had documented them.

**Result**: No such overlap found. PolinRider's own Stage 5 (what Beavertail drops as
persistence) uses different artifact names that are not yet documented in public GitHub
repositories.

---

## New IOCs (from public reports, not previously in our registry)

| IOC | Type | Campaign |
|-----|------|---------|
| `check.git-service.com` | C2 domain | durabletask (May 2026) |
| `t.m-kosche.com` | C2 domain secondary | durabletask |
| `160.119.64.3` | C2 IP | durabletask |
| `185.95.159.32` | C2 IP secondary | durabletask |
| `git-tanstack.com` | C2 domain | Mini Shai-Hulud (May 2026) |
| `api.masscan.cloud` | C2 domain | Mini Shai-Hulud |
| `filev2.getsession.org` | C2 domain | Mini Shai-Hulud |
| `rope.pyz` | Stage 2 payload filename | durabletask |
| `router_init.js` | Stage 2 payload | Mini Shai-Hulud |
| `tanstack_runner.js` | Stage 2 payload | Mini Shai-Hulud |
| `~/.claude/router_runtime.js` | Persistence path | Mini Shai-Hulud (Claude Code target) |
| `~/.vscode/router_runtime.js` | Persistence path | Mini Shai-Hulud |
| `pgsql-monitor.service` | Persistence service | durabletask |
| SHA256 `ab4fcada...` | `router_init.js` | Mini Shai-Hulud (StepSecurity IOC) |
| SHA256 `2ec78d55...` | `tanstack_runner.js` | Mini Shai-Hulud (StepSecurity IOC) |
| SHA256 `069ac1dc...` | `rope.pyz` (28,703B) | durabletask |

---

## Outcome

**Scan result: no hits.** No GitHub repositories were found containing actual Stage 5
persistence artifacts from PolinRider or the related Shai-Hulud clusters. The IOC search
confirms that these DPRK clusters are actively tracked by the security community (Sigma rules,
OSSF malicious-packages, Socket.dev, Netskope, SafeDep) but their persistence artifacts do not
appear in public source repositories.

**Open gap (unchanged):** PolinRider's Stage 5 persistence artifact names are still unknown.
The `ANALYSIS_BEAVERTAIL_T.md` document (Stage 4 analysis) would be the source to check for
what the Beavertail RAT drops as Stage 5 persistence on Linux/macOS.

---

## Related Documents

- `ANALYSIS_AX_STAGE2_LIVE.md` — Stage 4 = Beavertail, beacon: `166.88.134.62:443`
- `ANALYSIS_BEAVERTAIL_T.md` — Stage 4 full analysis (Stage 5 persistence paths)
- `OVERVIEW_C2_INFRASTRUCTURE.md` — C2 IP routing table
- `ANALYSIS_C2_LIVENESS_U.md` — C2 liveness data
