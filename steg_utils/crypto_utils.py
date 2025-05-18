# steg_utils/crypto_utils.py

import base64
import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

BLOCK_SIZE = 16

def pad(data):
    pad_len = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([pad_len]) * pad_len

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

# 🔐 AES encryption with password (PBKDF2 key derivation)
def encrypt_with_password(data: bytes, password: str) -> bytes:
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data))
    return salt + cipher.iv + ct_bytes  # salt + IV + ciphertext

def decrypt_with_password(encrypted: bytes, password: str) -> bytes:
    salt = encrypted[:16]
    iv = encrypted[16:32]
    ciphertext = encrypted[32:]
    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext))

# 🔑 AES with randomly generated key
def generate_random_key(length=16):
    return base64.urlsafe_b64encode(get_random_bytes(length)).decode('utf-8')

def encrypt_with_key(data: bytes, key_str: str) -> bytes:
    key = base64.urlsafe_b64decode(key_str.encode('utf-8'))
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data))
    return cipher.iv + ct_bytes  # IV + ciphertext

def decrypt_with_key(encrypted: bytes, key_str: str) -> bytes:
    key = base64.urlsafe_b64decode(key_str.encode('utf-8'))
    iv = encrypted[:16]
    ciphertext = encrypted[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext))

# ✅ NEW: Combined encryption with random key
def encrypt_with_random_key(data: bytes):
    """
    Generates a random key and encrypts the data.
    Returns: (encrypted_data, key_str)
    """
    key_str = generate_random_key()
    encrypted = encrypt_with_key(data, key_str)
    return encrypted, key_str

# Robust decryption dispatcher
def decrypt(data: bytes, password_or_key: str) -> bytes:
    try:
        print("[*] Trying password-based decryption...")
        return decrypt_with_password(data, password_or_key)
    except Exception as e1:
        print(f"[!] Password-based decryption failed: {e1}")
        try:
            print("[*] Trying key-based decryption...")
            return decrypt_with_key(data, password_or_key)
        except Exception as e2:
            print(f"[!] Key-based decryption failed: {e2}")
            raise ValueError("Decryption failed: Incorrect password or key.")
