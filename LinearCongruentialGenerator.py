def lcg(a, b, m, x0, k):
    xs = []
    x = x0
    for _ in range(k):
        x = (a * x + b) % m
        xs.append(x)
    return xs

# Example with given values
a, b, m, x0 = 23, 31, 256, 7
lcg_values = lcg(a, b, m, x0, 10)

print("Linear Congruential Generator (x1..x10):")
print(lcg_values)