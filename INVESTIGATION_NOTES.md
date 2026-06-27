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

The three IP addresses (`166.88.134.62`, `198.105.127.210`, `23.27.202.27`) are hidden inside
the `_$_9f51` cipher in Stage 1 and were never visible in Stage 0 or infected repo files. Port
27017 on `23.27.202.27` confirms the actor's backend is MongoDB. The three-pool routing by
campaign ID suggests the actor is segmenting victims across multiple C2 servers at scale.

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

**B. Decode `_$_16d1` from W2 Stage 1**
W2 Stage 1 (June 20) delivers `_$_16d1` with activation code `8063` (return `8223`).
Extract the full encoded string table and seed, decode the string table, compare to W1 IOC set.
Check whether direct C2 IPs and W3 TRON wallet appear here too.

**E. TrustedSmartChain notification**
The `tsc-signer` infection (5-3-341, May 19) is a high-severity finding. The developer's
machine may have had the signing keys for the TSC blockchain exfiltrated. The TrustedSmartChain
org does not appear to have been notified. This warrants direct disclosure.

### Medium priority

**D. npm package analysis: `tailwind-mainanimation` / `tailwind-autoanimation`**
These are the primary infection vectors. Check npm registry for current status (pulled or live),
download history, postinstall scripts, author accounts.

**F. Cross-reference our victims with OpenSourceMalware's repo list**
Their 1,950+ repo list may contain our 9 external victims or link them to the npm infection
vector.

**G. Scan for `_$_16d1` and `_$_9f51` in GitHub repos**
Neither cipher is currently findable via GitHub code search. When infected repos appear, these
will be the signatures to watch.

**H. Investigate `config.bat`**
The charlie-goldenowl scanner lists `config.bat` as an orchestrator alongside `temp_auto_push.bat`.
We've only documented `temp_auto_push.bat`. What does `config.bat` do?

**I. Aptos address activity**
The two Aptos fallback addresses (`0xbe037400...`, `0x3f0e5781...`) haven't been queried for
transaction history. They may contain historical dead-drop data.

### Lower priority / passive monitoring

**J. TRON wallet W1 update cadence**
W1 has been updated at: May 23, Jun 18, Jun 23. Next update expected late June / early July.
W3 (Stage 2 wallet) has been updated every 3–6 days since June 2. Both worth monitoring.

**K. Check remaining unconfirmed victim repos (TrustedSmartChain/tsc main repo)**
The `tsc` (main chain software, updated 2026-06-09) may also be infected.
