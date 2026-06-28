# Task X: W3 Historical Stage 2 — Feb 25, 2026 Batch Decode

**Date:** 2026-06-28  
**Task:** Decode the W3 Feb 25, 2026 batch (12 BSC TXs) to map Stage 2 evolution before the
Function() UMD wrapper. Recover the pre-wrapper format and establish the Stage 2 baseline.

---

## Summary of Findings

The Feb 25, 2026 batch was not merely a routine payload update — it was a **live XOR key
rotation**. The actor changed the W3 dead-drop encryption key mid-session, re-deploying the
same payload under the new key within 2 minutes of the last old-key deployment. A full
historical XOR key has been recovered.

---

## Key Rotation Discovered

| Key | Used | First TX | Last TX |
|-----|------|---------|---------|
| `cA]2!+37v,-szeU}` (OLD) | Nov 2025 – Feb 25 18:05 | W3 genesis (Nov 13, 2025) | Feb 25 18:05 (BSC `0xa42016...`) |
| `2[gWfGj;<:-93Z^C` (NEW) | Feb 25 18:07 – present | Feb 25 18:07 (BSC `0xc721b2...`) | Jun 8, 2026 (BSC `0xb6c725...`) |

Recovery method: known-plaintext attack using the characteristic `(function(a,b){c` shuffle
cipher start confirmed by valid Feb 25 18:07 decode.

### The Rotation Event (Feb 25 18:05 → 18:07)

```
18:05 UTC  BSC 0xa42016...  OLD KEY → "function a0c(){const hc=['FqD6h8oz','WQGuWO5WW54'..."
18:07 UTC  BSC 0xc721b2...  NEW KEY → "function a0c(){const hc=['FqD6h8oz','WQGuWO5WW54'..."
```

**Both TXs decrypt to identical plaintext.** The actor:
1. Deployed the payload with OLD key at 18:05
2. Re-deployed the **exact same payload** with NEW key at 18:07 (2 minutes later)

This is a deliberate, live key rotation ceremony. The 12-TX Feb 25 batch was large precisely
because the actor needed to re-push multiple payload variants under the new key.

---

## Full Feb 25 Batch Decoded

| Time (UTC) | Size (chars) | Key used | Decode result |
|-----------|-------------|---------|--------------|
| 18:01 | 70,240 | OLD | `function a0d(a,b){const c=a0c();return a0d=function(d,e){d=d-0x1dd...` |
| 18:05 | 70,406 | OLD | `function a0c(){const hc=['FqD6h8oz','WQGuWO5WW54','W53cJJiK'...` |
| **18:07** | 70,406 | **NEW** | `function a0c(){const hc=['FqD6h8oz','WQGuWO5WW54','W53cJJiK'...` |
| 18:38 | 70,332 | NEW | `(function(a,b){const a0d6={a:0x542,b:'^[GB',c:0x23f...` |
| 18:54 | 70,173 | NEW | `(function(a,b){const a0d9={a:'qUI8',b:0x675,c:'53*('...` |
| 18:59 | 70,249 | NEW | `function a0c(){const h1=['ESolWONcOHK','WR/cPmo1WObS'...` |
| 20:00 | 69,909 | NEW | `(function(a,b){const a0da={a:0x26c,b:0x9e,c:0x2a...` |
| 20:39 | 70,445 | NEW | `(function(a,b){const a0d6={a:0x6a6,b:'qJaR',c:'SJf2'...` |
| 20:41 | 69,981 | NEW | `(function(a,b){const a0d8={a:0x1b4,b:'OBY#',c:0x188...` |
| 20:45 | 70,359 | NEW | `function a0d(a,b){const c=a0c();return a0d=function(d,e...` |
| 21:07 | 70,276 | NEW | `function a0c(){const hc=['hrtdGSoCWQBcMuDywmkHCmkB'...` |
| 21:44 | 70,300 | NEW | `function a0c(){const h9=['W4ldMConF1r6xCk4WOrne8kZ'...` |

The 18:01 TX is anomalous: it decodes to the `a0d(a,b)` lookup helper function, not the full
payload. This was likely a test or corrupted partial deployment — the same pattern as the Jun 11
2025 binary-memo failures. The actor detected the issue and pushed the full payload at 18:05.

---

## Stage 2 Payload Evolution (W3, Complete)

Cross-referencing all decoded W3 BSC TXs:

| Date | Phase | Size | Key | Format | Notes |
|------|-------|------|-----|--------|-------|
| Nov–Jan 2026 | 1 | ~91K–93K | `cA]2!+37v,-szeU}` | Shuffle cipher IIFE | Larger, possibly unminified |
| Feb 11 14:46 | 2 | ~70K | `cA]2!+37v,-szeU}` | Shuffle cipher IIFE | **Major payload redesign** |
| Feb 11 15:05 | 2 | 69,874 | `cA]2!+37v,-szeU}` | Shuffle cipher IIFE | Stabilized smaller size |
| Feb 12 | 2 | 69,454 | `cA]2!+37v,-szeU}` | Shuffle cipher IIFE | Further trim |
| Feb 25 | 3 | ~70K | OLD→NEW (rotation) | Shuffle cipher IIFE | Key rotation event |
| Mar 3 | 3 | 70,818 | `2[gWfGj;<:-93Z^C` | Shuffle cipher IIFE | Slight payload growth |
| Mar 18 | 3 | 75,113 | `2[gWfGj;<:-93Z^C` | Shuffle cipher IIFE | **+5KB new features** |
| *(2-month gap)* | | | | | Apr–May activity via C2 direct |
| May 20 | 4 | ~65K–68K | `2[gWfGj;<:-93Z^C` | Shuffle cipher IIFE | Resized after gap |
| May 21 (early) | 4 | ~67K–71K | `2[gWfGj;<:-93Z^C` | Shuffle cipher IIFE | Transitional |
| **May 21 (late)** | **5** | **70,251** | `2[gWfGj;<:-93Z^C` | **`Function("x",body)` wrapper** | **UMD wrapper added** |
| Jun 8 | 5 | 77,279 | `2[gWfGj;<:-93Z^C` | `Function("oTNBm2c",body)` | Current — 20d stable |

### Size Jump on Feb 11

The payload dropped from ~92K to ~70K **within the Feb 11 batch**:

```
Feb 11 14:14  →  92,443 chars  (function(a,b){const a0d6=... (large Phase 1)
Feb 11 14:22  →  92,114 chars  function a0c(){const h6=[...  (large Phase 1, variant)
Feb 11 14:46  →  70,647 chars  function a0c(){const hf=[...  ← PAYLOAD REDESIGN
Feb 11 15:05  →  69,874 chars  (function(a,b){const a0d5=...  (new size)
```

Four TXs on the same day document the transition. The actor pushed two variants of the large
payload, then immediately pushed a redesigned smaller payload in the same session. The ~22K
reduction (25%) was maintained through May 2026.

---

## Format: Pre-Wrapper Shuffle Cipher

All pre-May-21 W3 payloads use the **WJS shuffle cipher** format directly:

**Variant A — Array form:**
```javascript
function a0c(){const hc=['FqD6h8oz','WQGuWO5WW54','W53cJJiK','FCkjW6uOya','ASorWPXUW7TLW5Xac8oKW4OJ',...]}
```
Strings are in an array returned by `a0c()`. A separate decode function maps indices → array values.

**Variant B — Object form:**
```javascript
(function(a,b){const a0d6={a:0x542,b:'^[GB',c:0x23f,d:0x5ab,...},...}
```
The obfuscation seed data is packed into a local object rather than a separate array function.

Both variants produce the same obfuscated JS when evaluated; they are different outputs of the
same WJS obfuscator build, not different payloads. Multiple variants were deployed on the same
day (Feb 25 has both) — likely targeting different Stage 1 execution environments or as
redundant uploads during the key rotation.

There is **no LZString compression layer** in any of these payloads. The shuffle cipher
deobfuscation is the only encoding. This contrasts with the post-May-21 `Function()` wrapper
which wraps an embedded LZString decompressor around a compressed payload.

---

## IOC: Historical XOR Key

```
# W3 dead-drop XOR key (historical — retired Feb 25, 2026)
cA]2!+37v,-szeU}

# W3 dead-drop XOR key (current — Feb 25, 2026 – present)
2[gWfGj;<:-93Z^C
```

The old key `cA]2!+37v,-szeU}` was in use from W3's genesis (November 13, 2025) through
February 25, 2026 (18:05 UTC). Any Stage 1 payloads captured before that date that point to
W3 can be decrypted with this key to recover the historical Stage 2.

Note: The W1 key `2[gWfGj;<:-93Z^C` is not new — it was already in use for W1 throughout this
period. W3 adopted the W1 key on Feb 25, aligning the two channels on a single XOR key. This
simplifies the actor's key management but also means historical W3 content is now distinguishable
by key alone (old W3 key ≠ W1 key; new W3 key = W1 key).

---

## Why Feb 25 Had 12 TXs

Previously the largest batch had 6 TXs (May 21, the UMD wrapper introduction). Feb 25's 12 TXs
are explained by the key rotation:

1. The actor pushed 2 final TXs under the OLD key (18:01 test, 18:05 payload)
2. Then pushed 10 TXs under the NEW key (18:07–21:44)
3. The 10 new-key TXs represent multiple payload variants being "refreshed" — each variant 
   (array form vs object form, different obfuscation seeds) re-deployed under the new key

A similar pattern occurred on May 21 (6 TXs = wrapper introduction session). The actor uses
large batches for format transitions, pushing many variants in a single session to ensure
all Stage 1 code paths find a valid Stage 2 payload.

---

## Timeline: W3 Operational Phases

```
Phase 0 (W1/W2 only, Jun 2025 – Oct 2025):
  Stage 2 served directly from C2. No blockchain dead-drop.

Phase 1 (W3 genesis, Nov 2025 – Feb 11 2026):
  W3 adds blockchain Stage 2 delivery. ~92KB shuffle cipher IIFE.
  XOR key: cA]2!+37v,-szeU}

Phase 2 (payload redesign, Feb 11 – Feb 24 2026):
  Payload shrinks from 92K → 70K within one session.
  XOR key: cA]2!+37v,-szeU}

Phase 3 (key rotation, Feb 25 2026):
  Key rotated from cA]2!+37v,-szeU} → 2[gWfGj;<:-93Z^C.
  Payload size stable at ~70K. March: grows to 75K (+5K new features).
  XOR key: 2[gWfGj;<:-93Z^C

[2-month gap: Mar 19 – May 16 2026, W3 silent]
  Response to OSM YARA rule (Mar 7). Stage 2 rebuilt before W3 resumption.

Phase 4 (UMD wrapper transition, May 17 – May 20 2026):
  Payloads resume at ~65K. No wrapper.

Phase 5 (UMD + LZString, May 21 2026 – present):
  Function("param", LZString_decompressor)(moduleProxy) wrapper introduced.
  Size grows from 65K → 77K (Jun 8). 20-day quiet as of 2026-06-28.
```

---

## Nov 2025 BSC TXs

The TRON API did not return the Nov 2025 TRON TXs within the standard pagination window,
and the BSC archive has pruned transaction input data that old. The three Nov 2025 payloads
(Nov 14, 18, 19) are not recoverable from BSC. They would have used the old key
`cA]2!+37v,-szeU}` and likely contained Phase 1 (~92K) format payloads.

---

## Relationship to Public Reports

Neither the historical key `cA]2!+37v,-szeU}` nor the Feb 25 key rotation appear in any
public threat report as of 2026-06-28. All public analysis of PolinRider XOR keys (JFrog,
OpenSourceMalware, Dragon-Lady) documents only `2[gWfGj;<:-93Z^C` and `m6:tTh^D)cBz?NM]`,
which are the current W1 and W2 keys respectively.

The historical W3 key `cA]2!+37v,-szeU}` is **a new IOC** that enables decryption of any
W3-delivered Stage 2 payloads captured between November 2025 and February 25, 2026.
