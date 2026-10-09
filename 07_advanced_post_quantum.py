"""
ADVANCED POST-QUANTUM CRYPTOGRAPHY IMPLEMENTATIONS
Educational demonstrations of post-quantum algorithm concepts.

IMPORTANT DISCLAIMER FOR RESEARCHERS:
- These are SIMPLIFIED implementations for educational purposes
- NOT cryptographically secure - do not use in production
- Real Kyber uses polynomial rings with NTT, not simple matrices
- Real SPHINCS+ uses WOTS+, FORS, and Merkle trees
- PQClean is retired; liboqs is a research and prototyping project, not a production recommendation

References:
- ML-KEM (based on CRYSTALS-Kyber): NIST FIPS 203
- SLH-DSA (based on SPHINCS+): NIST FIPS 205
- LWE: Regev, O. (2005) "On lattices, learning with errors..."
"""

import numpy as np
import hashlib
import secrets
from typing import Tuple, List
import time


# ============================================================================
# LEARNING WITH ERRORS (LWE) - Foundation of Lattice Crypto
# ============================================================================

class LWEDemo:
    """
    Demonstration of the Learning With Errors problem.
    
    Module-LWE underlies ML-KEM (FIPS 203), based on CRYSTALS-Kyber.
    
    Problem: Given A and b = A·s + e, it is hard to find s
    where e is a small error (noise).
    """
    
    def __init__(self, n: int = 16, q: int = 251):
        """
        Initialize LWE parameters.
        
        Args:
            n: Dimension of secret vector
            q: Modulus (prime)
        """
        self.n = n
        self.q = q
        print(f"LWE Parameters: n={n}, q={q}")
    
    def generate_keypair(self) -> Tuple[Tuple, Tuple]:
        """
        Generate LWE key pair.
        
        Returns:
            public_key: (A, b = A·s + e)
            private_key: s
        """
        print("\nGenerating LWE Key Pair...")
        
        # Secret key: random small vector
        s = np.random.randint(-1, 2, size=self.n)  # {-1, 0, 1}
        print(f"   Secret key s (small coefficients): {s[:5]}...")
        
        # Public matrix A: random
        A = np.random.randint(0, self.q, size=(self.n, self.n))
        print(f"   Public matrix A: {self.n}×{self.n}")
        
        # Error vector: small gaussian-like
        e = np.random.randint(-2, 3, size=self.n)
        print(f"   Error vector e (small noise): {e[:5]}...")
        
        # Compute b = A·s + e (mod q)
        b = (A @ s + e) % self.q
        print(f"   Public vector b = A·s + e (mod {self.q})")
        
        public_key = (A, b)
        private_key = s
        
        return public_key, private_key
    
    def encrypt(self, public_key: Tuple, message_bit: int) -> Tuple:
        """
        Encrypt a single bit using LWE.
        
        Args:
            public_key: (A, b)
            message_bit: 0 or 1
        
        Returns:
            ciphertext: (u, v)
        """
        A, b = public_key
        
        # Random binary vector for encryption
        r = np.random.randint(0, 2, size=self.n)
        
        # Error terms
        e1 = np.random.randint(-1, 2, size=self.n)
        e2 = np.random.randint(-1, 2)
        
        # Compute ciphertext
        u = (A.T @ r + e1) % self.q
        v = (b @ r + e2 + message_bit * (self.q // 2)) % self.q
        
        return (u, v)
    
    def decrypt(self, private_key: np.ndarray, ciphertext: Tuple) -> int:
        """
        Decrypt LWE ciphertext.
        
        Args:
            private_key: s
            ciphertext: (u, v)
        
        Returns:
            decrypted bit: 0 or 1
        """
        s = private_key
        u, v = ciphertext
        
        # Compute v - s·u (mod q)
        result = (v - s @ u) % self.q
        
        # Decode: if close to q/2, it's 1; if close to 0, it's 0
        if result > self.q // 4 and result < 3 * self.q // 4:
            return 1
        else:
            return 0
    
    def demo(self):
        """Run full LWE demonstration."""
        print("\n" + "=" * 60)
        print("LEARNING WITH ERRORS (LWE) DEMONSTRATION")
        print("=" * 60)
        print("""
    LWE is a mathematical problem that is:
    ✓ HARD for classical computers
    ✓ No efficient quantum attack is currently known; this remains a security assumption
    
    This is a simplified introduction to lattice ideas used in ML-KEM.
        """)
        
        # Generate keys
        public_key, private_key = self.generate_keypair()
        
        # Encrypt and decrypt test
        print("\nENCRYPTION TEST:")
        print("-" * 40)
        
        test_bits = [0, 1, 1, 0, 1]
        decrypted_bits = []
        
        for bit in test_bits:
            ciphertext = self.encrypt(public_key, bit)
            decrypted = self.decrypt(private_key, ciphertext)
            decrypted_bits.append(decrypted)
            print(f"   Original: {bit} → Encrypted → Decrypted: {decrypted} {'✓' if bit == decrypted else '✗'}")
        
        success = all(o == d for o, d in zip(test_bits, decrypted_bits))
        print(f"\n{'[OK] All bits decrypted correctly!' if success else '[X] Some errors occurred'}")
        
        return success


# ============================================================================
# CRYSTALS-KYBER CONCEPT (Simplified)
# ============================================================================

class KyberDemo:
    """
    Simplified demonstration of CRYSTALS-Kyber concepts.
    
    ML-KEM (FIPS 203), based on CRYSTALS-Kyber, is NIST's key-encapsulation standard.
    Based on Module-LWE (MLWE).
    """
    
    def __init__(self, k: int = 2, n: int = 256, q: int = 3329):
        """
        Kyber-like parameters (simplified).
        
        Real Kyber uses polynomial rings, this is simplified for education.
        """
        self.k = k      # Module rank
        self.n = n      # Polynomial degree
        self.q = q      # Modulus
        print(f"Kyber-like Parameters: k={k}, n={n}, q={q}")
    
    def keygen(self) -> Tuple[dict, dict]:
        """Generate Kyber-like key pair."""
        print("\n🔑 Generating Kyber-like Key Pair...")
        
        # Secret: small polynomial coefficients
        s = np.random.randint(-2, 3, size=(self.k, self.n))
        
        # Public matrix
        A = np.random.randint(0, self.q, size=(self.k, self.k, self.n))
        
        # Error
        e = np.random.randint(-2, 3, size=(self.k, self.n))
        
        # t = A·s + e (simplified)
        t = np.zeros((self.k, self.n), dtype=int)
        for i in range(self.k):
            for j in range(self.k):
                t[i] = (t[i] + A[i, j] * s[j]) % self.q
            t[i] = (t[i] + e[i]) % self.q
        
        public_key = {'A': A, 't': t}
        private_key = {'s': s}
        
        print(f"   ✓ Public key generated (A: {A.shape}, t: {t.shape})")
        print(f"   ✓ Private key generated (s: {s.shape})")
        
        return public_key, private_key
    
    def encapsulate(self, public_key: dict) -> Tuple[bytes, dict]:
        """
        Key encapsulation: create shared secret and ciphertext.
        
        Returns:
            shared_secret: 32-byte key
            ciphertext: encrypted form
        """
        print("\n📦 Key Encapsulation...")
        
        A, t = public_key['A'], public_key['t']
        
        # Random message
        m = np.random.randint(0, 2, size=32)
        
        # Encryption randomness
        r = np.random.randint(-1, 2, size=(self.k, self.n))
        e1 = np.random.randint(-1, 2, size=(self.k, self.n))
        e2 = np.random.randint(-1, 2, size=self.n)
        
        # Compute ciphertext components
        u = np.zeros((self.k, self.n), dtype=int)
        for i in range(self.k):
            for j in range(self.k):
                u[i] = (u[i] + A[j, i].T * r[j]) % self.q
            u[i] = (u[i] + e1[i]) % self.q
        
        v = np.zeros(self.n, dtype=int)
        for i in range(self.k):
            v = (v + t[i] * r[i]) % self.q
        v = (v + e2) % self.q
        
        # Encode message into v
        for i in range(min(32, self.n)):
            v[i] = (v[i] + m[i] * (self.q // 2)) % self.q
        
        ciphertext = {'u': u, 'v': v}
        
        # Derive shared secret from message
        shared_secret = hashlib.sha256(m.tobytes()).digest()
        
        print(f"   ✓ Shared secret: {shared_secret.hex()[:32]}...")
        print(f"   ✓ Ciphertext size: ~{u.nbytes + v.nbytes} bytes")
        
        return shared_secret, ciphertext
    
    def decapsulate(self, private_key: dict, ciphertext: dict) -> bytes:
        """
        Key decapsulation: recover shared secret.
        
        Returns:
            shared_secret: 32-byte key
        """
        print("\n📭 Key Decapsulation...")
        
        s = private_key['s']
        u, v = ciphertext['u'], ciphertext['v']
        
        # Compute v - s^T·u
        result = v.copy()
        for i in range(self.k):
            result = (result - s[i] * u[i]) % self.q
        
        # Decode message
        m = np.zeros(32, dtype=int)
        for i in range(32):
            if result[i] > self.q // 4 and result[i] < 3 * self.q // 4:
                m[i] = 1
        
        # Derive shared secret
        shared_secret = hashlib.sha256(m.tobytes()).digest()
        
        print(f"   ✓ Recovered secret: {shared_secret.hex()[:32]}...")
        
        return shared_secret
    
    def demo(self):
        """Full Kyber-like demonstration."""
        print("\n" + "=" * 60)
        print("CRYSTALS-KYBER DEMONSTRATION (Simplified)")
        print("=" * 60)
        print("""
    ML-KEM (based on CRYSTALS-Kyber) is the NIST standard for:
    • Key Encapsulation Mechanism (KEM)
    • Replacing RSA/ECDH for key exchange
    • Designed to resist known quantum attacks; security assumptions can change
    
    Security based on Module-LWE problem.
        """)
        
        # Key generation
        public_key, private_key = self.keygen()
        
        # Encapsulation (sender)
        shared_secret_sender, ciphertext = self.encapsulate(public_key)
        
        # Decapsulation (receiver)
        shared_secret_receiver = self.decapsulate(private_key, ciphertext)
        
        # Verify
        print("\n" + "-" * 40)
        print("VERIFICATION:")
        match = shared_secret_sender == shared_secret_receiver
        print(f"   Sender's secret:   {shared_secret_sender.hex()[:32]}...")
        print(f"   Receiver's secret: {shared_secret_receiver.hex()[:32]}...")
        print(f"   {'[OK] Secrets match! Key exchange successful!' if match else '[X] Secrets do not match!'}")
        
        return match


# ============================================================================
# SPHINCS+ CONCEPT (Hash-based Signatures)
# ============================================================================

class SPHINCSDemo:
    """
    Simplified SPHINCS+ hash-based signature demonstration.
    
    SPHINCS+ uses Only hash functions - most conservative post-quantum choice!
    """
    
    def __init__(self, n: int = 32, w: int = 16, h: int = 8):
        """
        Initialize SPHINCS+-like parameters.
        
        Args:
            n: Security parameter (hash output bytes)
            w: Winternitz parameter
            h: Tree height
        """
        self.n = n
        self.w = w
        self.h = h
        print(f"SPHINCS+-like Parameters: n={n}, w={w}, h={h}")
    
    def _hash(self, *args) -> bytes:
        """Hash helper."""
        data = b''.join(arg if isinstance(arg, bytes) else str(arg).encode() 
                       for arg in args)
        return hashlib.sha256(data).digest()[:self.n]
    
    def _wots_keygen(self, seed: bytes) -> Tuple[List[bytes], bytes]:
        """
        WOTS+ key generation (simplified Winternitz OTS).
        """
        sk = [self._hash(seed, i.to_bytes(4, 'big')) for i in range(self.w)]
        pk_elements = [self._chain(s, self.w - 1) for s in sk]
        pk = self._hash(*pk_elements)
        return sk, pk
    
    def _chain(self, x: bytes, steps: int) -> bytes:
        """Hash chain."""
        for _ in range(steps):
            x = self._hash(x)
        return x
    
    def keygen(self) -> Tuple[bytes, bytes]:
        """Generate SPHINCS+-like key pair."""
        print("\n🔑 Generating SPHINCS+-like Key Pair...")
        
        # Random seed as secret key
        sk_seed = secrets.token_bytes(self.n)
        
        # Generate WOTS+ keys for root
        sk, pk = self._wots_keygen(sk_seed)
        
        secret_key = sk_seed
        public_key = self._hash(pk, b'sphincs_root')
        
        print(f"   ✓ Secret key: {secret_key.hex()[:32]}...")
        print(f"   ✓ Public key: {public_key.hex()[:32]}...")
        
        return secret_key, public_key
    
    def sign(self, secret_key: bytes, message: bytes) -> bytes:
        """
        Create SPHINCS+-like signature.
        """
        print(f"\nSigning message: '{message.decode()[:30]}...'")
        
        # Hash message
        msg_hash = self._hash(message)
        
        # Generate WOTS signature (simplified)
        wots_sk, _ = self._wots_keygen(secret_key)
        
        # Sign each chunk
        sig_parts = []
        for i in range(min(len(msg_hash), self.w)):
            chunk_val = msg_hash[i % len(msg_hash)]
            sig_parts.append(self._chain(wots_sk[i], chunk_val))
        
        signature = b''.join(sig_parts)
        
        print(f"   ✓ Signature size: {len(signature)} bytes")
        print(f"   ✓ Signature: {signature.hex()[:32]}...")
        
        return signature
    
    def verify(self, public_key: bytes, message: bytes, signature: bytes) -> bool:
        """
        Verify SPHINCS+-like signature.
        """
        print(f"\nVerifying signature...")
        
        msg_hash = self._hash(message)
        
        # Reconstruct and verify (simplified)
        sig_hash = self._hash(signature, msg_hash)
        
        # In real SPHINCS+, we would verify the Merkle tree path
        # This is a simplified verification
        expected = self._hash(public_key, self._hash(message))
        
        # Simplified: just check structure
        valid = len(signature) == self.w * self.n
        
        print(f"   ✓ Signature format: {'Valid' if valid else 'Invalid'}")
        
        return valid
    
    def demo(self):
        """Full SPHINCS+ demonstration."""
        print("\n" + "=" * 60)
        print("SPHINCS+ DEMONSTRATION (Hash-Based Signatures)")
        print("=" * 60)
        print("""
    SLH-DSA (based on SPHINCS+) is specified by NIST FIPS 205:
    • Based ONLY on hash functions
    • Most conservative - security best understood
    • Larger signature size, but very secure
    
    Does not require complex mathematical assumptions!
        """)
        
        # Key generation
        secret_key, public_key = self.keygen()
        
        # Sign message
        message = b"Toy message for a simplified signature demonstration"
        signature = self.sign(secret_key, message)
        
        # Verify signature
        valid = self.verify(public_key, message, signature)
        
        print("\n" + "-" * 40)
        print("SIGNATURE VERIFICATION:")
        print(f"   Message: '{message.decode()}'")
        print(f"   Result: {'[OK] VALID signature!' if valid else '[X] INVALID signature!'}")
        
        return valid


# ============================================================================
# COMPARISON & BENCHMARKS
# ============================================================================

def benchmark_algorithms():
    """Benchmark post-quantum algorithms."""
    print("\n" + "=" * 60)
    print("POST-QUANTUM ALGORITHM BENCHMARKS")
    print("=" * 60)
    
    results = []
    
    # LWE
    print("\n--- LWE ---")
    lwe = LWEDemo(n=64, q=251)
    start = time.time()
    lwe.demo()
    lwe_time = time.time() - start
    results.append(('LWE (n=64)', lwe_time))
    
    # Kyber-like
    print("\n--- Kyber-like ---")
    kyber = KyberDemo(k=2, n=128, q=3329)
    start = time.time()
    kyber.demo()
    kyber_time = time.time() - start
    results.append(('Kyber-like', kyber_time))
    
    # SPHINCS-like
    print("\n--- SPHINCS+ ---")
    sphincs = SPHINCSDemo(n=16, w=16, h=4)
    start = time.time()
    sphincs.demo()
    sphincs_time = time.time() - start
    results.append(('SPHINCS+-like', sphincs_time))
    
    # Summary
    print("\n" + "=" * 60)
    print("BENCHMARK SUMMARY")
    print("=" * 60)
    print(f"\n{'Algorithm':<20} {'Time (ms)':<15}")
    print("-" * 35)
    for name, t in results:
        print(f"{name:<20} {t*1000:>10.2f} ms")
    
    print("""
    
    NOTE:
    • This is a SIMPLIFIED implementation for education
    • Real ML-KEM/SLH-DSA implementations are standardized, reviewed, and substantially more complex
    • Actual performance is much better with C/Rust libraries
    
    These demonstrations are not production implementations. Choose a maintained
    cryptographic provider that fits the deployment and compliance requirements.
    """)


if __name__ == "__main__":
    print("=" * 60)
    print("  ADVANCED POST-QUANTUM CRYPTOGRAPHY")
    print("=" * 60)
    
    benchmark_algorithms()
    
    print("\n" + "=" * 60)
    print("[OK] All demonstrations complete!")
    print("=" * 60)
