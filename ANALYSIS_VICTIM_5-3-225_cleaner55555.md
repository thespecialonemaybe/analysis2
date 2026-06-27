# Victim Analysis: cleaner55555 — Campaign 5-3-225

**Date of injection:** 2026-05-20T02:23–02:30Z (7-minute window)  
**Campaign:** 5-3-225  
**Cipher:** `_$_913e` (identical to campaign 5-3-298)  
**Status:** Live and unpatched at time of analysis (2026-06-27)  
**Victim type:** Real developer — GitHub account created 2010-08-31 (16-year-old account)

---

## Summary

The actor compromised the machine or GitHub credentials of user `cleaner55555` and injected
campaign 5-3-225 payloads into **three repositories simultaneously** on 2026-05-20, completing
all force-pushes within a 7-minute window. This is consistent with the `temp_auto_push.bat`
automation scanning all writable repositories on the victim's machine and injecting each in
sequence.

The developer was an active user of AI coding assistants (Claude Code / Cursor, evidenced by
UUID-style auto-commit messages and a fork of the Continue.dev extension), making them a
high-value target for this campaign which specifically hunts developer workstations.

---

## Infected Repositories and Files

| Repo | File | Commit SHA | Injected | Author date | Gap |
|------|------|------------|----------|-------------|-----|
| `reflection-business-erp` | `postcss.config.mjs` | `bac9f171` | 2026-05-20T02:30Z | 2026-05-20T01:02Z | +87m |
| `brandspark-ai-studio` | `postcss.config.mjs` | `f75f8c70` | 2026-05-20T02:23Z | 2026-05-11T21:35Z | +11,808m (~8 days) |
| `eve-code` | `binary/build.js` | `204b38cd` | 2026-05-20T02:26Z | 2026-04-17T03:27Z | +47,458m (~33 days) |
| `eve-code` | `gui/postcss.config.cjs` | `204b38cd` | 2026-05-20T02:26Z | 2026-04-17T03:27Z | +47,458m (~33 days) |

**4 files across 3 repos, all in 7 minutes.** The `brandspark-ai-studio` and `eve-code` commits
have multi-day gaps, confirming old commits were rewritten and force-pushed — the actor
preserved original authorship metadata while changing the committer timestamp and content.

---

## Victim Profile

- **GitHub login:** cleaner55555
- **Account age:** Created 2010-08-31 — a long-standing real developer account, not a throwaway
- **Public repos:** 16 (spanning 2020–2026, variety of web/JS/TS projects)
- **Git author name:** `Z User` — indicates a misconfigured git identity, typical of a cloud IDE
  or AI coding environment where `user.name` was never set
- **Commit style:** Mostly UUID strings (`682fb62a-1b96-45bb-a374-c4c73887e31d`, etc.) —
  consistent with Claude Code or Cursor auto-commit mode where messages are generated without
  user input
- **`eve-code`:** A fork of `continuedev/continue` (the open-source AI coding assistant
  VS Code extension). The developer actively works with and modifies AI dev tooling.

The UUID commit pattern and Continue.dev fork together confirm this developer was heavily using
AI coding assistants. **The actor specifically targets developers using AI coding tools** — their
machines have Claude Code / Cursor sessions running with broad filesystem and git access, making
them ideal vectors for `temp_auto_push.bat` to operate undetected.

---

## Payload Analysis

The Stage 0 payload in all four files is **byte-for-byte identical** (4,820 bytes each where
applicable). String table decoded from `_$_913e` cipher (seed 36301):

```
[ 0] 'r'                    <- require alias
[ 1] 'object'               <- typeof check
[13] 'https'
[26] 'https://api.trongrid.io/v1/accounts/'       <- TRON dead-drop C2
[27] '/transactions?only_confirmed=true&only_from=true&limit=1'
[33] 'https://fullnode.mainnet.aptoslabs.com/v1/accounts/'  <- Aptos fallback
[39] 'eth_getTransactionByHash'  <- BSC RPC method
[40] 'bsc-dataseed.binance.org'
[41] 'bsc-rpc.publicnode.com'
[49] '_p_t'                 <- re-execution guard key
[50] '2[gWfGj;<:-93Z^C'    <- XOR key (shared across ALL campaigns)
[51] 'TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF'  <- W1 TRON wallet
[52] '0x9d202c824402ca89e9aaccd2390b6f8b332ae743caa1469c695feb2781d56519'  <- BSC dead-drop 1
[53] 'm6:tTh^D)cBz?NM]'    <- second XOR key (new — not seen in 5-3-161)
[54] 'TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH'  <- W2 TRON wallet
[55] '0x3d2075f97b7b1e3234bd653779d21c605d7d8c6ec9c98d983880be5c7f4f9471'  <- BSC dead-drop 2
[56] 'node'
[57] '-e'
[58] "global['_V']='"       <- Stage 1 invocation prefix
[59] "';"
[60] 'ignore'
[61] 'spawn'
[62] 'child_process'
```

**IOC overlap with known campaigns:** 100% — same TRON wallets (W1, W2), same BSC dead-drop
hashes, same XOR key `2[gWfGj;<:-93Z^C`, same C2 infrastructure as campaigns 5-3-161, 5-3-298,
and 5-2-319. The only unique element is a second XOR key at index [53] (`m6:tTh^D)cBz?NM]`)
which was also present in 5-3-298 but not 5-3-161.

**`binary/build.js` injection:** Infecting a build script (`binary/build.js`) in a fork of
Continue.dev is a more aggressive injection target than a PostCSS config — build scripts execute
during `npm run build` and in CI pipelines. If this fork were ever used to build and distribute
a Continue extension, the payload could reach downstream users.

---

## New IOC: Second XOR Key

```
'm6:tTh^D)cBz?NM]'   (string table index [53])
```

This key appears in stage 0 string tables for campaigns using `_$_913e` (5-3-225, 5-3-298) but
is absent from 5-3-161 (`_$_46e0`). It is likely a second-layer XOR key used for decoding
one of the blockchain-retrieved payloads.

---

## Injection Wave Context

The `cleaner55555` injections at 02:23–02:30Z on 2026-05-20 are part of a broader wave:

| Time (UTC) | Target | Campaign |
|------------|--------|----------|
| 02:23Z | cleaner55555/brandspark-ai-studio | 5-3-225 |
| 02:26Z | cleaner55555/eve-code (×2 files) | 5-3-225 |
| 02:30Z | cleaner55555/reflection-business-erp | 5-3-225 |
| 08:04Z | TypeTerrors/Stable-Diffuser-UI | 5-3-252 |

The `TypeTerrors` injection 5.5 hours later on the same day suggests either a second machine
was compromised in the same automation batch, or the actor ran a second wave after the first.
