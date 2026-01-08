# ⚛️ Quantum Threat to Encryption

Comprehensive educational project demonstrating why quantum computing threatens current encryption and what solutions exist.

![Complexity Comparison](visualizations/01_complexity_comparison.png)

## 🎯 What You'll Learn

1. **How RSA works** - The encryption protecting the internet
2. **Why RSA is secure (classically)** - Prime factorization is hard
3. **Shor's Algorithm** - Quantum algorithm that breaks RSA
4. **The Timeline** - When will quantum computers break encryption?
5. **Post-Quantum Solutions** - NIST standards (Kyber, SPHINCS+)
6. **Advanced Implementations** - LWE, Lattice-based crypto

## 📁 Project Structure

```
QuantumCrypto/
├── 01_rsa_basics.py           # RSA encryption fundamentals
├── 02_classical_attack.py     # Brute force factorization (slow)
├── 03_shors_algorithm.py      # Quantum attack using Qiskit
├── 04_comparison.py           # Classical vs Quantum complexity
├── 05_post_quantum.py         # NIST post-quantum standards
├── 06_visualizations.py       # Generate threat visualizations
├── 07_advanced_post_quantum.py # LWE, Kyber, SPHINCS+ implementations
├── visualizations/
│   ├── 01_complexity_comparison.png
│   ├── 02_quantum_speedup.png
│   ├── 03_threat_timeline.png
│   ├── 04_algorithm_comparison.png
│   └── 05_qubit_progress.png
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run each module
python 01_rsa_basics.py
python 02_classical_attack.py
python 03_shors_algorithm.py
python 04_comparison.py
python 05_post_quantum.py
python 06_visualizations.py      # Generates charts
python 07_advanced_post_quantum.py  # Advanced implementations
```

## 📊 Key Visualizations

### 1. Classical vs Quantum Complexity
Shows the exponential gap between classical and quantum factoring.

### 2. Quantum Speedup Factor
- RSA-512: 10^11x faster
- RSA-2048: 10^25x faster
- RSA-4096: 10^36x faster

### 3. Threat Timeline
From Shor's Algorithm (1994) to predicted Q-Day (~2035).

### 4. Algorithm Security
Classical vs quantum security levels for different algorithms.

### 5. Qubit Progress
Racing toward the ~4000 logical qubits needed to break RSA-2048.

## ⚠️ Key Takeaways

| Encryption | Classical Attack | Quantum Attack |
|------------|------------------|----------------|
| RSA-2048 | ~10^18 years | ~8.59 seconds! |
| AES-256 | ~10^30 years | ~10^15 years (safe!) |
| Kyber-768 | Safe | Safe ✓ |
| SPHINCS+ | Safe | Safe ✓ |

## 🔐 Post-Quantum Algorithms Covered

| Algorithm | Type | Use Case |
|-----------|------|----------|
| **CRYSTALS-Kyber** | Lattice-based | Key Exchange |
| **CRYSTALS-Dilithium** | Lattice-based | Digital Signatures |
| **SPHINCS+** | Hash-based | Digital Signatures |
| **LWE** | Learning With Errors | Encryption basis |

## 📚 Resources

- [Qiskit Textbook](https://qiskit.org/learn)
- [NIST Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [IBM Quantum](https://quantum-computing.ibm.com/)
- [Open Quantum Safe](https://openquantumsafe.org/)

## 📜 License

Educational use only. MIT License.

---

**⚠️ Action Required**: Migrate to post-quantum cryptography before "Q-Day" (~2030-2035)
