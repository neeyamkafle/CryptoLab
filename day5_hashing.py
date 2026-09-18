"""
Day 5 Complete: Hashing & the Avalanche Effect - built by Neeyam Kafle

This file documents an honest engineering journey: building a naive hash
function, iterating on it through testing, and discovering WHY real
cryptographic hash functions (like SHA-256) need far more sophisticated
mixing than a simple formula can provide.
"""

import hashlib


def simple_hash(text):
    """
    A naive, educational hash function. NOT cryptographically secure.
    Final version after iterating through several attempts:
    - v1: hash*31 + ord(char) -- last char changes hash by a tiny, predictable amount
    - v2: added ord(char)**(index+1) -- fixed last-char issue but overweighted late chars
    - v3: ord(char)*(index+1) -- fixed overweighting but reintroduced small last-char changes
    - v4 (this one): split exponent scheme (first half vs second half of string) --
      best balance found, but still nowhere near real avalanche effect (see comparison below)
    """
    hash_value = 0
    for index, char in enumerate(text):
        if index < (len(text) // 2):
            hash_value = (hash_value * 31 + ord(char) ** (index + 1)) % (2**32)
        else:
            hash_value = (hash_value * 31 + ord(char) ** index) % (2**32)
    return hash_value


def real_sha256(text):
    """Real, production-grade cryptographic hash for comparison."""
    return hashlib.sha256(text.encode()).hexdigest()


def compare_avalanche_effect(text1, text2):
    """Show side-by-side how a naive hash vs real SHA-256 respond to a small input change."""
    print(f"Comparing '{text1}' vs '{text2}':\n")

    print("Naive simple_hash:")
    print(f"  {text1} -> {simple_hash(text1)}")
    print(f"  {text2} -> {simple_hash(text2)}")
    print(f"  Difference: {abs(simple_hash(text1) - simple_hash(text2))}")

    print("\nReal SHA-256:")
    print(f"  {text1} -> {real_sha256(text1)}")
    print(f"  {text2} -> {real_sha256(text2)}")
    print("  (Notice: every character of the output differs, with no visible pattern)")


if __name__ == "__main__":
    print("=" * 60)
    print("HASHING & THE AVALANCHE EFFECT")
    print("=" * 60)
    print()
    compare_avalanche_effect("hello", "hellp")
