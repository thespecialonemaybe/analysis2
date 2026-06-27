# Research References -- ZurichJS / DEV#POPPER Attribution

Links used during attribution analysis. All confirmed relevant to this campaign.

---

## Primary Attribution Sources

### DEV#POPPER / OmniStealer

- **eSentire TRU -- "DEV#POPPER RAT and OmniStealer (Everyday I'm Shufflin')"** (Feb 2026)
  https://www.esentire.com/blog/north-korean-apt-malware-analysis-dev-popper-rat-and-omnistealer-everyday-im-shufflin
  *Documents OmniStealer Python harvester, C2 port 27017, Sec-V header, EmbedIO/3.5.2 fingerprint.
  Directly names 198.105.127.210 as DEV#POPPER C2 node. Identical blockchain three-chain architecture.*

- **Securonix -- "Analysis of DEV#POPPER"** (2024/2025)
  https://www.securonix.com/blog/analysis-of-devpopper-new-attack-campaign-targeting-software-developers-likely-associated-with-north-korean-threat-actors/
  *Original DEV#POPPER campaign analysis. Attributes to DPRK Lazarus Group. Documents fake job interview
  delivery (GitHub repo take-home test). Lists 198.105.127.210 as C2.*

### PolinRider

- **OpenSourceMalware / PolinRider -- Full Technical Dossier** (March 2026)
  https://github.com/OpenSourceMalware/PolinRider
  https://github.com/OpenSourceMalware/PolinRider/blob/main/README.md
  *1,951 compromised repos, 1,047 unique owners. Documents global['_V'] version routing, shuffle cipher
  seeds, TRON/BSC/Aptos dead-drop addresses (identical to our sample), ShoeVista/StakingGame templates.*

- **Nocturnalknight -- "The Polinrider and Glassworm Supply Chain Offensive"** (2026)
  https://nocturnalknight.co/the-polinrider-and-glassworm-supply-chain-offensive-a-forensic-post-mortem/
  *Forensic post-mortem. Documents temp_auto_push.bat git history falsification, historical C2 IPs,
  Vercel C2 subdomain list. Confirms Evoxt ASN as primary hosting provider.*

- **branch8/PolinRiderScanner** -- Detection scripts (IOC-based scanner)
  https://github.com/branch8/PolinRiderScanner
  *Community-built scanner using XOR key IOCs to detect PolinRider infections locally.*

- **finom/finom -- polinrider-scan skill**
  https://github.com/finom/finom/tree/main/skills/polinrider-scan
  *Another community scanner implementation with IOC references.*

### Blockchain Dead-Drop Analysis

- **Ransom-ISAC -- "Cross-Chain TxDataHiding Crypto Heist Part 2"** (2026)
  https://ransom-isac.org/blog/cross-chain-txdatahiding-crypto-heist-part-2/
  *Documents the TRON->Aptos->BSC calldata relay architecture. Provides TRON wallet addresses
  (identical to our sample). Cross-references DEV#POPPER and PolinRider as same infrastructure.*

- **Malwarebytes -- "OmniStealer Uses the Blockchain to Steal Everything"** (April 2026)
  https://www.malwarebytes.com/blog/news/2026/04/omnistealer-uses-the-blockchain-to-steal-everything-it-can
  *OmniStealer deep dive. Same Python harvester we decoded in Stage 5. Confirms Telegram fallback
  exfil, AES ZIP packaging, cross-platform browser credential theft.*

- **0xCryptoZen/malware-scan** -- IOC reference collection
  https://github.com/0xCryptoZen/malware-scan
  *Community IOC repository. Contains our XOR keys and BSC calldata delimiter in patterns.md,
  confirming these are known-bad signatures.*

---

## Broader Campaign Context

### Contagious Interview / Lazarus Group

- **Microsoft Security Blog -- "Contagious Interview malware via fake developer job interviews"** (March 2026)
  https://www.microsoft.com/en-us/security/blog/2026/03/11/contagious-interview-malware-delivered-through-fake-developer-job-interviews/
  *Documents fake Next.js repos (ShoeVista template), VS Code tasks.json vector, BeaverTail/InvisibleFerret
  payload chain. Confirms Next.js developer targeting as primary Lazarus Group focus in 2026.*

- **MITRE ATT&CK -- Contagious Interview (G1052)**
  https://attack.mitre.org/groups/G1052/
  *Authoritative threat actor profile. Use for OpenCTI relationship linking.*

- **ESET -- "DeceptiveDevelopment targets freelance developers"** (2026)
  https://www.welivesecurity.com/en/eset-research/deceptivedevelopment-targets-freelance-developers/
  *Alternative tracking name for same cluster. Documents LinkedIn/Upwork recruiter lure, 1,700+
  malicious npm packages, freelance developer targeting globally.*

- **The Hacker News -- "N. Korean Hackers Spread 1,700 Malicious Packages"** (April 2026)
  https://thehackernews.com/2026/04/n-korean-hackers-spread-1700-malicious.html
  *Scale overview. npm, PyPI, Go, Rust, PHP packages all affected since January 2025.*

- **The Hacker News -- "Fake Next.js Repos Target Developers"** (Feb 2026)
  https://thehackernews.com/2026/02/fake-nextjs-repos-target-developers.html
  *ShoeVista template campaign. Confirms Next.js/next.config.mjs as primary injection target.*

### Related Supply-Chain Attacks (Same Actor / Infrastructure)

- **Axios npm Supply Chain Compromise** (April 2026, attributed to Sapphire Sleet / DPRK)
  - Microsoft: https://www.microsoft.com/en-us/security/blog/2026/04/01/mitigating-the-axios-npm-supply-chain-compromise/
  - Elastic: https://www.elastic.co/security-labs/axios-one-rat-to-rule-them-all
  - Google Cloud: https://cloud.google.com/blog/topics/threat-intelligence/north-korea-threat-actor-targets-axios-npm-package
  *Compromised axios (100M weekly downloads). Same DPRK cluster. C2: sfrclak[.]com:8000.*

- **RATatouille / rand-user-agent attack** (May 2025)
  https://www.aikido.dev/blog/catching-a-rat-remote-access-trojian-rand-user-agent-supply-chain-compromise
  https://cybersecuritynews.com/new-supply-chain-attack-targets-legitimate-npm-package/
  *Used port 27017 for C2 file exfil (http://85.239.62.36:27017/u/f). Campaign ID "7-randuser84"
  -- same hyphen-delimited format as our "5-3-161". Structurally closest public match.*

- **CanisterWorm / CanisterSprawl** (March-April 2026, TeamPCP)
  https://labs.cloudsecurityalliance.org/research/csa-research-note-canisterworm-blockchain-c2-supply-chain-20/
  https://socket.dev/blog/canisterworm-npm-publisher-compromise-deploys-backdoor-across-29-packages
  *Uses ICP blockchain canisters as C2 dead-drop. Different actor but same dead-drop technique.
  Documents how blockchain-based C2 is structurally un-takedownable.*

### Infrastructure / Hosting

- **Proofpoint -- "TA416 Resumes European Government Espionage"** (2025-2026)
  https://www.proofpoint.com/us/blog/threat-insight/id-come-running-back-eu-again-ta416-resumes-european-government-espionage
  https://thehackernews.com/2026/04/china-linked-ta416-targets-european.html
  *Documents Evoxt Enterprise (AS149440) as "heavily favored" APT hosting provider. Confirms
  same ASN used by Chinese TA416 for PlugX C2 -- independently selected by DPRK actors too.*

- **ipinfo.io / BGP.tools -- AS149440 Evoxt Enterprise**
  https://ipinfo.io/AS149440
  https://bgp.tools/as/149440
  *ASN registration data: Malaysia (Evoxt Sdn. Bhd.), routed via London (SYN LTD),
  abuse contact: abuse@syn.one*

---

## GitHub Code Search Hits (Campaign IOCs in Public Repos)

Searched 2026-05-07 using GitHub code search API. No live infected repos found -- all hits
are in security research / IOC tracking repositories.

| Query | Hits | Repos (research only) |
|-------|------|----------------------|
| XOR key1 `2[gWfGj;<:-93Z^C` | 11 | PolinRider dossier, Ransom-ISAC, branch8/PolinRiderScanner, finom/finom, 0xCryptoZen, elastic/cicd-abuse-detector |
| XOR key2 `m6:tTh^D)cBz?NM` | 8 | Same security repos |
| BSC calldata delimiter `?.?` | 1 | 0xCryptoZen/malware-scan |
| C2 IP `198.105.127.210` | 0 | -- |
| TRON wallet 1 | 0 | -- |
| Campaign codes `EV-4A6OE6M0E` | 0 | -- |
| Telegram bot ID `7870147428` | 0 | -- |
| Infection commit hash | 0 | -- |
| Shuffle seeds in config files | 0 | -- (GitHub may have de-indexed) |

**Conclusion:** The zurichjs repo was either the sole injection for this specific `_V=5-3-161` campaign
instance, or other infected repos are private / not yet indexed. The attack infrastructure (IP, port,
keys, blockchain addresses) is confirmed shared with documented DEV#POPPER campaigns.

---

## Elastic / cicd-abuse-detector

- https://github.com/elastic/cicd-abuse-detector
  *Elastic's CI/CD abuse detection tool. Contains our XOR key1 in example malicious diff
  (`examples/malicious/backdated-config-trojan.diff`) -- confirms Elastic has catalogued this
  specific implant variant as a reference example.*
