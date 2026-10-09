import time
import math
from typing import Tuple, Optional
import random


def trial_division(n: int, verbose: bool = True) -> Tuple[Optional[int], Optional[int], float, int]:
   
    if verbose:
        print(f"\nTrying to factorize n = {n}")
        print("-" * 50)
    
    start_time = time.time()
    attempts = 0
    
  
    attempts += 1
    if n % 2 == 0:
        time_taken = time.time() - start_time
        return 2, n // 2, time_taken, attempts
    
    
    i = 3
    sqrt_n = int(math.sqrt(n)) + 1
    
    while i <= sqrt_n:
        attempts += 1
        if n % i == 0:
            time_taken = time.time() - start_time
            if verbose:
                print(f"[OK] Factor found! {n} = {i} × {n // i}")
                print(f"   Attempts: {attempts:,}")
                print(f"   Time: {time_taken:.6f} seconds")
            return i, n // i, time_taken, attempts
        i += 2
        
        
        if verbose and attempts % 100000 == 0:
            print(f"   ... checked {attempts:,} candidates ...")
    
    time_taken = time.time() - start_time
    if verbose:
        print(f"[X] No factors found - {n} is prime!")
        print(f"   Attempts: {attempts:,}")
        print(f"   Time: {time_taken:.6f} seconds")
    return None, None, time_taken, attempts


def pollard_rho(n: int, verbose: bool = True) -> Tuple[Optional[int], Optional[int], float, int]:
   
    if verbose:
        print(f"\nPollard's Rho on n = {n}")
        print("-" * 50)
    
    start_time = time.time()
    attempts = 0
    
    if n % 2 == 0:
        return 2, n // 2, time.time() - start_time, 1
    
    x = random.randint(2, n - 1)
    y = x
    c = random.randint(1, n - 1)
    d = 1
    
    while d == 1:
        attempts += 1
        x = (x * x + c) % n
        y = (y * y + c) % n
        y = (y * y + c) % n
        d = math.gcd(abs(x - y), n)
        
        if attempts > n:  
            break
    
    time_taken = time.time() - start_time
    
    if d != n and d != 1:
        if verbose:
            print(f"[OK] Factor found! {n} = {d} × {n // d}")
            print(f"   Iterations: {attempts:,}")
            print(f"   Time: {time_taken:.6f} seconds")
        return d, n // d, time_taken, attempts
    
    if verbose:
        print(f"[X] Failed to find factors")
    return None, None, time_taken, attempts


def demo_classical_attack():
   
    
    print("\n" + "=" * 70)
    print("CLASSICAL ATTACK DEMONSTRATION")
    print("=" * 70)
    
   
    test_cases = [
        ("Tiny (8-bit)", 143),           
        ("Small (16-bit)", 10403),        
        ("Medium (24-bit)", 1018081),     
        ("Larger (32-bit)", 2147483659), 
    ]
    
    results = []
    
    for name, n in test_cases:
        print(f"\n{'='*60}")
        print(f"Test: {name}")
        print(f"   n = {n} ({n.bit_length()} bits)")
        print("=" * 60)
        
        
        p, q, time_td, attempts_td = trial_division(n)
        
        
        p2, q2, time_pr, attempts_pr = pollard_rho(n)
        
        results.append({
            'name': name,
            'n': n,
            'bits': n.bit_length(),
            'td_time': time_td,
            'td_attempts': attempts_td,
            'pr_time': time_pr,
            'pr_attempts': attempts_pr
        })
    
    
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print(f"{'Size':<20} {'Bits':>6} {'Trial Div Time':>15} {'Pollard Time':>15}")
    print("-" * 70)
    for r in results:
        print(f"{r['name']:<20} {r['bits']:>6} {r['td_time']:>14.6f}s {r['pr_time']:>14.6f}s")
    
    return results


def estimate_rsa_crack_time():
   
    
    print("\n" + "=" * 70)
    print("CLASSICAL FACTORIZATION: QUALITATIVE STATUS")
    print("=" * 70)
    
    estimates = [
        ("RSA-512", 512, "Factored in 1999", "Historical result"),
        ("RSA-768", 768, "Factored in 2009", "Historical result"),
        ("RSA-1024", 1024, "No fixed estimate", "Inadequate for new use"),
        ("RSA-2048", 2048, "No fixed estimate", "Classically infeasible today"),
        ("RSA-4096", 4096, "No fixed estimate", "Classically infeasible today"),
    ]
    
    print(f"\n{'Key Size':<12} {'Bits':>6} {'Historical result / estimate':>28} {'Status':>22}")
    print("-" * 70)
    for name, bits, time_est, status in estimates:
        print(f"{name:<12} {bits:>6} {time_est:>28} {status:>22}")
    
    print("""
    
    These are qualitative comparisons, not wall-clock estimates. Real
    factoring cost depends on implementation, hardware, and the number's
    structure. RSA-1024 is no longer an appropriate size for new deployments.

    Shor's algorithm has polynomial asymptotic complexity in the modulus bit
    length, but that does not imply a practical attack today. Resource
    estimates for RSA-2048 are model-dependent; one published 2021 estimate
    uses about 20 million physical qubits for an 8-hour computation. This is
    an estimate for a particular architecture, not a universal threshold or
    a forecast of when such a computer will exist.
    """)


def complexity_comparison():
   
    print("\n" + "=" * 70)
    print("COMPLEXITY COMPARISON: CLASSICAL vs QUANTUM")
    print("=" * 70)
    
    print("""
    FACTORING n (where n ≈ 2^k, k = bit length):
    
    ┌────────────────────────────────────────────────────────────────────┐
    │  ALGORITHM                    │  COMPLEXITY           │  TYPE      │
    ├────────────────────────────────────────────────────────────────────┤
    │  Trial Division               │  O(√n) = O(2^(k/2))   │  Classical │
    │  Pollard's Rho                │  O(n^(1/4))           │  Classical │
    │  Quadratic Sieve              │  O(exp(√(k·ln(k))))   │  Classical │
    │  General Number Field Sieve   │  Sub-exponential     │  Classical │
    ├────────────────────────────────────────────────────────────────────┤
    │  SHOR'S ALGORITHM             │  O(k³) = O((log n)³)  │  QUANTUM   │
    └────────────────────────────────────────────────────────────────────┘
    
    KEY DIFFERENCE:
    
    • Classical GNFS: SUB-EXPONENTIAL in bit size (k)
      - Cost still grows rapidly with key size
      - RSA-2048 is practically impossible to break
    
    • Quantum (Shor): POLYNOMIAL in bit size (k)
      - Asymptotic growth is polynomial in key size
      - Practical cost still depends on a large fault-tolerant machine
    
    Example for RSA-2048 (k = 2048):

    • Classical GNFS has sub-exponential asymptotic complexity.
    • Shor's algorithm has polynomial asymptotic complexity in k.

    These expressions are not direct operation counts and cannot be converted
    into comparable runtimes by substituting k. A practical quantum attack
    would require a large fault-tolerant machine; there is no reliable date
    for when one might be built.
    """)


if __name__ == "__main__":
    print("=" * 70)
    print("  QUANTUM CRYPTO EDUCATION - Part 2: Classical Attack  ")
    print("=" * 70)
    
    
    demo_classical_attack()
    estimate_rsa_crack_time()
    complexity_comparison()
    
    print("\n" + "=" * 70)
    print("--> NEXT: See 03_shors_algorithm.py for QUANTUM attack!")
    print("=" * 70)
