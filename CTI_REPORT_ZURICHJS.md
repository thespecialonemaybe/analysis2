# CTI Report: ZurichJS Incident — PolinRider Reinfection Case
### Campaigns 5-3-161 and 5-3-298 — zurich-js/zurichjs-website

**TLP: WHITE — Approved for unrestricted distribution**
**Report date:** 2026-07-23
**Confidence:** High
**Distribution:** SOC · Threat Detection · Incident Response
**Scope:** ZurichJS incident only — see `CTI_REPORT_POLINRIDER.md` for full campaign IOCs

---

## Executive Summary

The `zurich-js/zurichjs-website` GitHub repository was compromised twice by a DPRK-aligned
supply-chain actor (PolinRider / Void Dokkaebi / DEV#POPPER) through the same developer
account (`farisaziz12`, GitHub ID 53216647).

The first compromise (campaign 5-3-161) ran undetected for **74 days**. After remediation,
the actor retained persistent remote access to the developer's machine and re-injected 21 days
later (campaign 5-3-298). The second compromise was caught and remediated within 24 hours —
indicating the ZurichJS team had implemented monitoring after the first incident.

**Campaign 5-3-298 represents a capability escalation** over 5-3-161. The malware evolved
from a credential harvester to a full-featured RAT with socket.io WebSocket C2, remote shell,
clipboard capture, and persistent injection into VS Code, npm, Discord, and GitHub Desktop —
meaning the actor's foothold survives removal of the infected repository.

**Key finding:** The actor pre-staged blockchain dead-drop payloads for 5-3-298 six days
before executing the injection, confirming planned rather than opportunistic targeting.

---

## 1. Incident Timeline

```
2026-02-19  Campaign 5-3-161 begins
            next.config.mjs injected via farisaziz12 account
            Commit disguised within a 12-file legitimate refactor
            2,784 trailing spaces hide 4,630B payload on final line

2026-05-04  5-3-161 remediated ("remove junk" commit)
            74-day dwell time
            Actor retains persistent access to farisaziz12's machine

2026-05-19  Actor pre-stages 5-3-298 blockchain payloads
            W4 and W3 TRON dead-drop transactions written
            6 days before the injection — planned operation

2026-05-25  Campaign 5-3-298 begins (18:32:10 UTC)
            postcss.config.mjs injected via farisaziz12 account
            Commit message: "fix twint"
            Cover: legitimate TWINT payment button added to donate.tsx
            2,700+ trailing spaces hide payload on line 10

2026-05-26  5-3-298 remediated (15:46:46 UTC)
            21 hours 14 minutes active window
```

---

## 2. Campaign Comparison

| Component | 5-3-161 | 5-3-298 |
|-----------|---------|---------|
| Injected file | `next.config.mjs` | `postcss.config.mjs` |
| Trailing spaces | 2,784 | 2,700+ |
| Infection commit | `556dba47` | `bd6cf2ba` |
| Commit message | fix(tshirt): resolve hydration mismatch error | fix twint |
| Cover in commit | 11 legitimate tshirt component files | donate.tsx TWINT button (legitimate) |
| Active window | 74 days | 21 hours 14 minutes |
| C2 IP | `198.105.127.210` | `198.105.127.210` (same) |
| C2 port | 27017 | 443 |
| C2 framework | EmbedIO / C# | Express.js / Node.js |
| C2 protocol | HTTP REST | socket.io WebSocket |
| Malware class | Credential harvester (Stage 5 Python infostealer) | Full RAT + persistence |
| Persistent injection | No | Yes — VS Code, npm, Discord, GitHub Desktop |
| Remote shell | No | Yes — full interactive |
| XOR keys | Same | Same (no rotation) |
| Blockchain wallets | Same (W4, W2, W3) | Same (no rotation) |
| Actor test hostnames | `EV-CHQG3L42M`, `EV-4A6OE6M0E` | `EV-CHQG3L42MMQ`, `EV-4A6OE6M0E2D` |

**100% infrastructure overlap.** Only the port, framework, and capability tier changed.

---

## 3. Attack Technique: Commit Tampering via temp_auto_push.bat

Both injections were committed using `temp_auto_push.bat`, a tool the actor deploys to
compromised developer machines. It makes a malicious commit appear indistinguishable from
the legitimate developer's prior work:

1. Extracts the most recent commit's metadata (author, email, timestamp, message)
2. Temporarily alters the system clock to match the original commit date
3. Amends the commit to insert the payload (appended after thousands of trailing spaces)
4. Uses `--no-verify` to bypass pre-commit hooks
5. Force-pushes to overwrite remote history

`temp_auto_push.bat` SHA-256 hashes (Trend Micro TRU):
```
23e37cf4e2a7d55ed107b3bc3eb7812a0e3d8f90b23b0c8f549d5c10d089a2c8
834a92277f1bd82d4d473ac0aa2ddb23208a3a8763a576b882e7326c42bc5412
```

**Consequence:** Commit timestamps, author metadata, and messages in the git log are
unreliable for these campaigns. Do not use commit date as a triage anchor — check file
content instead.

---

## 4. Initial Access: farisaziz12

| Field | Value |
|-------|-------|
| GitHub username | `farisaziz12` |
| GitHub ID | `53216647` |
| Used in | Both 5-3-161 (Feb 2026) and 5-3-298 (May 2026) |
| Evidence of persistent access | Two injection events 21 days after remediation |

**The initial access vector is not confirmed.** The actor had persistent remote access to
this developer's machine — evidenced by `temp_auto_push.bat` use and the ability to re-inject
21 days after the first infection was removed. How the machine was first compromised is unknown.

Candidates:
- **Fake job interview lure** — the primary documented vector for this actor; developer is
  invited to a live coding challenge and asked to clone and run a repository locally
- **Infection via repo clone** — cloning another already-compromised repository could have
  delivered Stage 0 through a `.vscode/tasks.json` or config file injection
- **Phishing or credential theft** — less consistent with the TTPs but not ruled out

What is known: the actor retained access between February and May 2026 (at minimum), and
executed two separate injections against the same target through the same account.

---

## 5. Payload Chain (5-3-298)

Stage 0 triggers on `npm run dev/build` (PostCSS invocation) and spawns a detached node
subprocess — which survives PostCSS process exit.

```
postcss.config.mjs (line 10 — 2700+ trailing spaces)
  │  global.i = '5-3-298'
  │  shuffle cipher seed: 36301
  │  spawns detached: node -e "global['_V']='5-3-298'; <stage1>"
  │
  ▼
Stage 1 (5,369 chars, XOR key: 2[gWfGj;<:-93Z^C)
  │  Reads TRON wallet → Aptos fallback → BSC TX hash
  │  BSC calldata split on "?.?" → XOR decrypt → Stage 2
  │  C2: http://198.105.127.210:443
  │
  ▼
Stage 2 (1,534 chars, seed: 1347634)
  │  Second blockchain dead-drop read (Stage 1b wallet TA48dct...)
  │  BSC TX updated 2026-05-19 (6 days pre-injection) and again 2026-06-05
  │
  ▼
Stage 3 (77,365 chars, XOR + LZString)  ← fetched from C2 /$/boot
  │  Installs: socket.io-client, axios → ~/.node_modules
  │  Persistence: injects Stage 4 into VS Code, Cursor, npm, Discord, GitHub Desktop
  │  Sandbox check: aborts on CI/cloud/kali/WSL hints
  │  Blocklist: EV-CHQG3L42MMQ, EV-4A6OE6M0E2D (actor's own machines)
  │  WebSocket: connects to 166.88.54.158
  │  Marker appended to injected files: /*RS260605*/ or /*C25XXXXXX*/
  │
  ▼
Stage 4 (69,913 chars)  ← GET /0x/js?_V=5-3-298 from C2, build marker /*RS260605*/
  │  Full socket.io WebSocket RAT
  │  Commands: remote shell, file up/download, clipboard, directory listing,
  │            remote eval (plaintext + base64), injection management, C2 redirect
  │
  ▼
Stage 5 (Python infostealer)
     Targets: browser credentials, crypto wallets, SSH keys, .env files,
              AWS/GCP/Azure creds, npm tokens, Kubernetes configs, GPG keys
     Exfil: <hostname>$<username>.zip → Telegram bot + C2 /u/e and /u/f
```

**Important:** Stage 3 persistence survives removal of the infected repository. Any
developer who ran the infected version of `postcss.config.mjs` may have Stage 4 embedded
in their local VS Code, npm, or Discord installation.

---

## 6. Pre-Staging Evidence

The actor updated blockchain dead-drop transactions on **2026-05-19 — six days before the
injection** on 2026-05-25. The Stage 1b wallet (TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v)
received a new BSC TX hash that day, positioning the Stage 2 payload.

This pre-staging pattern shows deliberate planning: the actor prepared the payload chain
before executing the commit injection, not opportunistically.

A second Stage 1b update occurred on **2026-06-05 at 14:31 UTC** — the same day the live
payload analysis was conducted, confirming the C2 was still actively maintained.

---

## 7. ZurichJS-Specific IOCs

### Commit artifacts

```
# Campaign 5-3-161
556dba47cede89f7b1c753b2df2d76cd2a7ab0e8   injection commit
87196d26de2360cb2fbd49cb3a480aa6043f56d7   remediation commit ("remove junk")
next.config.mjs                              infected file

# Campaign 5-3-298
bd6cf2bae2c628b9d6f7f3477669ada1d0c5e2e3   injection commit
19ef30866396a414d985af5cd02cf821368b680a   remediation commit
postcss.config.mjs                           infected file
```

### File hashes (SHA-256)

```
c1314e72963f6be2aaa0f5d51a34608203b69401eb7e4b2828f5fc7413febc37
    postcss.config.mjs (5-3-298, infected version)

d017fe6e8e138630575050902acde5a41a4d676f73eace64ecc47d49262e2330
    stage1_decrypted.js (5-3-298 Stage 1 payload)

c74e11f97168d9f1f3a434248c9d875b0012cca23e90a5940b7bd4a61063172d
    stage4_live.js (retrieved from C2 2026-06-05, 69,913 bytes)
```

### Campaign IDs (Sec-V header value / global['_V'] / global.i)

```
5-3-161   (first ZurichJS campaign)
5-3-298   (second ZurichJS campaign)
```

### Network — C2 used in ZurichJS campaigns

```
198.105.127.210:443    primary C2 (5-3-298) — Stage 4 delivery + socket.io RAT
198.105.127.210:27017  primary C2 (5-3-161) — original HTTP REST framework
23.27.202.27:443       secondary socket.io listener (5-3-298)
166.88.54.158          Stage 3 socket.io WebSocket (confirmed)
```

All on **AS149440 Evoxt Sdn. Bhd.**

### Blockchain wallets used in ZurichJS campaigns

```
TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF   W4 — Stage 0/1 primary TRON (both campaigns)
TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH   W5 — Stage 0/1 fallback TRON (both campaigns)
TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v   W3 — Stage 1b / Stage 2 TRON (both campaigns)
```

XOR keys (both campaigns, no rotation):
```
2[gWfGj;<:-93Z^C    primary XOR key
m6:tTh^D)cBz?NM]   secondary XOR key
```

---

## 8. Incident Response: If You Cloned zurich-js/zurichjs-website

The active window for 5-3-298 was **21 hours 14 minutes (2026-05-25 18:32 UTC to 2026-05-26
15:46 UTC)**. Anyone who ran a PostCSS build (e.g., `npm run dev` or `npm run build`) during
that window may have executed the Stage 0 payload.

**Stage 3 persistence means the threat extends beyond the repo.** Check your local
development machine:

**Immediate steps:**
```bash
# Check for Stage 3 persistence markers in VS Code
grep -r "RS260605\|_p_t\|ThZG+0jfXE6VAGOJ" \
  "/Applications/Visual Studio Code.app" \
  "$HOME/.vscode" \
  "$(npm root -g)/npm/lib/" 2>/dev/null

# Check for planted node_modules directory (should not exist at home dir level)
ls -la ~/.node_modules 2>/dev/null && echo "SUSPICIOUS: ~/.node_modules exists"

# Check for exfil staging (look for zip matching hostname$username pattern)
ls /tmp/.npm/*.zip 2>/dev/null
```

**Revoke immediately if Stage 3+ was reached:**
- GitHub PATs and SSH keys (any repos you have push access to may have been targeted)
- npm auth tokens (`~/.npmrc`)
- AWS / GCP / Azure credentials
- Browser-saved passwords (treat as compromised)
- Crypto wallet seed phrases

**Assess propagation:**
- Review repos you committed to in the past 6 months for `.vscode/tasks.json` with
  `runOn: folderOpen`, or unexpected binary files (`.woff2`) in source directories
- Notify collaborators who may have cloned any affected repositories

**Re-image recommendation:** If Stage 3 or later was confirmed reached, re-image the
machine. Stage 4 provides full remote shell and arbitrary eval — assume unrestricted access.

---

## 9. Attribution

This incident is attributed to the **PolinRider** campaign cluster, also tracked as:
- **Void Dokkaebi** (Trend Micro TRU)
- **DEV#POPPER** (Securonix)
- **Famous Chollima / Contagious Interview** (CrowdStrike)
- **Lazarus Group** (broader DPRK attribution)

The ZurichJS incident shares 100% infrastructure with a campaign that infected 750+
repositories globally (Trend Micro, March 2026), with named victims including DataStax
and Neutralinojs.

For the full campaign scope — including 9 malicious npm packages, 16 Go packages, all
C2 IP addresses, all blockchain wallets, YARA/Sigma rules, and hunt queries — see:
**`CTI_REPORT_POLINRIDER.md`**

---

## 10. References

| Source | Date | Notes |
|--------|------|-------|
| `ANALYSIS_REPORT_5-3-161.md` | 2026-05-06 | First ZurichJS campaign static analysis |
| `ANALYSIS_REPORT.md` | 2026-06-05 (updated 2026-06-18) | Second ZurichJS campaign full chain analysis |
| Trend Micro TRU — Void Dokkaebi | Apr 2026 | Scale data (750+ repos), `temp_auto_push.bat` |
| Securonix — DEV#POPPER | 2025–2026 | Stage 3–5 RAT/infostealer detail |
| JFrog Security Research — ChainVeil | 2026-06-24 | Full 5-stage chain confirmation |
