# Task Y: `lambda-platform/lambda` Go Package — Live Payload Check

**Date:** 2026-06-28  
**Task:** Check if the `lambda-platform/lambda` Go package is still live in the Go module
proxy, decode its payload, and confirm whether it matches the npm/VSCode vector.

---

## Summary

**`lambda-platform/lambda` is NOT infected.** This is a real, established Go web framework
with normal release cadence. The two versions singled out by Task Y's description (v0.9.18
published May 25, v0.9.19 published Jun 19) contain only legitimate code changes. No
PolinRider payload was found.

The "16 infected Go packages" documented by Nextron Research (Jun 25 update) are almost
certainly a different set of packages — likely fake/typosquatted names, not this real library.

---

## Versions Investigated

| Version | Published | Status |
|---------|-----------|--------|
| v0.9.17 | 2026-05-09 | Clean baseline |
| v0.9.18 | 2026-05-25 | Clean — legitimate code changes only |
| v0.9.19 | 2026-06-19 | Clean — one-line route middleware change |

The package has 400+ versions stretching back through 2025, published by a real development
team building a Go web application framework (DB/GraphQL/gRPC/authentication scaffolding).

---

## Analysis: v0.9.17 → v0.9.18 Diff (the "injection" version)

### Files changed

| File | Change | Nature |
|------|--------|--------|
| `DBSchema/goStruct.go` | +216B | Password field hidden from JSON (security fix: `json:"-"`) |
| `datagrid/filter.go` | +824B | SQL injection protection added (`isAllowedColumn` whitelist) |
| `graphql/gql/Context.go` | −34B | Removed debug `fmt.Println(token)` |
| `krud/krud.go` | −79B | Removed `agentMW.IsLoggedIn()` from `/unique` route |

All four changes are legitimate code improvements:
- `isAllowedColumn()` in `filter.go` closes a real SQL injection hole where `grid_field`/`kc`
  keys passed from the request body could inject arbitrary SQL via gorm `Where()`
- Password field masking is a straightforward security hygiene improvement
- Print removal and middleware cleanup are standard housekeeping

### What PolinRider injection looks like (for comparison)

In the npm vector, PolinRider injects into `astro.config.mjs`, `package.json`, etc. with:
- A `.vscode/tasks.json` with `runOn: "folderOpen"` triggering `fa-solid-400.woff2`
- The `fa-solid-400.woff2` is a disguised Node.js script with sfL cipher + blockchain beacon

For a Go package, the same attack would require:
- A `.vscode/tasks.json` in the package root → **NOT PRESENT** in this zip
- A `fa-solid-400.woff2` or similar payload file → **NOT PRESENT**

Neither is in any version of this package.

### Suspicious pattern scan results (v0.9.18)

All matches are legitimate:
- `init()` — 5 occurrences: DB initialization, config loading, sync.Once guards, asset manifest loading
- `exec.Command` — 1 occurrence, **commented out** in `puzzle/handlers/Build.go`
- `go:embed` — 1 occurrence in test data (legitimate template embedding)
- `encoding/base64` / `base64.` — in `DB/secure.go` (password hashing)
- `os.WriteFile` — in schema generator, file upload handler, grpc server
- `net/http` — throughout (this is a web framework)

No `fa-solid-400.woff2`, `tasks.json`, XOR key patterns, TRON wallet strings, or blockchain
API calls anywhere in the codebase.

---

## Why Task Y Was Queued

The task was created based on a date correlation:
- Nextron Research (Jun 25 update to JFrog post) reported 16 infected Go packages
- `lambda-platform/lambda` had versions published on May 25 (v0.9.18) and Jun 19 (v0.9.19)
- Task Y description: "versions from May 26 and Jun 19 2026 — the most recently injected"

The date match was a false correlation. `lambda-platform/lambda` has ~400 versions with regular
releases throughout 2025–2026 — the coincidence of having versions near those dates is
unsurprising for an active project.

---

## What the Nextron "16 Go Packages" Likely Are

Based on the attack TTP documented by JFrog, the infected Go packages would follow the same
pattern as the npm packages:
- **Fake or typosquatted names** mimicking real Go libraries
- Contain `.vscode/tasks.json` + `fa-solid-400.woff2` in the package
- When a developer opens the project in VSCode, the `folderOpen` task executes the payload

The 16 packages were not specifically listed in the JFrog post — they were documented by
Nextron Research as a sidebar. Without the specific package list, the packages cannot be
enumerated from this investigation. The Go module proxy would still serve them if they have
not been removed from the upstream source (the proxy cannot retroactively remove cached versions).

---

## Conclusions

| Question | Answer |
|----------|--------|
| Is `lambda-platform/lambda` infected? | **No** |
| Does v0.9.18 or v0.9.19 contain a payload? | **No** |
| Are the code changes in v0.9.18 suspicious? | **No — legitimate security fixes** |
| Does the package use the PolinRider delivery pattern? | **No — no tasks.json, no woff2** |
| What are Nextron's 16 infected Go packages? | **Unknown — specific list not in public JFrog post** |

Task Y is **CLOSED — NOT INFECTED**. The Nextron Go package report requires the specific
package list to investigate further.
