# MATH-305 Intro to Cryptography (Dr. Zhang)
# This is for Homework 3 and 4 question 3

import string
from collections import Counter
import textwrap
import wordsegment 

wordsegment.load()

ALPHABET = string.ascii_lowercase
L2N = {ch: i for i, ch in enumerate(ALPHABET)}  # letter → number
N2L = {i: ch for i, ch in enumerate(ALPHABET)}  # number → letter

# Ciphertext
cipher = """ocwyikoooniwugpmxwktzdwgtssayjzwyemdlbnqaaavsuwdvbrflauplo oubf
gqhgcscmgzlatoedcsdeidpbhtmuovpiekifpimfnoamvlpqfxejsm
xmpgkccaykwfzpyuavtelwhrhmwkbbvgtguvtefjlodfefkvpxsgrsorvg
tajbsauhzrzalkwuowhgedefnswmrciwcpaaavogpdnfpktdbalsisurln
psjyeatcuceesohhdarkhwotikbroqrdfmzghgucebvgwcdqxgpbgqwlpb
daylooqdmuhbdqgmyweuik""".replace("\n","").replace(" ","")

# English letter frequency
eng_freq = {
    'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253, 'e': 0.12702,
    'f': 0.02228, 'g': 0.02015, 'h': 0.06094, 'i': 0.06966, 'j': 0.00153,
    'k': 0.00772, 'l': 0.04025, 'm': 0.02406, 'n': 0.06749, 'o': 0.07507,
    'p': 0.01929, 'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,
    'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150, 'y': 0.01974, 'z': 0.00074
}

def friedman_ic(s):
    """Compute Index of Coincidence for a string."""
    N = len(s)
    counts = Counter(s)
    numerator = sum(c*(c-1) for c in counts.values())
    denominator = N*(N-1)
    return numerator/denominator if denominator else 0.0

def avg_ic_by_period(s, m):
    """Average IC across m columns for key length m."""
    cols = ['' for _ in range(m)]
    for i, ch in enumerate(s):
        cols[i % m] += ch
    return sum(friedman_ic(col) for col in cols) / m

def chi_squared(text):
    """Chi-squared statistic comparing text frequency to English frequency."""
    N = len(text)
    obs = Counter(text)
    chi2 = 0
    for ch in ALPHABET:
        expected = eng_freq[ch] * N
        observed = obs.get(ch, 0)
        chi2 += (observed - expected)**2 / (expected if expected > 0 else 1)
    return chi2

def best_shift_for_column(col):
    """Try all 26 shifts and pick the one with lowest chi-squared score."""
    best = None
    for k in range(26):
        # Decrypt this column with shift k
        p = ''.join(ALPHABET[(L2N[ch] - k) % 26] for ch in col)
        score = chi_squared(p)
        if best is None or score < best[0]:
            best = (score, k, p)
    return best  # (chi2, shift, plaintext_col)

def vigenere_decrypt(ct, key):
    """Decrypt a ciphertext with a given Vigenère key."""
    key_nums = [L2N[ch] for ch in key]
    out = []
    for i, ch in enumerate(ct):
        k = key_nums[i % len(key_nums)]
        p = (L2N[ch] - k) % 26
        out.append(N2L[p])
    return ''.join(out)

# Step 1: Find key length

ics = [(m, avg_ic_by_period(cipher, m)) for m in range(1, 21)]
for m, ic in ics:
    print(f"Key length {m:2d}: average IC = {ic:.5f}")

# Pick key length with highest IC (visually around m = 6)
m_guess = max(ics, key=lambda x: x[1])[0]
print("\nMost likely key length =", m_guess)

# Step 2: Find each key letter

cols = ['' for _ in range(m_guess)]
for i, ch in enumerate(cipher):
    cols[i % m_guess] += ch

best_shifts = [best_shift_for_column(col)[1] for col in cols]
key = ''.join(ALPHABET[k] for k in best_shifts)
print("Recovered key =", key)

# Step 3: Decrypt

plaintext = vigenere_decrypt(cipher, key)
print("\nPlaintext sample:")
for line in textwrap.wrap(plaintext[:400], 80):
    print(line)

# Step 4: Making to easier to read

spaced_text = ' '.join(wordsegment.segment(plaintext))
print("\nPlaintet with smart spacing:\n")
for line in textwrap.wrap(spaced_text, 80):
    print(line)