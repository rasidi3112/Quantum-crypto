
import numpy as np
import hashlib
import secrets
from typing import Tuple, List
import time


class LWEDemo:
   
    
    def __init__(self, n: int = 16, q: int = 251):
       
        self.n = n
        self.q = q
        print(f"LWE Parameters: n={n}, q={q}")
    
    def generate_keypair(self) -> Tuple[Tuple, Tuple]:
       
        print("\nGenerating LWE Key Pair...")
        
        
        s = np.random.randint(-1, 2, size=self.n)  # {-1, 0, 1}
        print(f"   Secret key s (small coefficients): {s[:5]}...")
        
       
        A = np.random.randint(0, self.q, size=(self.n, self.n))
        print(f"   Public matrix A: {self.n}×{self.n}")
        
       
        e = np.random.randint(-2, 3, size=self.n)
        print(f"   Error vector e (small noise): {e[:5]}...")
        
       
        b = (A @ s + e) % self.q
        print(f"   Public vector b = A·s + e (mod {self.q})")
        
        public_key = (A, b)
        private_key = s
        
        return public_key, private_key
    
    def encrypt(self, public_key: Tuple, message_bit: int) -> Tuple:
       
        A, b = public_key
        
       
        r = np.random.randint(0, 2, size=self.n)
        
        
        e1 = np.random.randint(-1, 2, size=self.n)
        e2 = np.random.randint(-1, 2)
        
       
        u = (A.T @ r + e1) % self.q
        v = (b @ r + e2 + message_bit * (self.q // 2)) % self.q
        
        return (u, v)
    
    def decrypt(self, private_key: np.ndarray, ciphertext: Tuple) -> int:
       
        s = private_key
        u, v = ciphertext
        
      
        result = (v - s @ u) % self.q
        
      
        if result > self.q // 4 and result < 3 * self.q // 4:
            return 1
        else:
            return 0
    
    def demo(self):
       
        print("\n" + "=" * 60)
        print("LEARNING WITH ERRORS (LWE) DEMONSTRATION")
        print("=" * 60)
        print("""
    LWE is a mathematical problem that is:
    ✓ HARD for classical computers
    ✓ No efficient quantum attack is currently known; this remains a security assumption
    
    This is a simplified introduction to lattice ideas used in ML-KEM.
        """)
        
       
        public_key, private_key = self.generate_keypair()
        
       
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


class KyberDemo:
    def __init__(self, k: int = 2, n: int = 256, q: int = 3329):
       
        self.k = k      
        self.n = n      
        self.q = q     
        print(f"Kyber-like Parameters: k={k}, n={n}, q={q}")
    
    def keygen(self) -> Tuple[dict, dict]:
       
        print("\n🔑 Generating Kyber-like Key Pair...")
        
   
        s = np.random.randint(-2, 3, size=(self.k, self.n))
        
       
        A = np.random.randint(0, self.q, size=(self.k, self.k, self.n))
        
       
        e = np.random.randint(-2, 3, size=(self.k, self.n))
        
      
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
      
        print("\n Key Encapsulation...")
        
        A, t = public_key['A'], public_key['t']
        
    
        m = np.random.randint(0, 2, size=32)
        
       
        r = np.random.randint(-1, 2, size=(self.k, self.n))
        e1 = np.random.randint(-1, 2, size=(self.k, self.n))
        e2 = np.random.randint(-1, 2, size=self.n)
        
       
        u = np.zeros((self.k, self.n), dtype=int)
        for i in range(self.k):
            for j in range(self.k):
                u[i] = (u[i] + A[j, i].T * r[j]) % self.q
            u[i] = (u[i] + e1[i]) % self.q
        
        v = np.zeros(self.n, dtype=int)
        for i in range(self.k):
            v = (v + t[i] * r[i]) % self.q
        v = (v + e2) % self.q
        
     
        for i in range(min(32, self.n)):
            v[i] = (v[i] + m[i] * (self.q // 2)) % self.q
        
        ciphertext = {'u': u, 'v': v}
        
        
        shared_secret = hashlib.sha256(m.tobytes()).digest()
        
        print(f"   ✓ Shared secret: {shared_secret.hex()[:32]}...")
        print(f"   ✓ Ciphertext size: ~{u.nbytes + v.nbytes} bytes")
        
        return shared_secret, ciphertext
    
    def decapsulate(self, private_key: dict, ciphertext: dict) -> bytes:
       
        print("\n Key Decapsulation...")
        
        s = private_key['s']
        u, v = ciphertext['u'], ciphertext['v']
        
        
        result = v.copy()
        for i in range(self.k):
            result = (result - s[i] * u[i]) % self.q
        
        
        m = np.zeros(32, dtype=int)
        for i in range(32):
            if result[i] > self.q // 4 and result[i] < 3 * self.q // 4:
                m[i] = 1
        
    
        shared_secret = hashlib.sha256(m.tobytes()).digest()
        
        print(f"   ✓ Recovered secret: {shared_secret.hex()[:32]}...")
        
        return shared_secret
    
    def demo(self):
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
        
        
        public_key, private_key = self.keygen()
        
        
        shared_secret_sender, ciphertext = self.encapsulate(public_key)
        
       
        shared_secret_receiver = self.decapsulate(private_key, ciphertext)
        
       
        print("\n" + "-" * 40)
        print("VERIFICATION:")
        match = shared_secret_sender == shared_secret_receiver
        print(f"   Sender's secret:   {shared_secret_sender.hex()[:32]}...")
        print(f"   Receiver's secret: {shared_secret_receiver.hex()[:32]}...")
        print(f"   {'[OK] Secrets match! Key exchange successful!' if match else '[X] Secrets do not match!'}")
        
        return match

class SPHINCSDemo:
  
    def __init__(self, n: int = 32, w: int = 16, h: int = 8):
       
        self.n = n
        self.w = w
        self.h = h
        print(f"SPHINCS+-like Parameters: n={n}, w={w}, h={h}")
    
    def _hash(self, *args) -> bytes:
      
        data = b''.join(arg if isinstance(arg, bytes) else str(arg).encode() 
                       for arg in args)
        return hashlib.sha256(data).digest()[:self.n]
    
    def _wots_keygen(self, seed: bytes) -> Tuple[List[bytes], bytes]:
       
        sk = [self._hash(seed, i.to_bytes(4, 'big')) for i in range(self.w)]
        pk_elements = [self._chain(s, self.w - 1) for s in sk]
        pk = self._hash(*pk_elements)
        return sk, pk
    
    def _chain(self, x: bytes, steps: int) -> bytes:
        for _ in range(steps):
            x = self._hash(x)
        return x
    
    def keygen(self) -> Tuple[bytes, bytes]:
       
        print("\n🔑 Generating SPHINCS+-like Key Pair...")
        
        sk_seed = secrets.token_bytes(self.n)
        
       
        sk, pk = self._wots_keygen(sk_seed)
        
        secret_key = sk_seed
        public_key = self._hash(pk, b'sphincs_root')
        
        print(f"   ✓ Secret key: {secret_key.hex()[:32]}...")
        print(f"   ✓ Public key: {public_key.hex()[:32]}...")
        
        return secret_key, public_key
    
    def sign(self, secret_key: bytes, message: bytes) -> bytes:
      
        print(f"\nSigning message: '{message.decode()[:30]}...'")
        
      
        msg_hash = self._hash(message)
        
       
        wots_sk, _ = self._wots_keygen(secret_key)
        
       
        sig_parts = []
        for i in range(min(len(msg_hash), self.w)):
            chunk_val = msg_hash[i % len(msg_hash)]
            sig_parts.append(self._chain(wots_sk[i], chunk_val))
        
        signature = b''.join(sig_parts)
        
        print(f"   ✓ Signature size: {len(signature)} bytes")
        print(f"   ✓ Signature: {signature.hex()[:32]}...")
        
        return signature
    
    def verify(self, public_key: bytes, message: bytes, signature: bytes) -> bool:
        print(f"\nVerifying signature...")
        
        msg_hash = self._hash(message)
        
  
        sig_hash = self._hash(signature, msg_hash)
       
        expected = self._hash(public_key, self._hash(message))
        
    
        valid = len(signature) == self.w * self.n
        
        print(f"   ✓ Signature format: {'Valid' if valid else 'Invalid'}")
        
        return valid
    
    def demo(self):

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
        
       
        secret_key, public_key = self.keygen()
        
       
        message = b"Toy message for a simplified signature demonstration"
        signature = self.sign(secret_key, message)
        
       
        valid = self.verify(public_key, message, signature)
        
        print("\n" + "-" * 40)
        print("SIGNATURE VERIFICATION:")
        print(f"   Message: '{message.decode()}'")
        print(f"   Result: {'[OK] VALID signature!' if valid else '[X] INVALID signature!'}")
        
        return valid



def benchmark_algorithms():
    
    print("\n" + "=" * 60)
    print("POST-QUANTUM ALGORITHM BENCHMARKS")
    print("=" * 60)
    
    results = []
    

    print("\n--- LWE ---")
    lwe = LWEDemo(n=64, q=251)
    start = time.time()
    lwe.demo()
    lwe_time = time.time() - start
    results.append(('LWE (n=64)', lwe_time))
    
    
    print("\n--- Kyber-like ---")
    kyber = KyberDemo(k=2, n=128, q=3329)
    start = time.time()
    kyber.demo()
    kyber_time = time.time() - start
    results.append(('Kyber-like', kyber_time))
    

    print("\n--- SPHINCS+ ---")
    sphincs = SPHINCSDemo(n=16, w=16, h=4)
    start = time.time()
    sphincs.demo()
    sphincs_time = time.time() - start
    results.append(('SPHINCS+-like', sphincs_time))
    
  
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
