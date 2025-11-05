def bbs_bits(p, q, x0, k):
    n = p * q
    xs = []
    bits = []
    x = x0
    for _ in range(k):
        x = pow(x, 2, n)
        xs.append(x)
        bits.append(x & 1)
    return xs, bits

# Example with given values
p, q, x0 = 19, 31, 17
bbs_states, bbs_output = bbs_bits(p, q, x0, 10)

print("Blum Blum Shub states (x1..x10):")
print(bbs_states)
print("BBS output bits (b1..b10):")
print(bbs_output)