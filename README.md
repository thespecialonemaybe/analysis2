# ZurichJS Supply-Chain Attack — Analysis Archive

**Actor:** DEV#POPPER / PolinRider / Void Dokkaebi (Famous Chollima, DPRK-nexus)  
**Target organisation:** `zurich-js` (GitHub)  
**Campaigns confirmed:** 5-3-161 · 5-3-298 · 5-2-319  
**Injections found:** 5 across 2 repositories, spanning 2026-02-22 to 2026-06-26  

---

## Discovery & Analysis Order

### 1 — Campaign 5-3-161 (first encounter)

**Files:** `ANALYSIS_REPORT_5-3-161.md` · `OPENCTI_REPORT_5-3-161.md` · `artifacts_5-3-161.zip`

The first attack to be found. Commit `556dba47ce` in `zurich-js/zurichjs-website`
modified `next.config.mjs` with a hidden payload appended after thousands of trailing
spaces. Author date 2026-02-19, committer date 2026-02-22 — a 70-hour gap that later
became the key detection fingerprint for all subsequent injections.

The file sat in the repository undetected for **~71 days** before being cleaned on
2026-05-04. This was the initial static analysis: decoding the XOR cipher (`_$_46e0`),
tracing the C2 chain through TRON and BSC blockchain dead-drops, and recovering the
Stage 0–4 payload chain.

The OpenCTI structured report and research references were produced at this stage.

---

### 2 — Campaign 5-3-298 (reinfection, ~3 weeks later)

**Files:** `ANALYSIS_REPORT_5-3-298.md` · `artifacts_5-3-298.zip`

Only 21 days after campaign 5-3-161 was cleaned, the actor returned. Commit `bd6cf2bae2`
in `zurich-js/zurichjs-website` injected `postcss.config.mjs` on 2026-05-25 — this time
using 2,700+ trailing spaces and a new cipher (`_$_913e`). Detected and remediated within
**~21 hours** (2026-05-26), showing the team had improved monitoring after the first incident.

This analysis went deeper into the payload chain: Stage 0–4 fully decoded, Stage 3 recovered
as a full **RAT** — socket.io WebSocket C2, persistent injection into VS Code / Cursor /
Discord / GitHub Desktop / NPM, remote shell, and clipboard capture. The C2 was observed
live and updated during the analysis on 2026-06-05. A liveness recheck was performed on
2026-06-18, recovering an updated Stage 4 build.

The two Stage 4 builds from this campaign (`stage4_live_20260605.js`, `stage4_live_20260618.js`)
are in the artifact zip alongside Stage 1–3 and all decoder scripts.

---

### 3 — Campaign 5-2-319 (third infection, 2026-06-26)

**Files:** `ANALYSIS_REPORT_5-2-319.md` · `artifacts_5-2-319.zip`

On 2026-06-26 a new injection was found in `zurich-js/zurichjs-conf`, commit `e7b90585`,
via PR #199 (`claude/gifted-goodall-ppwr5d`). This prompted a deep investigation that
uncovered:

- **The merge-commit-injection technique:** the PR branch itself was clean; the payload
  appeared only in the force-pushed merge commit. This was a new evasion step vs the
  first campaign.
- **Stage 4 retrieval:** the live Stage 4 payload (`stage4_5-2-319.js`, 65 KB) was
  retrieved from the C2 server, partially decoded, and a BSC dead-drop hash recovered.
- **Campaign version `5-2-319`** using a new cipher (`_$_4445`) and new XOR seed,
  while sharing identical blockchain wallet addresses with campaign 5-3-161.

The `decode_stage4_strings.py` script and `stage4_v3_strings.txt` were produced here.

---

### 3 — Retroactive discovery of previously unknown injections

*All findings below were made during the 5-2-319 analysis and are documented in
`ANALYSIS_REPORT_5-2-319.md`.*

#### 3a — PR #177 in zurichjs-conf (campaign 5-3-298, previously undocumented)

Querying the commit history of `postcss.config.mjs` in `zurichjs-conf` surfaced commit
`4b46f2e197` — PR #177 ("Make flight form fields nullable"), force-pushed at
2026-05-25T18:31Z with a **+5h29m** author/committer gap. Campaign ID `5-3-298`, cipher
`_$_913e`. Remediated within 20 minutes by Ilie Bogdan ("clean").

#### 3b — zurichjs-website companion injection (campaign 5-3-298)

A date-range scan of `zurichjs-website` commits found `bd6cf2bae2` ("fix twint"),
force-pushed 42 seconds after PR #177 (18:32:10Z), with a **4-day** author/committer
gap. Same campaign ID `5-3-298`, same cipher, same automation run.

#### 3c — PR #77 in zurichjs-conf (campaign 5-3-161)

A systematic scan of all config file commit histories across every `zurich-js` repo
found commit `a035927600` — PR #77 ("Ticket invoices"), force-pushed 2026-03-31 with a
**+20h38m** gap. Campaign `5-3-161`, cipher `_$_46e0`, byte-for-byte identical payload
to the zurichjs-website first infection. Window: **~33 days**. Notably the branch name
(`ticket-invoices`) does not follow the `claude/` pattern, showing that branch name
alone is not a sufficient detection signal.

#### 3d — Broader external victims

GitHub code search for `_$_913e`, `_$_b229`, and `global.i='5-` revealed **9 additional
live-infected repositories** across unrelated organisations, all still unpatched at time
of analysis. New campaign IDs found: `5-3-225`, `5-3-252`, `5-3-296`, `5-3-341`,
`5-2-328`, `5-4-39`, `5-167`. A new cipher `_$_b229` appeared in the June 2026 wave.

---

## Complete Injection Timeline (zurichjs only)

| # | Campaign | Cipher | Repo | Infected commit | Injected | Remediated | Window |
|---|----------|--------|------|-----------------|----------|------------|--------|
| 1 | 5-3-161 | `_$_46e0` | zurichjs-website | `556dba47ce` | 2026-02-22 | 2026-05-04 | ~71 days |
| 2 | 5-3-161 | `_$_46e0` | zurichjs-conf PR#77 | `a035927600` | 2026-03-31 | 2026-05-03 | ~33 days |
| 3 | 5-3-298 | `_$_913e` | zurichjs-conf PR#177 | `4b46f2e197` | 2026-05-25T18:31Z | 2026-05-25T18:51Z | ~20 min |
| 4 | 5-3-298 | `_$_913e` | zurichjs-website | `bd6cf2bae2` | 2026-05-25T18:32Z | 2026-05-26T15:46Z | ~21h |
| 5 | 5-2-319 | `_$_4445` | zurichjs-conf PR#199 | `e7b90585dc` | 2026-06-26T04:55Z | 2026-06-26T11:11Z | ~6h |

---

## File Index

| File | Campaign | Description |
|------|----------|-------------|
| `ANALYSIS_REPORT_5-3-161.md` | 5-3-161 | Full static analysis — first campaign |
| `OPENCTI_REPORT_5-3-161.md` | 5-3-161 | Structured OpenCTI threat-intel report |
| `RESEARCH_REFERENCES.md` | all | External references, CVEs, Trend Micro write-up links |
| `artifacts_5-3-161.zip` | 5-3-161 | Malware samples — password: `infected` |
| `ANALYSIS_REPORT_5-3-298.md` | 5-3-298 | Full analysis — second campaign (reinfection) |
| `artifacts_5-3-298.zip` | 5-3-298 | Stage 0–4 samples, Stage 3 ELF, two Stage 4 builds, decoder scripts — password: `infected` |
| `ANALYSIS_REPORT_5-2-319.md` | 5-2-319 + all | Full analysis of third campaign; retroactive coverage of all five injections and external victims |
| `artifacts_5-2-319.zip` | 5-2-319 | Stage 0/1/4 samples + string table + decoder — password: `infected` |
| `decode_stage4_strings.py` | 5-2-319 | Static base91 decoder for the Stage 4 string table |
| `stage4_v3_strings.txt` | 5-2-319 | Decoded `ePVaOH6` string table (170 entries) |
| `ANALYSIS_VICTIM_5-3-225_cleaner55555.md` | 5-3-225 | cleaner55555 victim analysis (3 repos, 7-minute wave) |
| `ANALYSIS_VICTIM_5-3-252_TypeTerrors.md` | 5-3-252 | TypeTerrors/Stable-Diffuser-UI victim analysis |
| `ANALYSIS_VICTIM_5-3-296_transcribe_needle.md` | 5-3-296 | artzkaizen/transcribe + Lu-Yanru/42_Needle_Hackathon — eval(atob) injection vector, collateral spread via collaborator repos |
| `artifacts_5-3-296.zip` | 5-3-296 | Infected TypeScript entry points (4 files, 2 repos) — password: `infected` |

---

## Key IOCs (summary)

```
# C2 server
198.105.127.210

# TRON wallets
TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF   (W1)
TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH   (W2)
TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v   (W3, active as of 2026-06-08)

# Shared XOR key (all campaigns)
2[gWfGj;<:-93Z^C

# Compromised GitHub account
farisaziz12 (ID 53216647) — push access to zurich-js org

# Commit tampering fingerprint
author/committer timestamp gap > 60s on a config file commit
```
