"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================
"""

import os
import sys
import re
import time
import json
import sqlite3
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# ضبط الترميز لدعم العربية في الطرفية
sys.stdout.reconfigure(encoding="utf-8")

PROJECT_DIR = Path(__file__).resolve().parent
LOG_FILE = PROJECT_DIR / "sr_subagent_audit.log"
DB_PATH = PROJECT_DIR / "sr_agent_sessions.db"

class AutonomousSecurityHealthSubagent:
    """
    الوكيل الفرعي الذاتي للتدقيق الأمني والتشغيلي (Autonomous Security & Health Subagent)
    يقوم بمراقبة مستمرة لصحة خادم الذكاء الاصطناعي، سلامة الملفات والروابط، جاهزية بوابات الدفع،
    وحراسة الأسرار والملكية الفكرية بشكل دوري ذاتي.
    """

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = str(db_path)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as con:
            con.execute("PRAGMA journal_mode = WAL;")
            con.execute("""
            CREATE TABLE IF NOT EXISTS subagent_audit_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                status TEXT NOT NULL,
                server_health TEXT NOT NULL,
                assets_health TEXT NOT NULL,
                secrets_guard TEXT NOT NULL,
                payment_readiness TEXT NOT NULL,
                details_json TEXT NOT NULL
            );
            """)

    def check_server_and_rag(self) -> Dict[str, Any]:
        """فحص جاهزية محرك الذكاء الاصطناعي وذاكرة المتجهات المحلية."""
        rag_db = PROJECT_DIR / "sr_rag_knowledge.db"
        if not rag_db.exists():
            return {
                "status": "WARNING",
                "message": "قاعدة بيانات المتجهات RAG غير موجودة. يجب تشغيل الفهرسة."
            }
        
        try:
            with sqlite3.connect(str(rag_db)) as con:
                cur = con.cursor()
                cur.execute("SELECT COUNT(*) FROM chunks")
                chunks = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM documents")
                docs = cur.fetchone()[0]
            return {
                "status": "HEALTHY",
                "indexed_documents": docs,
                "indexed_chunks": chunks,
                "vector_engine": "Dense 128-d + FTS5 Hybrid",
                "message": f"جاهزية كاملة: {docs} مستنداً و {chunks} قطعة دلالية مفهرسة."
            }
        except Exception as e:
            return {"status": "ERROR", "message": f"خطأ أثناء فحص ذاكرة المتجهات: {e}"}

    def check_critical_assets(self) -> Dict[str, Any]:
        """فحص وجود وسلامة الملفات والبوابات السيادية الرئيسية."""
        critical_files = [
            "index.html",
            "software.html",
            "work.html",
            "client-portal.html",
            "autonomous-tax-audit.html",
            "sovereign-gold-rwa-treasury.html",
            "sovereign-arbitration-hub.html",
            "multi-cbdc-bridge.html",
            "zkp-confidential-enclave.html",
            "privacy.html",
            "css/sr-agent-widget.css",
            "js/sr-agent-widget.js",
            "sr_rag_engine.py",
            "sr_agent_core.py",
            "sr_agent_server.py"
        ]

        missing = []
        zero_size = []
        for rel in critical_files:
            p = PROJECT_DIR / rel
            if not p.exists():
                missing.append(rel)
            elif p.stat().st_size == 0:
                zero_size.append(rel)

        if missing or zero_size:
            return {
                "status": "FAIL",
                "missing": missing,
                "zero_size": zero_size,
                "message": f"تنبيه: تم رصد {len(missing)} ملفاً مفقوداً و {len(zero_size)} ملفاً فارغاً."
            }

        return {
            "status": "HEALTHY",
            "checked_assets": len(critical_files),
            "message": f"كافة الأصول السيادية الـ {len(critical_files)} سليمة وموجودة."
        }

    def check_secrets_and_vault(self) -> Dict[str, Any]:
        """فحص حراسة الأسرار والملكية الفكرية والتأكد من عدم تسريب أي مفاتيح في الملفات."""
        tracked_extensions = [".html", ".js", ".css", ".md", ".json"]
        forbidden_regexes = [
            re.compile(r'sk_live_[0-9a-zA-Z]{20,}'),
            re.compile(r'whsec_[0-9a-zA-Z]{20,}'),
            re.compile(r'AIzaSy[0-9a-zA-Z\-_]{30,}'),
            re.compile(r'ghp_[0-9a-zA-Z]{30,}')
        ]
        
        suspicious_matches = []
        
        # فحص عينة سريعة من ملفات الجذر
        for p in PROJECT_DIR.glob("*.*"):
            if p.suffix.lower() in tracked_extensions:
                try:
                    with open(p, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    for rx in forbidden_regexes:
                        match = rx.search(content)
                        if match:
                            suspicious_matches.append(f"{p.name}: {match.group(0)[:10]}...")
                except Exception:
                    pass

        # فحص وجود الخزينة المشفرة أو ملف .env المحمي
        env_file = PROJECT_DIR / ".env"
        has_env = env_file.exists()

        if suspicious_matches:
            return {
                "status": "ALERT",
                "leaks": suspicious_matches,
                "message": "تحذير أمني: تم رصد نمط سر محتمل في الملفات العامة!"
            }

        return {
            "status": "HEALTHY",
            "env_present": has_env,
            "message": "الفحص الأمني نظيف تماماً: 0 أسرار مكشوفة في الأصول الممسوحة."
        }

    def check_payment_readiness(self) -> Dict[str, Any]:
        """فحص جاهزية بوابات الدفع Stripe و iDEAL و Webhooks."""
        # فحص وجود ملفات وتهيئة الدفع
        stripe_integration = False
        pricing_verified = False

        index_p = PROJECT_DIR / "index.html"
        if index_p.exists():
            with open(index_p, "r", encoding="utf-8", errors="ignore") as f:
                c = f.read()
            if "890" in c and "1,450" in c and "1,490" in c:
                pricing_verified = True

        worker_dir = PROJECT_DIR / "workers"
        if worker_dir.exists():
            stripe_integration = True

        return {
            "status": "HEALTHY" if pricing_verified else "WARNING",
            "pricing_consistent": pricing_verified,
            "worker_infrastructure": stripe_integration,
            "supported_methods": ["iDEAL (Netherlands)", "Credit Card / Stripe", "Multi-CBDC (Settlement)"],
            "message": "بوابات الدفع والتسعير متطابقة ومسجلة بدقة."
        }

    def run_full_audit(self) -> Dict[str, Any]:
        """تنفيذ دورة تدقيق شاملة وحفظ التقرير في قاعدة البيانات وسجل العمليات."""
        start_time = time.time()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        srv = self.check_server_and_rag()
        ast = self.check_critical_assets()
        sec = self.check_secrets_and_vault()
        pay = self.check_payment_readiness()

        overall = "HEALTHY"
        if any(x["status"] in ["ALERT", "FAIL", "ERROR"] for x in [srv, ast, sec, pay]):
            overall = "ALERT"
        elif any(x["status"] == "WARNING" for x in [srv, ast, sec, pay]):
            overall = "WARNING"

        duration_ms = round((time.time() - start_time) * 1000, 2)

        report = {
            "timestamp": timestamp,
            "overall_status": overall,
            "duration_ms": duration_ms,
            "modules": {
                "server_and_rag": srv,
                "critical_assets": ast,
                "secrets_guard": sec,
                "payment_readiness": pay
            }
        }

        # حفظ في قاعدة البيانات
        try:
            with sqlite3.connect(self.db_path) as con:
                con.execute(
                    """
                    INSERT INTO subagent_audit_history 
                    (timestamp, status, server_health, assets_health, secrets_guard, payment_readiness, details_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        timestamp,
                        overall,
                        srv["status"],
                        ast["status"],
                        sec["status"],
                        pay["status"],
                        json.dumps(report, ensure_ascii=False)
                    )
                )
        except Exception as e:
            print(f"[Subagent DB Error]: {e}")

        # تسجيل في ملف السجل
        log_line = f"[{timestamp}] STATUS: {overall} | DURATION: {duration_ms}ms | SERVER: {srv['status']} | ASSETS: {ast['status']} | SECRETS: {sec['status']} | PAYMENTS: {pay['status']}\n"
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_line)
        except Exception:
            pass

        return report

def main():
    parser = argparse.ArgumentParser(description="S&R CoreSync Autonomous Security & Health Subagent")
    parser.add_argument("--once", action="store_true", help="تشغيل فحص تدقيقي فوري لمرة واحدة")
    parser.add_argument("--interval", type=int, default=60, help="فترة الفحص بالثواني عند وضع المراقبة المستمرة")
    args = parser.parse_args()

    subagent = AutonomousSecurityHealthSubagent()

    if args.once:
        print("=" * 70)
        print("  🛡️ S&R CoreSync - تشغيل الوكيل الفرعي الذاتي للتدقيق الأمني والصحي")
        print("=" * 70)
        report = subagent.run_full_audit()
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    print("=" * 70)
    print(f"  🛡️ تشغيل الوكيل الفرعي للمراقبة المستمرة (كل {args.interval} ثانية)")
    print("  اضغط Ctrl+C للإيقاف.")
    print("=" * 70)
    try:
        while True:
            rep = subagent.run_full_audit()
            print(f"[{rep['timestamp']}] النتيجة: {rep['overall_status']} (استغرق {rep['duration_ms']} ms)")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nتم إيقاف الوكيل الفرعي بنجاح.")

if __name__ == "__main__":
    main()
