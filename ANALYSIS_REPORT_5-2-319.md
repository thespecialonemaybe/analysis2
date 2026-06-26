# ZurichJS Supply-Chain Attack -- THIRD CAMPAIGN (5-2-319)
# DEV#POPPER / PolinRider / Void Dokkaebi (Famous Chollima) -- `zurichjs-conf`

**TLP: WHITE**
**Report date:** 2026-06-26
**Confidence:** High
**Related to:**
- Campaign 5-3-298 (zurichjs-website, 2026-05-25 to 2026-05-26) — [see analysis2 repository]
- Campaign 5-3-161 (zurichjs-website, 2026-02-19 to 2026-05-04)

---

## Summary

A third malicious payload was injected into the ZurichJS GitHub organisation today (**2026-06-26**),
this time targeting `zurich-js/zurichjs-conf` (the ZurichJS conference website), via merge commit
`e7b90585dca28b9a5bd5155a96634ccea7416c57` from pull request #199. The injection was remediated
6 hours 16 minutes later by contributor Ilie Bogdan.

**Same actor, same infrastructure, new target repo and new technique.**

Infrastructure overlap with campaigns 5-3-298 and 5-3-161: **100%** — same C2 IP, same blockchain
wallets, same XOR keys. Only the target repository and campaign version string changed.

**Critical new finding — injection hidden in merge commit, not in PR:**
The PR branch itself (`claude/gifted-goodall-ppwr5d`) is clean. The malicious `postcss.config.mjs`
modification appears only in the merge commit, which diverges from the PR branch's final state.
This means standard PR review of the diff would not reveal the injection. The technique abuses
the `temp_auto_push.bat` commit-tampering tool (documented by Trend Micro [8]) to amend the merge
commit after GitHub processed the merge, then force-pushing to overwrite the merge commit SHA.

**This repo was also targeted on 2026-05-25** via a separate PR (#177), which was remediated the
same day — the third known injection attempt in this series.

---

## Injection Details

| Field | Value |
|-------|-------|
| Repository | zurich-js/zurichjs-conf |
| Injection commit | e7b90585dca28b9a5bd5155a96634ccea7416c57 (merge commit) |
| Author timestamp | 2026-06-26T04:55:43Z |
| Committer timestamp | 2026-06-26T10:54:03Z (**+5h58m gap** — evidence of commit rewrite) |
| Commit message | "Merge pull request #199 from zurich-js/claude/gifted-goodall-ppwr5d" |
| Author account | farisaziz12 (Faris Aziz, GitHub ID 53216647) |
| Infected file | postcss.config.mjs |
| Payload offset | After 1,952 trailing ASCII spaces on the closing `};` line |
| Total infected file size | 5,860 bytes |
| Remediation commit | c030ec0524d3 (Ilie Bogdan, 2026-06-26T11:11:31Z) |
| Active window | **6 hours 16 minutes** |
| Campaign version | `5-2-319` (new; prior campaigns: `5-3-298`, `5-3-161`, `A`, `C`) |

### Distraction File

The PR also legitimately modifies `src/pages/volunteer.tsx` to add PostHog analytics tracking
to the "Apply to Volunteer" CTA buttons — a real, useful change that makes the PR description
credible. This is the same distraction technique as campaign 5-3-298 (which added a donate.tsx
TWINT payment button in the same commit as the injection).

### PR #199 — The Clean Branch Trick

| Detail | Value |
|--------|-------|
| PR title | "Add analytics tracking for volunteer application CTAs" |
| PR created | 2026-06-26T04:54:36Z |
| PR merged | 2026-06-26T04:55:44Z (68 seconds after creation — instant self-merge) |
| Branch | claude/gifted-goodall-ppwr5d |
| Branch author | Claude Opus 4.8 (`noreply@anthropic.com`) |
| Claude session | `https://claude.ai/code/session_01Q52Ggxh6mVMc6hTzx92Cdv` |
| Branch commit sha | 53577ac40ac0cc4af42eca277b1e556481bf7dfc |
| Branch commit content | **Only `volunteer.tsx`** — postcss.config.mjs NOT modified |

The branch was created using a legitimate Claude Code session (Co-Authored-By: Claude Opus 4.8).
The `postcss.config.mjs` injection exists **only in the merge commit**, not in any PR branch
commit. An attacker with access to `farisaziz12`'s machine used `temp_auto_push.bat` to amend
the merge commit after GitHub created it, rewriting history to include the infection.

The branch name format (`claude/<adjective>-<name>-<hash>`) mimics Claude Code's automatic branch
naming convention, lending the PR additional apparent legitimacy.

---

## Previously Undocumented Injection: zurichjs-conf PR #177 (2026-05-25)

A prior injection into the same repository was discovered during this analysis.

| Field | Value |
|-------|-------|
| PR #177 | "Make flight form fields nullable and handle async save operations" |
| Branch | claude/modest-cray-WgarO |
| PR created | 2026-05-25T13:01:08Z |
| PR merged | 2026-05-25T13:01:52Z (44 seconds — instant self-merge) |
| Merge commit | 4b46f2e19783 |
| Author timestamp | 2026-05-25T13:01:52Z |
| Committer timestamp | 2026-05-25T18:31:28Z (**+5h30m gap** — same commit rewrite signature) |
| Remediation | Bogdan Ilie "clean" commit d3f27a237cf8 at 2026-05-25T18:51:17Z |
| Follow-up fix | Claude Code commit 221ee12a9b48 at 2026-05-25T19:11:19Z |

This injection ran concurrently with campaign 5-3-298 on `zurichjs-website` (injected 18:32 UTC
the same day). The actor targeted both ZurichJS repositories simultaneously on 2026-05-25.

---

## Stage 0 Analysis: postcss.config.mjs Implant

```javascript
import { createRequire } from 'module';    // legitimate new import
const require = createRequire(import.meta.url);
export default {
  plugins: ["@tailwindcss/postcss"],
};                                          // 1,952 trailing spaces
global.i='5-2-319';var _$_4445=(function(k,p){...shuffle cipher, seed 4606094...})("s%nb%entcmt_f...", 4606094);
// ... [full Stage 0 payload, 3,764 bytes]
```

The two lines added at the top of the file (`import { createRequire }` and `const require = ...`)
are **not present in the original file** and are not needed by the legitimate PostCSS config. They
serve to ensure `require()` is available in ES module context for the injected Node.js payload
below. This is a new adaptation vs campaign 5-3-298, which targeted a CommonJS config file where
`require` was already available.

### Stage 0 String Table (seed 4606094)

```
[ 0] 'r'                      <- require alias name
[ 1] 'object'                 <- typeof check
[13] 'https'                  <- HTTPS module
[26] 'https://api.trongrid.io/v1/accounts/'   <- TRON dead-drop URL
[27] '/transactions?only_confirmed=true&only_from=true&limit=1'
[28] 'hex'
[33] 'https://fullnode.mainnet.aptoslabs.com/v1/accounts/'   <- Aptos fallback URL
[39] 'eth_getTransactionByHash'   <- BSC RPC method
[40] 'bsc-dataseed.binance.org'   <- BSC RPC
[41] 'bsc-rpc.publicnode.com'     <- BSC RPC fallback
[50] '2[gWfGj;<:-93Z^C'          <- XOR key (SAME as all prior campaigns)
[51] 'TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF'   <- W1 TRON (SAME)
[52] '0x9d202c824402ca89e9aaccd2390b6f8b332ae743caa1469c695feb2781d56519'  <- Aptos-1 (SAME)
[53] 'm6:tTh^D)cBz?NM]'          <- W2/Aptos-2 XOR key
[54] 'TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH'   <- W2 TRON (SAME)
[55] '0x3d2075f97b7b1e3234bd653779d21c605d7d8c6ec9c98d983880be5c7f4f9471'  <- Aptos-2 (SAME)
[56] 'node'    <- subprocess executable
[57] '-e'
[58] "global['_V']='"
[59] "';"
[60] 'ignore'
[61] 'spawn'
[62] 'child_process'
```

Identical W1 and W2 wallets and XOR key to campaigns 5-3-298 and 5-3-161.

---

## Stage 1 Analysis

BSC hash from W1: `0x5ab85abe6c67adb94322e5700a36915c38d1db1e604920da8aa4fcb530408af0`
(unchanged since 2026-05-19 — same Stage 1 payload as all prior campaigns)

XOR key: `2[gWfGj;<:-93Z^C` (same), Stage 1 size: 5,369 bytes.

### Stage 1 String Table (seed 2191935)

Stage 1 sets four globals that all subsequent stages read:

```
[0] '_t_s'  = 'http://198.105.127.210:443'   <- primary C2 (SAME)
[2] '_t_u'  = 'http://198.105.127.210:80'    <- C2 fallback (SAME)
[4] '_t_1'  = 'TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v'  <- W3 TRON (SAME)
[6] '_t_2'  = '0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1'  <- Aptos-3 (SAME)
```

100% infrastructure continuity with prior campaigns.

---

## Stage 4 Status (retrieved live 2026-06-26)

The C2 at `198.105.127.210:443` serves a new Stage 4 version for `_V=5-2-319`:

| Field | Value |
|-------|-------|
| URL | `http://198.105.127.210:443/0x/js?_V=5-2-319&id=<uuid>` |
| Size | **65,580 bytes** |
| MD5 | `91273f2b2b2d1095926752c3b03406c7` |
| SHA-256 | `7ad66ecc604d61e727f813f13beb39276b32b6473bf0c29b983d5e1f64380328` |
| Build marker | `/*RS260605*/` (same as v1 and v2) |
| Retrieved | 2026-06-26 (today) |

**Stage 4 size progression:**

| Date retrieved | Size | MD5 | Notes |
|----------------|------|-----|-------|
| 2026-06-05 | 69,913 B | `c74e11f9...` (SHA-256) | v1 |
| 2026-06-18 | 68,572 B | `c45e510e59bc503d06e66a7cf046af5a` | v2 silent hotfix (-1,341 B) |
| 2026-06-26 | 65,580 B | `91273f2b2b2d1095926752c3b03406c7` | v3 (-2,992 B from v2) |

The actor has trimmed ~4,333 bytes from the RAT since June 5. Build marker unchanged, suggesting
iterative cleanup of the same build rather than a rewrite. W3 was last updated 2026-06-08 (18 days
ago) — Stage 3 has not changed.

### Stage 4 Static Analysis — v2 vs v3 Diff

Full dynamic execution was blocked by the `with`-inside-generator-function construction (a known
static analysis evasion technique that prevents execution in Node.js strict-mode contexts). Static
structural comparison between v2 (68,572 B) and v3 (65,580 B):

| Metric | v2 (2026-06-18) | v3 (2026-06-26) | Delta |
|--------|-----------------|-----------------|-------|
| Generator functions | 24 | 23 | **-1** |
| String table max index | `0xd6` = 214 | `0xa9` = 169 | **-45 entries** |
| Unique string indices accessed | 66 | 72 | +6 |
| Encoded string chunks | 186 | 149 | **-37** |
| Main encoded string payload | ~5,928 chars | ~4,308 chars | **-1,620 chars** |
| Encoding alphabets | 20 | 19 | -1 |
| Variable names | dfifCQ, wQvnfg, MQLFmK... | yZGmjVt, oDCXdB, _frDQc... | Fully re-randomized |

**Interpretation:** One complete generator function was removed along with ~45 string table entries.
This is consistent with a capability module removal rather than code optimization — a pure size
reduction would not systematically shrink the string table by 21%. The removed module likely
corresponds to one of the documented Stage 4 capabilities (multi-operator session management,
persistence injection, clipboard capture, or CI/CD evasion). Without dynamic execution the exact
capability cannot be determined.

Variable names are fully re-randomized between versions, confirming the actor re-runs their
obfuscator on each build. The two encoding alphabets visible in plaintext (base-91/base-92 LZString
variants) changed between versions but are the same structure.

---

## Campaign Timeline (full ZurichJS series)

| # | Campaign | Repository | File | Injected | Remediated | Window |
|---|----------|------------|------|----------|------------|--------|
| 1 | 5-3-161 | zurichjs-website | next.config.mjs | 2026-02-19 | 2026-05-04 | **74 days** |
| 2 | (unknown) | zurichjs-conf | postcss.config.mjs | 2026-05-25T13:01 | 2026-05-25T18:51 | ~5h50m |
| 3 | 5-3-298 | zurichjs-website | postcss.config.mjs | 2026-05-25T18:32 | 2026-05-26T15:46 | ~21h |
| 4 | 5-2-319 | zurichjs-conf | postcss.config.mjs | 2026-06-26T04:55 | 2026-06-26T11:11 | **6h16m** |

Campaigns 2 and 3 were simultaneous — the actor targeted both repos on the same day (2026-05-25).
Detection times are shortening significantly: 74 days → 21 hours → 6 hours.

---

## New Technique: Merge Commit Injection

This campaign introduces a technique not documented in the previous two campaigns: the injection
is placed in the **merge commit**, not in any PR branch commit.

**Why this matters:**
- GitHub's PR review UI shows the diff between the PR branch and the base branch. Reviewers
  who inspect PR #199 see only the clean `volunteer.tsx` analytics changes.
- The `postcss.config.mjs` change appears only in the merge commit, which is created by GitHub
  when the PR is merged and then rewritten by `temp_auto_push.bat` via force-push.
- Branch protection rules requiring PR review do not protect against this, because the PR
  itself passes review — the injection is added post-merge.
- The committer timestamp being 5h58m after the author timestamp is the primary forensic
  indicator of this technique (compare: PR #177 also showed a +5h30m gap).

**Detection:** Compare the merge commit diff to the sum of PR branch commit diffs. Any file
modified in the merge commit that was not in the PR branch is suspicious.

---

## Indicators of Compromise

### Network (all independently verified — this analysis)

```
198.105.127.210:443      # Primary C2 — Stage 4 delivery + socket.io RAT — ALIVE 2026-06-26
23.27.202.27:443         # Secondary C2 — socket.io WebSocket listener only
136.0.9.8                # Former C2 — DEAD

GET  /0x/js?_V=5-2-319&id=<uuid>     # Stage 4 delivery (new campaign version)
GET  /0x/js?_V=5-3-298&id=<uuid>     # Stage 4 delivery (prior campaign)
POST /u/f                              # File upload exfiltration
POST /verify-human/<channel>           # Operator notification
GET  /socket.io/?EIO=4&transport=...  # WebSocket C2 channel
```

### File Hashes

```
# Infected postcss.config.mjs (zurichjs-conf, campaign 5-2-319)
879dc2be804225e985040989b3f261b317e24e5fdb57e953cfffaa7467115a93  postcss.config.mjs.infected (SHA-256)
8949d7db9c5780d4420cdf010226d620                                   postcss.config.mjs.infected (MD5)

# Stage 4 v3 (live from C2, 2026-06-26)
7ad66ecc604d61e727f813f13beb39276b32b6473bf0c29b983d5e1f64380328  stage4_5-2-319.js (SHA-256)
91273f2b2b2d1095926752c3b03406c7                                   stage4_5-2-319.js (MD5)

# Build markers present in Stage 4 (all versions)
/*RS260605*/    # root script marker
/*C250617A*/    # child injection stubs (also C250618A–C250620A, C260511A, C260512A)
```

### Blockchain Addresses (all independently verified)

```
# TRON wallets
TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF   <- W1 Stage 0/1 primary   (dormant since 2026-05-19)
TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH   <- W2 Stage 0/1 fallback  (dormant since 2026-02-27)
TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v   <- W3 Stage 1b active      (last tx 2026-06-08)

# Aptos addresses
0x9d202c824402ca89e9aaccd2390b6f8b332ae743caa1469c695feb2781d56519  # Aptos-1 (mirrors W1)
0x3d2075f97b7b1e3234bd653779d21c605d7d8c6ec9c98d983880be5c7f4f9471  # Aptos-2 (mirrors W2)
0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1  # Aptos-3 (mirrors W3)

# Stage 1 BSC payload (unchanged)
0x5ab85abe6c67adb94322e5700a36915c38d1db1e604920da8aa4fcb530408af0

# Stage 3 BSC payload (most recent, written 2026-06-08)
0xb6c725890be6890fd2c735eedc47e24b85a350301f6c19a3864e43c35e470968
```

### Git / Repository Indicators

```
# Injection pattern in postcss.config.mjs (ES module variant)
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
...
};                 [1,900+ trailing spaces]global.i='[version]';

# Commit tampering signature
- PR branch commit: clean (only volunteers.tsx or other legitimate file)
- Merge commit: contains postcss.config.mjs modification not in PR
- Committer timestamp vs author timestamp: gap of 5-6 hours

# Branch naming mimicking Claude Code
claude/<adjective>-<name>-<hash>     # e.g. claude/gifted-goodall-ppwr5d

# Instant PR self-merge (under 2 minutes from creation to merge)
```

---

## Analysis Artifacts

```
/root/zurichjs3_analysis/
  exports/
    postcss.config.mjs.infected    <- Stage 0 (from commit e7b90585, 5,860 bytes)
    stage1_decrypted.js            <- Stage 1 (XOR-decrypted from BSC 0x5ab85a...)
  c2_data/
    stage4_5-2-319.js              <- Stage 4 v3 (live from C2, 2026-06-26, 65,580 bytes)
```

---

## References

1. Campaign 5-3-298 analysis (zurichjs-website, second campaign): https://github.com/thespecialonemaybe/analysis2
2. Injection commit: https://github.com/zurich-js/zurichjs-conf/commit/e7b90585dca28b9a5bd5155a96634ccea7416c57
3. PR #199 (clean branch, dirty merge): https://github.com/zurich-js/zurichjs-conf/pull/199
4. Prior zurichjs-conf injection (PR #177): https://github.com/zurich-js/zurichjs-conf/pull/177
5. Remediation commit: https://github.com/zurich-js/zurichjs-conf/commit/c030ec0524d3
6. eSentire TRU -- DEV#POPPER RAT and OmniStealer: https://www.esentire.com/blog/north-korean-apt-malware-analysis-dev-popper-rat-and-omnistealer-everyday-im-shufflin
7. Securonix -- Analysis of DEV#POPPER: https://www.securonix.com/blog/analysis-of-devpopper-new-attack-campaign-targeting-software-developers-likely-associated-with-north-korean-threat-actors/
8. Trend Micro TRU -- Void Dokkaebi (Famous Chollima) campaign (Apr 2026): https://www.trendmicro.com/en_us/research/26/d/void-dokkaebi-uses-fake-job-interview-lure-to-spread-malware-via-code-repositories.html
