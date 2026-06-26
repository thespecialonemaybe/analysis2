#!/usr/bin/env python3
"""
Stage 4 v3 string table decoder - static deobfuscation (no execution).

Stage 4 uses multiple base91 alphabets for different index ranges.
This script tries all known alphabets and reports decoded strings.

Methodology: black-box tracing of decoder functions in stage4_5-2-319.js.
  - ePVaOH6[idx] -> base91_decode(encoded, alphabet[idx]) -> v46AfAl(bytes) -> UTF-8
  - v46AfAl performs Buffer.from(bytes).toString('utf-8')
  - Different index ranges use different alphabets (see ALPHABET_MAP below)

File: stage4_5-2-319.js (65,580 bytes, SHA-256: 7ad66...)
"""

import re
import base64

# ──────────────────────────────────────────────────────────────────────────────
# ALPHABETS  (confirmed by decoder-function analysis + known-plaintext checks)
# ──────────────────────────────────────────────────────────────────────────────

ALPHABETS = {
    # A1: TVR2sfT variable in the oDCXdB outer function (pos 7239)
    # Confirmed: 0x4f → 'undefined', 0x8d → 'Buffer', 0x8e → 'from'
    'A1_TVR2sfT': '+YtZVu}9BiSEm,|(a=v."qRCN0Q)8zl2x~ky%61TAJsd*_3w?o{]WXM&Onh:p/@>rLgIcDGF<54`U7#HK^[;Pfbe$!j',

    # A2: _EpyyfS variable in jqMZAe generator (pos 25065)
    # Confirmed: 0x5b → 'JSON', 0x5c → 'parse'
    'A2_EpyyfS':  'ABh%fT(z8L^2kiwxEqI5]@)3}VQr6sp_H&[jyW>ZSMg/U=Yb$7Jue;XR<"4v0cCDl?PK|Om~{FG,Nn1#d+9.*a`!t:o',

    # A3: Uy8j0G variable in xRuVZ7/Xb5CB4.AYrc9T generator (pos 2171)
    # Used by NExDtEL (the default string decoder) for indices 0x00-0x4d
    'A3_Uy8j0G':  'rylABFUijTVokIg8Q?pMWa2|J$N<=z@*O0L/:m1+#%73u}&XYv9,`S>)[hEtw(ZdR!xDqG;Hne]{.C4_KcP"6s~fb5^',

    # A4: jk4P02 variable in local QUqs9e function (pos 54561)
    # Confirmed: 0x9c → 'fromCharCode', 0x9a → 'charCodeAt', 0x9b → 'String'
    'A4_jk4P02':  '&z`$"+^/u@v|._<2,{41JGVg%A!jZtN9bqFQSon)cDrKM6WaUwih;yk~eH:p(?Bl}#0IY=xE*[Ld3TCXsR>O57]fP8m',
}


def base91_decode(encoded: str, alphabet: str) -> bytes:
    """Standard basE91 decode with custom alphabet."""
    v = -1; b = 0; n = 0; o = []
    for c in encoded:
        p = alphabet.find(c)
        if p == -1:
            continue
        if v < 0:
            v = p
        else:
            v += p * 91
            b |= v << n
            n += 13 if (v & 8191) > 88 else 14
            v >>= 14
            while n > 7:
                o.append(b & 255)
                b >>= 8
                n -= 8
            v = -1
    if v > -1:
        o.append((b | v << n) & 255)
    return bytes(o)


def is_printable_ascii(data: bytes) -> bool:
    return len(data) > 0 and all(32 <= x < 127 or x == 10 for x in data)


def extract_array(js_text: str) -> list:
    """Extract ePVaOH6 array from stage4 JS source."""
    pos = js_text.find('UqL_pQ3.ePVaOH6=[')
    if pos < 0:
        raise ValueError("ePVaOH6 not found")
    ctx = js_text[pos:]
    start = ctx.index('[')
    result = []
    current = ''
    in_string = False
    escape_next = False
    for ch in ctx[start:]:
        if escape_next:
            current += ch
            escape_next = False
            continue
        if ch == '\\' and in_string:
            current += ch
            escape_next = True
            continue
        if ch == '"' and not in_string:
            in_string = True
            current = ''
            continue
        if ch == '"' and in_string:
            in_string = False
            result.append(current)
            current = ''
            continue
        if in_string:
            current += ch
            continue
        if ch == ']' and not in_string:
            break
    return result


def decode_all(encoded_strings: list) -> list:
    """Try all alphabets for each index; return best decode."""
    results = []
    for idx, s in enumerate(encoded_strings):
        best_text = None
        best_alpha = None
        for alpha_name, alpha in ALPHABETS.items():
            raw = base91_decode(s, alpha)
            try:
                text = raw.decode('utf-8')
                if is_printable_ascii(raw):
                    best_text = text
                    best_alpha = alpha_name
                    break
            except UnicodeDecodeError:
                pass
        results.append({
            'idx': idx,
            'encoded': s,
            'decoded': best_text,
            'alphabet': best_alpha,
        })
    return results


if __name__ == '__main__':
    import sys
    import os

    stage4_path = os.path.join(os.path.dirname(__file__), 'c2_data', 'stage4_5-2-319.js')
    if not os.path.exists(stage4_path):
        print(f"Error: {stage4_path} not found")
        sys.exit(1)

    js_text = open(stage4_path).read()
    encoded_strings = extract_array(js_text)
    print(f"Extracted {len(encoded_strings)} encoded strings from ePVaOH6\n")

    results = decode_all(encoded_strings)

    # Print decoded strings
    print("=" * 72)
    print("STAGE 4 v3 STRING TABLE — DECODED")
    print("=" * 72)
    for r in results:
        idx = r['idx']
        if r['decoded'] is not None:
            print(f"[0x{idx:02x}] ({r['alphabet']}) {repr(r['decoded'])}")
        else:
            print(f"[0x{idx:02x}] (?) OPAQUE: {r['encoded'][:40]!r}...")

    # Highlight IOCs and key strings
    print()
    print("=" * 72)
    print("KEY FINDINGS")
    print("=" * 72)
    for r in results:
        d = r['decoded']
        if d is None:
            continue
        idx = r['idx']
        # BSC transaction hash
        if d.startswith('0x') and len(d) >= 66 and all(c in '0123456789abcdef' for c in d[2:66]):
            print(f"  [0x{idx:02x}] BSC TX HASH (dead-drop C2): {d}")
        # Guard key
        elif d.startswith('_t_'):
            print(f"  [0x{idx:02x}] Global guard key: global['{d}']")
        # Interesting APIs
        elif d in ('Buffer', 'from', 'JSON', 'parse', 'Promise', 'undefined',
                   'String', 'charCodeAt', 'fromCharCode', 'length'):
            print(f"  [0x{idx:02x}] JS API/keyword: {repr(d)}")

    # Save to exports
    out_path = os.path.join(os.path.dirname(__file__), 'exports', 'stage4_v3_strings.txt')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        f.write(f"Stage 4 v3 string table — {len(encoded_strings)} entries\n")
        f.write(f"Source: stage4_5-2-319.js (SHA-256: 7ad66ecc604d61e727f813f13beb39276b32b6473bf0c29b983d5e1f64380328)\n")
        f.write(f"Decoded: {sum(1 for r in results if r['decoded'])} / {len(results)} strings\n")
        f.write("=" * 72 + "\n\n")
        for r in results:
            idx = r['idx']
            if r['decoded'] is not None:
                f.write(f"[0x{idx:02x}] {repr(r['decoded'])}\n")
            else:
                f.write(f"[0x{idx:02x}] OPAQUE({r['alphabet'] or 'unknown'}): {r['encoded'][:60]!r}\n")
    print(f"\nResults saved to: {out_path}")
