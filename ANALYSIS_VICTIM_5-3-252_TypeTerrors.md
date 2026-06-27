# Victim Analysis: TypeTerrors/Stable-Diffuser-UI — Campaign 5-3-252

**Date of injection:** 2026-05-20T08:04Z  
**Campaign:** 5-3-252  
**Cipher:** `_$_913e` (seed 36301 — identical to 5-3-225 and 5-3-298)  
**Status:** Live and unpatched at time of analysis (2026-06-27)  
**Victim type:** Real developer — Web3/AI engineer, personal project repo

---

## Summary

The actor force-pushed a **130-day-old legitimate commit** (`f85a13b9ba`) with the campaign
5-3-252 payload injected into `fe/postcss.config.mjs`. The original developer commit ("add
button to download prompt for specific image") dated 2026-01-10 was rewritten and re-pushed
on 2026-05-20T08:04Z — the same day as the `cleaner55555` wave (which completed at 02:30Z,
5.5 hours earlier).

A critical operator error surfaced during this injection: **the committer name field is "Joe"**,
not the developer's name. The actor spoofed the author email (`nate@natd.ca`) but their own
git `user.name = "Joe"` leaked into the committer metadata. This is the same class of error
seen in the zurichjs campaigns where "Faris" vs "Faris Aziz" differed between injections —
consistent with `temp_auto_push.bat` running from a different machine or operator account for
each target.

---

## Injection Details

| Field | Value |
|-------|-------|
| Repository | TypeTerrors/Stable-Diffuser-UI |
| Infected file | `fe/postcss.config.mjs` |
| Infected commit SHA | `f85a13b9ba4a8b2c2ad7e5d3f1c0e9b8a7d6e5f4` |
| Original author | `nate del duca <nate@natd.ca>` |
| Original author date | 2026-01-10T04:26:43Z (legitimate commit, ~130 days before injection) |
| Committer name | **`Joe`** ← operator git config leak |
| Committer email | `nate@natd.ca` (spoofed to match author) |
| Committer date | 2026-05-20T08:04:09Z |
| Gap | **+3,097 hours (~130 days)** |
| Parent commit | `19415236a3` (legitimate merge commit, 2026-01-09) |
| Other files in commit | `be/internal/services/api_handlers_rest.go`, `fe/src/app/_home/useHomeController.ts`, `fe/src/app/page.tsx`, `fe/.gitignore`, `fe/eslint.config.mjs`, `fe/src/app/_home/utils.ts` — all legitimate developer changes from Jan 2026 preserved |

---

## Operator Forensic: Committer Name "Joe"

This is the most significant finding from this victim analysis.

In all zurichjs injections the committer name was either `Faris` or `Faris Aziz` — the
compromised developer's own name, correctly spoofed. Here, the actor spoofed the email
(`nate@natd.ca`) but left their own git identity (`user.name = Joe`) in the committer field.

Cross-referencing committer names across confirmed injection commits:

| Campaign | Commit | Committer name | Match to developer? |
|----------|--------|----------------|---------------------|
| 5-3-161 | `556dba47ce` (zurichjs-website) | `Faris` | Partial (real name: Faris Aziz) |
| 5-3-298 | `4b46f2e197` (zurichjs-conf PR#177) | `Faris` | Partial |
| 5-3-298 | `bd6cf2bae2` (zurichjs-website) | `Faris` | Partial |
| 5-3-161 | `a035927600` (zurichjs-conf PR#77) | `Faris` | Partial |
| 5-2-319 | `e7b90585dc` (zurichjs-conf PR#199) | `Faris Aziz` | Full |
| 5-3-225 | `bac9f171cc` (reflection-business-erp) | `Z User` | No (developer git unconfigured) |
| 5-3-225 | `f75f8c70d7` (brandspark-ai-studio) | `Z User` | No |
| 5-3-225 | `204b38cd01` (eve-code) | `Nate Sesti` | No (upstream commit author) |
| **5-3-252** | **`f85a13b9ba`** | **`Joe`** | **No — operator name leaked** |

**"Joe" is a new operator identity** not seen in any prior injection. Two explanations:
1. The actor runs `temp_auto_push.bat` from multiple machines with different git configs,
   and the machine used for `TypeTerrors` had `user.name=Joe` set.
2. Multiple operators share the tooling; "Faris"-configured machines handle the zurichjs
   targets while a "Joe"-configured machine handled this one.

Either way, `Joe` is an operator-level IOC distinct from the compromised developer account.

---

## Victim Profile

- **GitHub login:** TypeTerrors
- **Display name:** Type Terrors
- **Account created:** 2024-07-03 (2-year-old account)
- **Public repos:** 12 — primarily Go backend projects, one TypeScript project
- **Developer identity:** Uses `nated.eth` as git identity in some commits — active Web3
  participant; owns `nated.ca` domain; repos include `nated.ai` and `nated.io`
- **`Stable-Diffuser-UI`:** Self-hosted Stable Diffusion frontend for an NVIDIA DGX Spark
  (a personal AI accelerator card). This is a personal project for local AI image generation,
  indicating the developer has a high-capability GPU workstation — exactly the kind of machine
  the actor's Stage 3 RAT would want persistent access to.

---

## Payload Analysis

Stage 0 string table (63 strings, `_$_913e`, seed 36301) is **byte-for-byte identical** to
campaigns 5-3-225 and 5-3-298. All IOCs are shared:

- W1 TRON: `TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF`
- W2 TRON: `TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH`
- BSC dead-drop 1: `0x9d202c824402ca89e9aaccd2390b6f8b332ae743caa1469c695feb2781d56519`
- BSC dead-drop 2: `0x3d2075f97b7b1e3234bd653779d21c605d7d8c6ec9c98d983880be5c7f4f9471`
- XOR key 1: `2[gWfGj;<:-93Z^C`
- XOR key 2: `m6:tTh^D)cBz?NM]`
- Guard key: `_p_t`

The campaign ID `5-3-252` is the only differentiator. This confirms that across campaigns
5-3-225, 5-3-252, and 5-3-298 the actor deployed **one compiled Stage 0 binary** and only
varied the injected campaign ID string per target.

---

## Why a DGX Spark Developer is a High-Value Target

`Stable-Diffuser-UI` is a personal Stable Diffusion interface for a DGX Spark. If the actor's
Stage 3 RAT achieved persistence on this machine:

- GPU resources available for actor use (compute theft / cryptomining)
- Local model weights and generated images accessible
- `nated.eth` wallet potentially accessible via browser/local keystore
- Other developer projects on the same machine (Go services, AI agents) could be further
  compromised and used to pivot to downstream infrastructure

---

## 2026-05-20 Wave Summary

| Time (UTC) | Victim | Campaign | Committer leaked |
|------------|--------|----------|-----------------|
| 02:23Z | cleaner55555/brandspark-ai-studio | 5-3-225 | — (Z User, env default) |
| 02:26Z | cleaner55555/eve-code ×2 | 5-3-225 | — |
| 02:30Z | cleaner55555/reflection-business-erp | 5-3-225 | — |
| 08:04Z | **TypeTerrors/Stable-Diffuser-UI** | **5-3-252** | **`Joe`** |

The 5.5-hour gap between the `cleaner55555` wave and the `TypeTerrors` injection suggests
these were separate automation runs, possibly from different machines or against different
credential sets stolen at different times.
