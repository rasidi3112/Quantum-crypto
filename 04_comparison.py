"""
📊 COMPARISON: CLASSICAL vs QUANTUM ATTACKS
Perbandingan antara serangan klasik dan quantum pada RSA.
"""

import math

def classical_complexity(bits: int) -> float:
    """GNFS complexity for factoring."""
    n = 2 ** bits
    ln_n = bits * math.log(2)
    ln_ln_n = math.log(ln_n)
    c = (64/9) ** (1/3)
    return min(math.exp(c * (ln_n ** (1/3)) * (ln_ln_n ** (2/3))), 1e100)

def quantum_complexity(bits: int) -> float:
    """Shor's algorithm complexity."""
    return bits ** 3

def ops_to_time(ops: float) -> str:
    """Convert operations to time (1 GHz)."""
    secs = ops / 1e9
    if secs < 60: return f"{secs:.2f} sec"
    elif secs < 3600: return f"{secs/60:.2f} min"
    elif secs < 86400: return f"{secs/3600:.2f} hours"
    elif secs < 31536000: return f"{secs/86400:.2f} days"
    else: return f"{secs/31536000:.2e} years"

if __name__ == "__main__":
    print("=" * 70)
    print("📊 CLASSICAL vs QUANTUM COMPARISON")
    print("=" * 70)
    
    sizes = [512, 1024, 2048, 4096]
    print(f"\n{'Key':<10} {'Classical':<25} {'Quantum':<20} {'Speedup':<15}")
    print("-" * 70)
    
    for bits in sizes:
        c = classical_complexity(bits)
        q = quantum_complexity(bits)
        print(f"RSA-{bits:<5} {ops_to_time(c):<25} {ops_to_time(q):<20} {c/q:.2e}")
    
    print("\n⚠️  Quantum provides EXPONENTIAL speedup!")
    print("   RSA-2048 safe classically, but vulnerable to quantum!")
