"""
Day 1 Complete: Caesar Cipher + Automatic Frequency-Analysis Codebreaker
Built entirely from scratch by Neeyam Kafle

THE MATH:
- Encryption/decryption use modular arithmetic: (position +/- shift) % 26
- Codebreaking uses statistics: English letters have known frequencies
  (e is most common, z is rarest). Scoring each of the 26 possible
  decryptions against real English letter frequency, and picking the
  lowest-scoring (most English-like) result reveals the correct shift
  without ever knowing it in advance.
"""

def caesar_encrypt(text, shift):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    result = ""
    for letter in text:
        if letter in alphabet:
            position = alphabet.index(letter)
            new_position = (position + shift) % 26
            result = result + alphabet[new_position]
        elif letter.lower() in alphabet:
            position = alphabet.index(letter.lower())
            new_position = (position + shift) % 26
            result = result + alphabet[new_position].upper()
        else:
            result = result + letter
    return result


def caesar_decrypt(text, shift):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    result = ""
    for letter in text:
        if letter in alphabet:
            position = alphabet.index(letter)
            new_position = (position - shift) % 26
            result = result + alphabet[new_position]
        elif letter.lower() in alphabet:
            position = alphabet.index(letter.lower())
            new_position = (position - shift) % 26
            result = result + alphabet[new_position].upper()
        else:
            result = result + letter
    return result


def score_text(text):
    """Lower score = more statistically similar to real English"""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    ENGLISH_FREQ = {
        'a': 8.2, 'b': 1.5, 'c': 2.8, 'd': 4.3, 'e': 12.7, 'f': 2.2, 'g': 2.0,
        'h': 6.1, 'i': 7.0, 'j': 0.15, 'k': 0.77, 'l': 4.0, 'm': 2.4, 'n': 6.7,
        'o': 7.5, 'p': 1.9, 'q': 0.095, 'r': 6.0, 's': 6.3, 't': 9.1, 'u': 2.8,
        'v': 0.98, 'w': 2.4, 'x': 0.15, 'y': 2.0, 'z': 0.074
    }
    score = 0
    freq = {}
    for letters in alphabet:
        freq[letters] = 0
    for letter in text:
        if letter.lower() in alphabet:
            if letter.lower() in freq:
                freq[letter.lower()] += 1
    eng_freq = {}
    for a in freq:
        eng_freq[a] = (freq[a] / sum(freq.values())) * 100
    for i in ENGLISH_FREQ:
        score += (ENGLISH_FREQ[i] - eng_freq[i]) ** 2
    return score


def break_caesar(ciphertext):
    """Try all 26 shifts, return (best_score, best_shift)"""
    a = 0
    shift = 0
    for i in range(26):
        c = score_text(caesar_decrypt(ciphertext, i))
        if a == 0 or c < a:
            a = c
            shift = i
    return a, shift


if __name__ == "__main__":
    print("=" * 60)
    print("CRYPTOLAB DAY 1: CAESAR CIPHER + CODEBREAKER")
    print("=" * 60)

    message = "Applied mathematics is the foundation of secure systems"
    shift_used = 19

    encrypted = caesar_encrypt(message, shift_used)
    print(f"\nOriginal:  {message}")
    print(f"Shift used (secret): {shift_used}")
    print(f"Encrypted: {encrypted}")

    print("\n--- Breaking it with NO knowledge of the shift ---")
    best_score, found_shift = break_caesar(encrypted)
    decrypted = caesar_decrypt(encrypted, found_shift)

    print(f"Found shift: {found_shift}")
    print(f"Decrypted:   {decrypted}")
    print(f"Correct: {decrypted == message}")
