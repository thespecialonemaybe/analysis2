# Report Comparison: CTI_REPORT_ZURICHJS vs CTI_REPORT_POLINRIDER
### What's in each report, what's unique to each, and who should receive which

**Last updated:** 2026-07-23

---

## Quick Reference

| Need | Use |
|------|-----|
| Brief a team about the ZurichJS incident specifically | **CTI_REPORT_ZURICHJS.md** |
| Send to ZurichJS org, affected developers, or orgs with similar incidents | **CTI_REPORT_ZURICHJS.md** |
| Full campaign picture for SOC, Threat Hunting, Threat Detection | **CTI_REPORT_POLINRIDER.md** |
| Deploy detection rules (YARA, Sigma, hunt queries) | **CTI_REPORT_POLINRIDER.md** |
| Share with an external audience unfamiliar with PolinRider | **CTI_REPORT_POLINRIDER.md** |

---

## What ZurichJS Report Has That the Full Report Does Not

These items are specific to the ZurichJS incident and are either absent from or only
summarized in `CTI_REPORT_POLINRIDER.md`.

### Incident-specific commit data
- Injection and remediation commit hashes for both campaigns
  - 5-3-161: injection `556dba47`, remediation `87196d26`
  - 5-3-298: injection `bd6cf2ba`, remediation `19ef30866`
- Commit messages used as cover ("fix(tshirt): resolve hydration mismatch error...", "fix twint")
- Cover-commit technique detail for 5-3-298: the legitimate TWINT payment button in `donate.tsx`
  was added in the same commit to make it appear routine

### Dwell-time and timing data
- 74-day dwell for 5-3-161
- 21h 14min active window for 5-3-298
- Exact UTC timestamps for injection and remediation
- 6-day pre-staging timeline: W4 and W3 TRON dead-drops written May 19 before the May 25 injection

### farisaziz12 account detail
- GitHub ID 53216647
- Use in both campaigns (same account, same machine compromised)
- Evidence of persistent access: actor re-injected 21 days after first remediation

### 5-3-161 vs 5-3-298 capability comparison table
- Full side-by-side of what changed between the two campaigns: C2 port/framework,
  malware class (harvester → RAT), persistence added, remote shell added
- Actor test-hostname changes between campaigns:
  `EV-CHQG3L42M` / `EV-4A6OE6M0E` → `EV-CHQG3L42MMQ` / `EV-4A6OE6M0E2D`

### ZurichJS-specific file hashes
- `postcss.config.mjs` infected version (5-3-298):
  `c1314e72963f6be2aaa0f5d51a34608203b69401eb7e4b2828f5fc7413febc37`
- Stage 1 decrypted (5-3-298):
  `d017fe6e8e138630575050902acde5a41a4d676f73eace64ecc47d49262e2330`
- Stage 4 from C2 (2026-06-05, 5-3-298):
  `c74e11f97168d9f1f3a434248c9d875b0012cca23e90a5940b7bd4a61063172d`

### 5-3-161 specific content
- Original Stage 5 Python infostealer delivery (not present in 5-3-298 decoded chain)
- Old C2 framework: EmbedIO/C# on port 27017, compared to Express.js/Node.js on 443
- Port 27017 decoy: nginx 302 → legitimate GitHub file (analyst misdirection detail)
- Stage 1 dual-path (eval + spawn) architecture, which simplified in 5-3-298
- Additional Trend Micro TRU C2 IPs (154.91.0.196, 85.239.62.36, 83.168.68.219, etc.)
  that appeared in ANALYSIS_REPORT.md but were not validated in this investigation

### IR guidance framed for ZurichJS cloners
- Specific window (May 25 18:32 UTC to May 26 15:46 UTC) to check against clone/run logs
- PostCSS as the specific trigger (not just "any build")

---

## What the Full Report Has That the ZurichJS Report Does Not

These items go beyond the ZurichJS incident and reflect broader campaign research.

### A6 npm packages (9 malicious packages — ChainVeil series)
- `tailwindcss-merge`, `sass-formats`, `sass-format`, `tailwindcss-animates-kit`,
  `tailwindcss-animatics`, `clsx-tailwind`, `rate-limit-flexible`, `rate-limits-flexible`,
  `typeorm-encrypt`
- Campaign ID: A6-519-79 (confirmed in sass-formats 1.0.2 advisory)
- New cipher seed 2540575 (tailwindcss-merge — distinct from prior seeds)
- Removed by Amazon Inspector 2026-06-11 (13 days before JFrog disclosure)
- Typosquatting targets, file hashes from OSV advisories MAL-2026-5625 through 5633

### Go packages (16 packages)
- The `lambda-platform/lambda` hijacking and 16-package npm/Go delivery vector
- Execution path and Go-specific delivery details

### Additional victim repos and organizations
- DataStax (5 repos, Jan–Feb 2026)
- Neutralinojs (4 repos, 8,400 stars)
- 33+ framework config file infections across the broader campaign
- 750+ total infected public repositories (Trend Micro scale data)

### Full C2 infrastructure across all campaigns
- `23.27.13.43` (A6-prefix victim C2, Jun 20–25 only) — not used in ZurichJS
- `136.0.9.8` (former C2, confirmed dead) — not used in ZurichJS
- WinRM fleet signature details (4 of 6 C2 IPs with port 5985 open)
- Full Shodan fingerprinting across all 6 IPs

### Wallet W1 / W2 (canonical wallets used in non-ZurichJS campaigns)
- `TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP` (W1) and `TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG` (W2)
- The ZurichJS campaigns used W4/W5/W3 (TCqf6Z, TFMryB9, TA48dct); W1/W2 emerged later
  in the campaign and appear in the AX-series infections (aegre/damian, etc.)
- W4 payload recovery task (AY) — unresolved, 23 pruned BSC TX hashes documented

### YARA rules (4 rules)
- `PolinRider_Stage1_Loader` — XOR key + wallet + TRON/Aptos string detection
- `PolinRider_Persistence_Marker` — app file injection marker detection
- `PolinRider_Stage0_FakeFont` — fake .woff2 file detection
- `PolinRider_VSCode_TasksJson` — malicious tasks.json detection

### Sigma rules (5 rules)
- C2 boot beacon (`/$/boot` + `Sec-V:` header)
- Blockchain dead-drop DNS detection
- Detached node -e spawn detection
- WinRM outbound to C2 IPs
- VS Code / npm file modification

### Hunt queries (7 queries)
- Proxy/DNS-based blockchain API detection
- `/$/boot` beacon query
- node -e process spawn query
- lockfile retroactive exposure search
- App file marker grep
- `~/.node_modules` existence check
- Exfil archive filename pattern

### A6 scope analysis
- GitHub code-search results confirming A6 campaign IDs only appeared in npm packages,
  not in infected GitHub repositories — the npm packages are the sole delivery vector for A6

### Actor OPSEC section
- Infrastructure provider lock-in: 100% AS149440 Evoxt
- Wallet silence precedes public disclosure pattern (W3 silent 16 days before JFrog)
- Pre-staging behavior documented as a repeating pattern
- Self-exclusion hostname blocklist evolution

---

## What Both Reports Cover

These items appear in both reports (sometimes at different levels of detail):

| Item | ZurichJS report | Full report |
|------|-----------------|-------------|
| Stage 0–5 kill chain | Yes (5-3-298 detailed) | Yes (composite summary) |
| temp_auto_push.bat technique | Yes (full detail) | Yes (summary) |
| farisaziz12 initial access: unconfirmed | Yes | Yes |
| Primary C2 `198.105.127.210` | Yes | Yes |
| W3/W4/W5 TRON wallets | Yes (with ZurichJS TX dates) | Yes (current status) |
| XOR keys | Yes | Yes |
| Persistence markers (`/*RS260605*/`) | Yes | Yes |
| Stage 3 app injection targets | Yes | Yes |
| Stage 5 exfil: Telegram + C2 /u/e /u/f | Yes (brief) | Yes |
| Attribution: DPRK / Famous Chollima | Yes (brief) | Yes (full) |
| IR checklist | Yes (scoped to ZurichJS clone scenario) | Yes (general) |

---

## Audience Guidance

**`CTI_REPORT_ZURICHJS.md` — send to:**
- ZurichJS organization / zurichjs-website maintainers
- Developers who cloned `zurich-js/zurichjs-website` and may have run a build during the
  active windows (Feb 19 – May 4, 2026 for 5-3-161; May 25–26, 2026 for 5-3-298)
- IR teams investigating a specific victim machine tied to this incident
- Any audience that needs the incident facts without the full campaign scope

**`CTI_REPORT_POLINRIDER.md` — send to:**
- Internal SOC teams deploying detection rules
- Threat detection and threat hunting teams building coverage
- IR teams who need to scope beyond ZurichJS to the broader campaign infrastructure
- Any team needing the full IOC set (all wallets, all C2 IPs, npm packages, Go packages)
- External sharing with partner organizations or ISACs

**`CTI_REPORT_COMPARISON.md` (this file) — use for:**
- Internal briefing prep: knowing which report to pull for which audience
- Onboarding analysts joining the investigation mid-stream
- Verifying that a specific data point (e.g., a commit hash, a campaign ID) is in the
  right report before sending it out
