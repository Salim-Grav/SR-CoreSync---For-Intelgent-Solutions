"""
==============================================================================
S&R CoreSync - مولّد مفاتيح API لمصادقة الخادم السيادي (Security Remediation P0-1)
==============================================================================
الاستخدام:
    python scripts/generate_auth_keys.py                     # مفتاح admin واحد
    python scripts/generate_auth_keys.py --client site-ww    # إضافة مفتاح client

يقوم بـ:
  1. توليد مفاتيح عشوائية آمنة (secrets.token_urlsafe).
  2. تخزين البصمة SHA-256 فقط في auth_keys.json (الملف النصي الصريح يُطبع مرة واحدة).
  3. ضبط صلاحيات الملف على 600.

تنبيه: auth_keys.json مُدرج في .gitignore ولا يجوز إيداعه أبداً.
"""

import argparse
import json
import os
import secrets
import stat
import sys
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
AUTH_FILE = Path(os.getenv("CORESYNC_AUTH_FILE", str(PROJECT_DIR / "auth_keys.json")))


def load_existing() -> dict:
    if AUTH_FILE.is_file():
        try:
            return json.loads(AUTH_FILE.read_text(encoding="utf-8"))
        except Exception:
            print(f"⚠️ الملف {AUTH_FILE} تالف؛ سيُستبدل بملف جديد.", file=sys.stderr)
    return {"keys": []}


def secure_write(payload: dict) -> None:
    AUTH_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        AUTH_FILE.chmod(stat.S_IRUSR | stat.S_IWUSR)  # 600
    except OSError:
        pass


def main() -> int:
    parser = argparse.ArgumentParser(description="توليد مفاتيح API للخادم السيادي")
    parser.add_argument("--name", default=None, help="اسم المفتاح (مثال: ops-console)")
    parser.add_argument("--role", choices=["admin", "client"], default=None,
                        help="الدور: admin (كل الصلاحيات) أو client (قراءة ومحادثة)")
    parser.add_argument("--client", metavar="NAME", help="اختصار: إضافة مفتاح client بهذا الاسم")
    args = parser.parse_args()

    name = args.client or args.name or "ops-console"
    role = "client" if args.client else (args.role or "admin")

    plain_key = "srk_" + secrets.token_urlsafe(32)
    digest = __import__("hashlib").sha256(plain_key.encode("utf-8")).hexdigest()

    data = load_existing()
    data["keys"] = [k for k in data.get("keys", []) if k.get("name") != name]
    data["keys"].append({
        "name": name,
        "key_sha256": digest,
        "role": role,
        "created_at": datetime.now().isoformat(),
    })
    secure_write(data)

    print("=" * 64)
    print(f"✅ تم توليد المفتاح وحفظ بصمته في: {AUTH_FILE}")
    print(f"   الاسم : {name}")
    print(f"   الدور : {role}")
    print("-" * 64)
    print("   المفتاح النصي (يُعرض مرة واحدة فقط، خزّنه في مدير أسرار):")
    print(f"   {plain_key}")
    print("=" * 64)
    print("   الاستخدام:  curl -H 'X-API-Key: <المفتاح>' http://127.0.0.1:8000/api/rag/stats")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
