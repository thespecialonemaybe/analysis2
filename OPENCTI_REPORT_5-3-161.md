# ZurichJS Supply-Chain Attack -- DEV#POPPER / PolinRider (Lazarus Group)

**TLP: AMBER**  
**Report date:** 2026-05-06  
**Author:** Internal threat analysis  
**Confidence:** High  

---

## Summary

On 2026-02-19, a malicious payload was injected into the public GitHub repository
`zurich-js/zurichjs-website` via commit `556dba47cede89f7b1c753b2df2d76cd2a7ab0e8`. The payload
was hidden after 2,784 trailing ASCII space characters on the final line of `next.config.mjs`,
making it invisible in standard editors and GitHub diff views. It remained active for **74 days**
before being removed on 2026-05-04.

The implant is a confirmed instance of the **DEV#POPPER / OmniStealer** malware family, attributed
with high confidence to **Lazarus Group** (Contagious Interview / DeceptiveDevelopment / PolinRider,
MITRE G1052), a DPRK state-sponsored APT. The same C2 IP (`198.105.127.210`), port (`27017`),
hosting ASN (Evoxt Enterprise, AS149440), `Sec-V` header protocol, TRON/Aptos/BSC blockchain
dead-drop architecture, and OmniStealer Python harvester have been documented across multiple
prior DEV#POPPER campaigns by eSentire TRU, Securonix, Ransom-ISAC, and Malwarebytes.

The implant fires on `npm run dev`, `npm run build`, or `npm run start` -- i.e., any developer
who cloned the repo and started the Next.js application during the 74-day window is at risk of
full credential compromise.

---

## Threat Actor

| Field | Value |
|-------|-------|
| **Name** | Lazarus Group |
| **Aliases** | Contagious Interview, DEV#POPPER, PolinRider, DeceptiveDevelopment, Sapphire Sleet, TAG-121, Void Dokkaebi, UNC1069, PurpleBravo |
| **MITRE ID** | G1052 |
| **Country** | North Korea (DPRK) |
| **Motivation** | Financial -- cryptocurrency theft, credential harvesting |
| **Target sector** | Software developers (Next.js, React, blockchain, crypto) |

---

## Malware Families

| Name | Stage | Description |
|------|-------|-------------|
| DEV#POPPER RAT | Stage 3 | Node.js RAT -- 65 KB, XOR-encrypted, delivered from `/$/boot`; registers victim, spawns Python dropper |
| OmniStealer | Stage 5 | Python credential harvester -- 82 KB, cross-platform (Linux/macOS/Windows), 2,356 lines; targets browsers, wallets, SSH, GitHub tokens |
| DEV#POPPER Stager | Stages 0-2 | Multi-layer JS implant using 7 shuffle-cipher layers + XOR; TRON/Aptos/BSC blockchain dead-drop resolver |

---

## Attack Pattern (MITRE ATT&CK)

| ID | Technique | Details |
|----|-----------|---------|
| T1195.002 | Supply Chain Compromise: Software Supply Chain | Malicious commit to `zurich-js/zurichjs-website` via compromised/sock-puppet GitHub account `farisaziz12` (ID 53216647) |
| T1059.007 | Command and Scripting: JavaScript | Payload embedded in `next.config.mjs`, evaluated at Next.js startup |
| T1059.006 | Command and Scripting: Python | OmniStealer Python harvester fetched and executed via Stage 4 dropper |
| T1102 | Web Service -- Dead Drop Resolver | Payload URLs encoded in BSC transaction calldata, retrieved via TRON/Aptos wallet lookups |
| T1027 | Obfuscated Files or Information | 7 independent shuffle-cipher layers + XOR encryption across stages |
| T1027.002 | Software Packing | RC4 string table (876 call sites) in Stage 3 |
| T1082 | System Information Discovery | `os.platform()`, `os.hostname()`, `os.userInfo().username`, `os.release()` -- used for victim profiling and sandbox detection |
| T1057 | Process Discovery | `tasklist /FO CSV /NH` on Windows; each process name MD5-hashed and checked against blocklist |
| T1480 | Execution Guardrails | 52-entry CI/sandbox hostname+username blocklist; aborts before fetching any live payload |
| T1555.003 | Credentials from Web Browsers | Chrome, Edge, Brave, Firefox, Opera, Vivaldi, Arc -- passwords, cookies, saved cards |
| T1555 | Credentials from Password Stores | macOS Keychain, GNOME Keyring, KDE Wallet, Windows Credential Manager |
| T1552.001 | Unsecured Credentials in Files | `~/.git-credentials`, VS Code extension storage, SSH private keys |
| T1528 | Steal Application Access Token | GitHub PATs, npm tokens, cloud API keys (AWS/GCP/Azure) from environment variables |
| T1041 | Exfiltration over C2 Channel | ZIP archive uploaded via POST to `198.105.127.210:27017/u/f` |
| T1567.002 | Exfiltration to Cloud: Telegram | Fallback exfil via `@file_1018_bot` to group "Z-File" when HTTP upload fails |
| T1036.005 | Masquerading: Match Legitimate Name | C2 port 27017 mimics MongoDB; server presents EmbedIO/3.5.2 fingerprint |

---

## Infrastructure

### C2 Server

| Indicator | Value | Notes |
|-----------|-------|-------|
| IP | `198.105.127.210` | Confirmed live 2026-05-06 |
| Port | `27017` | HTTP (not MongoDB); mimics MongoDB port |
| ASN | AS149440 Evoxt Enterprise | Budget VPS, Kuala Lumpur / London |
| Path -- Stage 3 delivery | `GET /$/boot` | XOR-encrypted JS payload, 65,438 bytes |
| Path -- Stage 5 delivery | `GET /$/1` | base64+zlib Python payload, 32,737 bytes raw |
| Path -- victim registration | `POST /u/e` | Sends hostname, username, OS, campaign ID |
| Path -- file upload | `POST /u/f` | Receives ZIP archive with harvested credentials |
| Path -- operator alert | `POST /verify-human/{channel}` | Notifies operator of new victim |
| Path -- binary delivery | `GET /d/7zr.exe`, `GET /d/python.7z`, `GET /d/python.zip` | Windows Python installer fallback |
| Custom header | `Sec-V: 5-3-161` | Campaign version sent on every request |
| User-Agent (fake) | `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36` | |

### Blockchain Dead-Drop

| Chain | Address/Endpoint | Role |
|-------|-----------------|------|
| TRON (index) | `TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF` | Primary wallet -- latest tx hash -> BSC tx hash |
| TRON (fallback) | `TFMryB9m6d4kBMRjEVyFRbqKSV1cV2NcpH` | Secondary wallet |
| TRON (stage 1b) | `TA48dct6rFW8BXsiLAtjFaVFoSuryMjD3v` | Stage 1b path |
| Aptos (fallback 1) | `0x9d202c824402ca89e9aaccd2390b6f8b332ae743caa1469c695feb2781d56519` | Fallback when TRON API fails |
| Aptos (fallback 2) | `0x3d2075f97b7b1e3234bd653779d21c605d7d8c6ec9c98d983880be5c7f4f9471` | |
| Aptos (stage 1b) | `0x533b2dbcaeff19cd1f799234a27b578d713d8fcaa341b7501e4526106483e0b1` | |
| BSC RPC | `bsc-dataseed.binance.org`, `bsc-rpc.publicnode.com` | Payload calldata retrieval via `eth_getTransactionByHash` |
| Calldata delimiter | `?.?` | Splits prefix from XOR-encrypted payload in tx calldata |

### Telegram Exfiltration Channel

| Field | Value |
|-------|-------|
| Bot token | `7870147428:AAGbYG_eYkiAziCKRmkiQF-GnsGTic_3TTU` |
| Bot username | `@file_1018_bot` |
| Chat ID | `-4697384025` |
| Chat name | "Z-File" |
| Trigger | HTTP upload failure OR `-tg` flag; file < 50 MB |

---

## Indicators of Compromise (IOCs)

### Network IOCs

```
198.105.127.210        # C2 -- confirmed active 2026-05-06
  port 27017           # HTTP C2 (all stages)
api.trongrid.io        # TRON blockchain API (dead-drop lookup)
fullnode.mainnet.aptoslabs.com   # Aptos blockchain API (dead-drop fallback)
bsc-dataseed.binance.org         # BSC RPC (payload retrieval)
bsc-rpc.publicnode.com           # BSC RPC fallback
api.telegram.org                 # Exfil fallback channel
```

### File Hashes (SHA-256)

```
# Raw live payloads (most unique -- re-hash if freshness matters)
448ed92f3542140af570c5ecc114038fb602bb74c03ad9b34240e5f0b658389c  stage3_raw.bin  (GET /$/boot)
55fd483e76ee33700143a1597e2fcfc91e2df18d313718f0d0081a8946de292f  stage5_raw.bin  (GET /$/1)

# Implant (Stage 0)
4583081d304bae4ecae255d62fead827c8fc1f73d462fb364717fca829d36ff2  next.config.mjs.infected

# Decoded/deobfuscated analysis artifacts
e3b30d380e766a7f9070bac1d1710524c9d1350399bf3866eeb1a67d07674079  final_decoded.js
2cfede38fb121a71a2f3607474aa8cd588a99f51b37e5e6f0d8cb789fa275032  stage3_decrypted.js
d1ef28f044ed9d682926554ab84fdc70144e51e4749ac271d8d63b1aae382a1a  stage4_python.py
0bda1fef1b234ed0c9912c1a6ddb8fca6b785c35cb3e8e00fa42612e07b16618  stage5_decoded.py
```

### Git Indicators

```
Repository:      zurich-js/zurichjs-website
Infection commit:    556dba47cede89f7b1c753b2df2d76cd2a7ab0e8  (2026-02-19T10:11:43Z)
Commit message:  "fix(tshirt): resolve hydration mismatch error and refactor into components"
Author account:  farisaziz12  (GitHub ID 53216647)  -- compromised or sock puppet
Remediation commit:  87196d26de2360cb2fbd49cb3a480aa6043f56d7  (2026-05-04)
```

### Runtime Globals (detect in live Node.js process memory)

```javascript
global.i          // = '5-3-161'  campaign marker
global._V         // = '5-3-161'  forwarded as Sec-V header
global._H         // = 'http://198.105.127.210:27017'  C2 base URL
global._t_t       // timestamp -- set when implant runs (dedup guard)
global._t_1       // = 'TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF'  TRON wallet 1
global._t_2       // Aptos address 1
```

### Stage 3 Campaign Strings (sent to C2 during victim registration)

```
Campaign codes:   EV-4A6OE6M0E  /  EV-CHQG3L42M
Campaign version: 5-3-161
```

### Process Indicators (Stage 5 on Windows)

```
wscript.exe           # runs VBScript to decrypt DPAPI blobs
reg query             # reads browser installation paths from registry
```

---

## Victim Profile and Exposure Assessment

**Who is affected:**  
Any developer who cloned `zurich-js/zurichjs-website` and ran `npm run dev`, `npm run build`,
or `npm run start` between **2026-02-19 and 2026-05-04**.

**What was at risk** (OmniStealer harvests):
- Browser credentials and session cookies from Chrome, Edge, Brave, Firefox, Opera, Vivaldi, Arc
- 60+ cryptocurrency wallet browser extensions (MetaMask, Phantom, Rabby, TronLink, Keplr...)
- GitHub Personal Access Tokens (`~/.git-credentials`, VS Code extension storage)
- SSH private keys
- macOS Keychain / GNOME Keyring / Windows Credential Manager
- All environment variables containing API keys (AWS, GCP, Azure, npm, GitHub)
- npm auth tokens
- Cloud storage directories (Dropbox, Google Drive, iCloud, OneDrive)

**Exfiltration:** Credentials packaged as AES-256 encrypted ZIP and uploaded to
`198.105.127.210:27017/u/f`. Fallback: Telegram bot `@file_1018_bot`.

---

## Recommended Actions

1. **Rotate all credentials** on any machine that ran the application during the exposure window:
   - GitHub PATs
   - npm tokens
   - SSH keys
   - All browser-stored passwords and session cookies (treat as fully compromised)
   - Cloud provider API keys (AWS, GCP, Azure)

2. **Revoke active sessions** for all services accessible from affected machines (GitHub, npm, cloud
   consoles, crypto exchanges).

3. **Block network IOCs:**
   ```
   198.105.127.210:27017
   ```

4. **Report Telegram bot** `@file_1018_bot` to Telegram at https://t.me/abuse for takedown.

5. **Submit to VirusTotal / threat intel sharing:**  
   SHA-256 hashes above -- particularly `448ed92f...` (Stage 3) and `55fd483e...` (Stage 5) as
   these are live C2 payloads unique to this infrastructure.

6. **Monitor TRON wallet** `TCqf6ZkaQD84vYsC2cuu1jRwB6JveTaRrF` for new transactions -- the
   operator rotates payloads via new BSC transactions when changing Stage 4/5.

---

## References

1. eSentire TRU -- "DEV#POPPER RAT and OmniStealer (Everyday I'm Shufflin')", Feb 2026  
   https://www.esentire.com/blog/north-korean-apt-malware-analysis-dev-popper-rat-and-omnistealer-everyday-im-shufflin

2. Securonix -- "Analysis of DEV#POPPER", 2024/2025  
   https://www.securonix.com/blog/analysis-of-devpopper-new-attack-campaign-targeting-software-developers-likely-associated-with-north-korean-threat-actors/

3. OpenSourceMalware / PolinRider dossier, March 2026  
   https://github.com/OpenSourceMalware/PolinRider

4. Ransom-ISAC -- "Cross-Chain TxDataHiding Crypto Heist Part 2", 2026  
   https://ransom-isac.org/blog/cross-chain-txdatahiding-crypto-heist-part-2/

5. Malwarebytes -- "OmniStealer Uses the Blockchain to Steal Everything", April 2026  
   https://www.malwarebytes.com/blog/news/2026/04/omnistealer-uses-the-blockchain-to-steal-everything-it-can

6. Nocturnalknight -- "The Polinrider and Glassworm Supply Chain Offensive", 2026  
   https://nocturnalknight.co/the-polinrider-and-glassworm-supply-chain-offensive-a-forensic-post-mortem/

7. Microsoft Security Blog -- "Contagious Interview malware via fake developer job interviews", March 2026  
   https://www.microsoft.com/en-us/security/blog/2026/03/11/contagious-interview-malware-delivered-through-fake-developer-job-interviews/

8. MITRE ATT&CK -- Contagious Interview (G1052)  
   https://attack.mitre.org/groups/G1052/

9. Proofpoint -- "TA416 Resumes European Government Espionage" (Evoxt/AS149440 context), 2025-2026  
   https://www.proofpoint.com/us/blog/threat-insight/id-come-running-back-eu-again-ta416-resumes-european-government-espionage

10. Google Cloud / Elastic / Microsoft -- Axios npm supply chain compromise (DPRK, Sapphire Sleet), April 2026  
    https://cloud.google.com/blog/topics/threat-intelligence/north-korea-threat-actor-targets-axios-npm-package
