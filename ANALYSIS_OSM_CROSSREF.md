# Task F: Cross-Reference with OpenSourceMalware Victim List

**Date:** 2026-06-27  
**Source:** `OpenSourceMalware/PolinRider/polinrider-master-2026-04-11.csv` (431 KB, 1,950 repos)  
**Archive:** `OpenSourceMalware/PolinRider/archive/affected_repos_2026-03-18.csv` (769 repos)

---

## Result: No Overlap — Different Time Windows

**None of our 9 external victims appear in either OSM CSV.**

This is expected rather than surprising. All of our victims were infected in **May–June 2026**
using ciphers `_$_913e` (first seen May 13) and `_$_b229` (first seen June 3). OSM's master
CSV is dated **April 11, 2026** — before any `_$_913e` infection existed. The two datasets are
non-overlapping windows of the same campaign:

| Dataset | Coverage period | Ciphers | Repo count |
|---------|----------------|---------|------------|
| OSM archive (Mar 18) | Jan–Mar 2026 | `_$_1e42` / `rmcej%otb%` | 769 |
| OSM master (Apr 11) | Jan–Apr 2026 | `_$_1e42`, `Cot%3t=shtP`, bat-only | 1,950 |
| **This investigation** | **May–Jun 2026** | **`_$_913e`, `_$_b229`, `_$_4445`** | **9+ known** |

The cipher evolution timeline now maps cleanly to three distinct documentation windows:
- `_$_1e42` (`rmcej%otb%`) — Jan–Mar: OSM's original detection
- `Cot%3t=shtP` — Mar–Apr: post-YARA rotation, captured by OSM's April update
- `_$_913e` → `_$_b229` → `_$_4445` — May–Jun: **our wave, not yet in any public list**

---

## OSM Master CSV — Key Statistics

| Field | Count |
|-------|-------|
| Total repos | 1,950 |
| Still live as of Apr 11 | **1,807 (92.7%)** |
| Deleted | 1 |
| Needs marker recheck | 142 |
| With bat file artifact (`LAST_COMMIT-bat` or `temp_auto_push.bat`) | **236** |
| JS payload only | 1,319 |
| Both JS payload + bat artifact | 57 |

**1,807 of 1,950 tracked repos were still live and unpatched as of April 11.** No mass
takedown or notification campaign has occurred at that scale.

---

## Marker Family Breakdown

| Marker family | Count | Meaning |
|--------------|-------|---------|
| `_$_1e42` | 1,266 | Old cipher — YARA-detectable via `rmcej%otb%` string |
| (empty) | 394 | No signature found — bat artifact or other indicator |
| `LAST_COMMIT-bat` | 105 | `config.bat` / `temp_auto_push.bat` artifact, no JS payload |
| `temp_auto_push.bat,LAST_COMMIT-bat` | 74 | Both bat scripts found |
| `Cot%3t=shtP-sg` | 40 | Rotated cipher (post-March 7 YARA evasion) |
| `_$_1e42,LAST_COMMIT-bat` | 30 | Old cipher + bat artifact |
| `temp_auto_push.bat,_$_1e42,LAST_COMMIT-bat` | 27 | All three |
| `function-MDy` | 13 | Earliest `MDy` inner cipher variant |
| `function-MDy,Cot%3t=shtP-sg` | 1 | Both |

**The `LAST_COMMIT-bat` marker is named after the `LAST_COMMIT_DATE`/`LAST_COMMIT_TIME`
variables inside `config.bat`.** OSM detects the bat file by these distinctive variable names.
236 total repos had `config.bat` or `temp_auto_push.bat` present — consistent with our Task H
finding that the bat files are the primary npm-vector artifact on victim machines.

---

## `Cot%3t=shtP-sg` — The Interim Cipher Wave

The 41 `Cot%3t=shtP-sg` repos represent the **March–April rotation** that replaced `_$_1e42`
after OSM's YARA rule publication on March 7. Key characteristics:

**Star count:** min 117, max 596, average 299 — substantially higher-profile targets than the
`_$_1e42` wave. The actor appears to have shifted toward more popular repositories as the
campaign matured.

**Crypto/Web3 targeting:** 11 of 41 repos are explicitly blockchain/crypto projects:

| Repo | Stars | Description |
|------|-------|-------------|
| `herasoftlabs/ChainLab` | 417 | Blockchain development platform |
| `MoralisWeb3/moralis-analytics-js` | 420 | Web3 analytics SDK |
| `armujahid/solana-voting` | 416 | Solana voting dApp |
| `herasoftlabs/Dappify` | 217 | Decentralized app platform |
| `Web3-Builders-Alliance/convergence` | 241 | Web3 Builders Alliance |
| `sanketnighot/sat-token-deployer-ui` | 256 | Token deployer UI |
| `ysfkel/solana-tweeter` | 215 | Solana social dApp |
| `jackkru69/ton-wallet-ext` | 181 | TON wallet extension |
| `Staking-Facilities-GmbH/ReactCosmosDelegationUI` | 170 | Cosmos staking UI |
| `morganjweaver/liquibet` | 261 | Chainlink/DeFi hackathon project |
| `raiv200/Metaverse-app` | 122 | Web3/Moralis React app |

This crypto concentration confirms DPRK-nexus financial motivation. The `Cot%3t=shtP-sg` wave
was specifically targeting developers with blockchain/DeFi tooling in their repos.

---

## `new-computers` Org — Confirmed in OSM List

The `new-computers` org (which we found had `temp_interactive_push.bat` committed across
multiple repos) appears in OSM's **`LAST_COMMIT-bat` only** category:

```
new-computers/seeder          (91 stars)
new-computers/arena-toolkit   (24 stars)
new-computers/guides          (28 stars)
new-computers/cabal           (24 stars)
new-computers/writing         ( 6 stars)
new-computers/syllabi         ( 1 star)
```

6 of their 10 repos are in OSM's list — the entire working developer portfolio of this org
appears to be infected. OSM detected only the bat artifact (no JS payload) suggesting either
the JS payload had already been cleaned or the bat file was written before the JS injection
occurred.

---

## Submission Rounds — Discovery Timeline

| Round | Count | Timeframe |
|-------|-------|-----------|
| `pre_existing_osm` | 257 | Documented before OSM started |
| `round1_pre_2026-03-18` | 177+ | First systematic scan (Mar 2026) |
| `round2_2026-04-10` | 696+ | Largest batch — Apr 10 scan |
| `round3_candidate` | 142+ | Flagged for follow-up |
| `round3_2026-04-11` | 72+ | Final confirmed round |

Round 2 (April 10) is the largest single batch — 696 repos. This corresponds to OSM's
expanded scanning after the March YARA rule attracted attention. Round 3 (April 11) closed
out the list at 1,950.

**No new public list has been published since April 11, 2026.** The May–June wave
(`_$_913e`/`_$_b229`) is entirely undocumented in the OSM dataset.

---

## What This Means for Our Victims

Our 9 external victims represent the **leading edge of the undocumented wave**. They were
infected using ciphers that no public YARA rule covers, with C2 IPs and TRON wallets that
appear in no public threat report. Without our investigation, they would remain undetected in
the gap between OSM's April 11 cutoff and any future scan.

The OSM list had 40 `Cot%3t=shtP` repos and 1,266 `_$_1e42` repos from the March-April wave.
If the May-June wave scaled comparably, the current untracked infection count is likely in the
hundreds to low thousands — with 1,807 of the OSM-tracked repos still unpatched as of
April 11.

---

## Combined Timeline: Full Campaign Arc

```
Jan 2026     _$_1e42 wave begins (~1,266 repos documented)
Feb 22       zurichjs-website first injection (campaign 5-3-161, cipher _$_46e0)
Mar 7        OpenSourceMalware publishes rmcej_otb_payload YARA rule
Mar 13       tailwind-mainanimation npm package taken down (same day as YARA)
Mar 18       OSM first CSV: 769 repos
Apr 10–11   OSM round 2/3: 1,950 repos total; 1,807 still live
[GAP — no public tracking]
May 13       _$_913e first seen (TrustedSmartChain/tsc-signer, kinyichukwu/val-ai)
May 25       zurichjs reinfection (5-3-298, _$_913e)
Jun 3        _$_b229 first seen (PostNia, intelli-app-store)
Jun 20       W2 Stage 1 updated (TXfxHUet wallet)
Jun 23       W1 Stage 1 updated (TMfKQEd7 wallet, new features)
Jun 24       postcss-minify-selector*, tailwind-textform-fill npm packages published
Jun 26       zurichjs third injection (5-2-319, _$_4445); tw-style-utils published
Jun 27       This analysis: C2 IPs, W3 wallet, Stage 2 RAT retrieved
[No public list covers anything after Apr 11]
```
