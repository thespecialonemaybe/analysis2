# npm Package Analysis: PolinRider Infection Vectors

**Date:** 2026-06-27  
**Status:** Cross-referenced with OSV, GHSA, and GitHub code search

---

## Overview

PolinRider deploys two complementary infection mechanisms: (1) **git commit injection** into
compromised developer repos, and (2) **malicious npm packages** that seed the initial
compromise. This document covers the npm infection vector — six packages identified across two
confirmed-attribution and four suspected-attribution buckets.

---

## Confirmed PolinRider npm Packages

Both original packages are confirmed PolinRider by OpenSourceMalware. Neither has recoverable
original content — npm has completely purged the author, description, scripts, and dependency
metadata, leaving only security-holding tombstone versions.

### `tailwind-autoanimation`

| Field | Value |
|-------|-------|
| OSV ID | MAL-2026-148 |
| Taken down | **2026-01-07T23:40:46Z** |
| Detection | Amazon Inspector + GHSA |
| Post-takedown downloads | 54 (npm's mandatory retention period) |
| Original author/scripts | **Purged — not recoverable** |

### `tailwind-mainanimation`

| Field | Value |
|-------|-------|
| OSV ID | MAL-2026-1418 |
| Taken down | **2026-03-13T14:19:40Z** |
| Detection | Amazon Inspector + GHSA |
| Post-takedown downloads | 60 |
| Original author/scripts | **Purged — not recoverable** |

**Critical timing observation:** `tailwind-mainanimation` was taken down on the **exact same
day** that OpenSourceMalware published the `rmcej_otb_payload` YARA rule (2026-03-13). The
YARA publication did not directly target the npm packages, but it triggered enough attention
that npm's automated pipeline or a reporter acted the same day. This confirms the actor's
observation of public detection is bidirectional: the actor monitors for detection, and
detection events accelerate the takedown timeline.

Both packages use Tailwind CSS naming (`tailwind-*`, `*animation`) to target frontend
developers who auto-install devDependencies from tutorial templates. The low post-takedown
download counts (54 / 60) represent the security-holding tombstone only; the pre-takedown
infection counts are unknown due to purging.

---

## June 2026 Wave — Attribution: Likely Same Cluster

Four additional packages appeared in June 2026, all taken down within minutes to hours of
publication. Attribution to PolinRider specifically is based on circumstantial timing and
naming pattern evidence rather than recovered payload content — the packages were removed too
quickly for payload extraction.

### `postcss-minify-selector` + `postcss-minify-selector-parser`

**Published 5 seconds apart:** `postcss-minify-selector` at 2026-06-24T01:36:05Z,
`postcss-minify-selector-parser` at 2026-06-24T01:36:10Z. The two packages are a
coordinated pair published in the same automated batch.

#### `postcss-minify-selector`

| Field | Value |
|-------|-------|
| OSV ID | MAL-2026-5837 |
| OSV published | 2026-06-15T20:17Z (Amazon Inspector scan date; pre-creation) |
| npm created | 2026-06-24T01:36:05Z (security holding date) |
| Versions | 2.0.2, 2.0.1, 0.1.2, 0.1.3 |
| GitHub package.json refs | **1,324** |

**Typosquat target:** `postcss-minify-selectors` (with trailing `s`) — a component of the
[cssnano](https://cssnano.github.io/) PostCSS minification suite, maintained since 2015.
The removal of a single character from the end is a one-char typosquat.

**Technical indicator (Amazon Inspector):** The package "advertises itself as `postcss-minify-selector`
(singular) but its internal postcss plugin identifier is `postcss-minify-selectors` (plural) —
the canonical name of the legitimate cssnano plugin." The first executable line of `src/index.js`
is a side-effect-only `require('postcss-minify-selector-parser/cjs-runner')` — the companion
package provides the actual payload.

The 1,324 GitHub `package.json` references are primarily from repos that reference the
legitimate `postcss-minify-selectors` and mistype it, not confirmed infected repositories.

#### `postcss-minify-selector-parser`

| Field | Value |
|-------|-------|
| OSV ID | MAL-2026-5737 |
| OSV published | 2026-06-13T07:17Z |
| Versions | 1.0.11–1.0.18, 2.0.1 (9 versions) |

**Technical indicator (Amazon Inspector):** The package re-exports the legitimate
`postcss-selector-parser` library verbatim from `src/selector-parser.js` as cover. In
addition, it ships a sealed AES-GCM ciphertext in `src/config/defaults.js` with hardcoded
passphrase `default-dev-passphrase`. `src/pipeline/custom-codec-pipeline.js` line 53 decrypts
the blob and evaluates the cleartext via `new Function("require", runnable)(require)` — handing
the decrypted payload full `require` capability.

**Execution pattern note:** This payload delivery mechanism (hardcoded-key AES-GCM + `new
Function("require", …)`) is conceptually similar to PolinRider's XOR + blockchain dead-drop
pattern, but the specific implementation differs. The `new Function("require", ...)` invocation
is structurally identical to the `Function("oTNBm2c", LZString_decompressor)` invocation found
in PolinRider Stage 2 (both pass `require` as a parameter to grant the decrypted code module
access). Attribution to PolinRider specifically is plausible but not conclusively established
from the mechanism alone.

**Key indicator linking the pair:** `postcss-minify-selector` calls `postcss-minify-selector-parser/cjs-runner`
as a side effect on import — the outer package is the delivery vehicle, the inner package is
the payload container. This two-package architecture prevents single-package scanners from
flagging the entry point.

---

### `tailwind-textform-fill`

| Field | Value |
|-------|-------|
| OSV ID | MAL-2026-6360 |
| GHSA | GHSA-4wh6-h6rw-f94h |
| Published / taken down | 2026-06-24T01:52:54Z (within ~1 min — same night as the postcss pair) |
| OSV published | 2026-06-24T01:53:31Z (31 seconds after npm creation — automated detection) |
| Severity | Critical (GHSA: "fully compromised") |
| GitHub package.json refs | **5** |

**Attribution signal:** Name follows the confirmed PolinRider `tailwind-*` pattern. Published on
the same night (2026-06-24T01:52Z, 16 minutes after the postcss pair at 01:36Z).

**Victim pattern:** All 5 GitHub repos referencing this package are forks of a single
"Travel-and-Tourism-Management-System-MERN" tutorial template:
- `Darius1231231/Travel-and-Tourism-Management-System-MERN-main`
- `linkser34/Travel-and-Tourism-Management-System-MERN`
- `tejash111/temp1`
- `amirHdev/Travel-and-Tourism-Management-System-MERN`
- `Feroz723/travel`

This fork pattern suggests the actor seeded the dependency into one upstream tutorial/template
repository and it propagated through forks. The MERN stack (MongoDB, Express, React, Node.js)
is a primary target demographic — junior and intermediate developers building portfolio
projects, with npm installed and running by default.

---

### `tw-style-utils`

| Field | Value |
|-------|-------|
| OSV ID | MAL-2026-6508 |
| npm created | **2026-06-26T05:17:09Z** |
| OSV published | **2026-06-26T05:17:40Z** (+31 seconds — automated detection) |
| Severity | GHSA: "fully compromised" |
| GitHub package.json refs | **2** |

**Critical timing correlation:** zurichjs PR#199 (the 5-2-319 injection, cipher `_$_4445`) was
merged into `zurichjs/zurichjs-conf` at **2026-06-26T04:55Z**. `tw-style-utils` was published
**22 minutes later** at 05:17Z. The git injection and the npm lure package were deployed within
the same ~25-minute operational window on the same day.

This tight coupling suggests the actor was actively operational — running both attack vectors
simultaneously, likely via the same automated tooling (`config.bat` / `temp_auto_push.bat`).
It is not possible to determine causal order from timestamps alone: either the npm package was
a pre-planned companion to the git injection, or the two were independent automated actions
that happened to fire close together.

**Victim profile (2 GitHub refs):**
- `joshschcom/smart-contract-engineer-role` — blockchain/smart contract developer environment
- `prakhar7017/vaultpay-home-task` — payment processing take-home project

Both repos represent high-value developer targets for a DPRK-nexus actor: blockchain tooling
and financial infrastructure. This is consistent with PolinRider's known target profile
(cryptocurrency developers, DeFi engineers).

**Detection speed note:** The 31-second gap between npm creation and OSV publication reflects
npm's real-time security scanning pipeline. The package was effectively never available as a
functioning install source — which means the 2 GitHub references pre-date the package, or were
added from a cached / mirrored version.

---

## Timeline

```
2026-01-07  tailwind-autoanimation taken down (MAL-2026-148)
2026-03-07  OpenSourceMalware publishes YARA rule (rmcej_otb_payload)
2026-03-13  tailwind-mainanimation taken down (MAL-2026-1418) ← same day as YARA
2026-06-13  postcss-minify-selector-parser detected (MAL-2026-5737 scan date)
2026-06-15  postcss-minify-selector detected (MAL-2026-5837 scan date)
2026-06-24T01:36:05Z  postcss-minify-selector published (npm creation / security hold)
2026-06-24T01:36:10Z  postcss-minify-selector-parser published (+5 seconds — same batch)
2026-06-24T01:52:54Z  tailwind-textform-fill published (+16 min — same night)
2026-06-24T01:53:31Z  tailwind-textform-fill OSV advisory published (+37 seconds — auto)
2026-06-26T04:55Z     zurichjs PR#199 merged (5-2-319 injection, cipher _$_4445)
2026-06-26T05:17:09Z  tw-style-utils published (+22 min after PR merge)
2026-06-26T05:17:40Z  tw-style-utils OSV advisory published (+31 seconds — auto)
```

---

## Methodology: Tailwind/PostCSS Targeting

All six packages target the same developer toolchain:

| Package | Lure pattern | Real target |
|---------|-------------|-------------|
| `tailwind-autoanimation` | Tailwind CSS animation util | devs using tailwind-animation |
| `tailwind-mainanimation` | Tailwind CSS main animation | devs using tailwind-animation |
| `postcss-minify-selector` | PostCSS selector minifier | devs using postcss-minify-**selectors** (typosquat) |
| `postcss-minify-selector-parser` | PostCSS parser companion | devs using postcss-selector-parser (re-exported as cover) |
| `tailwind-textform-fill` | Tailwind form fill util | Tailwind MERN stack devs |
| `tw-style-utils` | Tailwind style utilities | Tailwind frontend devs |

The actor consistently targets the PostCSS/Tailwind/cssnano ecosystem — tooling that is
installed at project creation time, often without careful version pinning, and that runs
Node.js at `npm install` via `postinstall` scripts. This gives the malware execution at the
moment of package installation, before any code review occurs.

---

## Attribution Assessment

| Package | Confidence | Basis |
|---------|-----------|-------|
| `tailwind-autoanimation` | **Confirmed PolinRider** | OpenSourceMalware report |
| `tailwind-mainanimation` | **Confirmed PolinRider** | OpenSourceMalware report |
| `tailwind-textform-fill` | **High** (same naming convention, same night as postcss pair) | Name pattern + timing |
| `tw-style-utils` | **High** (22-min window with confirmed zurichjs injection) | Timing correlation + target profile |
| `postcss-minify-selector` | **Moderate** (different package namespace; AES-GCM vs XOR delivery) | Timing + 5-sec pairing |
| `postcss-minify-selector-parser` | **Moderate** (same as above) | Published with `postcss-minify-selector` |

**The postcss pair represents a potentially distinct sub-cluster.** The AES-GCM +
`new Function("require", ...)` payload delivery documented by Amazon Inspector differs from
PolinRider's confirmed XOR + TRON blockchain dead-drop chain. It is possible that:

1. PolinRider evolved their npm delivery mechanism to use AES-GCM for the postinstall payload
   while keeping the blockchain chain for the in-repo Stage 0, or
2. The postcss pair is a different actor exploiting the same PostCSS naming space around the
   same timeframe, or
3. The postcss pair uses the same TRON/BSC delivery internally (inside the decrypted AES-GCM
   blob) and the outer AES-GCM layer is just the npm-level obfuscation

Without extracting and analyzing the actual decrypted payload from `postcss-minify-selector-parser`,
the attribution cannot be conclusively confirmed for those two packages.

---

## YARA / Detection Notes

All six packages are now security holdings on npm. No YARA rules can target them in npm
registry form. Detection value is:

1. **Filesystem artifacts:** If any of these were installed, `node_modules/<package-name>`
   artifacts may remain. The `postcss-minify-selector-parser` package specifically ships
   `src/config/defaults.js` (AES-GCM ciphertext) and `src/pipeline/custom-codec-pipeline.js`
   (decryption + eval) — these file paths/names are detectable via filesystem scan.

2. **`package.json` references:** Any project `package.json` listing these packages as
   dependencies was infected. Scanning for the six package names in `dependencies`,
   `devDependencies`, or `optionalDependencies` is a reliable host-level indicator.

3. **`package-lock.json` / `yarn.lock`:** If a lockfile resolved one of these packages,
   the lockfile entry persists even after `npm uninstall`. This is the most reliable
   retrospective indicator on developer workstations.

---

## IOCs

```
# Malicious npm packages (confirmed or suspected PolinRider)
tailwind-autoanimation              (MAL-2026-148)      confirmed
tailwind-mainanimation              (MAL-2026-1418)     confirmed
tailwind-textform-fill              (MAL-2026-6360 / GHSA-4wh6-h6rw-f94h)   suspected
tw-style-utils                      (MAL-2026-6508)     suspected
postcss-minify-selector             (MAL-2026-5837)     suspected (different mechanism)
postcss-minify-selector-parser      (MAL-2026-5737)     suspected (different mechanism)

# Hardcoded passphrase (postcss-minify-selector-parser)
default-dev-passphrase

# Amazon Inspector hash for postcss-minify-selector
1bc7341d6762a6209e4bde3d99f31f1a8650b6971e64a19547b9f35e7a51abb3

# Amazon Inspector hash for postcss-minify-selector-parser
957f5cbb74f4dd4b4770e8c9cc1a8aac88a4450cb01dbc0fa5242c42e343f54c
```
