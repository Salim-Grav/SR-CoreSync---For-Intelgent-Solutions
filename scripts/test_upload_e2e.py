"""
End-to-End Upload Test Script for S&R CoreSync
===============================================
Tests: POST /api/upload with real PDF file
Usage: python scripts/test_upload_e2e.py [base_url]
"""
import urllib.request
import urllib.error
import json
import os
import sys
import time

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
PDF_PATH = os.path.join(os.path.dirname(__file__), "..", "test.pdf")


def test_health():
    print("\n=== TEST 1: Health Check ===")
    try:
        with urllib.request.urlopen(f"{BASE_URL}/", timeout=8) as r:
            data = json.loads(r.read())
            print(f"  ✅ Status: {r.status}")
            print(f"  Service: {data.get('service')}")
            print(f"  Model:   {data.get('model')}")
    except Exception as e:
        print(f"  ❌ FAIL: {e}")


def test_rag_stats():
    print("\n=== TEST 2: RAG Stats ===")
    try:
        with urllib.request.urlopen(f"{BASE_URL}/api/rag/stats", timeout=8) as r:
            data = json.loads(r.read())
            print(f"  ✅ Status: {r.status}")
            print(f"  Total documents: {data.get('total_documents')}")
            print(f"  Total chunks:    {data.get('total_chunks')}")
            print(f"  Hybrid mode:     {data.get('hybrid_mode')}")
    except Exception as e:
        print(f"  ❌ FAIL: {e}")


def test_cockpit():
    print("\n=== TEST 3: Cockpit Dashboard ===")
    try:
        with urllib.request.urlopen(f"{BASE_URL}/cockpit", timeout=8) as r:
            content = r.read().decode("utf-8")
            print(f"  ✅ Status: {r.status}")
            print(f"  Content-Length: {len(content)} bytes")
            print(f"  Has viewport tag: {'viewport' in content}")
            print(f"  Has RAG stats:    {'rag' in content.lower() or 'stats' in content.lower()}")
            print(f"  Preview: {content[:200].strip()}")
    except Exception as e:
        print(f"  ❌ FAIL: {e}")


def test_upload():
    print("\n=== TEST 4: File Upload (/api/upload) ===")
    if not os.path.exists(PDF_PATH):
        print(f"  ⚠️  test.pdf not found at {PDF_PATH}")
        return

    boundary = b"----SR_CoreSync_Boundary_20261101"
    with open(PDF_PATH, "rb") as f:
        pdf_bytes = f.read()

    body = (
        b"--" + boundary + b"\r\n"
        b'Content-Disposition: form-data; name="files"; filename="test.pdf"\r\n'
        b"Content-Type: application/pdf\r\n\r\n"
        + pdf_bytes
        + b"\r\n--" + boundary + b"--\r\n"
    )

    req = urllib.request.Request(
        f"{BASE_URL}/api/upload",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary.decode()}"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            result = json.loads(r.read())
            print(f"  ✅ Status: {r.status}")
            print(f"  Response: {json.dumps(result, ensure_ascii=False, indent=4)}")
    except urllib.error.HTTPError as e:
        body_err = e.read().decode("utf-8", errors="replace")
        print(f"  ❌ HTTP {e.code}: {body_err}")
    except Exception as e:
        print(f"  ❌ FAIL: {e}")


def test_sessions():
    print("\n=== TEST 5: Sessions List ===")
    try:
        with urllib.request.urlopen(f"{BASE_URL}/api/sessions?limit=3", timeout=8) as r:
            data = json.loads(r.read())
            sessions = data.get("sessions", [])
            print(f"  ✅ Status: {r.status}")
            print(f"  Sessions found: {len(sessions)}")
            for s in sessions:
                print(f"    - {s.get('session_id')} | msgs: {s.get('message_count')}")
    except Exception as e:
        print(f"  ❌ FAIL: {e}")


def test_subagent_status():
    print("\n=== TEST 6: Subagent Status ===")
    try:
        with urllib.request.urlopen(f"{BASE_URL}/api/subagent/status", timeout=8) as r:
            data = json.loads(r.read())
            print(f"  ✅ Status: {r.status}")
            print(f"  Overall: {data.get('overall_status', data.get('overall'))}")
    except Exception as e:
        print(f"  ❌ FAIL: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("  S&R CoreSync — End-to-End API Test Suite")
    print(f"  Target: {BASE_URL}")
    print("=" * 60)

    test_health()
    test_rag_stats()
    test_cockpit()
    test_upload()
    test_sessions()
    test_subagent_status()

    print("\n" + "=" * 60)
    print("  ✅ All tests completed.")
    print("=" * 60)

