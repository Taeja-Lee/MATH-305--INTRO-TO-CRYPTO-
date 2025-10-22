# MATH-305 Intro to Cryptography (Dr. Zhang)
# This is for Homework 3 and 4 question 3

import random
import textwrap
import string

ALPH = string.ascii_uppercase

last_name  = "Lee"
first_name = "Hyunchul"
seed_value = 951753      

paragraph = (
    "The mission of Campbell University is to graduate students with exemplary "
    "academic and professional skills who are prepared for purposeful lives and meaningful "
    "service. The University is informed and inspired by its Baptist heritage and three basic "
    "theological and biblical presuppositions: learning is appointed and conserved by God as "
    "essential to the fulfillment of human destiny; in Christ all things consist and find "
    "ultimate unity; and the Kingdom of God in this world is rooted and grounded in Christian "
    "community. The University embraces the conviction that there is no conflict between the "
    "life of faith and the life of inquiry. This course is consistent with the aforementioned "
    "mission and provides students a positive environment for learning."
)

def build_key_from_names(last: str, first: str, seed: int = 0) -> str:
    """
    Construct a 26-letter cipher alphabet from:
      LAST + FIRST + (randomized remainder of A..Z), dropping repeats.
    Returns a permutation of A..Z (no repeats, length 26).
    """
    base = (last + first).upper()
    base = "".join(ch for ch in base if ch.isalpha())

    seen = set()
    prefix = []
    for ch in base:
        if ch not in seen:
            seen.add(ch)
            prefix.append(ch)

    # Remaining letters not in prefix, shuffled by seed
    remaining = [ch for ch in ALPH if ch not in seen]
    rng = random.Random(seed)
    rng.shuffle(remaining)

    full = (prefix + remaining)[:26]
    # Safety checks
    assert len(full) == 26, "Key must be 26 letters"
    assert len(set(full)) == 26, "Key must have unique letters"

    return "".join(full)

def subst_encrypt(text: str, key_map: str) -> str:
    """
    Substitute plaintext letters A..Z to the letters in key_map.
    Preserves original case; leaves non-letters unchanged.
    """
    out = []
    for ch in text:
        if ch.isalpha():
            idx = ord(ch.upper()) - ord('A')
            c = key_map[idx]
            out.append(c if ch.isupper() else c.lower())
        else:
            out.append(ch)
    return "".join(out)

def subst_decrypt(text: str, key_map: str) -> str:
    """
    Inverse substitution using the key_map to recover plaintext.
    """
    inv = ['?'] * 26
    for i, c in enumerate(key_map):
        inv[ord(c) - ord('A')] = chr(ord('A') + i)

    out = []
    for ch in text:
        if ch.isalpha():
            idx = ord(ch.upper()) - ord('A')
            p = inv[idx]
            out.append(p if ch.isupper() else p.lower())
        else:
            out.append(ch)
    return "".join(out)

# Build key, encrypt, decrypt
key = build_key_from_names(last_name, first_name, seed_value)

ciphertext = subst_encrypt(paragraph, key)
roundtrip  = subst_decrypt(ciphertext, key)

print("Substitution key (maps A..Z ->):")
print(key)
print("\nCiphertext (wrapped to 90 columns):")
for line in textwrap.wrap(ciphertext, 90):
    print(line)

print("\nDecryption check (should equal the original paragraph):")
for line in textwrap.wrap(roundtrip, 90):
    print(line)
