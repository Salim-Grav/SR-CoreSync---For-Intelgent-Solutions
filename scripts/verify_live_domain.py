# -*- coding: utf-8 -*-
"""
S&R CoreSync - Live Domain and Multilingual Portal Health Auditor
Audits https://sr-coresync.com/ for all 29 language portals, demo pages, and sovereign hubs.
"""

import urllib.request
import urllib.error
import ssl
import time
import json
import sys

DOMAIN = "https://sr-coresync.com"

LANGUAGES = [
    "de", "fr", "nl", "en", "es", "it", "sv", "no", "da", "fi",
    "pl", "pt", "el", "cs", "ro", "hu", "bg", "sk", "hr", "lt",
    "sl", "lv", "et", "ga", "mt", "tr", "ku", "ckb"
]

CORE_HUBS = [
    "api-docs.html",
    "smart-business-advisor.html",
    "autonomous-tax-audit.html",
    "sovereign-gold-rwa-treasury.html",
    "autonomous-cyber-range.html",
    "sovereign-arbitration-hub.html",
    "multi-cbdc-bridge.html",
    "zkp-confidential-enclave.html"
]

def check_url(url, timeout=10):
    ctx = ssl.create_default_context()
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SR-CoreSync-Live-Auditor/2026.1"
        }
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            elapsed = int((time.time() - t0) * 1000)
            status = resp.status
            size = len(resp.read())
            return {"url": url, "status": status, "size": size, "elapsed_ms": elapsed, "error": None}
    except urllib.error.HTTPError as e:
        elapsed = int((time.time() - t0) * 1000)
        return {"url": url, "status": e.code, "size": 0, "elapsed_ms": elapsed, "error": str(e)}
    except Exception as e:
        elapsed = int((time.time() - t0) * 1000)
        return {"url": url, "status": 0, "size": 0, "elapsed_ms": elapsed, "error": str(e)}

def main():
    print("=" * 75)
    print(" S&R CoreSync - Live Production Audit: https://sr-coresync.com/")
    print("=" * 75)

    results = []
    
    # 1. Root and Arabic
    root_urls = [
        f"{DOMAIN}/",
        f"{DOMAIN}/demo.html",
    ]
    print("\n[+] Auditing Root Arabic Portals...")
    for u in root_urls:
        res = check_url(u)
        status_mark = "✓" if res["status"] == 200 else "✗"
        print(f"  [{status_mark}] {u:<45} Status: {res['status']} | Size: {res['size']:>8} B | Latency: {res['elapsed_ms']}ms")
        results.append(res)

    # 2. Multilingual 28 Languages
    print(f"\n[+] Auditing 28 Non-Arabic Portals ({len(LANGUAGES)*2} URLs)...")
    success_count = 0
    for lang in LANGUAGES:
        for page in ["", "demo.html"]:
            u = f"{DOMAIN}/{lang}/{page}" if page else f"{DOMAIN}/{lang}/"
            res = check_url(u)
            status_mark = "✓" if res["status"] == 200 else "✗"
            if res["status"] == 200:
                success_count += 1
            print(f"  [{status_mark}] {u:<45} Status: {res['status']} | Size: {res['size']:>8} B | Latency: {res['elapsed_ms']}ms")
            results.append(res)

    # 3. Core Sovereign Hubs
    print(f"\n[+] Auditing Core Sovereign Platform Hubs ({len(CORE_HUBS)} URLs)...")
    hubs_success = 0
    for hub in CORE_HUBS:
        u = f"{DOMAIN}/{hub}"
        res = check_url(u)
        status_mark = "✓" if res["status"] == 200 else "✗"
        if res["status"] == 200:
            hubs_success += 1
        print(f"  [{status_mark}] {u:<55} Status: {res['status']} | Size: {res['size']:>8} B | Latency: {res['elapsed_ms']}ms")
        results.append(res)

    print("\n" + "=" * 75)
    print(" AUDIT SUMMARY REPORT")
    print("=" * 75)
    total_checked = len(results)
    passed_200 = sum(1 for r in results if r["status"] == 200)
    print(f"Total Live URLs Audited : {total_checked}")
    print(f"Passed (HTTP 200 OK)    : {passed_200} / {total_checked} ({passed_200/total_checked*100:.1f}%)")
    
    if passed_200 == total_checked:
        print("\nALL 29 MULTILINGUAL PORTALS AND SOVEREIGN HUBS ARE LIVE AND HEALTHY!")
    else:
        print(f"\nWarning: {total_checked - passed_200} URLs failed. Details:")
        for r in results:
            if r["status"] != 200:
                print(f"  FAILED: {r['url']} -> Status: {r['status']} | Error: {r['error']}")

if __name__ == "__main__":
    main()

