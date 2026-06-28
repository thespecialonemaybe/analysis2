# Task W: Dragon-Lady npm Package Registry Check

**Date:** 2026-06-28  
**Task:** Check all Dragon-Lady-documented npm packages for live status, publish dates, publisher accounts.

---

## Summary

All 9 packages are **removed** — replaced with npm security holding packages on 2026-06-11.
Each has a GHSA advisory filed the same day. Tarballs have been purged from the CDN.
~3,000+ combined downloads across the last month = ~3,000+ potentially compromised developer machines.

---

## Package Status Table

| Package | Status | Malicious versions | Published | Removed | Downloads (last month) | GHSA |
|---------|--------|--------------------|-----------|---------|----------------------|------|
| `tailwindcss-merge` | 0.0.1-security | v1.0.1–1.0.4 | 2026-06-07 | 2026-06-11 | **934** | GHSA-m2xh-rw7p-69rx |
| `typeorm-encrypt` | 0.0.1-security | v1.0.1–1.0.2 | 2026-06-07 | 2026-06-11 | **751** | GHSA-f7h6-4xj8-8qh7 |
| `rate-limit-flexible` | 0.0.1-security | v1.0.1–1.0.2 | 2026-06-07 | 2026-06-11 | **721** | GHSA-v7vx-48xw-jwm8 |
| `sass-formats` | 0.0.1-security | v1.0.1–1.0.5 | 2026-06-07 | 2026-06-11 | — | GHSA-pvrm-39m5-j3c4 |
| `clsx-tailwind` | 0.0.1-security | v1.0.1 | 2026-06-07 | 2026-06-11 | — | GHSA-373j-j35f-q4gx |
| `tailwindcss-animates-kit` | 0.0.1-security | v1.0.1 | 2026-05-19 | 2026-06-11 | **199** | GHSA-v4xp-qgj3-gphm |
| `tailwindcss-animatics` | 0.0.1-security | v1.0.1 | 2026-05-19 | 2026-06-11 | — | GHSA-mp9h-24x9-xc7r |
| `sass-format` | 0.0.1-security | v1.0.1 | 2026-06-10 | 2026-06-11 | — | GHSA-m8x4-pc4m-p5gv |
| `rate-limits-flexible` | 0.0.1-security | v1.0.1 | 2026-06-10 | 2026-06-11 | — | GHSA-hg8j-2wmv-w4v6 |

All GHSA advisories rated **critical** severity, filed 2026-06-11 (same day as npm takedown).
Standard malware boilerplate: "considered fully compromised."

---

## Injection Waves

Three distinct injection batches, all revoked on the same day:

### Wave 1 — May 19, 2026 (early/test deployment)
- `tailwindcss-animates-kit` v1.0.1
- `tailwindcss-animatics` v1.0.1

Single version each. Low download count (199 for animates-kit). Likely a test run or
smaller-scale initial targeting. These packages sat live for 23 days before removal.

### Wave 2 — June 7, 2026 (main campaign)
- `tailwindcss-merge` v1.0.1–1.0.4 (4 versions in one day)
- `sass-formats` v1.0.1–1.0.5 (5 versions in one day)
- `typeorm-encrypt` v1.0.1–1.0.2
- `rate-limit-flexible` v1.0.1–1.0.2
- `clsx-tailwind` v1.0.1

Rapid versioning on June 7 (multiple versions per package within hours) is consistent with:
- Key rotation between versions (known actor behavior from W3 blockchain analysis)
- Payload variant testing
- Targeting different dependency version ranges

### Wave 3 — June 10, 2026 (final additions)
- `sass-format` v1.0.1
- `rate-limits-flexible` v1.0.1

Added 3 days after the main wave; removed the next day (only 1 day live).

---

## `tailwindcss-merge` Pre-2026 History

```
v0.0.1  2024-01-17  ← original publish
v0.0.2  2024-01-18
(silent 2+ years)
v1.0.1  2026-06-07  ← malicious injection
v1.0.2  2026-06-07
v1.0.3  2026-06-07
v1.0.4  2026-06-07
```

`tailwindcss-merge` existed as v0.0.1/v0.0.2 since January 2024 — 2.5 years before the
malicious injection. The pre-2026 tarball is no longer available (purged by npm security hold),
so it cannot be confirmed whether the 2024 versions were:
1. **Pre-positioned name squatting** — actor registered the name early, sat on it, then
   weaponized it 2.5 years later when the campaign was ready
2. **Legitimate package (account hijacked)** — a real developer's v0.0.1 package was
   later taken over by the actor via credential theft

The `tailwindcss-merge` name closely mimics the legitimate `tailwind-merge` package
(different npm name, same concept). Pre-positioning the typosquat in 2024 and only
weaponizing in June 2026 would be operationally consistent with a patient, long-term actor.

**All other packages were fresh registrations with no pre-2026 history.**

---

## Publisher Identity

**Unknown.** npm's security hold process clears maintainer metadata. The `maintainers` field
is now an empty array for all 9 packages, and the version-level `_npmUser` fields have been
purged. The tarballs are 404 on the CDN.

No publisher account name could be recovered from registry data alone.

Possible avenues for future identification:
- GitHub commit history in any package that linked to a repository
- npm download log correlation (internal npm data, not public)
- Socket.dev or Phylum security databases which may have captured publisher at report time
- Dragon-Lady's `sources.md` may reference the original publisher accounts

---

## Scale Assessment

| Package | Downloads (May 29 – Jun 27) |
|---------|--------------------------|
| `tailwindcss-merge` | 934 |
| `typeorm-encrypt` | 751 |
| `rate-limit-flexible` | 721 |
| `tailwindcss-animates-kit` | 199 |
| Others (est.) | ~500 |
| **Total** | **~3,100+** |

Each download = one `npm install` = one potential victim machine with Stage 0 installed.
If the install triggers `postinstall` scripts or VSCode task execution, infection is immediate.

`typeorm-encrypt` and `rate-limit-flexible` are high-value targets:
- `typeorm-encrypt`: NestJS/Express backends — targets server-side developers, meaning the
  infected machine likely has database credentials, API keys, service account access
- `rate-limit-flexible`: Redis/Memcached integration — similarly targets backend developers
  with infrastructure access

These are more dangerous than the CSS tooling packages, which target frontend developers
with typically less privileged access.

---

## Unknown Publisher: Next Steps

The publisher account could potentially be identified via:
1. **Task Z**: Dragon-Lady `sources.md` may explicitly name the npm account
2. **Socket.dev blog**: "Famous Chollima Targets PHP Developers Through Compromised Packagist Package"
   may cross-reference npm accounts
3. Phylum's advisory feed (phylum.io) — Phylum often captures publisher names before npm
   removes them
