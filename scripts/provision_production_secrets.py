# -*- coding: utf-8 -*-
"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================
"""

"""
S&R CoreSync - Live Production Secrets & Cloudflare Worker Provisioner
======================================================================
Audits, encrypts (.env.vault AES-256-GCM), and provisions live production
secrets for Stripe/iDEAL (`STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`) and
Meta WhatsApp Cloud API (`WHATSAPP_ACCESS_TOKEN`, `WHATSAPP_PHONE_NUMBER_ID`
for official hotline +31 618111116) into Cloudflare Workers (`workers/sr-lead-capture`).

Usage:
    python scripts/provision_production_secrets.py --audit
    python scripts/provision_production_secrets.py --sync-vault
    python scripts/provision_production_secrets.py --push-cloudflare
"""

import argparse
import os
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(ROOT, ".env")
WORKER_DIR = os.path.join(ROOT, "workers", "sr-lead-capture")

REQUIRED_PRODUCTION_SECRETS = [
    ("STRIPE_PUBLISHABLE_KEY", "pk_live_", "Stripe / iDEAL Live Publishable Key"),
    ("STRIPE_SECRET_KEY", "sk_live_", "Stripe / iDEAL Live Secret Key"),
    ("STRIPE_WEBHOOK_SECRET", "whsec_", "Stripe Webhook Signing Secret"),
    ("MOLLIE_API_KEY", "live_", "Mollie iDEAL / SEPA Live Gateway Key"),
    ("WHATSAPP_ACCESS_TOKEN", "EAA", "Meta WhatsApp Cloud API Permanent Token (+31 618111116)"),
    ("WHATSAPP_PHONE_NUMBER_ID", "", "Meta WhatsApp Business Phone Number ID (+31 618111116)"),
    ("SMTP_HOST", "", "Purelymail / Transactional SMTP Host"),
    ("SMTP_USER", "", "Transactional SMTP Username"),
    ("SMTP_PASS", "", "Transactional SMTP Password"),
]


def parse_env_file(path):
    env_map = {}
    if not os.path.isfile(path):
        return env_map
    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            s = line.strip()
            if not s or s.startswith("#") or "=" not in s:
                continue
            k, v = s.split("=", 1)
            env_map[k.strip()] = v.strip().strip('"').strip("'")
    return env_map


def is_placeholder(val):
    if not val:
        return True
    low = val.lower()
    markers = ("your_", "placeholder", "xxxx", "example", "test_", "sk_test_", "pk_test_")
    return any(m in low for m in markers)


def audit_secrets_readiness(env_map):
    print("=" * 78)
    print("S&R CoreSync - Live Production Secrets Readiness Audit (+31 618111116)")
    print("=" * 78)
    ready_count = 0
    for key, live_prefix, desc in REQUIRED_PRODUCTION_SECRETS:
        val = env_map.get(key, "")
        if val and not is_placeholder(val) and (not live_prefix or val.startswith(live_prefix)):
            status = "✅ LIVE READY"
            ready_count += 1
        elif val:
            status = "⚠️ SANDBOX / PLACEHOLDER CONFIGURED"
        else:
            status = "⏳ PENDING IN .env"
        print(f"  - {key:<26} : {status:<35} ({desc})")
    print("-" * 78)
    print(f"Summary: {ready_count}/{len(REQUIRED_PRODUCTION_SECRETS)} live production keys active; remaining keys running in safe sandbox simulation.")
    print("=" * 78)
    return ready_count


def sync_vault():
    vault_script = os.path.join(ROOT, "scripts", "sovereign_vault.py")
    if os.path.isfile(vault_script):
        subprocess.run([sys.executable, vault_script, "encrypt"], cwd=ROOT, check=False)


def push_to_cloudflare(env_map):
    print("=" * 78)
    print("S&R CoreSync - Pushing Live Secrets to Cloudflare Worker (sr-lead-capture)")
    print("=" * 78)
    pushed = 0
    for key, _, _ in REQUIRED_PRODUCTION_SECRETS:
        val = env_map.get(key, "")
        if not val or is_placeholder(val):
            continue
        proc = subprocess.run(
            ["npx", "wrangler", "secret", "put", key],
            input=val.encode("utf-8"),
            cwd=WORKER_DIR if os.path.isdir(WORKER_DIR) else ROOT,
            capture_output=True,
        )
        if proc.returncode == 0:
            print(f"  ✅ Synced `{key}` to Cloudflare Worker.")
            pushed += 1
        else:
            print(f"  ⚠️ Could not push `{key}` (check `npx wrangler login` status).")
    print(f"Completed Cloudflare Worker secret sync ({pushed} secret(s) updated).")


def main():
    parser = argparse.ArgumentParser(description="Provision S&R CoreSync Live Production Secrets")
    parser.add_argument("--audit", action="store_true", help="Audit .env production secret readiness")
    parser.add_argument("--sync-vault", action="store_true", help="Encrypt .env into .env.vault (AES-256-GCM)")
    parser.add_argument("--push-cloudflare", action="store_true", help="Push live secrets to Cloudflare Worker via Wrangler")
    args = parser.parse_args()

    env_map = parse_env_file(ENV_PATH)
    audit_secrets_readiness(env_map)

    if args.sync_vault:
        sync_vault()

    if args.push_cloudflare:
        push_to_cloudflare(env_map)

    return 0


if __name__ == "__main__":
    sys.exit(main())
