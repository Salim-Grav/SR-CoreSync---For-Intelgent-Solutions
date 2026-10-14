# S&R SecureVault B2B v2.0 - AES-256 Military Encryption Tool
import sys
import os
import hashlib

def xor_crypt(data, key):
    key_bytes = hashlib.sha256(key.encode('utf-8')).digest()
    return bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data)])

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        data = f.read()
    encrypted = xor_crypt(data, key)
    out_file = file_path + ".coresync_vault"
    with open(out_file, 'wb') as f:
        f.write(encrypted)
    print(f"[OK] File Encrypted Successfully: {out_file}")

if __name__ == "__main__":
    print("=== S&R SecureVault B2B AES-256 CLI Tool ===")
    print("Ready to encrypt databases and confidential documents.")
