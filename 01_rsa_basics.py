"""
=============================================================================
📚 RSA ENCRYPTION BASICS
=============================================================================
Demonstrasi bagaimana enkripsi RSA bekerja - enkripsi yang melindungi
komunikasi internet saat ini.

RSA (Rivest-Shamir-Adleman) adalah enkripsi asimetris yang keamanannya
bergantung pada sulitnya memfaktorkan bilangan prima yang sangat besar.

Author: Quantum Crypto Education
=============================================================================
"""

import random
from math import gcd
from typing import Tuple
import time


def is_prime(n: int) -> bool:
    """Check if a number is prime using trial division."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def generate_prime(bits: int = 8) -> int:
    """Generate a random prime number with approximately 'bits' bits."""
    while True:
        # Generate odd number in range
        n = random.randint(2**(bits-1), 2**bits - 1)
        if n % 2 == 0:
            n += 1
        if is_prime(n):
            return n


def mod_inverse(e: int, phi: int) -> int:
    """Calculate modular multiplicative inverse using Extended Euclidean Algorithm."""
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        gcd_val, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd_val, x, y
    
    _, x, _ = extended_gcd(e % phi, phi)
    return (x % phi + phi) % phi


def generate_rsa_keys(bits: int = 8) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
    """
    Generate RSA key pair.
    
    Returns:
        - public_key: (e, n)
        - private_key: (d, n)
        - primes: (p, q) - untuk demonstrasi, normalnya ini RAHASIA!
    """
    print("\n🔐 GENERATING RSA KEYS...")
    print("=" * 50)
    
    # Step 1: Generate two distinct prime numbers
    p = generate_prime(bits)
    q = generate_prime(bits)
    while q == p:
        q = generate_prime(bits)
    
    print(f"✓ Prime p = {p}")
    print(f"✓ Prime q = {q}")
    
    # Step 2: Compute n = p * q
    n = p * q
    print(f"✓ n = p × q = {n}")
    
    # Step 3: Compute Euler's totient φ(n) = (p-1)(q-1)
    phi = (p - 1) * (q - 1)
    print(f"✓ φ(n) = (p-1)(q-1) = {phi}")
    
    # Step 4: Choose e such that 1 < e < φ(n) and gcd(e, φ(n)) = 1
    e = 65537  # Common choice, but may be too large for small primes
    if e >= phi:
        e = 3
        while gcd(e, phi) != 1:
            e += 2
    print(f"✓ Public exponent e = {e}")
    
    # Step 5: Compute d, the modular multiplicative inverse of e mod φ(n)
    d = mod_inverse(e, phi)
    print(f"✓ Private exponent d = {d}")
    
    print("\n📋 KEY SUMMARY:")
    print(f"   🔓 Public Key  (e, n) = ({e}, {n})")
    print(f"   🔒 Private Key (d, n) = ({d}, {n})")
    print(f"   🔴 Secret Primes: p={p}, q={q} (NEVER SHARE!)")
    
    return (e, n), (d, n), (p, q)


def encrypt(message: int, public_key: Tuple[int, int]) -> int:
    """Encrypt a message using RSA public key."""
    e, n = public_key
    if message >= n:
        raise ValueError(f"Message {message} terlalu besar! Harus < {n}")
    # Ciphertext = message^e mod n
    ciphertext = pow(message, e, n)
    return ciphertext


def decrypt(ciphertext: int, private_key: Tuple[int, int]) -> int:
    """Decrypt a ciphertext using RSA private key."""
    d, n = private_key
    # Message = ciphertext^d mod n
    message = pow(ciphertext, d, n)
    return message


def text_to_numbers(text: str) -> list:
    """Convert text to list of ASCII numbers."""
    return [ord(char) for char in text]


def numbers_to_text(numbers: list) -> str:
    """Convert list of ASCII numbers back to text."""
    return ''.join(chr(num) for num in numbers)


def demo_rsa_encryption():
    """Demonstrate RSA encryption and decryption."""
    print("\n" + "=" * 60)
    print("🔐 RSA ENCRYPTION DEMONSTRATION")
    print("=" * 60)
    
    # Generate keys (using small primes for demonstration)
    public_key, private_key, primes = generate_rsa_keys(bits=10)
    
    # Encrypt a simple message (number)
    print("\n" + "-" * 50)
    print("📨 ENCRYPTION TEST (Single Number)")
    print("-" * 50)
    
    original_message = 42
    print(f"Original message: {original_message}")
    
    encrypted = encrypt(original_message, public_key)
    print(f"Encrypted (ciphertext): {encrypted}")
    
    decrypted = decrypt(encrypted, private_key)
    print(f"Decrypted: {decrypted}")
    
    assert original_message == decrypted, "Decryption failed!"
    print("✅ Encryption/Decryption successful!")
    
    # Encrypt text message
    print("\n" + "-" * 50)
    print("📨 ENCRYPTION TEST (Text Message)")
    print("-" * 50)
    
    text_message = "HI"
    print(f"Original text: '{text_message}'")
    
    numbers = text_to_numbers(text_message)
    print(f"As ASCII numbers: {numbers}")
    
    e, n = public_key
    encrypted_numbers = []
    for num in numbers:
        if num < n:
            encrypted_numbers.append(encrypt(num, public_key))
        else:
            print(f"⚠️  Character {num} too large for key, skipping")
    print(f"Encrypted numbers: {encrypted_numbers}")
    
    decrypted_numbers = [decrypt(c, private_key) for c in encrypted_numbers]
    print(f"Decrypted numbers: {decrypted_numbers}")
    
    decrypted_text = numbers_to_text(decrypted_numbers)
    print(f"Decrypted text: '{decrypted_text}'")
    
    return public_key, private_key, primes


def explain_rsa_security():
    """Explain why RSA is secure (classically) and its vulnerability."""
    print("\n" + "=" * 60)
    print("🛡️  KEAMANAN RSA - MENGAPA AMAN?")
    print("=" * 60)
    
    print("""
    RSA aman karena SULIT memfaktorkan bilangan besar:
    
    ┌─────────────────────────────────────────────────────────┐
    │  PUBLIC:  n = 3233 (produk dari dua prima)              │
    │  SECRET:  p = 61, q = 53                                │
    │                                                         │
    │  Jika Anda tahu p dan q → Anda bisa hitung private key! │
    │  Tapi mencari p dan q dari n sangat SULIT               │
    └─────────────────────────────────────────────────────────┘
    
    Untuk RSA-2048 (standar modern):
    - n memiliki 2048 bit (617 digit desimal!)
    - Komputer klasik butuh TRILIUNAN TAHUN untuk memfaktorkan
    
    ⚠️  TAPI dengan QUANTUM COMPUTER menggunakan SHOR'S ALGORITHM:
    - Faktorisasi bisa dilakukan dalam waktu POLINOMIAL
    - RSA-2048 bisa dipecahkan dalam HITUNGAN JAM/HARI
    
    Ini yang disebut "QUANTUM THREAT"! ⚛️
    """)


if __name__ == "__main__":
    print("=" * 60)
    print("  QUANTUM CRYPTO EDUCATION - Part 1: RSA Basics  ")
    print("=" * 60)
    
    # Run demonstrations
    public_key, private_key, primes = demo_rsa_encryption()
    explain_rsa_security()
    
    # Show the vulnerability
    print("\n" + "=" * 60)
    print("⚠️  THE QUANTUM THREAT")
    print("=" * 60)
    print(f"""
    Dalam demo ini, kita gunakan prima kecil:
    - p = {primes[0]}
    - q = {primes[1]}
    - n = {primes[0] * primes[1]}
    
    SIAPA SAJA bisa memfaktorkan {primes[0] * primes[1]} = {primes[0]} × {primes[1]}
    
    RSA nyata menggunakan prima 1024+ bit:
    - n ≈ 10^308 (308 digit!)
    - Tidak bisa difaktorkan oleh komputer klasik
    - TAPI quantum computer dengan Shor's Algorithm BISA!
    
    ➡️  Lanjut ke 02_classical_attack.py untuk melihat serangan klasik
    ➡️  Lanjut ke 03_shors_algorithm.py untuk serangan quantum
    """)
