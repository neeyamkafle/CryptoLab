def caesar_encrypt(text, shift):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    result = ""
    for letter in text:
      if letter in alphabet:
        position=alphabet.index(letter)
        new_position=(position+shift)%26
        result=result+alphabet[new_position]
      elif letter.lower() in alphabet:
        position=alphabet.index(letter.lower())
        new_position=(position+shift)%26
        result=result+alphabet[new_position].upper()
      else: result=result+letter
    return result

def caesar_decrypt(text, shift):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    result = ""
    for letter in text:
      if letter in alphabet:
        position=alphabet.index(letter)
        new_position=(position-shift)%26
        result=result+alphabet[new_position]
      elif letter.lower() in alphabet:
        position=alphabet.index(letter.lower())
        new_position=(position-shift)%26
        result=result+alphabet[new_position].upper()
      else: result=result+letter
    return result

def score_text(text):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    ENGLISH_FREQ = {'a':8.2,'b':1.5,'c':2.8,'d':4.3,'e':12.7,'f':2.2,'g':2.0,'h':6.1,'i':7.0,'j':0.15,'k':0.77,'l':4.0,'m':2.4,'n':6.7,'o':7.5,'p':1.9,'q':0.095,'r':6.0,'s':6.3,'t':9.1,'u':2.8,'v':0.98,'w':2.4,'x':0.15,'y':2.0,'z':0.074}
    freq = {a:0 for a in alphabet}
    for letter in text:
        if letter.lower() in alphabet:
            freq[letter.lower()] += 1
    total = sum(freq.values())
    if total == 0: return float('inf')
    score = sum((ENGLISH_FREQ[l] - (freq[l]/total)*100)**2 for l in alphabet)
    return score

def break_caesar(ciphertext):
    a=0
    shift=0
    for i in range(26):
        c = score_text(caesar_decrypt(ciphertext, i))
        if a==0 or c<a:
            a=c
            shift=i
    return a, shift

def mod_pow(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 != 0:
            result = (result * base) % mod
        base = (base ** 2) % mod
        exp = exp // 2
    return result

def extended_gcd(a, b):
    if b == 0: return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    return gcd, y1, x1 - (a//b)*y1

def mod_inverse(e, phi_n):
    gcd, x, y = extended_gcd(e, phi_n)
    return x % phi_n

def generate_keys(p, q, e):
    n = p*q
    phi_n = (p-1)*(q-1)
    d = mod_inverse(e, phi_n)
    return e, d, n

def rsa_encrypt(m, e, n): return mod_pow(m, e, n)
def rsa_decrypt(c, d, n): return mod_pow(c, d, n)
def rsa_encrypt_text(text, e, n): return [rsa_encrypt(ord(ch), e, n) for ch in text]
def rsa_decrypt_text(lst, d, n): return "".join(chr(rsa_decrypt(n_, d, n)) for n_ in lst)

def generate_shared_secret(g, priv, p): return mod_pow(g, priv, p)
def diffie_hellman_demo(p, g, ap, bp):
    apub, bpub = mod_pow(g,ap,p), mod_pow(g,bp,p)
    return generate_shared_secret(bpub,ap,p), generate_shared_secret(apub,bp,p), apub, bpub

import hashlib
def real_sha256(text): return hashlib.sha256(text.encode()).hexdigest()
def compare_avalanche_effect(t1, t2):
    print(f"SHA256('{t1}') = {real_sha256(t1)}")
    print(f"SHA256('{t2}') = {real_sha256(t2)}")

def main_menu():
    print("=== CryptoLab ===")
    print("1. Caesar Cipher (encrypt/decrypt)")
    print("2. Break a Caesar Cipher (frequency analysis)")
    print("3. RSA (generate keys, encrypt/decrypt text)")
    print("4. Diffie-Hellman Key Exchange Demo")
    print("5. Hash Comparison (naive vs SHA-256)")
    print("6. Exit")
    choice = ""
    while choice!=6:
      choice = input("Choose an option: ")
      if choice == "1":
        message = input("Enter your message: ")
        shift = int(input("Enter the shift number: "))
        result = caesar_encrypt(message, shift)
        print("Encrypted:", result)
      elif choice == "2":
        ciphertext = input("Enter the encrypted text: ")
        score, shift = break_caesar(ciphertext)
        decrypted = caesar_decrypt(ciphertext, shift)
        print(f"Found shift: {shift}")
        print(f"Decrypted: {decrypted}")
      elif choice == "3":
        e, d, n = generate_keys(61, 53, 17)
        message = input("Enter a message to encrypt with RSA: ")
        encrypted = rsa_encrypt_text(message, e, n)
        print("Encrypted (as numbers):", encrypted)
        decrypted = rsa_decrypt_text(encrypted, d, n)
        print("Decrypted back:", decrypted)
      elif choice == "4":
        alice_secret, bob_secret, alice_pub, bob_pub = diffie_hellman_demo(23, 5, 6, 15)
        print(f"Alice's shared secret: {alice_secret}")
        print(f"Bob's shared secret: {bob_secret}")
        print(f"Match: {alice_secret == bob_secret}")
      elif choice == "5":
        text1 = input("Enter first text: ")
        text2 = input("Enter second text (try changing one letter): ")
        compare_avalanche_effect(text1, text2)
      elif choice == "6":
        print("Goodbye!")
        break

main_menu()
