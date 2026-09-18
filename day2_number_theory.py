"""
Day 2 Complete: Number Theory Toolkit - built entirely from scratch
by Neeyam Kafle, hand-tracing every algorithm before coding it.

These three functions are the complete mathematical engine behind RSA.
"""

def mod_pow(base, exp, mod):
    """Fast modular exponentiation using square-and-multiply."""
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 != 0:
            result = (result * base) % mod
        base = (base ** 2) % mod
        exp = exp // 2
    return result


def extended_gcd(a, b):
    """Returns (gcd, x, y) such that a*x + b*y = gcd(a, b)."""
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y


def mod_inverse(e, phi_n):
    """Find d such that (e * d) % phi_n == 1."""
    gcd, x, y = extended_gcd(e, phi_n)
    if gcd != 1:
        raise ValueError("No modular inverse exists (e and phi_n aren't coprime)")
    return x % phi_n


if __name__ == "__main__":
    print("=" * 60)
    print("NUMBER THEORY TOOLKIT")
    print("=" * 60)

    print("\n--- Fast Modular Exponentiation ---")
    print("mod_pow(7, 128, 13) =", mod_pow(7, 128, 13))
    print("Verify vs Python built-in:", pow(7, 128, 13))

    print("\n--- Extended Euclidean Algorithm ---")
    gcd, x, y = extended_gcd(56, 15)
    print(f"extended_gcd(56, 15) = gcd={gcd}, x={x}, y={y}")
    print(f"Verify: 56*{x} + 15*{y} = {56*x + 15*y}")

    print("\n--- Modular Inverse ---")
    e, phi = 17, 3120
    d = mod_inverse(e, phi)
    print(f"mod_inverse({e}, {phi}) = {d}")
    print(f"Verify: ({e} * {d}) % {phi} = {(e*d) % phi} (should be 1)")
