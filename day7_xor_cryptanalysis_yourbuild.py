"""
Bonus: XOR Cryptanalysis - built by Neeyam Kafle

Extends Day 1's frequency-analysis technique to a real, general-purpose
attack: breaking both single-byte and repeating-key XOR ciphers with
NO prior knowledge of the key, using only statistical letter-frequency
scoring.

Includes an honest documented limitation discovered through testing:
frequency analysis becomes unreliable on small samples, directly
connecting to the Law of Large Numbers explored in the Day 5 birthday
paradox simulation.
"""


def score_text(text):
    """
    Lower score = more statistically similar to real English.
    Includes two guards added after real bugs were found through testing:
    1. Rejects non-printable text (fixes a case-insensitivity blind spot
       that let wrong keys tie with the correct one)
    2. Rejects text with zero letters (avoids a division-by-zero crash)
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    ENGLISH_FREQ = {
        'a': 8.2, 'b': 1.5, 'c': 2.8, 'd': 4.3, 'e': 12.7, 'f': 2.2, 'g': 2.0,
        'h': 6.1, 'i': 7.0, 'j': 0.15, 'k': 0.77, 'l': 4.0, 'm': 2.4, 'n': 6.7,
        'o': 7.5, 'p': 1.9, 'q': 0.095, 'r': 6.0, 's': 6.3, 't': 9.1, 'u': 2.8,
        'v': 0.98, 'w': 2.4, 'x': 0.15, 'y': 2.0, 'z': 0.074
    }

    if not all(32 <= ord(c) <= 126 for c in text):
        return float('inf')

    freq = {a: 0 for a in alphabet}
    for letter in text:
        if letter.lower() in alphabet:
            freq[letter.lower()] += 1

    total = sum(freq.values())
    if total == 0:
        return float('inf')

    eng_freq = {a: (freq[a] / total) * 100 for a in freq}
    return sum((ENGLISH_FREQ[l] - eng_freq[l]) ** 2 for l in alphabet)


def break_single_byte_xor(ciphertext_bytes):
    """Try all 256 possible single-byte keys, return the best-scoring one."""
    best_score, best_key = None, None
    for key_byte in range(256):
        decrypted = bytes(b ^ key_byte for b in ciphertext_bytes)
        try:
            decrypted_text = decrypted.decode('ascii')
        except UnicodeDecodeError:
            continue
        score = score_text(decrypted_text)
        if best_score is None or score < best_score:
            best_score = score
            best_key = key_byte
    return best_key, best_score


def split_into_groups(ciphertext_bytes, key_length):
    """Split ciphertext into key_length groups, each XORed with one key byte."""
    return [ciphertext_bytes[offset::key_length] for offset in range(key_length)]


def break_repeating_key_xor(ciphertext_bytes, key_length):
    """
    Break a repeating-key XOR cipher of known length by treating each
    byte-position group as an independent single-byte XOR problem.
    """
    groups = split_into_groups(ciphertext_bytes, key_length)
    key = []
    for group in groups:
        best_key_byte, score = break_single_byte_xor(group)
        key.append(best_key_byte)
    return bytes(key)


def known_plaintext_xor_attack(ciphertext_bytes, known_plaintext_prefix):
    """
    If part of the plaintext is known (e.g. a fixed header like 'crypto{'),
    recover that many bytes of the key directly via XOR -- no brute force
    needed for this portion.
    """
    return bytes(
        ciphertext_bytes[i] ^ known_plaintext_prefix[i]
        for i in range(len(known_plaintext_prefix))
    )


if __name__ == "__main__":
    print("=" * 60)
    print("XOR CRYPTANALYSIS")
    print("=" * 60)

    print("\n--- 1. Known-plaintext attack (recover partial key) ---")
    ciphertext = bytes.fromhex(
        "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e"
        "175d0e077e263451150104"
    )
    known_prefix = b"crypto{"
    partial_key = known_plaintext_xor_attack(ciphertext, known_prefix)
    print(f"Recovered {len(partial_key)} key bytes from known flag format: {partial_key}")
    print("(Limitation: only recovers as many bytes as known plaintext available)")

    print("\n--- 2. Single-byte XOR brute force ---")
    test_message = "the quick brown fox jumps over the lazy dog"
    test_key = 42
    encrypted = bytes(ord(c) ^ test_key for c in test_message)
    found_key, score = break_single_byte_xor(encrypted)
    print(f"True key: {test_key}, Found key: {found_key}")

    print("\n--- 3. Repeating-key XOR (general case, unknown multi-byte key) ---")
    long_message = (
        "the quick brown fox jumps over the lazy dog while thinking about "
        "mathematics and cryptography. applied mathematics is the foundation "
        "of secure systems, and understanding number theory helps build real "
        "cryptographic tools from scratch. this longer message gives "
        "frequency analysis enough data to work with properly."
    )
    repeating_key = b"key"
    encrypted_long = bytes(
        ord(long_message[i]) ^ repeating_key[i % len(repeating_key)]
        for i in range(len(long_message))
    )
    found_repeating_key = break_repeating_key_xor(encrypted_long, key_length=3)
    print(f"True key: {repeating_key}, Found key: {found_repeating_key}")

    print("\n--- Known limitation: small samples are unreliable ---")
    print("On a SHORTER message (~75 chars) split into 3 groups (~25 chars each),")
    print("this same attack found 'KLY' or 'kly' instead of 'key' -- a real")
    print("statistical sample-size problem, not a logic bug. Same principle as")
    print("the Law of Large Numbers explored in the Day 5 birthday paradox sim:")
    print("small samples give unreliable frequency signals; more data resolves it.")
