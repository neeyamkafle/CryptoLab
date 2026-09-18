"""
Day 4 Complete: Diffie-Hellman Key Exchange - built by Neeyam Kafle

Demonstrates how two parties (Alice and Bob) can agree on a shared
secret over a public channel, and why an eavesdropper (Eve) cannot
easily recover it -- the discrete logarithm problem.
"""

from day2_number_theory import mod_pow


def generate_shared_secret(g, private_key, p):
    """Compute g^private_key mod p."""
    return mod_pow(g, private_key, p)


def diffie_hellman_demo(p, g, alice_private, bob_private):
    """Simulate the full exchange. Returns (alice_secret, bob_secret) -- should match."""
    alice_public = mod_pow(g, alice_private, p)
    bob_public = mod_pow(g, bob_private, p)

    alice_shared_secret = generate_shared_secret(bob_public, alice_private, p)
    bob_shared_secret = generate_shared_secret(alice_public, bob_private, p)

    return alice_shared_secret, bob_shared_secret, alice_public, bob_public


def brute_force_discrete_log(g, p, target):
    """Eve's only option: try every exponent until one matches. Feasible only for small p."""
    for a in range(p):
        if mod_pow(g, a, p) == target:
            return a
    return None


if __name__ == "__main__":
    print("=" * 60)
    print("DIFFIE-HELLMAN KEY EXCHANGE")
    print("=" * 60)

    p, g = 23, 5
    alice_private, bob_private = 6, 15

    alice_secret, bob_secret, alice_public, bob_public = diffie_hellman_demo(
        p, g, alice_private, bob_private
    )

    print(f"\nPublic parameters: p={p}, g={g}")
    print(f"Alice's public value: {alice_public} (private key kept secret: {alice_private})")
    print(f"Bob's public value:   {bob_public} (private key kept secret: {bob_private})")
    print(f"\nAlice's computed shared secret: {alice_secret}")
    print(f"Bob's computed shared secret:   {bob_secret}")
    print(f"Match: {alice_secret == bob_secret}")

    print("\n--- Eve's attack: brute-force the discrete log ---")
    cracked_alice_private = brute_force_discrete_log(g, p, alice_public)
    print(f"Eve brute-forces Alice's private key: {cracked_alice_private}")
    print(f"(Trivial here since p={p} is tiny -- real DH uses primes with hundreds of digits)")
