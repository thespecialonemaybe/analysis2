# Task U: C2 Infrastructure Liveness Check

**Date:** 2026-06-28  
**Task:** Check liveness of all known C2 IPs. Scan ports, probe known endpoints.  
**IPs checked:** `166.88.54.158`, `166.88.134.62`, `198.105.127.210`, `23.27.202.27`, `23.27.13.43`

---

## Summary

Two of five C2 servers are fully operational as of 2026-06-28. The socket.io WS C2
(`166.88.54.158`) and both MongoDB-related IPs are down. Both live servers are serving a
**new Stage 2 payload format** (`/*RS260605*/`) not previously captured from the blockchain.

---

## Port Scan Results

| IP | :80 | :443 | :27017 | Role |
|----|-----|------|--------|------|
| `166.88.54.158` | CLOSED | CLOSED | CLOSED | **DEAD** — socket.io WS C2 (Dragon-Lady documented) |
| `166.88.134.62` | CLOSED | **OPEN** | CLOSED | **LIVE** — admin/testing server |
| `198.105.127.210` | CLOSED | **OPEN** | **OPEN** | **LIVE** — production victim server + MongoDB |
| `23.27.202.27` | CLOSED | CLOSED | CLOSED | **DEAD** — MongoDB backend was here |
| `23.27.13.43` | CLOSED | CLOSED | CLOSED | **DEAD** — removed from Stage 2 code Jun 25 |

---

## HTTP Endpoint Probe (live servers)

Both live servers run **plain HTTP on port 443** (not TLS). `X-Powered-By: Express` confirms Node.js
backend.

| Path | 166.88.134.62 | 198.105.127.210 | Notes |
|------|--------------|----------------|-------|
| `/0x/js` | **200 — 67,583 bytes** | **200 — 69,972 bytes** | Live Stage 2 payload — new format |
| `/socket.io/?EIO=4&transport=polling` | **200 — 119 bytes** | **200 — 119 bytes** | Stage 3 backdoor endpoint active |
| `/$/boot` | 404 | 404 | Old JFrog-documented path; replaced by `/0x/js` |
| `/upload` | 404 | 404 | Not exposed on HTTP (WS only, or rotated) |
| `/snv` | 404 | 404 | Python bootstrapper path not responding |
| `/u/e` | 404 | 404 | — |
| `/u/f` | 404 | 404 | — |
| `/verify-human/test` | 404 | 404 | Cloudflare decoy page not served |
| `/` | 404 | 404 | No web UI |

### socket.io Handshake (2026-06-28T18:12Z)

```
198.105.127.210: {"sid":"JT9tShoey9n93QYlBFXv","upgrades":["websocket"],"pingInterval":25000,"pingTimeout":60000,"maxPayload":10000000}
166.88.134.62:  {"sid":"3LUCo0Q90Pw7zLEIRCdE","upgrades":["websocket"],"pingInterval":25000,"pingTimeout":60000,"maxPayload":10000000}
```

Both accept connections and generate unique session IDs — the Stage 3 backdoor is fully operational
on both servers.

---

## New Stage 2 Payload Format (`/*RS260605*/`)

The `/0x/js` endpoint returns a **new payload format** not previously seen in this investigation.

### Build tag

```
/*RS260605*/
```

`RS260605` = likely "Release/build S, 2026-06-05". Same tag on both servers — same codebase,
different random variable names (standard WJS re-obfuscation).

### Obfuscation style

Previous (blockchain, BSC `0xb6c72589...` ~Jun 8):
```javascript
Function("oTNBm2c", <LZString decompressor>)(<compressed payload>)
```

New (C2-served, RS260605):
```javascript
/*RS260605*/function*vVL9lkD(eDtWRj,oB8371,DtJ1uFR={HCRVhxw:{}},FlUWAiM){
  while(eDtWRj+oB8371!==0x5a)
    with(DtJ1uFR.OwzVEFe||DtJ1uFR)
      switch(eDtWRj+oB8371){...}
```

Generator functions (`function*`) with `while`+`switch`+`with` — a new obfuscation pattern,
possibly replacing or supplementing the LZString wrapper. Strings are now inline encrypted
literals (e.g. `"Xh?*^VbV~*"`, `"!/B%/&A}]aX,(5~AR$<3SVET{y?"`) rather than a lookup table.

### Size comparison

| Source | Date | Size | Format |
|--------|------|------|--------|
| C2 admin `166.88.134.62` | RS260605 (~Jun 5) | 67,583 bytes | `function*` generator |
| C2 prod `198.105.127.210` | RS260605 (~Jun 5) | 69,972 bytes | `function*` generator |
| Blockchain BSC `0xb6c72589...` | ~Jun 8 | 77,279 bytes | `Function("oTNBm2c", LZString)` |

The two C2-served payloads are different builds of the same codebase (different sizes despite same
build tag). The blockchain payload is ~10KB larger and uses the older LZString wrapper — possibly
a separate release branch, or the blockchain copy lags C2 deployment by a few days.

### Strings / IOC analysis

- No plaintext `tasklist` strings found — sandbox check strings are now inline-encrypted
- No hardcoded IP addresses visible in plaintext — all C2 URLs encrypted
- `_V` campaign ID reference still present (obfuscated context)
- `new Function("return this")()` global accessor pattern preserved

The `9a47bb48b7b8ca41fc138fd3372e8cc0` MD5 sandbox hash is NOT present in plaintext in either
C2-served payload. It may be encoded within the encrypted string literals.

---

## Key Observations

### `166.88.54.158` is down

The Dragon-Lady report documented `ws://166.88.54.158:443` as the socket.io WS C2. It is now
dead on all ports. This IP was likely the primary Stage 3 C2 until it was taken down or
the actor migrated.

### `23.27.13.43` confirmed dead

This IP was discovered in W2 Stage 1 (`_$_a478[3]`) in an earlier task and was already absent
from the Jun 25 Stage 2. Port scan confirms it is fully offline. Consistent with the actor
deprecating it when they updated the Stage 2 routing table.

### `23.27.202.27:27017` confirmed dead

MongoDB backend is offline. The actor may have migrated MongoDB to a co-located instance on
`198.105.127.210` (port 27017 open there) or shut down the separate MongoDB server.

### `198.105.127.210:27017` is the active MongoDB

Port 27017 is open alongside port 443 on the production server. Victim data is likely stored
in MongoDB on the same host as the Node.js C2.

### Endpoint naming changed

JFrog (Jun 24) documented `/$/boot` as the boot endpoint. The live server returns 404 for that
path. The actual boot endpoint is `/0x/js?_V=<id>&id=<uuid>` (confirmed 200 in all our probes).
The actor may have renamed endpoints between the JFrog report capture and now, or JFrog's
sample was from an older build.

---

## IOC Delta (new vs. prior)

| IOC | Status |
|-----|--------|
| `166.88.54.158:443` (socket.io WS) | **NOW DEAD** — was live per Dragon-Lady |
| `166.88.134.62:443` (admin Express) | **STILL LIVE** |
| `198.105.127.210:443` (prod Express) | **STILL LIVE** |
| `198.105.127.210:27017` (MongoDB) | **STILL LIVE** |
| `23.27.202.27:27017` (MongoDB) | **NOW DEAD** |
| `23.27.13.43` (deprecated pool) | **STILL DEAD** (confirmed) |
| `/0x/js` endpoint | **LIVE** — now serves `/*RS260605*/` format |
| `/socket.io/` endpoint | **LIVE** — on both 166.88.134.62 and 198.105.127.210 |
| `/$/boot` | **DEAD** (404) — path retired |
| `/*RS260605*/` build tag | **NEW IOC** — Stage 2 build identifier |

---

## Payload Samples Captured

```
/tmp/stage2_live_admin_67k.js  — 166.88.134.62:443/0x/js  (67,583 bytes, RS260605)
/tmp/stage2_live_prod_70k.js   — 198.105.127.210:443/0x/js (69,972 bytes, RS260605)
```

These are new Stage 2 variants not previously documented. Full deobfuscation is task-scope
for a future session.
