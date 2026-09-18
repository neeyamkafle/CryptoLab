"""
Bonus: Birthday Paradox via Monte Carlo Simulation - built by Neeyam Kafle

Connects directly to Day 5's hash collision discussion: this demonstrates
WHY hash functions need enormous output spaces to resist collision attacks.
The "birthday paradox" shows that finding a collision needs only roughly
sqrt(N) attempts, not N attempts -- a critical fact in cryptographic
hash function design.
"""

import random


def simulate_one_trial(num_possible_values):
    """Pick random values until one repeats. Return how many picks that took."""
    seen = set()
    count = 0
    while True:
        value = random.randint(1, num_possible_values)
        count += 1
        if value in seen:
            return count
        seen.add(value)


def monte_carlo_birthday(num_possible_values, num_trials):
    """Run many trials and average the results -- Monte Carlo estimation."""
    results = [simulate_one_trial(num_possible_values) for _ in range(num_trials)]
    average = sum(results) / len(results)
    return average, results


def theoretical_estimate(num_possible_values):
    """The birthday paradox formula: expected collisions after ~1.25*sqrt(N) picks."""
    return 1.25 * (num_possible_values ** 0.5)


if __name__ == "__main__":
    print("=" * 60)
    print("BIRTHDAY PARADOX: MONTE CARLO SIMULATION")
    print("=" * 60)

    for n in [365, 1000, 10000]:
        avg, _ = monte_carlo_birthday(n, num_trials=2000)
        theory = theoretical_estimate(n)
        print(f"\nPossible values: {n}")
        print(f"  Simulated average picks until collision: {avg:.2f}")
        print(f"  Theoretical prediction (1.25*sqrt(n)):    {theory:.2f}")

    print("\n--- Why this matters for hashing ---")
    print("For a hash with 2^32 possible outputs, collisions are expected")
    print("after roughly sqrt(2^32) = ~65,536 attempts, NOT 2^32 attempts.")
    print("This is exactly why SHA-256 uses 2^256 possible outputs --")
    print("even with the birthday shortcut, 2^128 attempts is still infeasible.")
