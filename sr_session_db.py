import os
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "sr_agent_sessions.db")

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    """تهيئة جداول الجلسات والرسائل في قاعدة بيانات SQLite المحلية"""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                title TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL, -- 'user' أو 'assistant' أو 'system'
                content TEXT NOT NULL,
                source TEXT DEFAULT 'google_antigravity_agent',
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
            );
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id);
        """)
        conn.commit()

def ensure_session(session_id: str, title: Optional[str] = None) -> str:
    """التأكد من وجود الجلسة أو إنشائها"""
    init_db()
    clean_id = session_id.strip() if session_id else "default"
    now_iso = datetime.now().isoformat()
    with get_connection() as conn:
        cursor = conn.execute("SELECT session_id FROM sessions WHERE session_id = ?", (clean_id,))
        if not cursor.fetchone():
            default_title = title or f"جلسة {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            conn.execute(
                "INSERT INTO sessions (session_id, title, created_at, last_active, metadata) VALUES (?, ?, ?, ?, ?)",
                (clean_id, default_title, now_iso, now_iso, json.dumps({}))
            )
        else:
            conn.execute("UPDATE sessions SET last_active = ? WHERE session_id = ?", (now_iso, clean_id))
        conn.commit()
    return clean_id

def add_message(session_id: str, role: str, content: str, source: str = "google_antigravity_agent"):
    """إضافة رسالة إلى سجل الجلسة وتحديث وقت النشاط الأخير"""
    clean_id = ensure_session(session_id)
    now_iso = datetime.now().isoformat()
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO messages (session_id, role, content, source, timestamp) VALUES (?, ?, ?, ?, ?)",
            (clean_id, role, content, source, now_iso)
        )
        conn.execute("UPDATE sessions SET last_active = ? WHERE session_id = ?", (now_iso, clean_id))
        conn.commit()

def get_history(session_id: str, limit: int = 30) -> List[Dict[str, Any]]:
    """استرجاع تاريخ الرسائل لجلسة محددة مرتبة زمنياً"""
    init_db()
    clean_id = session_id.strip() if session_id else "default"
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT id, role, content, source, timestamp FROM messages WHERE session_id = ? ORDER BY id ASC LIMIT ?",
            (clean_id, limit)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def get_formatted_context(session_id: str, max_turns: int = 5) -> str:
    """توليد ملخص نصي مرتب لآخر أدوار الحوار لإضافتها كسياق محادثة للوكيل"""
    history = get_history(session_id, limit=max_turns * 2)
    if not history:
        return ""
    lines = ["--- سياق المحادثة السابقة من الجلسة ---"]
    for msg in history:
        role_label = "المستخدم" if msg["role"] == "user" else "المستشار"
        lines.append(f"{role_label}: {msg['content']}")
    lines.append("--- نهاية سياق المحادثة السابقة ---")
    return "\n".join(lines)

def list_all_sessions(limit: int = 20) -> List[Dict[str, Any]]:
    """استعراض الجلسات النشطة مع إحصائيات الرسائل"""
    init_db()
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT s.session_id, s.title, s.created_at, s.last_active, COUNT(m.id) as message_count
            FROM sessions s
            LEFT JOIN messages m ON s.session_id = m.session_id
            GROUP BY s.session_id
            ORDER BY s.last_active DESC
            LIMIT ?;
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]

def clear_session(session_id: str):
    """مسح محتويات جلسة معينة"""
    init_db()
    clean_id = session_id.strip() if session_id else "default"
    with get_connection() as conn:
        conn.execute("DELETE FROM messages WHERE session_id = ?", (clean_id,))
        conn.execute("DELETE FROM sessions WHERE session_id = ?", (clean_id,))
        conn.commit()

# التهيئة المبدئية عند استيراد الملف
init_db()

