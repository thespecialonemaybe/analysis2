# Victim Analysis: TrustedSmartChain/tsc-signer (5-3-341) + kinyichukwu/val-ai (5-2-328)

**Dates of injection:** 2026-05-13T18:57Z (val-ai) · 2026-05-19T19:25Z (tsc-signer)  
**Campaigns:** 5-3-341 · 5-2-328  
**Cipher:** `_$_913e` (seed 36301 — identical encoded string table across all `_$_913e` campaigns)  
**Status:** Both live and unpatched at time of analysis (2026-06-27)

---

## Summary

Two separate victims; two significant findings:

1. **TrustedSmartChain/tsc-signer (5-3-341):** The actor injected a payload into the signing
   CLI tool for a custom Cosmos-SDK Layer 1 blockchain. A signing tool is among the highest-value
   targets in this campaign — persistence on the developer's machine could expose private keys
   for the entire chain. The committer name forensic also reveals a new data point: local git
   `user.name = "Christian"` (first name only) vs the full GitHub profile "Christian Brotherson",
   matching the same truncation pattern seen in `"Faris"` vs `"Faris Aziz"` on the zurichjs
   injections.

2. **kinyichukwu/val-ai (5-2-328):** The largest author/committer gap in the campaign by far:
   **+10,878 hours (453 days)**, with a Feb 2025 commit rewritten and force-pushed in May 2026.
   The `5-2-*` campaign ID prefix (also used for zurichjs-conf 5-2-319) suggests this victim
   was processed in the same batch as the zurichjs third-campaign targets.

The val-ai injection on 2026-05-13 predates all other `_$_913e` external victims confirmed so
far, making it the **earliest known external infection** in the May–June 2026 wave.

---

## 1. TrustedSmartChain/tsc-signer — Campaign 5-3-341

### Injection Details

| Field | Value |
|-------|-------|
| Repository | TrustedSmartChain/tsc-signer |
| Infected file | `src/index.ts` |
| Commit SHA | `420c8efe2` |
| Commit message | "Add queries" |
| Author | `Christian Brotherson <108023689+cbrotherson@users.noreply.github.com>` |
| Author date | 2026-04-15T17:09:58Z (34 days before injection) |
| Committer name | **`Christian`** ← local git config (first name only) |
| Committer email | `108023689+cbrotherson@users.noreply.github.com` |
| Committer date | 2026-05-19T19:25:54Z |
| Gap | **+818 hours 15 minutes (~34 days)** |
| Payload vector | `eval("global.i='5-3-341';" + atob('...'))` after trailing spaces in `src/index.ts` |
| Payload offset | byte 19,723 (file: 24,746 bytes total) |
| Clean file size | 11,761 bytes (parent commit `96c1a0866`) |
| Parent commit | `96c1a0866` — "Update readme" (2026-04-15T16:24Z) |

The actor rewrote a real April 15 developer commit, preserving all legitimate changes — including
the addition of a new file `src/query.ts` (262 lines) and 207-line-net update to `src/index.ts`
— while injecting the payload into `index.ts`. The `src/query.ts` file added in this commit is
clean; only `index.ts` contains the payload.

### Forensic: "Christian" vs "Christian Brotherson"

The author email `108023689+cbrotherson@users.noreply.github.com` and the committer email
`108023689+cbrotherson@users.noreply.github.com` are **identical** — same GitHub user ID 108023689,
confirmed as cbrotherson. The only difference is the name field:

- Author: `Christian Brotherson` (full name, from original commit)
- Committer: `Christian` (first name only, from local `user.name` config on the compromised machine)

This is the same truncation pattern observed in the zurichjs injections where `"Faris Aziz"` (full
name in real commits) became `"Faris"` (local machine git config) in injected committer fields.
The compromised developer's local `user.name` is set to just `Christian` — possibly a deliberate
short name preference, or a default set during workstation provisioning.

The same GitHub user ID in both fields definitively places the injection as running from
**cbrotherson's own machine** using his local git credentials — not a different machine with the
same name.

### Target: TrustedSmartChain — a Custom Cosmos L1 Blockchain

TrustedSmartChain (GitHub org, created 2025-03-17) operates a custom Layer 1 blockchain built on
the Cosmos SDK. Their public repos reveal the scope:

| Repo | Purpose |
|------|---------|
| `tsc` | Main chain software |
| `tsc-signer` | **Signing CLI tool** (infected) |
| `mainnet-genesis` | Mainnet genesis configuration |
| `testnet-genesis` | Testnet genesis configuration |
| `devnet-genesis` | Devnet genesis configuration |

`tsc-signer` is a command-line signing tool; its clean `src/index.ts` ends with a `main()` call
that processes signing operations. The codebase also references `MSG_EXTEND_TYPE_URL` and cosmos
address types — consistent with a Cosmos SDK validator/delegator signing tool.

cbrotherson (GitHub ID 108023689, created 2022-06-22) also maintains:
- `chain-registry` (a fork of the Cosmos chain registry)
- `assetlists` (Cosmos asset list data)
- `keplr-chain-registry` (Keplr wallet chain registry fork)

This developer works in the Cosmos ecosystem and has access to the TSC chain's signing
infrastructure. If the Stage 3 RAT achieved persistence on cbrotherson's machine:

- **Private signing keys** for TSC chain operations accessible
- Access to mainnet validator credentials or transaction signing material
- The `tsc` main chain software repository writable (further supply chain attacks possible)
- Cosmos ecosystem connections (chain-registry contributions) as pivot points

A signing tool developer is the highest-privilege target in a blockchain organisation —
equivalent to compromising an HSM operator.

---

## 2. kinyichukwu/val-ai — Campaign 5-2-328

### Injection Details

| Field | Value |
|-------|-------|
| Repository | kinyichukwu/val-ai |
| Infected file | `tailwind.config.ts` |
| Commit SHA | `820f49abb` |
| Commit message | "Increase timeouts for OpenAI requests, optimize image processing with sharp, and improve error handling messages" |
| Author | `kinyichukwu <kinyichukwuose@gmail.com>` |
| Author date | 2025-02-14T12:02:08Z |
| Committer name | `kinyichukwu` |
| Committer email | `kinyichukwuose@gmail.com` |
| Committer date | 2026-05-13T18:57:46Z |
| **Gap** | **+10,878 hours 55 minutes = 453 days** |
| Payload vector | `eval("global.i='5-2-328';" + atob('...'))` on same line as `export default config;` |
| Trailing spaces | 596 spaces between `export default config;` and the eval call |
| Injection line | Line 80 of `tailwind.config.ts` |

The **453-day gap** is by far the largest observed in the campaign. A commit from February 14,
2025 was rewritten and force-pushed on May 13, 2026. This is not an extended infection window —
the repo was not compromised in early 2025. Rather, the actor selected a **very old commit** as
the base for the force-push rewrite, which mechanically produces a large author/committer gap.

The strategic reason for picking an old commit: the force-push replaces only the tip commit.
With a 453-day-old commit as the target, the commit's author date looks like normal old history
while the committer date (today) is recent. Any monitoring focused on "recent commits" would
see an old author date and potentially dismiss it.

### Injection Location: Same-Line Trailing-Space Injection

Unlike the most common pattern (injecting on a new blank-looking line after trailing spaces),
this injection is **on the same line** as `export default config;`:

```
export default config;[596 spaces]eval("global.i='5-2-328';"+atob('...'))
```

The GitHub diff shows `+1 -1` for `tailwind.config.ts` — one line was replaced (the original
`export default config;\n` became the same with 596 trailing spaces and the eval appended).

This is functionally identical to trailing-space injection but produces a slightly different
diff signature: rather than showing a new blank-looking line added, it shows one line changed —
which looks like a minor edit to an existing line.

### Campaign Number: `5-2-328` — Same Batch as zurichjs-conf

The campaign prefix `5-2-*` is shared with `5-2-319` (zurichjs-conf PR #199, June 26, 2026).
The sub-number 328 > 319 suggests `val-ai` was processed later in the same campaign generation
than the zurichjs third-campaign target. Both share:
- The same `_$_913e` cipher with identical encoded string tables
- The same C2 wallet addresses and blockchain dead-drops
- The same eval/atob injection wrapper

This confirms the `5-2-*` prefix designates a specific targeting batch — possibly corresponding
to a particular stolen credential set or a time-bounded campaign phase.

### Victim Profile: kinyichukwu

- **GitHub login:** kinyichukwu  
- **Display name:** Kinyichukwu  
- **Account created:** 2021-03-26 (5-year-old account)  
- **Public repos:** 84 — mix of Next.js, AI/ML, full-stack projects  
- **Real email (local git):** `kinyichukwuose@gmail.com`  
- **Committer name matches GitHub username:** The local git `user.name` was set to `kinyichukwu`

`val-ai` is an AI avatar generation service using OpenAI's image generation API. It processes
image uploads and uses OpenAI to generate styled avatar images, deployed as a Next.js application
with Vercel. The repo was created February 12, 2025 with active development through February 14.

With 84 public repos, kinyichukwu is a prolific developer — likely to have live production
services and stored API credentials on their development machine.

---

## Campaign Ordering — Numbers Are Not Injection Order

The campaign IDs across confirmed victims do not map to injection chronology:

| Injection time (UTC) | Campaign | Target |
|---------------------|----------|--------|
| 2026-05-13T18:57Z | **5-2-328** | kinyichukwu/val-ai |
| 2026-05-19T19:25Z | **5-3-341** | TrustedSmartChain/tsc-signer |
| 2026-05-20T02:23Z | 5-3-225 | cleaner55555/brandspark-ai-studio |
| 2026-05-20T02:26Z | 5-3-225 | cleaner55555/eve-code |
| 2026-05-20T02:30Z | 5-3-225 | cleaner55555/reflection-business-erp |
| 2026-05-20T08:04Z | 5-3-252 | TypeTerrors/Stable-Diffuser-UI |
| 2026-05-25T15:55Z | 5-3-296 | Lu-Yanru/42_Needle_Hackathon |
| 2026-05-25T17:02Z | 5-3-296 | artzkaizen/transcribe |
| 2026-05-25T18:31Z | 5-3-298 | zurichjs-conf PR#177 |
| 2026-05-25T18:32Z | 5-3-298 | zurichjs-website |

5-3-341 (injected May 19) has a **higher number** than 5-3-225, 5-3-252, 5-3-296, and 5-3-298,
all of which were injected **after** it. Similarly 5-2-328 (injected May 13) is earlier than all
`5-3-*` injections.

**Conclusion:** Campaign IDs are assigned at **configuration time** (when the actor prepares
targets), not at injection time. The actor pre-generates IDs for a batch of targets and then
runs injections over days or weeks in an order unrelated to the numbering. This makes campaign
ID ordering an unreliable chronological signal.

---

## Shared Payload — `_$_913e` String Table Confirmed Identical

Both `5-3-341` and `5-2-328` decode to 3,743-byte inner payloads with:
- The same 792-character encoded string table (`uldhbnle%at&Woe%...`)
- `_$_913e` cipher, seed 36301
- Identical IOCs: TRON W1/W2, BSC dead-drops, XOR keys, guard key `_p_t`

The encoded table is byte-for-byte identical to all confirmed `_$_913e` campaigns (5-3-225,
5-3-252, 5-3-296, 5-3-298). One compiled Stage 0 binary is reused across all targets with only
the campaign ID string changed per-target.
