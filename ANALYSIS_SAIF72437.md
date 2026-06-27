# Task N: saif72437 Full Infection Sweep

**Date:** 2026-06-27  
**Target:** `saif72437` GitHub account  
**Trigger:** Task G side discovery — all 30 (now 57) repos swept on 2026-06-15

---

## Summary

The `saif72437` GitHub account was fully swept by PolinRider's `config.bat` automation on
**2026-06-15 between 08:25–08:43 UTC** (18-minute window). Of 64 total repos, 57 were
updated in that window. 9 repos have live JS payload infections; 24 repos have
`temp_auto_push.bat` committed as an artifact.

Campaign ID extracted from live payload: `global['!']='8-765'` (outer) / `global['!']='11-#'` (inner).

---

## Sweep Timeline

| Metric | Value |
|--------|-------|
| Total repos | 64 |
| Repos updated June 15 | **57** |
| Sweep window | **08:25:37 – 08:43:31 UTC** (17m 54s) |
| Repos NOT swept | 7 (updated before/after June 15) |
| JS payload infections found | **9** |
| Repos with `temp_auto_push.bat` | **24** |
| Repos with no injectable target | ~24 (HTML/CSS/Java/Dart, no JS config files) |

The 57-repo sweep in under 18 minutes is consistent with `config.bat` (or the orchestrating RAT)
iterating through all locally-cloned repos with push access, invoking the bat file for each.
The `branch_structure.json` artifact likely pre-enumerated all repos as targets.

---

## Live JS Payload Infections (9 repos)

All 9 infections use the `_$_1e42` cipher with activation **2509** / return **1358**.

| Repo | Config file | Size |
|------|-------------|------|
| `medium-clone` | `tailwind.config.js` | 13,791b |
| `linkedin-post-editor` | `tailwind.config.js` | 14,536b |
| `Music-Academy` | `postcss.config.js` | 13,710b |
| `Growth-Automator-MVP` | `postcss.config.mjs` | 13,852b |
| `InnerBeast-Music-Player` | `tailwind.config.js` | 14,408b |
| `Email-Layout-Builder` | `postcss.config.mjs` | 13,852b |
| `FlowNote` | `postcss.config.mjs` | 13,798b |
| `abasin-consult` | `tailwind.config.js` | 14,126b |
| `Airbnb-Clone` | `next.config.js` | 13,741b |

**All 9 have identical payload tails** — confirmed by all sharing the same base64 tail:
`...KWVofW44bjIyY2cgUmNyUmUxTScpKTt2YXIgVGd3PWpGRChMUUkscFlkICk7VGd3KDI1MDkpO3JldHVybiAxMzU4fSkoKTs=`))`

Decoded: `...var Tgw=jFD(LQI,pYd);Tgw(2509);return 1358})();`

This confirms a single batch payload was deployed across all 9 repos.

---

## Bat Artifact Repos (24 repos with `temp_auto_push.bat` committed)

These repos had `config.bat`/`temp_auto_push.bat` executed but no injectable JS config file:

```
works-studio, vu-quiz-app, voice-and-text-translator-app, usability-hub,
two-good-co, sundown-studio, saif72437 (profile repo), responsive-music-website,
realtime-chatting-app, real-estate-app, nft-responsive, Mohammad-Naveed-Iqbal-minhas,
Lazarev, eco-brands, duo-studio, diet-plan-app, classes-with-lucah, BeSocially-,
anas-imtiaz, airplane-ticket-booking-app, aasim-shakeel, WebSockets,
full-stack-engineering-batch-1, saif-portfolio
```

These are mostly HTML/CSS portfolio projects, Java/Dart apps — no `tailwind.config.*` or
`postcss.config.*` to inject into. The bat ran, staged changes, attempted to amend the commit,
but had nothing to push (no payload staged). The bat file itself was then accidentally committed.

---

## Payload Structure — `_$_1e42` Wave, Inner Atob Layer

The payload in these repos has a two-layer structure:

```
OUTER (tailwind.config.js, line 9):
  global['!'] = '8-765'                    ← Campaign ID (outer)
  var _$_1e42 = (function(l,e){...})(...); ← outer cipher placeholder
  eval(atob('BASE64...'))                   ← decode and run inner layer

INNER (atob-decoded, 4,781 bytes):
  global['!'] = '11-#'                     ← Campaign ID override (inner)
  var _$_1e42 = (function(l,e){...cipher...})("rmcej%otb%", 2857687)
  global[_$_1e42[0]] = require              ← store require in global key
  if (typeof module === _$_1e42[1]) { global[_$_1e42[2]] = module }
  (function() {
    var LQI='', TUU=401-390;               // TUU=11
    function sfL(w) { ...cipher, seed=2667686... }  ← Stage 2 cipher
    var EKc = sfL('wuqktamcei...').substr(0,TUU);   // → 'constructor'
    var joW  = '...encoded decompressor...';
    var dgC  = sfL[EKc];                   // = Function constructor
    var Apa  = '';
    var jFD  = dgC;
    var xBg  = dgC(Apa, sfL(joW));         // build decompressor fn
    var pYd  = xBg(sfL('...stage2_enc...'));// decompress → Stage 2 body
    var Tgw  = jFD(LQI, pYd);             // Function('', stage2_body)
    Tgw(2509); return 1358;               // run Stage 2
  })();
```

**Inner cipher `sfL` parameters:**

| Parameter | Value |
|-----------|-------|
| Seed | **2667686** |
| Offset 1 | 228 |
| Mod 1 | 50332 |
| Offset 2 | 128 |
| Mod 2 | 52119 |
| Modulus | 4289487 |

These parameters are **distinct from the `Cot%3t=shtP` MDy cipher** (seed 1111436) — the
`_$_1e42` 2509/1358 cluster uses a different cipher instance for its Stage 2 bootstrap.

---

## Campaign IDs

| Layer | Value | Format |
|-------|-------|--------|
| Outer `global['!']` | `'8-765'` | `N-NNN` (older format) |
| Inner `global['!']` | `'11-#'` | `NN-#` (unclear — `#` may be literal) |

The outer `'8-765'` is set by Stage 0 for Stage 1 to read for victim routing. The inner
`'11-#'` overrides it when Stage 2 runs. The format differs from the newer `N-N-NNN` format
used in `_$_b229` campaigns (`'5-3-161'`, etc.).

If the format interpretation is consistent: `8-765` = batch 8, victim 765 (or similar
operator-defined scheme). The `#` in `'11-#'` may be a template placeholder filled at
injection time, or a literal character in this campaign's identifier.

---

## Developer Profile

`saif72437` appears to be a **Pakistani web development educator**:
- Courses: `full-stack-engineering-batch-1`, `full-stack-engineering-batch-2` (29 stars),
  `36-weeks-remote-jobs-preparation-challenge` (9 stars)
- Project portfolio: mix of Urdu/English names (`Umair-Portfolio-Website`, `Mohammad-Naveed-Iqbal-minhas`)
- Predominant stack: JavaScript/TypeScript, HTML/CSS, Flutter (Dart), some C++ and Java
- All repos are educational portfolio projects — low-stars, indicating this is a developer
  building skills rather than maintaining production software

The `config.bat` infection hit ALL repos regardless of stack — even Java and Dart repos got
the bat file, though the JS injection failed. This confirms the actor sweeps every git repo
with push access without filtering by stack first.

---

## Clean Repos (had injectable files but not infected)

| Repo | Notes |
|------|-------|
| `video-tube` | JavaScript, no tailwind/postcss found |
| `utube` | JavaScript, no tailwind/postcss found |
| `Postify` | JavaScript, has its own config structure |
| `PixelMind` | TypeScript, no standard config files |
| `full-stack-medium-clone` | TypeScript, no injected config |
| `cool-sketch` | TypeScript, no standard config files |
| `Magma` | JavaScript, no standard config files |
| `36-weeks-remote-*` | JavaScript, no standard config files |

These repos had the bat artifact run but no injectable config file was present (or had no
`node_modules`-typical config layout).

---

## Scale Comparison

| | saif72437 | Task L bat-file group | OSM combined |
|-|-|-|-|
| Total repos swept | 57 | 8 (config.bat) + 102 (interactive) | 1,950 |
| JS payload infected | 9 (16%) | ~22 (20%) | ~1,266 (65%) |
| Bat artifact | 24 (42%) | 102 (all) | 236 (12%) |
| Sweep duration | 18 min | unknown | distributed |
| Still live | 9/9 (100%) | 7/29 sampled | 1,807/1,950 (93%) |

The `_$_1e42` 2509/1358 cluster bat-file infections show consistently lower JS injection
success rates (~16-20%) vs the early campaign (65%) — likely because early OSM-tracked
victims were specifically selected for having JS config files, while the bat-file sweeps
hit all repos indiscriminately.

---

## IOCs (new from Task N)

```
# saif72437 — mass infection June 15, 2026
# 9 infected JS repos (all _$_1e42, act=2509, ret=1358)
saif72437/medium-clone               — tailwind.config.js
saif72437/linkedin-post-editor       — tailwind.config.js
saif72437/Music-Academy              — postcss.config.js
saif72437/Growth-Automator-MVP       — postcss.config.mjs
saif72437/InnerBeast-Music-Player    — tailwind.config.js
saif72437/Email-Layout-Builder       — postcss.config.mjs
saif72437/FlowNote                   — postcss.config.mjs
saif72437/abasin-consult             — tailwind.config.js
saif72437/Airbnb-Clone               — next.config.js

# Campaign IDs extracted from live payload
global['!']='8-765'   (outer — victim routing)
global['!']='11-#'    (inner — Stage 2 override)

# Inner cipher parameters (sfL, _$_1e42 wave)
seed=2667686, off1=228, mod1=50332, off2=128, mod2=52119, modulus=4289487

# Bat artifact repos (no JS payload, bat committed)
saif72437/works-studio, vu-quiz-app, voice-and-text-translator-app, usability-hub,
two-good-co, sundown-studio, saif72437, responsive-music-website,
realtime-chatting-app, real-estate-app, nft-responsive, Mohammad-Naveed-Iqbal-minhas,
Lazarev, eco-brands, duo-studio, diet-plan-app, classes-with-lucah, BeSocially-,
anas-imtiaz, airplane-ticket-booking-app, aasim-shakeel, WebSockets,
full-stack-engineering-batch-1, saif-portfolio
```
