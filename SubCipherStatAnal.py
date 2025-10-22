# MATH-305 Intro to Cryptography (Dr. Zhang)
# This is for Homework 3 and 4 question 5

import math
import random
from collections import Counter

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def keep_letters_and_spaces(s: str) -> str:
    return "".join(ch for ch in s.upper() if ch.isalpha() or ch.isspace())

def letters_only(s: str) -> str:
    return "".join(ch for ch in s.upper() if ch.isalpha())

def letter_frequency(text: str):
    t = letters_only(text)
    total = len(t) if len(t) > 0 else 1
    c = Counter(t)
    return {ch: c.get(ch, 0) / total for ch in ALPHABET}

# Quadgram model (compact)

def load_quadgrams():
    data = """
TION 13000
NTHE 12000
THER 11500
ETHE 11000
THAT 9500
OFTH 9000
DTHE 8500
INGT 8400
THEM 8300
INTH 8200
HERE 8000
EDTH 7900
THIS 7800
ATIO 7700
HAVE 7600
WITH 7500
MENT 7400
FROM 7300
IONS 7200
OUGH 7100
THES 7000
TING 6900
EVER 6800
RTHE 6700
THEA 6650
THEI 6600
THEY 6550
THE  6500
 AND 6400
AND  6300
ANDT 6250
 TO  6200
TO T 6150
ED A 6100
"""
    q = {}
    total = 0
    for line in data.strip().splitlines():
        gram, cnt = line[:4], int(line[5:])
        q[gram] = cnt
        total += cnt
    qlog = {k: math.log10(v / total) for k, v in q.items()}
    floor = math.log10(0.01 / total)
    return qlog, floor

QLOG, QFLOOR = load_quadgrams()

COMMON_WORDS = [
    "THE","AND","OF","TO","IN","THAT","IS","WITH","FOR","AS","ON","BE","ARE","BY",
    "THIS","WHICH","OR","FROM","AT","IT","AN","NOT","HAVE","HAS","WAS","WERE",
"THESE","THOSE","CAN","WILL","STUDENTS","UNIVERSITY","LEARNING","MISSION","COURSE"
]

def quadgram_score(s: str) -> float:
    s = letters_only(s)
    if len(s) < 4:
        return -1e9
    score = 0.0
    for i in range(len(s) - 3):
        gram = s[i:i+4]
        score += QLOG.get(gram, QFLOOR)
    return score

def common_word_bonus(s: str) -> float:
    u = s.upper()
    bonus = 0.0
    for w in COMMON_WORDS:
        bonus += u.count(w) * 5.0
    bonus += u.count(" ") * 0.05
    return bonus

def language_score(s: str) -> float:
    return quadgram_score(s) + common_word_bonus(s)

# Substitution cipher logic

def decrypt_with_key(ct: str, key: str) -> str:
    inv = {k: p for p, k in zip(ALPHABET, key)}
    out = []
    for ch in ct:
        if ch.upper() in inv:
            dec = inv[ch.upper()]
            out.append(dec if ch.isupper() else dec.lower())
        else:
            out.append(ch)
    return "".join(out)

def random_key(rng: random.Random) -> str:
    letters = list(ALPHABET)
    rng.shuffle(letters)
    return "".join(letters)

def tweak_key(key: str, rng: random.Random) -> str:
    a, b = rng.sample(range(26), 2)
    lst = list(key)
    lst[a], lst[b] = lst[b], lst[a]
    return "".join(lst)

def break_substitution(ciphertext: str, max_iters: int = 30000, restarts: int = 8, seed: int = 7):
    rng = random.Random(seed)
    best_global = (-1e9, None, None)
    ct = keep_letters_and_spaces(ciphertext)

    for _ in range(restarts):
        key = random_key(rng)
        pt = decrypt_with_key(ct, key)
        best_local = (language_score(pt), key, pt)
        T = 20.0
        cooling = 0.0004
        for _ in range(max_iters):
            cand_key = tweak_key(best_local[1], rng)
            cand_pt  = decrypt_with_key(ct, cand_key)
            cand_sc  = language_score(cand_pt)
            if cand_sc > best_local[0] or rng.random() < math.exp((cand_sc - best_local[0]) / T):
                best_local = (cand_sc, cand_key, cand_pt)
            T = max(0.001, T * (1 - cooling))
        if best_local[0] > best_global[0]:
            best_global = best_local

    return best_global  # (score, key, plaintext)

# Crib-based mapping helper

def build_mapping_from_pairs(pairs):
    m = {}
    for cword, pword in pairs:
        for c, p in zip(cword.upper(), pword.upper()):
            if c.isalpha():
                m[c] = p
    return m

def apply_partial_mapping(text: str, mapping: dict) -> str:
    out = []
    for ch in text:
        if ch.upper() in mapping:
            dec = mapping[ch.upper()]
            out.append(dec if ch.isupper() else dec.lower())
        elif ch.isalpha():
            out.append("_")
        else:
            out.append(ch)
    return "".join(out)

CIPHERTEXT = """LDG VOMMOTU TS AZVRHGWW KUOJGPMOLC OM LT IPZNKZLG MLKNGULM FOLD
GEGVRWZPC ZAZNGVOA ZUN RPTSGMMOTUZW MXOWWM FDT ZPG RPGRZPGN
STP RKPRTMGSKW WOJGM ZUN VGZUOUISKW MGPJOAG. LDG KUOJGPMOLC OM
OUSTPVGN ZUN OUMROPGN HC OLM HZRLOML DGPOLZIG ZUN LDPGG HZMOA
LDGTWTIOAZW ZUN HOHWOAZW RPGMKRRTMOLOTUM: WGZPUOUI OM
ZRRTOULGN ZUN ATUMGPJGN HC ITN ZM GMMGULOZW LT LDG SKWSOWWVGUL
TS DKVZU NGMLOUC; OU ADPOML ZWW LDOUIM ATUMOML ZUN SOUN KWLOVZLG
KUOLC; ZUN LDG XOUINTV TS ITN OU LDOM FTPWN OM PTTLGN ZUN IPTKUNGN
OU ADPOMLOZU ATVVKUOLC. LDG KUOJGPMOLC GVHPZAGM LDG ATUJOALOTU
LDZL LDGPG OM UT ATUSWOAL HGLFGGU LDG WOSG TS SZOLD ZUN LDG WOSG
TS OUQKOPC. LDOM ATKPMG OM ATUMOMLGUL FOLD LDG ZSTPGVGULOTUGN
VOMMOTU ZUN RPTJONGM MLKNGULM Z RTMOLOJG GUJOPTUVGUL STP
WGZPUOUI."""

STARTER_CRIBS = [
    ("LDG", "THE"),
    ("VOMMOTU", "MISSION"),
    ("TS", "OF"),
    ("AZVRHGWW", "CAMPBELL"),
    ("KUOJGPMOLC", "UNIVERSITY"),
]

def main():
    print("="*70)
    print("LETTER FREQUENCIES")
    print("="*70)
    freqs = letter_frequency(CIPHERTEXT)
    print(" ".join(f"{ch}:{freqs[ch]:.3f}" for ch in ALPHABET))

    print("\n" + "="*70)
    print("CRIB-BASED PARTIAL DECODE")
    print("="*70)
    mapping = build_mapping_from_pairs(STARTER_CRIBS)
    partial = apply_partial_mapping(CIPHERTEXT, mapping)
    print(partial)

    print("\n" + "="*70)
    print("AUTOMATED CRACK (Simulated Annealing)")
    print("="*70)
    score, key, pt = break_substitution(CIPHERTEXT, max_iters=20000, restarts=6, seed=11)
    print("Recovered key (plain→cipher order):", key)
    print("\nBest plaintext guess:\n")
    print(pt)

if __name__ == "__main__":
    main()
