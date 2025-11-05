import random

def random_digits(k, seed=None):
    if seed is not None:
        random.seed(seed)  # Optional: make results reproducible
    return [random.randint(0, 9) for _ in range(k)]

# Example: 10 random digits
digits = random_digits(10)
print("Ten random single-digit integers:")
print(digits)