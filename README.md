# CryptoLab

A cryptography toolkit built entirely from scratch — no external cryptography libraries — to genuinely understand the mathematics underlying computational security, not just call functions that implement it.

Built over 7 days as a self-directed project applying number theory, probability, and algorithmic thinking to real cryptographic systems: classical ciphers, RSA, Diffie-Hellman key exchange, and cryptographic hashing.

## Why this project exists

I'm applying to study Mathematics and Applied Mathematics with a focus on computational security. Rather than just describing that interest, I wanted to build real, working systems from their mathematical foundations — deriving each algorithm by hand before writing any code, and debugging every implementation myself rather than copying working solutions.

## What's inside

### `day1_complete.py` — Classical Cryptography & Statistics
A Caesar cipher, plus an automatic codebreaker that finds the encryption shift with no prior knowledge, using statistical letter-frequency analysis. Demonstrates why small "key spaces" (only 26 possible shifts) make a cipher fundamentally insecure — and how real English's non-random statistical structure can be exploited.

### `day2_number_theory.py` — The Mathematical Engine Behind RSA
Three functions built from first principles:
- **Fast modular exponentiation** — computes huge modular powers efficiently via square-and-multiply, hand-traced against its binary representation
- **Extended Euclidean Algorithm** — a recursive algorithm finding not just GCDs, but the integer coefficients satisfying Bézout's identity
- **Modular inverse** — built on the above, this is what makes RSA decryption mathematically possible

### `day3_rsa.py` — RSA From Scratch
Full RSA key generation, encryption, and decryption, built entirely on the Day 2 toolkit. Correctly reproduces the classic textbook example (p=61, q=53, e=17 → d=2753, n=3233) and handles arbitrary text via character-by-character encryption. The security rationale: RSA's private key requires factoring n back into its prime components, which is computationally infeasible for sufficiently large primes.

### `day4_diffie_hellman.py` — Key Exchange Over an Insecure Channel
Simulates Alice and Bob agreeing on a shared secret while an eavesdropper (Eve) watches every exchanged message. Includes a working brute-force attack demonstrating the discrete logarithm problem — and why it's the small size of the numbers here (not a flaw in the algorithm) that makes the attack feasible in this toy example.

### `day5_hashing.py` + `day5b_birthday_paradox.py` — Hashing, Honestly
This is the most important file in the project, not because the code is complex, but because of what it documents: **four successive attempts** to build a hash function with a genuine "avalanche effect" (where changing one input character scrambles the entire output), each one improving on a specific flaw discovered through testing, and each one still falling short of what real algorithms like SHA-256 achieve. The final comparison against Python's built-in SHA-256 makes the gap concrete and visible.

The birthday paradox simulation (Monte Carlo methods, validated against theoretical predictions across three parameter sets) explains *why* hash functions need enormous output spaces — collisions are findable in roughly √N attempts, not N attempts.

### `day6_cryptolab_cli.py` — Everything, Integrated
An interactive command-line tool tying every previous day's work into one usable program.

## What I actually learned (the honest version)

The hashing section taught me more than any other part of this project — not because I succeeded, but because I didn't, and had to understand *why*. Building a cryptographically strong hash function isn't a matter of finding the right formula; it requires many rounds of bitwise mixing applied to an entire internal state at once, a fundamentally different architecture than sequential character-by-character combination. Discovering this through iteration, rather than being told it upfront, is the kind of understanding I was hoping this project would produce.

## On the process

I built this with guidance from an AI tutor — working through the mathematics by hand first (tracing algorithms like Extended Euclidean by hand before coding them), then writing and debugging the actual implementation myself. Every bug in this project's history — modular arithmetic wraparound, case-sensitivity handling, the `extended_gcd` formula, the menu structure — was one I found and fixed, with conceptual explanations rather than solutions provided when I got stuck.

## Running it

Each file runs standalone (`python3 day1_complete.py`, etc.) and prints a demonstration. `day6_cryptolab_cli.py` is the interactive version tying everything together.

No external dependencies beyond Python's standard library (`hashlib` for the SHA-256 comparison in Day 5; everything else is built from scratch).
