# Victim Analysis: artzkaizen/transcribe + Lu-Yanru/42_Needle_Hackathon — Campaign 5-3-296

**Date of injections:** 2026-05-25T15:55Z (Lu-Yanru) and 2026-05-25T17:02Z (artzkaizen)  
**Campaign:** 5-3-296  
**Cipher:** `_$_913e` (seed 36301 — identical to 5-3-225, 5-3-252, and 5-3-298)  
**Status:** Live and unpatched at time of analysis (2026-06-27)  
**New technique:** `eval(atob(...))` wrapper around base64-encoded payload in TypeScript entry points

---

## Summary

Campaign 5-3-296 infected two repositories on 2026-05-25, both attributable to a **single
compromised machine** belonging to GitHub user `Artzkaizen` ("Jace"):

- `artzkaizen/transcribe` — Jace's own project (gap: +795 hours)
- `Lu-Yanru/42_Needle_Hackathon` — a collaborator repo where Jace had push access (gap: +77 hours)

Both injections occurred in the same afternoon, completing **~3 hours before** the zurichjs wave
(18:31–18:32Z) on the same day. The order suggests the actor ran a batch against Jace's accessible
repos first, then pivoted to the farisaziz12-accessible repos.

A key new finding in this campaign is the **injection vector**: rather than appending a raw
JavaScript payload after trailing whitespace in a config file, the actor injected base64-encoded
payloads via `eval("global.i='5-3-296';" + atob('...'))` calls directly into TypeScript server
entry points (`src/index.ts`, `src/main.ts`). The base64 encoding hides the payload from naive
`grep` searches on committed files.

---

## Infected Repositories

### 1. artzkaizen/transcribe — `src/index.ts`

| Field | Value |
|-------|-------|
| Repository | artzkaizen/transcribe |
| Infected file | `src/index.ts` |
| Infected commit SHA | `e8c483e9d7` |
| Commit message | "Add pagination to transcripts listing and implement delete endpoint for transcripts…" |
| Original author | `Jace <121627078+Artzkaizen@users.noreply.github.com>` |
| Author date | 2026-04-22T13:17:25Z (legitimate 33-day-old commit) |
| Committer name | `Jace` |
| Committer email | `121627078+Artzkaizen@users.noreply.github.com` |
| Committer date | 2026-05-25T17:02:29Z |
| Gap | **+795 hours (~33 days)** |
| Payload offset | Byte 9715 — after `export default app;` + 2,700+ trailing spaces |
| Payload size | 3,743 bytes (base64-wrapped) |

The commit rewrites a legitimate developer change from April 22 — "add pagination" and "delete
endpoint" are real features, preserved in full. The injection is hidden after the final export
statement behind thousands of trailing spaces, then delivered as:

```
eval("global.i='5-3-296';" + atob('BASE64_PAYLOAD_HERE'))
```

At 9,715 bytes total, the full file extension on disk is near-invisible to casual inspection.
The base64 payload decodes to 3,743 characters of minified JavaScript containing the `_$_913e`
Stage 0 cipher with seed 36301.

---

### 2. Lu-Yanru/42_Needle_Hackathon — `apps/server/src/index.ts` + `apps/agent/src/main.ts`

| Field | Value |
|-------|-------|
| Repository | Lu-Yanru/42_Needle_Hackathon |
| Infected files | `apps/server/src/index.ts` and `apps/agent/src/main.ts` |
| Infected commit SHA | `02ab282b58` |
| Commit message | "Merge branch 'main' of github.com:Lu-Yanru/42_Needle_Hackathon" |
| Commit type | **Merge commit** (2 parents: `4a026c569`, `b4ed04789`) |
| Original author | `Jace <arbeitchuka@gmail.com>` |
| Author date | 2026-05-22T10:19:23Z (3-day-old merge commit) |
| Committer name | `Jace` |
| Committer email | `arbeitchuka@gmail.com` |
| Committer date | 2026-05-25T15:55:40Z |
| Gap | **+77 hours 36 minutes** |
| Repo created | 2026-05-21T08:45:50Z |
| Repo age at infection | **4 days** |

Two server entry points were injected with the same `eval(atob(...))` pattern:
- `apps/server/src/index.ts` — likely an Express/Fastify server entry
- `apps/agent/src/main.ts` — likely an AI agent or background worker process

Both payloads carry campaign ID `5-3-296` and are base64-encoded with the identical Stage 0 string
table as all other `_$_913e` campaigns.

The repo is a hackathon project — created May 21, infected May 25. It would never have been the
actor's primary target; Lu-Yanru is a **collateral victim**.

---

## Collateral Victim: How Lu-Yanru Was Infected

`Lu-Yanru/42_Needle_Hackathon` was created 2026-05-21 as a hackathon project. Jace (artzkaizen)
contributed to the project as a collaborator with push access. When Jace's machine was
compromised, `temp_auto_push.bat` scanned all repositories accessible via the local git
credential store and injected each in sequence.

The actor did not target Lu-Yanru — they targeted Jace. Lu-Yanru's repo was collateral damage
from the same automation run.

Evidence for the collaborator attack surface:
- The infected commit `02ab282b58` is a **local merge commit** authored by Jace with his
  personal email `arbeitchuka@gmail.com` — not a commit created by Lu-Yanru
- The committer is also Jace — not the repo owner
- The timing fits: transcribe infected at 17:02Z, Lu-Yanru at 15:55Z, both within ~90 minutes,
  consistent with a single automation batch scanning multiple repos

This is a notable escalation: the infection propagates not just through the victim's own repos
but through **any repo they have write access to**, including collaborator repos belonging to
other developers who have no connection to the actor's primary target.

---

## New Injection Vector: `eval(atob(...))` in TypeScript Entry Points

Previous campaigns (`_$_46e0`, `_$_913e` in config files) appended raw JavaScript payloads
after trailing whitespace at the end of configuration files. Those payloads are visible to grep
as literal strings.

Campaign 5-3-296 introduces a new vector:

```typescript
// end of src/index.ts — legitimate code
export default app;                                          // real last line
                                                             // 2700+ trailing spaces
eval("global.i='5-3-296';" + atob('WyJyIiwib2JqZWN0...'))  // injected payload (base64)
```

**Why this is harder to detect:**
- `grep -r '_\$_913e'` on committed files finds nothing — the cipher name is inside the base64
- `grep -r 'global\.i='` finds the eval wrapper, but `global.i=` also appears in legitimate code
- The `eval()` and `atob()` calls look like a debugging snippet if spotted in isolation
- Standard static analysis of TypeScript source must decode base64 to identify it as malicious

The inner payload (3,743 bytes after decoding) is byte-for-byte identical to the `_$_913e`
Stage 0 deployed in config files across all other campaigns — same cipher, same seed, same string table.

---

## Forensic: Committer Identity and Email Discrepancy

The committer field in both injected commits identifies "Jace" — the compromised developer's own
git identity, consistent with `temp_auto_push.bat` running from Jace's machine using his local
git credentials.

| Commit | Committer name | Committer email | Source |
|--------|---------------|-----------------|--------|
| `e8c483e9d7` (transcribe) | `Jace` | `121627078+Artzkaizen@users.noreply.github.com` | GitHub privacy email (original commit was web/SSH) |
| `02ab282b58` (Lu-Yanru) | `Jace` | `arbeitchuka@gmail.com` | Local git config (`user.email`) |

The email difference is explained by the original commit context: the transcribe commit was
originally made with GitHub's privacy email substitution, so the committer field preserved that
email when the tree was rewritten. The Lu-Yanru commit was a local merge commit already using
Jace's real email.

The GitHub user ID `121627078` in the no-reply address confirms the committer is Artzkaizen —
this is a definitive machine-to-developer attribution via GitHub's own ID scheme.

---

## Payload Analysis

Stage 0 string table (63 strings, `_$_913e`, seed 36301) is **byte-for-byte identical** to
campaigns 5-3-225, 5-3-252, and 5-3-298. All IOCs are shared:

| IOC | Value |
|-----|-------|
| TRON W1 | `TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF` |
| TRON W2 | `TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH` |
| BSC dead-drop 1 | `0x9d202c824402ca89e9aaccd2390b6f8b332ae743caa1469c695feb2781d56519` |
| BSC dead-drop 2 | `0x3d2075f97b7b1e3234bd653779d21c605d7d8c6ec9c98d983880be5c7f4f9471` |
| XOR key 1 | `2[gWfGj;<:-93Z^C` |
| XOR key 2 / guard key | `m6:tTh^D)cBz?NM]` / `_p_t` |

The only differentiator is the campaign ID string `5-3-296`, confirming this is the same compiled
Stage 0 binary reused across the entire `_$_913e` wave with only the ID string swapped per target.

---

## Victim Profile: Jace / Artzkaizen

- **GitHub login:** Artzkaizen
- **GitHub ID:** 121627078
- **Display name:** Jace
- **Account created:** (not retrieved — active since at least 2024)
- **Public repos:** 49 — mix of TypeScript, Go, Docker tooling
- **Developer profile:** Full-stack developer; projects include `transcribe` (audio transcription
  service), `docker` (Bun HTTP proxy), and contributions to third-party hackathon projects
- **Notable:** Jace contributed to `42_Needle_Hackathon` as a collaborator — when his machine
  was compromised, his collaborator repos became attack surface

`transcribe` is an audio transcription service with a REST API. If the Stage 3 RAT achieved
persistence on Jace's machine:
- All locally stored audio transcripts and recordings accessible
- All git-accessible repos (49 own + collaborator repos) writable — further spread possible
- Any API keys or credentials in the development environment exposed

---

## 2026-05-25 Full Wave Timeline

These two injections took place on the same day as the zurichjs-conf PR #177 and zurichjs-website
infections, completing **before** the zurichjs injections:

| Time (UTC) | Target | Campaign | Committer | Vector |
|------------|--------|----------|-----------|--------|
| 15:55Z | Lu-Yanru/42_Needle_Hackathon (×2 files) | 5-3-296 | Jace / arbeitchuka@gmail.com | eval(atob) in .ts |
| 17:02Z | artzkaizen/transcribe | 5-3-296 | Jace / 121627078+Artzkaizen@… | eval(atob) in .ts |
| 18:31Z | zurichjs-conf PR#177 | 5-3-298 | Faris | trailing-space in .mjs |
| 18:32Z | zurichjs-website | 5-3-298 | Faris | trailing-space in .mjs |

The 2026-05-25 wave is the largest single-day injection event in the campaign, hitting 4 repos
across 3 organisations in under 3 hours from at least 2 different compromised machines (Jace's and
Faris's).
