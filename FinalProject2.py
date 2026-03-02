import string

def prepare_keyword_6x6(keyword: str) -> str:
    """
    Prepare keyword for 6x6 Playfair:
    - Uppercase
    - Keep only A-Z and 0-9
    - Remove duplicates (keep first occurrence)
    """
    allowed = set(string.ascii_uppercase + string.digits)
    keyword = keyword.upper()
    seen = set()
    result = []
    for ch in keyword:
        if ch in allowed and ch not in seen:
            seen.add(ch)
            result.append(ch)
    return "".join(result)

def build_key_square_6x6(keyword: str):
    """
    Build 6x6 Playfair key square for A-Z + 0-9.
    Returns:
        square: list of lists (6x6)
        pos: dict char -> (row, col)
    """
    base_chars = string.ascii_uppercase + "0123456789"  # 26 + 10 = 36
    key = prepare_keyword_6x6(keyword)

    for ch in base_chars:
        if ch not in key:
            key += ch

    square = [list(key[i:i+6]) for i in range(0, 36, 6)]
    pos = {}
    for r in range(6):
        for c in range(6):
            pos[square[r][c]] = (r, c)
    return square, pos

def clean_plaintext_6x6(text: str) -> str:
    """
    Clean plaintext:
    - Uppercase
    - Keep only A-Z and 0-9 (remove spaces and punctuation)
    """
    allowed = set(string.ascii_uppercase + string.digits)
    result = []
    for ch in text.upper():
        if ch in allowed:
            result.append(ch)
    return "".join(result)

def make_digraphs(text: str, padding_char: str = 'X'):
    """
    Split text into Playfair digraphs:
    - If pair letters are the same, insert padding_char after first
    - If odd length, pad last with padding_char
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
                # insert padding char between identical letters
                b = padding_char
                i += 1
            else:
                i += 2
        pairs.append(a + b)
    return pairs

def playfair_encrypt_pair(pair: str, square, pos):
    """
    Encrypt one digraph using Playfair rules (generic for 6x6).
    """
    n = len(square)  # should be 6
    a, b = pair[0], pair[1]
    r1, c1 = pos[a]
    r2, c2 = pos[b]

    if r1 == r2:
        # Same row -> shift right
        c1 = (c1 + 1) % n
        c2 = (c2 + 1) % n
    elif c1 == c2:
        # Same column -> shift down
        r1 = (r1 + 1) % n
        r2 = (r2 + 1) % n
    else:
        # Rectangle -> swap columns
        c1, c2 = c2, c1

    return square[r1][c1] + square[r2][c2]

def playfair_decrypt_pair(pair: str, square, pos):
    """
    Decrypt one digraph using Playfair rules (generic for 6x6).
    """
    n = len(square)
    a, b = pair[0], pair[1]
    r1, c1 = pos[a]
    r2, c2 = pos[b]

    if r1 == r2:
        # Same row -> shift left
        c1 = (c1 - 1) % n
        c2 = (c2 - 1) % n
    elif c1 == c2:
        # Same column -> shift up
        r1 = (r1 - 1) % n
        r2 = (r2 - 1) % n
    else:
        # Rectangle -> swap columns
        c1, c2 = c2, c1

    return square[r1][c1] + square[r2][c2]

def remove_padding_x(decrypted: str) -> str:
    """
    Method for part 2(d): remove padding 'X' from decrypted text.

    Heuristic:
    - If X is between two identical letters (A X A), treat as padding and remove it.
    - If X is the very last character, treat as padding and remove it.
    - Keep other X's (they might be real).
    """
    chars = list(decrypted)
    result = []
    for i, ch in enumerate(chars):
        if ch == 'X':
            # Check for AXA pattern
            if 0 < i < len(chars) - 1 and chars[i - 1] == chars[i + 1]:
                # skip padding X
                continue
            # Check last character
            if i == len(chars) - 1:
                # skip trailing padding X
                continue
        result.append(ch)
    return "".join(result)

# Main routine for Question 2

def playfair_q2():
    # 2(a) User input for keyword
    last_name = input("Enter your LAST name: ").strip()
    first_name = input("Enter your FIRST name: ").strip()
    extra = input("Enter any extra random characters to append (or press Enter for none): ").strip()

    keyword = last_name + first_name + extra
    print("\n[+] Keyword used for 6x6 Playfair (before cleaning):", keyword)

    # Build the 6x6 key square
    square, pos = build_key_square_6x6(keyword)

    print("\n[+] 6x6 Key Square (A-Z + 0-9):")
    for row in square:
        print(" ".join(row))

    # 2(b) Encrypt the given plaintext
    plaintext = "Did he play fair at St Andrews golf course"
    print("\n[+] Original plaintext:")
    print(plaintext)

    cleaned = clean_plaintext_6x6(plaintext)
    print("\n[+] Cleaned plaintext (A-Z and 0-9 only):")
    print(cleaned)

    digraphs = make_digraphs(cleaned, padding_char='X')
    print("\n[+] Digraphs for encryption (6x6):")
    print(digraphs)

    print("\n[+] Encryption steps (each digraph):")
    cipher_pairs = []
    for p in digraphs:
        c = playfair_encrypt_pair(p, square, pos)
        cipher_pairs.append(c)
        print(f"{p} -> {c}")

    ciphertext = "".join(cipher_pairs)
    print("\n[+] Final ciphertext (6x6):")
    print(ciphertext)

    # 2(c) Decrypt the ciphertext using same key
    print("\n[+] Ciphertext digraphs for decryption (6x6):")
    c_digraphs = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]
    print(c_digraphs)

    print("\n[+] Decryption steps (each digraph):")
    plain_pairs = []
    for p in c_digraphs:
        dec = playfair_decrypt_pair(p, square, pos)
        plain_pairs.append(dec)
        print(f"{p} -> {dec}")

    raw_decrypted = "".join(plain_pairs)
    print("\n[+] Decrypted text BEFORE removing padding X:")
    print(raw_decrypted)

    # 2(d) Apply method to remove padding X
    cleaned_decrypted = remove_padding_x(raw_decrypted)
    print("\n[+] Decrypted text AFTER removing padding X (method for 2d):")
    print(cleaned_decrypted)


if __name__ == "__main__":
    playfair_q2()
