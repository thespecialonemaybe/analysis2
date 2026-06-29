# Task AF: Campaign ID `10-010` — Routing and Operator Identification

## Overview

`madeeldev/flutter-vpn` contains a `_$_1e42` PolinRider payload with campaign ID `10-010`.
This ID uses the series-10 prefix — the first series-10 instance documented in this investigation.
The batch-push timestamp reveals the actual infection date as **2026-06-07**, despite the commit
being forged to appear as a 2022 commit.

---

## Payload Analysis

**File**: `public/fonts/fa-solid-400.woff2` (5,102 bytes)
**Cipher**: `_$_1e42` (seed 2667686, same as saif72437 cluster — Task N)
**Activation codes**: `Tgw(2509); return 1358` — same as Task N/O (saif72437 batch)

```javascript
global['!'] = '10-010';   // campaign ID
var _$_1e42 = (function(l,e){ ... })(...);  // shuffle cipher
// sfL → pYd → Stage 1 TRON dead-drop chain (identical to all other _$_1e42 variants)
```

Payload is byte-identical in size (5,102 bytes) and activation codes to the saif72437 `8-765`
cluster. Different campaign ID; same payload template.

---

## Campaign ID Routing

```
global['!'] = '10-010'
         ↓  (Stage 2 sets)
global['_V'] = 'A' + '10-010'  =  'A10-010'
         ↓
_V[0] == 'A'  →  old routing: 23.27.13.43 (dead since before Jun 25 2026)
               current routing (Jun 25 Stage 2): SILENT DROP
```

`10-010` victims receive no C2 beacon — routed to a dead server in the old routing and silently
dropped in the current Stage 2. These victims are not being actively exfiltrated.

The `10-` series corresponds to campaign ID space beyond the `8-` and `9-` series documented in
the `astro.config.mjs` cluster. Series assignment appears to be per-delivery-vector:
- Series `8-xxxx`: astro.config.mjs + `fa-solid-400.woff2` VSCode task infections
- Series `9-xxxx`: astro.config.mjs infections (higher IDs, later infections)
- Series `10-xxx`: `fa-solid-400.woff2` VSCode task infections — separate deployment batch

---

## Victim: `madeeldev` Developer Profile

Muhammad Adeel — Pakistani developer, active GitHub account since 2019.

```
Account created: 2019 (Leetcode Java repos)
Languages: Dart/Flutter (primary), PHP, JavaScript, Java, C#
Repos: 30+ covering student projects spanning 2019–2024
```

The developer's machine was compromised in early June 2026. Stage 2 ran on the infected machine
and swept **8 repos** in a 2-minute window using `temp_auto_push.bat` (or equivalent).

---

## Batch Infection: 8 Repos in 2 Minutes (2026-06-07)

All 8 repos share `pushed_at` between 02:29 and 02:31 UTC on 2026-06-07 — a sweep of the
victim's entire local git clone collection:

| Repo | `pushed_at` | Language | Payload injected |
|------|-------------|----------|-----------------|
| `admin-dashboard` | 02:29:13 | PHP | No — no `public/fonts/` structure |
| `flutter-doctor-consultation-app` | 02:29:58 | Dart | Yes — `fa-solid-400.woff2` (5,102B) |
| `flutter-simple-login-signup` | 02:30:02 | Dart | Yes — `fa-solid-400.woff2` (5,102B) |
| `flutter-vpn` | 02:30:06 | Dart | Yes — `fa-solid-400.woff2` (5,102B) |
| `gatsby-portfolio-dev` | 02:30:09 | JavaScript | Partial — tasks.json injected, woff2 missing |
| `Hacktoberfest-Flutter` | 02:30:25 | Dart | Yes — `fa-solid-400.woff2` (5,102B) |
| `laravel-app-starter-pack` | 02:31:04 | PHP | No — only vendor .bat files (legitimate) |
| `madeeldev` (profile) | 02:31:08 | — | Yes — `fa-solid-400.woff2` (5,102B) |

**5 repos with live woff2 payload, 1 partial (tasks.json only), 2 no infection (PHP/Laravel).**

The bat sweep pushed all repos regardless of successful injection — consistent with
`temp_auto_push.bat` behavior documented in Task H.

### Injection Failure Pattern

`gatsby-portfolio-dev` received the tasks.json but not the woff2 because the repo has no
`public/fonts/` directory. The actor's injection script places the payload at a hardcoded path;
repos with different structures get a broken tasks.json (fires but file not found → silent fail).

`laravel-app-starter-pack` was not infected at all — likely because the injection script
targets JS/Dart repos and skipped the PHP project, or because the `vendor/` tree was too large
for the bat to process.

---

## Timestamp Forgery (config.bat)

All payload commits have matching author/committer timestamps — config.bat successfully forged
all injection commits to blend with existing historical commits:

| Repo | Forged commit date | Real push date |
|------|--------------------|----------------|
| `flutter-vpn` | 2022-07-19 | 2026-06-07 |
| `flutter-doctor-consultation-app` | 2024-01-15 | 2026-06-07 |
| `flutter-simple-login-signup` | 2024-03-24 | 2026-06-07 |
| `Hacktoberfest-Flutter` | 2021-10-12 | 2026-06-07 |

The commit message used for all injections: `"Update README.md"` — a plausible catch-all message
that blends with the developer's own commit history.

**Detection signal**: `pushed_at: 2026-06-07T02:29–02:31Z` on all repos, with latest commit
dates of 2021–2024. A ~2–4 year gap between the newest commit date and `pushed_at` is the only
observable anomaly.

---

## IOCs

| Type | Value |
|------|-------|
| Campaign ID | `10-010` |
| Cipher | `_$_1e42` (seed 2667686, same as saif72437) |
| Activation codes | `Tgw(2509); return 1358` |
| Payload file | `public/fonts/fa-solid-400.woff2` (5,102 bytes) |
| Payload SHA (woff2) | (byte-identical across all 5 repos) |
| Victim account | `madeeldev` (GitHub, Pakistani developer) |
| Infected repos | `flutter-vpn`, `flutter-doctor-consultation-app`, `flutter-simple-login-signup`, `Hacktoberfest-Flutter`, `madeeldev` (profile) |
| Partial infection | `gatsby-portfolio-dev` (tasks.json only) |
| Infection date | 2026-06-07T02:29–02:31Z UTC |
| Forged commit msg | `"Update README.md"` |

---

## Assessment

**Attribution**: PolinRider — confirmed by `_$_1e42` cipher, `sfL` shuffle cipher (seed 2667686),
`Tgw(2509)/1358` activation codes, and `fa-solid-400.woff2` delivery pattern.

**Series-10 significance**: `10-010` is the only series-10 ID documented so far. The `10-`
prefix is likely a new deployment batch beyond the `9-xxxx` series seen in astro.config.mjs
infections (highest: `9-7226`). The `10-` series uses the same `fa-solid-400.woff2` + VSCode
task vector as Tasks B/V rather than `astro.config.mjs`.

**C2 status**: DEAD for these victims. Campaign IDs beginning with `A10-` route to `23.27.13.43`
(confirmed offline in Task U), and in the current Jun 25 Stage 2, all `A...` prefix victims are
silently dropped. Victims are not being actively exfiltrated.

**Operator**: Same PolinRider actor. No indicators of a different operator — cipher, activation
codes, and delivery template are identical to the Task N/O `8-765` batch. The `10-010` ID
suggests the operator assigned a new series number to a new victim pool (mobile/Dart developers)
rather than a different team.
