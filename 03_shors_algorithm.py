"""
=============================================================================
⚛️ SHOR'S ALGORITHM - THE QUANTUM THREAT
=============================================================================
Implementasi dan simulasi Shor's Algorithm menggunakan Qiskit.

Shor's Algorithm adalah algoritma quantum yang dapat memfaktorkan
bilangan besar dalam waktu POLINOMIAL - ancaman nyata untuk RSA!

Ditemukan oleh Peter Shor (1994) di MIT.

Author: Quantum Crypto Education
=============================================================================
"""

import numpy as np
from math import gcd, log2, ceil
from typing import Optional, Tuple, List
from fractions import Fraction
import random

# Try to import Qiskit
try:
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
    from qiskit_aer import AerSimulator
    from qiskit.synthesis.qft import synth_qft_full
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False
    print("⚠️  Qiskit not installed. Install with: pip install qiskit qiskit-aer")
    print("   Running in educational/simulation mode only.\n")


def explain_shors_algorithm():
    """Explain how Shor's Algorithm works."""
    
    print("\n" + "=" * 70)
    print("📚 HOW SHOR'S ALGORITHM WORKS")
    print("=" * 70)
    
    print("""
    GOAL: Factor N = p × q (where p, q are prime)
    
    CLASSICAL APPROACH:
    Try all possible factors → O(√N) → SLOW for large N
    
    SHOR'S QUANTUM APPROACH:
    Reduce factoring to PERIOD FINDING (which quantum does fast!)
    
    ═══════════════════════════════════════════════════════════════════
    
    STEP 1: Classical Pre-processing
    ─────────────────────────────────
    1. Check if N is even → if yes, factor = 2
    2. Check if N = a^b for some a, b → if yes, factor = a
    3. Pick random a where 1 < a < N
    4. Check gcd(a, N) → if > 1, we found a factor!
    
    STEP 2: Quantum Part (Period Finding)
    ──────────────────────────────────────
    Find the PERIOD r of the function: f(x) = a^x mod N
    
    This is where quantum provides EXPONENTIAL SPEEDUP!
    
    Quantum Fourier Transform (QFT) finds periodicity in superposition.
    
    STEP 3: Classical Post-processing
    ──────────────────────────────────
    If r is even and a^(r/2) ≢ -1 (mod N):
    
        factors = gcd(a^(r/2) ± 1, N)
    
    ═══════════════════════════════════════════════════════════════════
    
    QUANTUM CIRCUIT OVERVIEW:
    
    |0⟩ ─────────H─────────────────────────QFT†────── Measure
    |0⟩ ─────────H─────────────────────────QFT†────── Measure
    ...          ...                        ...
    |0⟩ ─────────H─────────────────────────QFT†────── Measure
                   │
                   │ Controlled
                   │ Modular Exponentiation
                   ▼
    |1⟩ ─────────[U^(2^k) mod N]───────────────────── (ancilla)
    
    The measurement gives us information about the period r!
    
    ═══════════════════════════════════════════════════════════════════
    
    COMPLEXITY:
    • Classical: O(exp(n^(1/3))) where n = bit length of N
    • Shor's:    O(n³)           → POLYNOMIAL! ← THIS IS THE BREAKTHROUGH
    
    """)


def classical_period_finding(a: int, N: int, verbose: bool = True) -> int:
    """
    Find period r such that a^r ≡ 1 (mod N) using classical method.
    This is O(r) - slow for large r.
    """
    if verbose:
        print(f"\n🔍 Classical period finding for a={a}, N={N}")
    
    r = 1
    current = a % N
    
    while current != 1:
        current = (current * a) % N
        r += 1
        if r > N:  # Safety limit
            if verbose:
                print(f"   Period not found (exceeded N)")
            return -1
    
    if verbose:
        print(f"   Found period r = {r}")
        print(f"   Verification: {a}^{r} mod {N} = {pow(a, r, N)}")
    
    return r


def classical_shors_simulation(N: int, verbose: bool = True) -> Tuple[Optional[int], Optional[int]]:
    """
    Simulate Shor's algorithm classically (for educational purposes).
    
    Note: This uses classical period finding, not quantum!
    Real quantum computers would do this exponentially faster.
    """
    if verbose:
        print(f"\n" + "=" * 60)
        print(f"🔬 SIMULATING SHOR'S ALGORITHM for N = {N}")
        print("=" * 60)
    
    # Step 1: Trivial checks
    if N % 2 == 0:
        if verbose:
            print(f"✓ N is even, trivial factor: 2")
        return 2, N // 2
    
    # Step 2: Check if N is a prime power
    for b in range(2, int(log2(N)) + 1):
        a = int(round(N ** (1/b)))
        if a ** b == N:
            if verbose:
                print(f"✓ N = {a}^{b}, factor: {a}")
            return a, N // a
    
    # Step 3: Main loop
    max_attempts = 10
    for attempt in range(max_attempts):
        if verbose:
            print(f"\n--- Attempt {attempt + 1} ---")
        
        # Pick random a
        a = random.randint(2, N - 1)
        if verbose:
            print(f"   Random a = {a}")
        
        # Check gcd
        g = gcd(a, N)
        if g > 1:
            if verbose:
                print(f"   Lucky! gcd({a}, {N}) = {g}")
            return g, N // g
        
        # Find period (this is where quantum speedup would occur)
        if verbose:
            print(f"   Finding period of f(x) = {a}^x mod {N}...")
        
        r = classical_period_finding(a, N, verbose=False)
        
        if r == -1:
            if verbose:
                print(f"   Period not found, trying again...")
            continue
        
        if verbose:
            print(f"   Period r = {r}")
        
        # Check if r is useful
        if r % 2 != 0:
            if verbose:
                print(f"   r is odd, trying again...")
            continue
        
        # Calculate a^(r/2)
        x = pow(a, r // 2, N)
        if verbose:
            print(f"   a^(r/2) mod N = {a}^{r//2} mod {N} = {x}")
        
        if x == N - 1:  # x ≡ -1 (mod N)
            if verbose:
                print(f"   a^(r/2) ≡ -1 (mod N), trying again...")
            continue
        
        # Success! Calculate factors
        factor1 = gcd(x - 1, N)
        factor2 = gcd(x + 1, N)
        
        if verbose:
            print(f"   gcd({x} - 1, {N}) = gcd({x-1}, {N}) = {factor1}")
            print(f"   gcd({x} + 1, {N}) = gcd({x+1}, {N}) = {factor2}")
        
        # Return non-trivial factors
        if factor1 not in [1, N]:
            if verbose:
                print(f"\n   ✅ SUCCESS! {N} = {factor1} × {N // factor1}")
            return factor1, N // factor1
        if factor2 not in [1, N]:
            if verbose:
                print(f"\n   ✅ SUCCESS! {N} = {factor2} × {N // factor2}")
            return factor2, N // factor2
    
    if verbose:
        print(f"\n   ❌ Failed after {max_attempts} attempts")
    return None, None


def create_shors_circuit_demo(N: int, a: int, n_count: int = 4) -> 'QuantumCircuit':
    """
    Create a simplified Shor's algorithm circuit for demonstration.
    
    Note: This is a simplified version. Full Shor's requires
    controlled modular exponentiation which is very complex.
    """
    if not QISKIT_AVAILABLE:
        print("⚠️  Qiskit required for circuit creation")
        return None
    
    # Create circuit
    qr_count = QuantumRegister(n_count, 'count')
    qr_aux = QuantumRegister(n_count, 'aux')
    cr = ClassicalRegister(n_count, 'meas')
    
    qc = QuantumCircuit(qr_count, qr_aux, cr)
    
    # Initialize counting register with Hadamards
    for i in range(n_count):
        qc.h(qr_count[i])
    
    # Initialize auxiliary register to |1⟩
    qc.x(qr_aux[0])
    
    qc.barrier()
    
    # Simplified controlled modular exponentiation
    # In a real implementation, this would be much more complex
    for i in range(n_count):
        # Placeholder for controlled U^(2^i) where U|y⟩ = |ay mod N⟩
        power = 2 ** i
        qc.cp(2 * np.pi * power / (2 ** n_count), qr_count[i], qr_aux[0])
    
    qc.barrier()
    
    # Inverse QFT on counting register
    iqft = synth_qft_full(n_count).inverse()
    qc.append(iqft, qr_count)
    
    qc.barrier()
    
    # Measure
    qc.measure(qr_count, cr)
    
    return qc


def demo_quantum_period_finding():
    """Demonstrate quantum period finding concept."""
    
    if not QISKIT_AVAILABLE:
        print("\n⚠️  Install Qiskit for quantum circuit demo:")
        print("   pip install qiskit qiskit-aer")
        return
    
    print("\n" + "=" * 60)
    print("⚛️ QUANTUM PERIOD FINDING DEMONSTRATION")
    print("=" * 60)
    
    # Simple example: factor 15
    N = 15
    a = 7  # coprime to 15
    
    print(f"\nTarget: Factor N = {N}")
    print(f"Using base a = {a}")
    
    # Show the function we're finding period of
    print(f"\nFunction f(x) = {a}^x mod {N}:")
    print("-" * 30)
    for x in range(10):
        fx = pow(a, x, N)
        print(f"  f({x}) = {a}^{x} mod {N} = {fx}")
    
    # Create and run circuit
    n_count = 4
    qc = create_shors_circuit_demo(N, a, n_count)
    
    print(f"\nQuantum Circuit (simplified):")
    print(qc.draw(output='text'))
    
    # Simulate
    simulator = AerSimulator()
    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts()
    
    print(f"\nMeasurement Results:")
    print("-" * 30)
    for state, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  |{state}⟩: {count} times ({count/10:.1f}%)")
    
    print("""
    
    INTERPRETING RESULTS:
    ─────────────────────
    The peaks in measurement correspond to multiples of 2^n/r,
    where r is the period we're looking for.
    
    Using continued fractions, we can extract r from these values
    and then compute factors using gcd(a^(r/2) ± 1, N).
    
    """)


def demo_full_factorization():
    """Demo complete factorization using simulated Shor's."""
    
    print("\n" + "=" * 70)
    print("🔓 FULL FACTORIZATION DEMO (Classical Simulation of Shor's)")
    print("=" * 70)
    
    test_numbers = [15, 21, 35, 77, 91, 143, 221, 323]
    
    print(f"\n{'N':>6} {'p':>6} {'q':>6} {'Status':>20}")
    print("-" * 42)
    
    for N in test_numbers:
        p, q = classical_shors_simulation(N, verbose=False)
        if p and q:
            status = "✅ Factored"
            print(f"{N:>6} {p:>6} {q:>6} {status:>20}")
        else:
            print(f"{N:>6} {'?':>6} {'?':>6} {'❌ Failed':>20}")
    
    print("""
    
    🔑 KEY INSIGHT:
    ───────────────
    The simulation above uses CLASSICAL period finding (slow).
    
    A real quantum computer would find the period EXPONENTIALLY faster
    using quantum parallelism and interference!
    
    For RSA-2048 (617 digit number):
    • Classical: ~10^30 operations (trillions of years)
    • Quantum:   ~10^10 operations (hours/days)
    
    This is why quantum computing is an EXISTENTIAL THREAT to RSA!
    """)


if __name__ == "__main__":
    print("=" * 70)
    print("  QUANTUM CRYPTO EDUCATION - Part 3: Shor's Algorithm  ")
    print("=" * 70)
    
    # Explain the algorithm
    explain_shors_algorithm()
    
    # Demo quantum circuit (if Qiskit available)
    demo_quantum_period_finding()
    
    # Demo full factorization
    demo_full_factorization()
    
    # Detailed example
    print("\n" + "=" * 70)
    print("📝 DETAILED EXAMPLE: Factoring 15")
    print("=" * 70)
    classical_shors_simulation(15, verbose=True)
    
    print("\n" + "=" * 70)
    print("➡️  NEXT: See 04_comparison.py for visual comparison")
    print("➡️  NEXT: See 05_post_quantum.py for solutions!")
    print("=" * 70)
