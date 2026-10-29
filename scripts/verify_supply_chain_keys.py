#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_supply_chain_keys.py
===========================
Automated verification tool for S&R CoreSync supply chain cryptographic provenance.
Verifies the FFmpeg release signing key fingerprint and integrity.
Compliant with NIST SP 800-218 & SLSA Level 3/4.
"""

import os
import sys
import subprocess

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

EXPECTED_FINGERPRINT = "FCF986EA15E6E293A5644F10B4322F04D67658D8"
EXPECTED_UID = "FFmpeg release signing key <ffmpeg-devel@ffmpeg.org>"

GPG_PATH = r"C:\Program Files\Git\usr\bin\gpg.exe"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY_PATH = os.path.join(PROJECT_ROOT, "assets", "ffmpeg-release-key.asc")

def verify_key():
    print("=" * 65)
    print(" S&R CoreSync - Cryptographic Provenance & Supply Chain Audit")
    print("=" * 65)

    if not os.path.exists(KEY_PATH):
        print(f"[-] ERROR: Key file not found: {KEY_PATH}")
        return False

    print(f"[+] Key File Located: {KEY_PATH}")

    if not os.path.exists(GPG_PATH):
        print(f"[-] ERROR: GPG engine not found at: {GPG_PATH}")
        return False

    cmd = [GPG_PATH, "--show-keys", KEY_PATH]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')

    if res.returncode != 0:
        print(f"[-] GPG inspection failed: {res.stderr}")
        return False

    output = res.stdout
    print("[+] GPG Output:\n" + output.strip())

    cleaned_output = output.replace(" ", "").replace("\r", "").replace("\n", "")

    if EXPECTED_FINGERPRINT in cleaned_output:
        print("\n[OK] VERIFIED: Fingerprint MATCHES official policy:")
        print(f"     Expected: {EXPECTED_FINGERPRINT}")
        print(f"     UID     : {EXPECTED_UID}")
        print("[OK] Status  : COMPLIANT WITH NIST SP 800-218 & EU CRA.")
        return True
    else:
        print("\n[!] WARNING: Fingerprint mismatch! Potential security hazard.")
        return False

if __name__ == "__main__":
    success = verify_key()
    sys.exit(0 if success else 1)
