import random
from math import gcd
from typing import Tuple
import time


def is_prime(n: int) -> bool:
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
   
    while True:
        
        n = random.randint(2**(bits-1), 2**bits - 1)
        if n % 2 == 0:
            n += 1
        if is_prime(n):
            return n


def mod_inverse(e: int, phi: int) -> int:
  
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
    
    print("\nGENERATING RSA KEYS...")
    print("=" * 50)
    
    
    p = generate_prime(bits)
    q = generate_prime(bits)
    while q == p:
        q = generate_prime(bits)
    
    print(f"✓ Prime p = {p}")
    print(f"✓ Prime q = {q}")
    
    
    n = p * q
    print(f"✓ n = p × q = {n}")
    
    
    phi = (p - 1) * (q - 1)
    print(f"✓ φ(n) = (p-1)(q-1) = {phi}")
    
    
    e = 65537  
    if e >= phi:
        e = 3
        while gcd(e, phi) != 1:
            e += 2
    print(f"✓ Public exponent e = {e}")
    
    
    d = mod_inverse(e, phi)
    print(f"✓ Private exponent d = {d}")
    
    print("\nKEY SUMMARY:")
    print(f"   Public Key  (e, n) = ({e}, {n})")
    print(f"   Private Key (d, n) = ({d}, {n})")
    print(f"   Secret Primes: p={p}, q={q} (NEVER SHARE!)")
    
    return (e, n), (d, n), (p, q)


def encrypt(message: int, public_key: Tuple[int, int]) -> int:
   
    e, n = public_key
    if message >= n:
        raise ValueError(f"Message {message} is too large! Must be < {n}")
   
    ciphertext = pow(message, e, n)
    return ciphertext


def decrypt(ciphertext: int, private_key: Tuple[int, int]) -> int:
    
    d, n = private_key
    
    message = pow(ciphertext, d, n)
    return message


def text_to_numbers(text: str) -> list:
  
    return [ord(char) for char in text]


def numbers_to_text(numbers: list) -> str:
   
    return ''.join(chr(num) for num in numbers)


def demo_rsa_encryption():
   
    print("\n" + "=" * 60)
    print("RSA ENCRYPTION DEMONSTRATION")
    print("=" * 60)
    
    
    public_key, private_key, primes = generate_rsa_keys(bits=10)
    
    
    print("\n" + "-" * 50)
    print("ENCRYPTION TEST (Single Number)")
    print("-" * 50)
    
    original_message = 42
    print(f"Original message: {original_message}")
    
    encrypted = encrypt(original_message, public_key)
    print(f"Encrypted (ciphertext): {encrypted}")
    
    decrypted = decrypt(encrypted, private_key)
    print(f"Decrypted: {decrypted}")
    
    assert original_message == decrypted, "Decryption failed!"
    print("[OK] Encryption/Decryption successful!")
    
    
    print("\n" + "-" * 50)
    print("ENCRYPTION TEST (Text Message)")
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
            print(f"[WARN] Character {num} too large for key, skipping")
    print(f"Encrypted numbers: {encrypted_numbers}")
    
    decrypted_numbers = [decrypt(c, private_key) for c in encrypted_numbers]
    print(f"Decrypted numbers: {decrypted_numbers}")
    
    decrypted_text = numbers_to_text(decrypted_numbers)
    print(f"Decrypted text: '{decrypted_text}'")
    
    return public_key, private_key, primes


def explain_rsa_security():
   
    print("\n" + "=" * 60)
    print("RSA SECURITY - WHY IS IT SECURE?")
    print("=" * 60)
    
    print("""
    RSA is secure because it is HARD to factor large numbers:
    
    ┌─────────────────────────────────────────────────────────┐
    │  PUBLIC:  n = 3233 (product of two primes)              │
    │  SECRET:  p = 61, q = 53                                │
    │                                                         │
    │  If you know p and q → You can compute the private key! │
    │  But finding p and q from n is very HARD                │
    └─────────────────────────────────────────────────────────┘
    
    For RSA-2048:
    - n has 2048 bits (617 decimal digits)
    - Factoring it with the best known classical methods is not practical
      with current computing resources.

    A sufficiently large, fault-tolerant quantum computer running Shor's
    algorithm could factor RSA moduli in polynomial time. No such machine
    exists today, and published resource estimates depend on hardware and
    error-correction assumptions; this demo does not estimate a break time.
    """)


if __name__ == "__main__":
    print("=" * 60)
    print("  QUANTUM CRYPTO EDUCATION - Part 1: RSA Basics  ")
    print("=" * 60)
    
    
    public_key, private_key, primes = demo_rsa_encryption()
    explain_rsa_security()
    
    print("\n" + "=" * 60)
    print("[!] THE QUANTUM THREAT")
    print("=" * 60)
    print(f"""
    In this demo, we use small primes:
    - p = {primes[0]}
    - q = {primes[1]}
    - n = {primes[0] * primes[1]}
    
    ANYONE can factor {primes[0] * primes[1]} = {primes[0]} × {primes[1]}
    
    Real deployments use much larger moduli (commonly RSA-2048 or larger):
    - Factoring them is infeasible with currently known classical resources
    - A sufficiently capable, fault-tolerant quantum computer could change
      that; current quantum devices cannot factor cryptographic-size RSA keys
    
    --> Continue to 02_classical_attack.py to see classical attacks
    --> Continue to 03_shors_algorithm.py for quantum attacks
    """)
