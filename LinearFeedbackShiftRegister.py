def lfsr_extend(seed6, k):
    seq = seed6[:]
    for _ in range(k):
        L = len(seq)
        next_bit = seq[L - 6] ^ seq[L - 3]  # XOR is addition mod 2
        seq.append(next_bit)
    return seq[6:6 + k]

# Example with given seed
seed = [0, 0, 1, 1, 1, 0]
next6 = lfsr_extend(seed, 6)

print("LFSR next six bits (7th to 12th):")
print(next6)