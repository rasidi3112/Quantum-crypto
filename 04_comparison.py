def main() -> None:
    print("CLASSICAL vs QUANTUM FACTORING (ASYMPTOTIC OVERVIEW)")
    print("=" * 70)
    print(f"{'Modulus':<12} {'Best known classical method':<34} {'Shor algorithm':<22}")
    print("-" * 70)

    for bits in (512, 1024, 2048, 4096):
        print(
            f"RSA-{bits:<7} {'GNFS: sub-exponential':<34} "
            f"{'Polynomial in bit length':<22}"
        )

    print("""

These are asymptotic descriptions, not operation counts, runtimes, or speedup
ratios. Shor's algorithm would require a sufficiently large fault-tolerant
quantum computer. Resource estimates depend on the circuit, hardware model,
error correction, and target runtime; there is no reliable date for such a
machine.
""")


if __name__ == "__main__":
    main()
