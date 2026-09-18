"""
Day 3 Complete: RSA From Scratch - built entirely by Neeyam Kafle
using only the number theory toolkit from Day 2 (mod_pow, extended_gcd,
mod_inverse) plus new key generation and text handling built today.

No external cryptography libraries used anywhere.
"""

from day2_number_theory import mod_pow, mod_inverse


def generate_keys(p, q, e):
    """p, q: two primes. e: public exponent. Returns (e, d, n)."""
    n = p * q
    phi_n = (p - 1) * (q - 1)
    d = mod_inverse(e, phi_n)
    return e, d, n


def rsa_encrypt(message, e, n):
    """Encrypt a single number. ciphertext = message^e mod n"""
    return mod_pow(message, e, n)


def rsa_decrypt(ciphertext, d, n):
    """Decrypt a single number. plaintext = ciphertext^d mod n"""
    return mod_pow(ciphertext, d, n)


def rsa_encrypt_text(text, e, n):
    """Encrypt a text string, one character at a time."""
    result = []
    for char in text:
        number = ord(char)
        encrypted_number = rsa_encrypt(number, e, n)
        result.append(encrypted_number)
    return result


def rsa_decrypt_text(encrypted_list, d, n):
    """Decrypt a list of encrypted numbers back into text."""
    result = ""
    for encrypted_number in encrypted_list:
        number = rsa_decrypt(encrypted_number, d, n)
        result = result + chr(number)
    return result


if __name__ == "__main__":
    print("=" * 60)
    print("RSA FROM SCRATCH")
    print("=" * 60)

    # Classic textbook prime pair
    e, d, n = generate_keys(61, 53, 17)
    print(f"\nPublic key:  (e={e}, n={n})")
    print(f"Private key: (d={d}, n={n})")

    message = "Neeyam builds RSA from scratch"
    print(f"\nOriginal message: {message}")

    encrypted = rsa_encrypt_text(message, e, n)
    print(f"Encrypted (first 5 numbers): {encrypted[:5]}...")

    decrypted = rsa_decrypt_text(encrypted, d, n)
    print(f"Decrypted message: {decrypted}")
    print(f"Match: {decrypted == message}")
