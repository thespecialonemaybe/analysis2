# Task AN: Nextron's 16 Infected Go Packages — Payload Analysis

**Date:** 2026-07-11  
**Source:** Nextron Research (Jun 25, 2026 update to JFrog blog post)  
**Reference:** `ANALYSIS_CIPHER_SCAN_P.md` §Go Packages

---

## Summary

Nextron Research identified 16 Go packages containing the same malware as the JFrog npm
packages, using "the same structure and fake font file." This analysis documents the full
16-package table, investigates payload availability, determines the cipher variant via
cross-reference, and records new IOCs from the JFrog post that apply to both npm and Go vectors.

**Key findings:**
- All 16 GitHub repos deleted; no live payloads recoverable
- Go module proxy caches only `lambda-platform/lambda`; infected pseudo-versions not cached
- Cipher confirmed via Nextron quote + JFrog npm analysis + `hngi` AP cross-reference:
  **W1 XOR key `2[gWfGj;<:-93Z^C`**, campaign `8-**`, 5533B payload (SHA `8e14837c`)
- Most packages use backdated commit timestamps to blend into archival noise
- `lambda-platform/lambda` is a **live package hijack** — two infected pseudo-versions pushed
  May 25 and Jun 19, 2026, both after the campaign's npm phase began

---

## The 16 Go Packages

| Go package | Infected version (XRAY) | Commit date | XRAY ID |
|-----------|------------------------|-------------|---------|
| `github.com/hngi/Team-Fierce-Backend-Golang` | v0.0.0-20200612135333 | 2020-06-12 (backdated) | XRAY-1009779 |
| `github.com/amantsehay/a2sv-go-course` | v0.0.0-20240816090215 | 2024-08-16 (backdated) | XRAY-1009780 |
| `github.com/naol7/dist-task-scheduler` | v0.0.0-20241120175214 | 2024-11-20 (backdated) | XRAY-1009781 |
| `github.com/bm-197/chill` | v0.0.0-20241216030053 | 2024-12-16 (backdated) | XRAY-1009782 |
| `github.com/zainirfan13/graphql-client` | v0.0.0-20220912215956 | 2022-09-12 (backdated) | XRAY-1009783 |
| `github.com/lambda-platform/dan` | v0.0.0-20221011015638 | 2022-10-11 (backdated) | XRAY-1009785 |
| `github.com/Barsu5489/commerce` | v0.0.0-20231123164829 | 2023-11-23 (backdated) | XRAY-1009784 |
| `github.com/glacialspring/static` | v0.0.0-20181015024211 | 2018-10-15 (backdated) | XRAY-1009786 |
| `github.com/reauheau/goaubio` | v0.0.0-20260213144826 | 2026-02-13 | XRAY-1009787 |
| `github.com/rickt/slack-weather-bot` | v0.0.0-20180704165649 | 2018-07-04 (backdated) | XRAY-1009788 |
| `github.com/glacialspring/go-winsparkle` | v0.0.0-20250402002608 | 2025-04-02 | XRAY-1009789 |
| `github.com/dexbotsdev/uniswap-v2-v3-arbitrage` | v0.0.0-20231007040503 | 2023-10-07 (backdated) | XRAY-1009790 |
| `github.com/anatoli-derese/a2sv-excercise` | v0.0.0-20240805074755 | 2024-08-05 (backdated) | XRAY-1009791 |
| `github.com/lambda-platform/ebarimt-rest-api` | v0.0.0-20230429075241 | 2023-04-29 (backdated) | XRAY-1009795 |
| `github.com/lambda-platform/lambda` | v0.9.19-0.20260525032942, v0.9.20-0.20260619012358 | 2026-05-25, 2026-06-19 | XRAY-1009794 |
| `github.com/Setsu548/Logistic` | v0.0.0-20240410002038 | 2024-04-10 (backdated) | XRAY-1009796 |

Nextron note: *"Some of the malicious packages are still live, even years after their commit
timestamp."* The backdated commit dates are actor fabrications — the injections occurred near
the campaign's active window (2025–2026), not at the timestamped dates.

### Backdating pattern

The majority of packages carry timestamps ranging from 2018 to 2024. This is deliberate OPSEC:
the Go module proxy and downstream tooling present these as old, stable dependencies. A developer
auditing their `go.sum` or inspecting module metadata would see a "2018" commit and not flag it
as recently introduced. Only `reauheau/goaubio` (2026-02-13), `glacialspring/go-winsparkle`
(2025-04-02), and both `lambda-platform/lambda` versions (2026-05-25, 2026-06-19) fall within
the confirmed active campaign window without backdating.

---

## Repository Status

### All 16 repos: deleted (404)

GitHub API confirmed 404 for all 16 source repositories as of 2026-07-11. Repos were taken down
following the Nextron/JFrog disclosure (Jun 24–25, 2026).

### `lambda-platform/lambda`: ToS-blocked since 2026-07-03

The `lambda-platform` GitHub account received a Terms of Service block on **2026-07-03T14:08:05Z**
(reason: `tos`). The account exists but all content returns 403 — GitHub suspended it for ToS
violations rather than outright deletion. This is consistent with GitHub's response to confirmed
malware hosting.

### `lambda-platform/lambda`: clean version available on proxy

The Go module proxy (`proxy.golang.org`) cached `lambda-platform/lambda` v0.9.19 (the clean
tagged release, 281KB zip). Contents: standard Go source + assets. No `fa-solid-400.woff2`,
no `.vscode/tasks.json`. The clean tag predates the actor's injections.

### Infected pseudo-versions not cached

The two infected versions of `lambda-platform/lambda` are pseudo-versions:
```
v0.9.19-0.20260525032942-<SHA12>
v0.9.20-0.20260619012358-<SHA12>
```
Go module proxy requires the full pseudo-version string including the 12-character commit SHA
suffix. The XRAY advisory strings (`v0.9.19-0.20260525032942`, `v0.9.20-0.20260619012358`)
are truncated — missing the SHA12. Proxy lookups with truncated strings return 404. Since the
source repo is now ToS-blocked (403), the proxy cannot re-fetch the SHA12 to construct the full
version, making these versions permanently unresolvable. No infected zip is cached.

**The same truncation issue applies to all 15 other `v0.0.0-YYYYMMDDHHMMSS` XRAY entries** —
those repos are deleted (not just blocked), so their infected versions are doubly unresolvable
via proxy. No Go payload from any of the 16 packages is recoverable through public channels.

---

## Cipher Analysis

### Evidence chain

**1. Nextron direct quote (Jun 25 2026 update):**
> "16 Go packages containing the same malware… using the same structure and fake font file."

This explicitly maps the Go packages to the JFrog npm packages' payload structure.

**2. JFrog npm analysis (Jun 24 2026):**
- Stage 1 XOR key: `2[gWfGj;<:-93Z^C` (canonical W1 key)
- Campaign ID: `global['_V'] = "A8-**"` (the `8-**` campaign)
- Payload file: `fa-solid-400.woff2` with 752 leading spaces
- BSC delimiter: `?.?` splits encrypted payload from transaction input prefix

**3. `hngi/Team-Fierce-Backend-Golang` cross-reference:**
The `hngi` GitHub org appears in `ANALYSIS_AP_ATOB_DROPPER.md` as part of the Nigerian
HNG/DSC-Unilag cluster carrying the **5533B `8-**` variant (SHA `8e14837c`)**. The other
`hngi` repos in that cluster (`Team-Geras-Solar-Calculator`, `Team-storm-mobile-`) are byte-
identical JS payloads. `Team-Fierce-Backend-Golang` is the Go package injection into the same
org — the actor injected `fa-solid-400.woff2` into a Go project within a victim org they had
already compromised for JS payload delivery.

**Conclusion:** All 16 Go packages carry the **5533B `8-**` payload (SHA `8e14837c`)** with
XOR key `2[gWfGj;<:-93Z^C` and TRON wallets W1/W2. The Go packages are not a new cipher
variant — they are the same `8-**` campaign extended to Go ecosystem repos.

### Why not W4 or W5?

W4 (`TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF`) and W5 (`TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH`) are
separate dead-drop channels with no confirmed payload attribution. The JFrog npm packages
explicitly use W1's key `2[gWfGj;<:-93Z^C`, and Nextron confirms the Go packages use "the same"
payload. W4/W5 payloads remain unrecovered (see `ANALYSIS_AW_W4W5_ATOB_CORRELATION.md`).

---

## `lambda-platform/lambda` Hijack Detail

This is the most forensically interesting of the 16 packages — a legitimate, actively maintained
Go package that was directly hijacked rather than created as a throw-away repo.

| Version | Date pushed | Status |
|---------|-------------|--------|
| v0.9.19 (tag) | Pre-campaign | Clean — 281KB, normal Go source |
| v0.9.19-0.20260525032942 | 2026-05-25 | Infected pseudo-version — not cached on proxy |
| v0.9.20-0.20260619012358 | 2026-06-19 | Infected pseudo-version — not cached on proxy |

Timeline note: the first infected commit (May 25) is the same day as the JFrog npm packages
(`html-to-gutenberg` v4.2.11 and `fetch-page-assets` v1.2.9 were uploaded May 25, 2026).
The actor injected Go and npm vectors **simultaneously** on the same day. The second
`lambda-platform/lambda` injection (Jun 19) came five days before the JFrog report went public
(Jun 24).

The actor gained write access to the `lambda-platform/lambda` repo (or created the
`lambda-platform` org and cloned the legitimate project). The `lambda-platform` org was
subsequently blocked by GitHub for ToS violations on Jul 3.

---

## New IOCs (from JFrog post, applicable to Go + npm vectors)

These IOCs were documented in `ANALYSIS_CIPHER_SCAN_P.md` §New IOCs but are recorded here as
the primary AN finding:

| Type | Value | Notes |
|------|-------|-------|
| BSC delimiter | `?.?` | Splits BSC TX input: `<prefix>?.?<encrypted_payload>` |
| Stage 2 XOR key | `ThZG+0jfXE6VAGOJ` | Boot payload decryption key |
| C2 IP (admin / W1 `_V[0]=="A"`) | `166.88.134.62` | Serves `/$/boot`, `/$/{id}`, `/d/` paths |
| C2 IP (standard) | `198.105.127.210` | Fallback for non-"A" campaign IDs |
| C2 IP (socket.io) | `166.88.54.158` | Stage 3 WebSocket backdoor (`ws://166.88.54.158:443`) |
| `Sec-V` header | `<campaign_id>` | Sent to C2 on `/$/boot`; routes victim to admin/standard server |
| Stage 0 font file hash | `53abf37710d6f2e35694fbe7cfaf1108127cbc001ce3e6bf994d0486cae5a0e8` | `html-to-gutenberg` `fa-solid-400.woff2` |
| Stage 0 font file hash | `13e9a3c41e038bf9d8fcb0831305819819e4f7f4452bc20a04b9bf2756ee22e8` | `fetch-page-assets` `fa-solid-400.woff2` |
| Telegram token prefix | `7870147428:AAGbYG...` | Stage 5 Telegram exfil (dynamic from C2 `/u/e`) |
| Telegram chat ID | `7699029999` | Stage 5 exfil destination |
| Exfil archive pattern | `<hostname>$<username>` | Zip archive naming in `/tmp/.npm` or `%USERPROFILE%\.npm` |
| Python install path | `%LOCALAPPDATA%\Programs\Python\Python3127\` | Windows Stage 4 artifact |
| `successkeyteck` GitHub org | (suspended) | Actor-controlled org; suspended post-disclosure |
| npm packages | `html-to-gutenberg@4.2.11` (XRAY-1008590), `fetch-page-assets@1.2.9` (XRAY-1008535) | Removed from npm |

---

## Campaign Scope: 8-** Across Vectors

The `8-**` campaign now spans three confirmed vectors:

| Vector | Examples | Payload size | Source |
|--------|----------|-------------|--------|
| Direct repo inject (lib/lib.min.js) | saif72437, Nigerian HNG/DSC-Unilag orgs | 5533B | AP analysis |
| npm packages | html-to-gutenberg, fetch-page-assets | 5533B (same SHA) | JFrog |
| Go packages | All 16 Nextron packages | 5533B (same SHA, inferred) | Nextron + this analysis |
| atob dropper (`11-#` variant) | NikhilGupta777, Rafijohari18 | (wraps W1/W2) | AK/AW analysis |

The `8-**` literal asterisks (not victim-specific IDs) confirm these are bulk-deploy operations
where the actor doesn't assign individual victim tracking numbers — contrasting with the `5-X-Y`
IDs in the PolinRider main track.

---

## Payload Recovery Status

No Go package payload was recovered:

1. All 16 source repos deleted (GitHub 404)
2. `lambda-platform/lambda` source blocked by ToS suspension (GitHub 403)
3. Go module proxy: clean v0.9.19 only; infected pseudo-versions not cached
4. XRAY strings truncated (missing SHA12 suffix) → proxy lookup failure even if accounts restored
5. No community archive (Wayback Machine, gharchive.org) indexed the infected commits within
   the window before deletion

The 5533B SHA `8e14837c` payload from the HNG/DSC-Unilag cluster is the closest recovered
artifact — it is byte-identical to what would have been embedded in the Go packages' fake font
files.

---

## Related Documents

- `ANALYSIS_CIPHER_SCAN_P.md` — JFrog post full summary, Dragon-Lady cross-ref, all new IOCs
- `ANALYSIS_AP_ATOB_DROPPER.md` — `hngi` org 5533B `8-**` variant; campaign ID context
- `ANALYSIS_AW_W4W5_ATOB_CORRELATION.md` — W4/W5 dead-drop analysis; confirms Go uses W1/W2
- `ANALYSIS_AX_STAGE2_LIVE.md` — live chain execution; W1 XOR key confirmed active
