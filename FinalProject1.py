import string

# ===============================
# Helper functions for 5x5 Playfair
# ===============================

def prepare_keyword_5x5(keyword: str) -> str:
    """
    Prepare keyword for 5x5 Playfair:
    - Uppercase
    - Keep only A–Z
    - Replace J with I
    - Remove duplicates (keep first occurrence)
    """
    keyword = keyword.upper()
    seen = set()
    result = []
    for ch in keyword:
        if ch.isalpha():
            if ch == 'J':
                ch = 'I'
            if ch not in seen:
                seen.add(ch)
                result.append(ch)
    return "".join(result)

def build_key_square_5x5(keyword: str):
    """
    Build 5x5 Playfair key square with I/J combined.
    Returns:
        square: list of lists, 5x5
        pos: dict char -> (row, col)
    """
    base_alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # J removed
    key = prepare_keyword_5x5(keyword)

    for ch in base_alphabet:
        if ch not in key:
            key += ch

    square = [list(key[i:i+5]) for i in range(0, 25, 5)]
    pos = {}
    for r in range(5):
        for c in range(5):
            pos[square[r][c]] = (r, c)
    # Map J to I's position so we can look up J too
    pos['J'] = pos['I']
    return square, pos

def clean_plaintext_5x5(text: str) -> str:
    """
    Clean plaintext:
    - Remove non-letters
    - Uppercase
    - Replace J with I
    """
    result = []
    for ch in text.upper():
        if ch.isalpha():
            if ch == 'J':
                ch = 'I'
            result.append(ch)
    return "".join(result)

def make_digraphs(text: str, padding_char: str = 'X'):
    """
    Split text into Playfair digraphs:
    - If pair letters are the same, insert padding_char after first
    - If odd length, pad last letter with padding_char
    """
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 == len(text):
            b = padding_char
            i += 1
        else:
            b = text[i + 1]
            if a == b:
                # Insert padding char between same letters
                b = padding_char
                i += 1
            else:
                i += 2
        pairs.append(a + b)
    return pairs

def playfair_encrypt_pair(pair: str, square, pos):
    """
    Encrypt one digraph using the Playfair rules.
    """
    a, b = pair[0], pair[1]
    r1, c1 = pos[a]
    r2, c2 = pos[b]
    n = 5

    if r1 == r2:
        # Same row: shift right
        c1 = (c1 + 1) % n
        c2 = (c2 + 1) % n
    elif c1 == c2:
        # Same column: shift down
        r1 = (r1 + 1) % n
        r2 = (r2 + 1) % n
    else:
        # Rectangle: swap columns
        c1, c2 = c2, c1

    return square[r1][c1] + square[r2][c2]

def playfair_decrypt_pair(pair: str, square, pos):
    """
    Decrypt one digraph using the Playfair rules.
    """
    a, b = pair[0], pair[1]
    r1, c1 = pos[a]
    r2, c2 = pos[b]
    n = 5

    if r1 == r2:
        # Same row: shift left
        c1 = (c1 - 1) % n
        c2 = (c2 - 1) % n
    elif c1 == c2:
        # Same column: shift up
        r1 = (r1 - 1) % n
        r2 = (r2 - 1) % n
    else:
        # Rectangle: swap columns
        c1, c2 = c2, c1

    return square[r1][c1] + square[r2][c2]

# ===============================
# Main routines for Question 1
# ===============================

def playfair_q1():
    # 1) Get user input for last and first name
    last_name = input("Enter your LAST name: ").strip()
    first_name = input("Enter your FIRST name: ").strip()

    # Optional: allow user to append extra random chars to the keyword
    extra = input("Enter any extra random characters to append (or press Enter for none): ").strip()

    # Build keyword: last name + first name + extra
    keyword = last_name + first_name + extra
    print("\n[+] Keyword used for Playfair (before cleaning):", keyword)

    # 2) Build 5x5 key square
    square, pos = build_key_square_5x5(keyword)

    print("\n[+] 5x5 Key Square (I/J combined):")
    for row in square:
        print(" ".join(row))

    # 3) Plaintext for Q1
    plaintext = "Did he play fair at St Andrews golf course"
    print("\n[+] Original plaintext:")
    print(plaintext)

    # 4) Clean plaintext
    cleaned = clean_plaintext_5x5(plaintext)
    print("\n[+] Cleaned plaintext (only A–Z, J->I):")
    print(cleaned)

    # 5) Form digraphs
    digraphs = make_digraphs(cleaned, padding_char='X')
    print("\n[+] Digraphs for encryption:")
    print(digraphs)

    # 6) Encrypt each digraph (show steps)
    print("\n[+] Encryption steps (each digraph):")
    cipher_pairs = []
    for p in digraphs:
        c = playfair_encrypt_pair(p, square, pos)
        cipher_pairs.append(c)
        print(f"{p} -> {c}")

    ciphertext = "".join(cipher_pairs)
    print("\n[+] Final ciphertext:")
    print(ciphertext)

    # 7) Decryption: split ciphertext back into digraphs
    print("\n[+] Ciphertext digraphs for decryption:")
    c_digraphs = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]
    print(c_digraphs)

    # 8) Decrypt each digraph (show steps)
    print("\n[+] Decryption steps (each digraph):")
    plain_pairs = []
    for p in c_digraphs:
        dec = playfair_decrypt_pair(p, square, pos)
        plain_pairs.append(dec)
        print(f"{p} -> {dec}")

    decrypted_text = "".join(plain_pairs)
    print("\n[+] Decrypted text (may include padding X):")
    print(decrypted_text)



if __name__ == "__main__":
    playfair_q1()
