#!/usr/bin/env python3
"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================

sovereign_vault.py
Military-Grade Sovereign Secret Vault for encrypting sensitive environment files (.env)
using authenticated AES-256-GCM and PBKDF2 key derivation.
"""

import os
import sys
import json
import base64
import hashlib
import secrets
from datetime import datetime, timezone
from pathlib import Path

# Force UTF-8 on Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
except ImportError:
    print("Error: The 'cryptography' package is required. Install via: pip install cryptography")
    sys.exit(1)

VAULT_VERSION = "2.0-SOVEREIGN-GCM"
DEFAULT_ENV_FILE = ".env"
DEFAULT_VAULT_FILE = ".env.vault"
KEY_FILE = os.path.join(".secrets", "master.key")
PBKDF2_ITERATIONS = 600000


def get_master_key(require_existing=True):
    """Retrieves master encryption key from environment, key file, or prompt."""
    env_key = os.environ.get("SOVEREIGN_VAULT_KEY")
    if env_key and env_key.strip():
        return env_key.strip()

    if os.path.exists(KEY_FILE):
        try:
            with open(KEY_FILE, "r", encoding="utf-8") as f:
                key = f.read().strip()
                if key:
                    return key
        except Exception as e:
            print(f"Warning: Could not read {KEY_FILE}: {e}")

    if not require_existing:
        return None

    print(f"[-] No master key found in SOVEREIGN_VAULT_KEY or '{KEY_FILE}'.")
    print(f"[*] To generate a sovereign master key, run: python scripts/sovereign_vault.py keygen")
    return None


def derive_aes_key(passphrase: str, salt: bytes) -> bytes:
    """Derives a 256-bit AES key using PBKDF2-HMAC-SHA256 with 600,000 rounds."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    return kdf.derive(passphrase.encode("utf-8"))


def cmd_keygen():
    """Generates a cryptographically strong 256-bit hexadecimal key."""
    os.makedirs(".secrets", exist_ok=True)
    raw_key = secrets.token_hex(32)  # 64 hex characters (256 bits)
    
    with open(KEY_FILE, "w", encoding="utf-8") as f:
        f.write(raw_key + "\n")

    print("==========================================================================")
    print("S&R CoreSync Sovereign Vault - Key Generation")
    print("==========================================================================")
    print(f"✅ Generated new 256-bit sovereign master key.")
    print(f"📁 Saved securely to: {KEY_FILE}")
    print(f"🔒 Note: '{KEY_FILE}' is protected by .gitignore and must NEVER be committed.")
    print(f"🔑 Key Preview: {raw_key[:8]}••••••••••••••••••••••••••••••••••••••••••••••••{raw_key[-8:]}")
    print("==========================================================================")
    return raw_key


def cmd_encrypt(env_path=DEFAULT_ENV_FILE, vault_path=DEFAULT_VAULT_FILE):
    """Encrypts .env into .env.vault using AES-256-GCM."""
    if not os.path.exists(env_path):
        print(f"Error: Source file '{env_path}' not found.")
        sys.exit(1)

    key = get_master_key(require_existing=False)
    if not key:
        print("[*] No existing key found. Auto-generating sovereign master key...")
        key = cmd_keygen()

    with open(env_path, "rb") as f:
        plaintext = f.read()

    salt = secrets.token_bytes(16)
    nonce = secrets.token_bytes(12)  # 96-bit nonce for GCM
    aes_key = derive_aes_key(key, salt)

    aesgcm = AESGCM(aes_key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    sha256_hash = hashlib.sha256(plaintext).hexdigest()

    vault_payload = {
        "format": VAULT_VERSION,
        "algorithm": "AES-256-GCM",
        "kdf": f"PBKDF2-HMAC-SHA256 ({PBKDF2_ITERATIONS} iterations)",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "source_file": os.path.basename(env_path),
        "source_sha256": sha256_hash,
        "salt_b64": base64.b64encode(salt).decode("ascii"),
        "nonce_b64": base64.b64encode(nonce).decode("ascii"),
        "ciphertext_b64": base64.b64encode(ciphertext).decode("ascii"),
    }

    with open(vault_path, "w", encoding="utf-8") as f:
        json.dump(vault_payload, f, indent=2)

    print(f"==========================================================================")
    print(f"S&R CoreSync Sovereign Secret Vault - Encryption Complete")
    print(f"==========================================================================")
    print(f"✅ Source file:     {env_path} ({len(plaintext)} bytes)")
    print(f"🔒 Encrypted vault: {vault_path} (Ciphertext: AES-256-GCM)")
    print(f"🛡️ Integrity Hash:  {sha256_hash[:16]}...")
    print(f"📁 Status:          Safe to store in repository; plaintext stays gitignored.")
    print(f"==========================================================================")


def cmd_decrypt(vault_path=DEFAULT_VAULT_FILE, out_path=DEFAULT_ENV_FILE):
    """Decrypts .env.vault into .env using AES-256-GCM."""
    if not os.path.exists(vault_path):
        print(f"Error: Vault file '{vault_path}' not found.")
        sys.exit(1)

    key = get_master_key(require_existing=True)
    if not key:
        sys.exit(1)

    with open(vault_path, "r", encoding="utf-8") as f:
        try:
            vault_payload = json.load(f)
        except Exception as e:
            print(f"Error: Invalid JSON in vault file: {e}")
            sys.exit(1)

    try:
        salt = base64.b64decode(vault_payload["salt_b64"])
        nonce = base64.b64decode(vault_payload["nonce_b64"])
        ciphertext = base64.b64decode(vault_payload["ciphertext_b64"])
    except KeyError as e:
        print(f"Error: Corrupted vault header, missing {e}")
        sys.exit(1)

    aes_key = derive_aes_key(key, salt)
    aesgcm = AESGCM(aes_key)

    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    except Exception:
        print("❌ Authentication failed! Master key is invalid or vault has been tampered with.")
        sys.exit(1)

    # Verify SHA256 integrity
    computed_hash = hashlib.sha256(plaintext).hexdigest()
    expected_hash = vault_payload.get("source_sha256")
    if expected_hash and computed_hash != expected_hash:
        print("❌ Integrity error: SHA256 checksum mismatch!")
        sys.exit(1)

    # Backup existing file if present
    if os.path.exists(out_path):
        backup_path = f"{out_path}.bak"
        with open(out_path, "rb") as f_in, open(backup_path, "wb") as f_out:
            f_out.write(f_in.read())
        print(f"[*] Backed up existing '{out_path}' -> '{backup_path}'")

    with open(out_path, "wb") as f:
        f.write(plaintext)

    print(f"==========================================================================")
    print(f"S&R CoreSync Sovereign Secret Vault - Decryption Successful")
    print(f"==========================================================================")
    print(f"✅ Decrypted to:    {out_path} ({len(plaintext)} bytes)")
    print(f"🛡️ Verified Hash:  {computed_hash[:16]}... (Valid)")
    print(f"==========================================================================")


def cmd_status():
    """Checks vault status, file sync, and Git safety."""
    print("==========================================================================")
    print("S&R CoreSync Sovereign Secret Vault - Audit Status")
    print("==========================================================================")

    key_exists = bool(get_master_key(require_existing=False))
    env_exists = os.path.exists(DEFAULT_ENV_FILE)
    vault_exists = os.path.exists(DEFAULT_VAULT_FILE)

    print(f"🔑 Master Key Present:   {'✅ Yes' if key_exists else '❌ No (run keygen)'}")
    print(f"📄 Plaintext .env:       {'✅ Present' if env_exists else '⚠️ Missing'}")
    print(f"🔒 Encrypted .env.vault: {'✅ Present' if vault_exists else '⚠️ Missing (run encrypt)'}")

    # Check Git safety
    import subprocess
    try:
        res = subprocess.run(["git", "ls-files", DEFAULT_ENV_FILE], capture_output=True, text=True)
        is_tracked = bool(res.stdout.strip())
        if is_tracked:
            print("🚨 CRITICAL WARNING: .env is currently TRACKED in Git! Untrack immediately via git rm --cached .env")
        else:
            print("🛡️ Git Protection:       ✅ .env is safely gitignored (Not tracked in Git)")
    except Exception:
        pass

    if env_exists and vault_exists:
        try:
            with open(DEFAULT_ENV_FILE, "rb") as f:
                env_hash = hashlib.sha256(f.read()).hexdigest()
            with open(DEFAULT_VAULT_FILE, "r", encoding="utf-8") as f:
                v_data = json.load(f)
                v_hash = v_data.get("source_sha256")

            if env_hash == v_hash:
                print("🔄 Vault Sync:           ✅ .env and .env.vault are in sync 100%")
            else:
                print("⚠️ Vault Sync:           Out of sync. Run 'python scripts/sovereign_vault.py encrypt' to update.")
        except Exception:
            pass
    print("==========================================================================")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in {"help", "-h", "--help"}:
        print("Usage: python scripts/sovereign_vault.py [encrypt|decrypt|keygen|status|rotate]")
        sys.exit(0)

    cmd = sys.argv[1].lower()
    if cmd == "keygen":
        cmd_keygen()
    elif cmd == "encrypt":
        cmd_encrypt()
    elif cmd == "decrypt":
        cmd_decrypt()
    elif cmd == "status":
        cmd_status()
    elif cmd == "rotate":
        print("[*] Rotating sovereign vault key...")
        cmd_decrypt()
        cmd_keygen()
        cmd_encrypt()
        print("✅ Key rotation complete.")
    else:
        print(f"Unknown command: '{cmd}'. Supported: encrypt, decrypt, keygen, status, rotate")
        sys.exit(1)


if __name__ == "__main__":
    main()
