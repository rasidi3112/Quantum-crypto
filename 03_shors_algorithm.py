import numpy as np
from math import gcd, log2, ceil
from typing import Optional, Tuple, List
from fractions import Fraction
import random


try:
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
    from qiskit_aer import AerSimulator
    from qiskit.synthesis.qft import synth_qft_full
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False
    print("[!] Qiskit not installed. Install with: pip install qiskit qiskit-aer")
    print("   Running in educational/simulation mode only.\n")


def explain_shors_algorithm():
   
    print("\n" + "=" * 70)
    print("HOW SHOR'S ALGORITHM WORKS")
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
    if verbose:
        print(f"\nClassical period finding for a={a}, N={N}")
    
    r = 1
    current = a % N
    
    while current != 1:
        current = (current * a) % N
        r += 1
        if r > N:  
            if verbose:
                print(f"   Period not found (exceeded N)")
            return -1
    
    if verbose:
        print(f"   Found period r = {r}")
        print(f"   Verification: {a}^{r} mod {N} = {pow(a, r, N)}")
    
    return r


def classical_shors_simulation(N: int, verbose: bool = True) -> Tuple[Optional[int], Optional[int]]:
    if verbose:
        print(f"\n" + "=" * 60)
        print(f"🔬 SIMULATING SHOR'S ALGORITHM for N = {N}")
        print("=" * 60)
   
    if N % 2 == 0:
        if verbose:
            print(f"✓ N is even, trivial factor: 2")
        return 2, N // 2
    
    for b in range(2, int(log2(N)) + 1):
        a = int(round(N ** (1/b)))
        if a ** b == N:
            if verbose:
                print(f"✓ N = {a}^{b}, factor: {a}")
            return a, N // a
    
    max_attempts = 10
    for attempt in range(max_attempts):
        if verbose:
            print(f"\n--- Attempt {attempt + 1} ---")
        
        a = random.randint(2, N - 1)
        if verbose:
            print(f"   Random a = {a}")
        
        g = gcd(a, N)
        if g > 1:
            if verbose:
                print(f"   Lucky! gcd({a}, {N}) = {g}")
            return g, N // g
        
    
        if verbose:
            print(f"   Finding period of f(x) = {a}^x mod {N}...")
        
        r = classical_period_finding(a, N, verbose=False)
        
        if r == -1:
            if verbose:
                print(f"   Period not found, trying again...")
            continue
        
        if verbose:
            print(f"   Period r = {r}")
        
 
        if r % 2 != 0:
            if verbose:
                print(f"   r is odd, trying again...")
            continue
        
      
        x = pow(a, r // 2, N)
        if verbose:
            print(f"   a^(r/2) mod N = {a}^{r//2} mod {N} = {x}")
        
        if x == N - 1:  
            if verbose:
                print(f"   a^(r/2) ≡ -1 (mod N), trying again...")
            continue
        
       
        factor1 = gcd(x - 1, N)
        factor2 = gcd(x + 1, N)
        
        if verbose:
            print(f"   gcd({x} - 1, {N}) = gcd({x-1}, {N}) = {factor1}")
            print(f"   gcd({x} + 1, {N}) = gcd({x+1}, {N}) = {factor2}")
        
      
        if factor1 not in [1, N]:
            if verbose:
                print(f"\n   [OK] SUCCESS! {N} = {factor1} × {N // factor1}")
            return factor1, N // factor1
        if factor2 not in [1, N]:
            if verbose:
                print(f"\n   [OK] SUCCESS! {N} = {factor2} × {N // factor2}")
            return factor2, N // factor2
    
    if verbose:
        print(f"\n   [X] Failed after {max_attempts} attempts")
    return None, None


def create_shors_circuit_demo(N: int, a: int, n_count: int = 4) -> 'QuantumCircuit':
    if not QISKIT_AVAILABLE:
        print("[!] Qiskit required for circuit creation")
        return None
    

    qr_count = QuantumRegister(n_count, 'count')
    qr_aux = QuantumRegister(n_count, 'aux')
    cr = ClassicalRegister(n_count, 'meas')
    
    qc = QuantumCircuit(qr_count, qr_aux, cr)
    
    for i in range(n_count):
        qc.h(qr_count[i])
    

    qc.x(qr_aux[0])
    
    qc.barrier()
   
    for i in range(n_count):
    
        power = 2 ** i
        qc.cp(2 * np.pi * power / (2 ** n_count), qr_count[i], qr_aux[0])
    
    qc.barrier()
    
    
    for i in range(n_count // 2):
        qc.swap(qr_count[i], qr_count[n_count - i - 1])
    for i in range(n_count):
        for j in range(i):
            qc.cp(-np.pi / 2 ** (i - j), qr_count[j], qr_count[i])
        qc.h(qr_count[i])
    
    qc.barrier()
    
  
    qc.measure(qr_count, cr)
    
    return qc


def demo_quantum_period_finding():
   
    
    if not QISKIT_AVAILABLE:
        print("\n[!] Install Qiskit for quantum circuit demo:")
        print("   pip install qiskit qiskit-aer")
        return
    
    print("\n" + "=" * 60)
    print("QUANTUM PERIOD FINDING DEMONSTRATION")
    print("=" * 60)
    
  
    N = 15
    a = 7 
    
    print(f"\nTarget: Factor N = {N}")
    print(f"Using base a = {a}")
    
 
    print(f"\nFunction f(x) = {a}^x mod {N}:")
    print("-" * 30)
    for x in range(10):
        fx = pow(a, x, N)
        print(f"  f({x}) = {a}^{x} mod {N} = {fx}")
    
 
    n_count = 4
    qc = create_shors_circuit_demo(N, a, n_count)
    
    print(f"\nQuantum Circuit (simplified):")
    print(qc.draw(output='text'))
    

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
   
    
    print("\n" + "=" * 70)
    print("FULL FACTORIZATION DEMO (Classical Simulation of Shor's)")
    print("=" * 70)
    
    test_numbers = [15, 21, 35, 77, 91, 143, 221, 323]
    
    print(f"\n{'N':>6} {'p':>6} {'q':>6} {'Status':>20}")
    print("-" * 42)
    
    for N in test_numbers:
        p, q = classical_shors_simulation(N, verbose=False)
        if p and q:
            status = "[OK] Factored"
            print(f"{N:>6} {p:>6} {q:>6} {status:>20}")
        else:
            print(f"{N:>6} {'?':>6} {'?':>6} {'[X] Failed':>20}")
    
    print("""
    
    🔑 KEY INSIGHT:
    ───────────────
    The simulation above uses CLASSICAL period finding (slow).
    
    A real quantum computer would find the period EXPONENTIALLY faster
    using quantum parallelism and interference!
    
    For RSA-2048 (617 digit number):
    • Classical (GNFS): sub-exponential complexity → computationally infeasible
    • Quantum (Shor):   polynomial O(n³) complexity → tractable
    
    IMPORTANT CAVEAT:
    Current quantum computers cannot factor cryptographic-size RSA keys.
    Resource estimates depend on circuit, hardware, and error-correction
    assumptions. For example, Gidney and Ekerå (2021) estimated about
    20 million physical qubits for an 8-hour RSA-2048 computation under their
    model. This is not a universal qubit threshold or a timeline prediction.
    """)


if __name__ == "__main__":
    print("=" * 70)
    print("  QUANTUM CRYPTO EDUCATION - Part 3: Shor's Algorithm  ")
    print("=" * 70)
    

    explain_shors_algorithm()
    
   
    demo_quantum_period_finding()
    
  
    demo_full_factorization()
    
  
    print("\n" + "=" * 70)
    print(" DETAILED EXAMPLE: Factoring 15")
    print("=" * 70)
    classical_shors_simulation(15, verbose=True)
    
    print("\n" + "=" * 70)
    print("--> NEXT: See 04_comparison.py for visual comparison")
    print("--> NEXT: See 05_post_quantum.py for solutions!")
    print("=" * 70)
