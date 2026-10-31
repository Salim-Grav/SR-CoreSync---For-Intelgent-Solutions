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
import math
import struct
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

# ضبط الترميز لدعم العربية في الطرفية
sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parent
DB_PATH = PROJECT_ROOT / "sr_rag_knowledge.db"
VECTOR_DIM = 128

# ==============================================================================
# 1. تطبيع النصوص واستخراج المتجهات الكثيفة محلياً (Dense Vector Embedder)
# ==============================================================================

def normalize_text(text: str) -> str:
    """تطبيع النصوص العربية والإنجليزية لإزالة التشكيل وتوحيد الحروف."""
    if not text:
        return ""
    # تطبيع الحروف العربية
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)  # إزالة التشكيل
    text = re.sub(r'[إأآا]', 'ا', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'ى', 'ي', text)
    # تنظيف المسافات والرموز الزائدة
    text = re.sub(r'[\r\n\t]+', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip().lower()

def compute_dense_vector(text: str, dim: int = VECTOR_DIM) -> List[float]:
    """
    توليد متجهة كثيفة (Dense Vector) بطول 128 بُعداً معيارياً (L2 Normalized)
    مستندة إلى مزيج من الكلمات والـ Character 3-grams والـ 4-grams
    لتمثيل المعنى السياقي والمورفولوجي العربي واللاتيني بكفاءة فائقة وسرعة دون اعتماديات خارجية.
    """
    clean = normalize_text(text)
    if not clean:
        return [0.0] * dim

    vec = [0.0] * dim
    words = clean.split()

    # 1. تضمين الكلمات
    for w in words:
        if len(w) < 2:
            continue
        h = int(hashlib.md5(w.encode('utf-8')).hexdigest(), 16)
        idx = h % dim
        sign = 1.0 if ((h >> 8) & 1) == 0 else -1.0
        vec[idx] += 1.5 * sign

    # 2. تضمين الـ n-grams للتشابه الصرفي (Subword morphology)
    for i in range(len(clean) - 2):
        trigram = clean[i:i+3]
        h = int(hashlib.md5(trigram.encode('utf-8')).hexdigest(), 16)
        idx = h % dim
        sign = 1.0 if ((h >> 8) & 1) == 0 else -1.0
        vec[idx] += 0.8 * sign

    for i in range(len(clean) - 3):
        fourgram = clean[i:i+4]
        h = int(hashlib.md5(fourgram.encode('utf-8')).hexdigest(), 16)
        idx = h % dim
        sign = 1.0 if ((h >> 8) & 1) == 0 else -1.0
        vec[idx] += 0.6 * sign

    # تطبيع المتجهة بالمعيار الإقليدي L2 Norm
    norm = math.sqrt(sum(x * x for x in vec))
    if norm > 1e-9:
        vec = [x / norm for x in vec]
    else:
        vec = [0.0] * dim

    return vec

def vector_to_blob(vec: List[float]) -> bytes:
    """تحويل المتجهة إلى تمثيل ثنائي مدمج BLOB."""
    return struct.pack(f"{len(vec)}f", *vec)

def blob_to_vector(blob: bytes) -> List[float]:
    """استرجاع المتجهة من الـ BLOB."""
    count = len(blob) // 4
    return list(struct.unpack(f"{count}f", blob))

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """حساب التشابه الجيبي (Cosine Similarity) بين متجهتين معياريتين."""
    if len(v1) != len(v2) or not v1 or not v2:
        return 0.0
    return sum(a * b for a, b in zip(v1, v2))

# ==============================================================================
# 2. مستودع المعرفة الهجين (SQLite Hybrid Store + FTS5)
# ==============================================================================

class SovereignRAGDatabase:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = str(db_path)
        self._init_schema()

    def get_connection(self) -> sqlite3.Connection:
        con = sqlite3.connect(self.db_path)
        con.execute("PRAGMA journal_mode = WAL;")
        con.execute("PRAGMA synchronous = NORMAL;")
        return con

    def _init_schema(self):
        with self.get_connection() as con:
            con.executescript("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT UNIQUE NOT NULL,
                title TEXT,
                category TEXT,
                file_hash TEXT,
                updated_at TEXT
            );

            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id INTEGER NOT NULL,
                chunk_index INTEGER NOT NULL,
                title TEXT,
                content TEXT NOT NULL,
                vector_blob BLOB NOT NULL,
                FOREIGN KEY (doc_id) REFERENCES documents(id) ON DELETE CASCADE
            );

            CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
                title,
                content,
                content='chunks',
                content_rowid='id'
            );

            -- Triggers to sync FTS5 with chunks table
            CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
                INSERT INTO chunks_fts(rowid, title, content) VALUES (new.id, new.title, new.content);
            END;

            CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
                INSERT INTO chunks_fts(chunks_fts, rowid, title, content) VALUES('delete', old.id, old.title, old.content);
            END;

            CREATE TRIGGER IF NOT EXISTS chunks_au AFTER UPDATE ON chunks BEGIN
                INSERT INTO chunks_fts(chunks_fts, rowid, title, content) VALUES('delete', old.id, old.title, old.content);
                INSERT INTO chunks_fts(rowid, title, content) VALUES (new.id, new.title, new.content);
            END;
            """)

    def get_document_by_path(self, path: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT id, path, title, category, file_hash, updated_at FROM documents WHERE path = ?", (path,))
            row = cur.fetchone()
            if row:
                return {
                    "id": row[0], "path": row[1], "title": row[2],
                    "category": row[3], "file_hash": row[4], "updated_at": row[5]
                }
            return None

    def upsert_document(self, path: str, title: str, category: str, file_hash: str, chunks: List[Dict[str, Any]]):
        with self.get_connection() as con:
            cur = con.cursor()
            now = datetime.now().isoformat()
            
            # Check existing document
            cur.execute("SELECT id FROM documents WHERE path = ?", (path,))
            existing = cur.fetchone()
            
            if existing:
                doc_id = existing[0]
                cur.execute(
                    "UPDATE documents SET title = ?, category = ?, file_hash = ?, updated_at = ? WHERE id = ?",
                    (title, category, file_hash, now, doc_id)
                )
                # Delete old chunks
                cur.execute("DELETE FROM chunks WHERE doc_id = ?", (doc_id,))
            else:
                cur.execute(
                    "INSERT INTO documents (path, title, category, file_hash, updated_at) VALUES (?, ?, ?, ?, ?)",
                    (path, title, category, file_hash, now)
                )
                doc_id = cur.lastrowid

            # Insert new chunks with vector BLOBs
            for idx, ch in enumerate(chunks):
                vec = compute_dense_vector(f"{ch.get('title', '')} {ch['content']}")
                blob = vector_to_blob(vec)
                cur.execute(
                    "INSERT INTO chunks (doc_id, chunk_index, title, content, vector_blob) VALUES (?, ?, ?, ?, ?)",
                    (doc_id, idx, ch.get("title", title), ch["content"], blob)
                )

    def hybrid_search(self, query: str, top_k: int = 4, alpha: float = 0.55) -> List[Dict[str, Any]]:
        """
        البحث الهجين (Hybrid Search): دمج البحث الدلالي بالمتجهات الكثيفة مع بحث الكلمات المفتاحية FTS5
        alpha: وزن المتجهات الكثيفة (0.55 Dense + 0.45 BM25)
        """
        clean_q = normalize_text(query)
        if not clean_q:
            return []

        query_vec = compute_dense_vector(query)

        with self.get_connection() as con:
            cur = con.cursor()

            # 1. بحث FTS5 (BM25)
            # استخراج الكلمات لتكوين استعلام FTS5 آمن
            tokens = [re.sub(r'[^\w\s]', '', t) for t in clean_q.split() if len(t) >= 2]
            fts_scores: Dict[int, float] = {}
            
            if tokens:
                fts_query = " OR ".join(f'"{t}"*' for t in tokens)
                try:
                    cur.execute("""
                        SELECT rowid, rank
                        FROM chunks_fts
                        WHERE chunks_fts MATCH ?
                        ORDER BY rank
                        LIMIT 30
                    """, (fts_query,))
                    rows = cur.fetchall()
                    if rows:
                        best_rank = abs(rows[0][1]) if rows[0][1] != 0 else 1.0
                        for r_id, rank in rows:
                            # Normalize BM25 rank score between 0.0 and 1.0
                            norm_score = max(0.0, 1.0 - (abs(rank) / (best_rank * 2.5)))
                            fts_scores[r_id] = norm_score
                except Exception:
                    pass

            # 2. بحث المتجهات الكثيفة (Dense Vector Cosine Similarity)
            cur.execute("""
                SELECT c.id, c.doc_id, c.title, c.content, c.vector_blob, d.path, d.category
                FROM chunks c
                JOIN documents d ON c.doc_id = d.id
            """)
            all_chunks = cur.fetchall()

            scored_results = []
            for c_id, doc_id, ch_title, ch_content, vec_blob, doc_path, category in all_chunks:
                ch_vec = blob_to_vector(vec_blob)
                dense_sim = cosine_similarity(query_vec, ch_vec)
                bm25_sim = fts_scores.get(c_id, 0.0)

                # دمج الدرجتين بالوزن التراكمي
                combined_score = (alpha * max(0.0, dense_sim)) + ((1.0 - alpha) * bm25_sim)

                # تعزيز إذا تطابقت كلمات العنوان
                if any(t in normalize_text(ch_title) for t in tokens):
                    combined_score += 0.15

                scored_results.append({
                    "id": c_id,
                    "doc_id": doc_id,
                    "title": ch_title,
                    "content": ch_content,
                    "path": doc_path,
                    "category": category,
                    "dense_score": round(dense_sim, 4),
                    "bm25_score": round(bm25_sim, 4),
                    "score": round(combined_score, 4)
                })

            # ترتيب النتائج بالأعلى درجة
            scored_results.sort(key=lambda x: x["score"], reverse=True)
            return scored_results[:top_k]

    def get_stats(self) -> Dict[str, Any]:
        with self.get_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM documents")
            doc_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM chunks")
            chunk_count = cur.fetchone()[0]
            cur.execute("SELECT path, title, updated_at FROM documents ORDER BY updated_at DESC LIMIT 5")
            recent = [{"path": r[0], "title": r[1], "updated_at": r[2]} for r in cur.fetchall()]
            return {
                "total_documents": doc_count,
                "total_chunks": chunk_count,
                "vector_dimension": VECTOR_DIM,
                "hybrid_mode": "Dense Vector (128-d) + SQLite FTS5 (BM25)",
                "recent_documents": recent
            }

# ==============================================================================
# 3. مفكك ومحلل صفحات HTML والملفات الذكي (Sovereign Document Crawler)
# ==============================================================================

def clean_html_to_chunks(html_content: str, source_path: str) -> Tuple[str, List[Dict[str, Any]]]:
    """استخراج العنوان وفقرات المحتوى النظيفة من ملف HTML وتقسيمها إلى قطع دلالية."""
    # استخراج عنوان الصفحة
    title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
    page_title = title_match.group(1).strip() if title_match else Path(source_path).stem
    page_title = re.sub(r'\|.*', '', page_title).strip()

    # إزالة أكواد السكربت والأنماط
    clean = re.sub(r'<script.*?</script>', ' ', html_content, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<style.*?</style>', ' ', clean, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<svg.*?</svg>', ' ', clean, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<!--.*?-->', ' ', clean, flags=re.DOTALL)

    # تفكيك المقاطع حسب العناوين h1, h2, h3, section
    sections = re.split(r'(<h[1-4][^>]*>.*?</h[1-4]>)', clean, flags=re.IGNORECASE)
    
    chunks = []
    current_title = page_title
    current_text = []

    for part in sections:
        header_match = re.search(r'<h[1-4][^>]*>(.*?)</h[1-4]>', part, re.IGNORECASE | re.DOTALL)
        if header_match:
            # إذا كان هناك نص متراكم سابقاً، نحفظه كقطعة
            if current_text:
                block = " ".join(current_text).strip()
                if len(block) > 60:
                    chunks.append({"title": current_title, "content": block})
                current_text = []
            header_text = re.sub(r'<[^>]+>', ' ', header_match.group(1))
            current_title = f"{page_title} - {header_text.strip()}"
        else:
            # تنظيف وسوم HTML واستخراج النص الخام
            raw_text = re.sub(r'<[^>]+>', ' ', part)
            raw_text = re.sub(r'\s+', ' ', raw_text).strip()
            if raw_text:
                current_text.append(raw_text)

    if current_text:
        block = " ".join(current_text).strip()
        if len(block) > 60:
            chunks.append({"title": current_title, "content": block})

    # تقسيم القطع الكبيرة جداً (> 600 كلمة)
    final_chunks = []
    for ch in chunks:
        words = ch["content"].split()
        if len(words) > 350:
            for i in range(0, len(words), 250):
                sub_block = " ".join(words[i:i+300])
                final_chunks.append({
                    "title": ch["title"],
                    "content": sub_block
                })
        else:
            final_chunks.append(ch)

    return page_title, final_chunks

def parse_markdown_to_chunks(md_content: str, source_path: str) -> Tuple[str, List[Dict[str, Any]]]:
    """استخراج العنوان والقطع الدلالية من ملفات Markdown."""
    lines = md_content.splitlines()
    doc_title = Path(source_path).name
    chunks = []
    current_heading = doc_title
    current_lines = []

    for line in lines:
        if line.startswith("#"):
            if current_lines:
                block = "\n".join(current_lines).strip()
                if len(block) > 40:
                    chunks.append({"title": current_heading, "content": block})
                current_lines = []
            current_heading = line.lstrip("#").strip()
        else:
            current_lines.append(line)

    if current_lines:
        block = "\n".join(current_lines).strip()
        if len(block) > 40:
            chunks.append({"title": current_heading, "content": block})

    return doc_title, chunks

def build_or_update_knowledge_index(root_dir: Path = PROJECT_ROOT) -> Dict[str, Any]:
    """
    مسح وفهرسة كافة صفحات وبوابات المشروع وملفات المعرفة السيادية وتوليد المتجهات الهجينة.
    """
    db = SovereignRAGDatabase()
    
    # قائمة الملفات المستهدفة
    target_files = []
    
    # 1. صفحات HTML في الجذر
    for p in root_dir.glob("*.html"):
        # استثناء الملفات المؤقتة غير الأساسية إن وجدت
        if not p.name.startswith("temp_"):
            target_files.append((p, "web_portal"))

    # 2. مقالات المدونة ورؤى المنظومة
    insights_dir = root_dir / "insights"
    if insights_dir.exists():
        for p in insights_dir.glob("*.html"):
            target_files.append((p, "blog_insight"))

    # 3. الوثائق والمستندات الأساسية
    docs = ["README.md", "GEMINI.md", "task.md"]
    for d in docs:
        p = root_dir / d
        if p.exists():
            target_files.append((p, "documentation"))

    indexed_count = 0
    skipped_count = 0
    total_chunks = 0

    for file_path, category in target_files:
        try:
            rel_path = str(file_path.relative_to(root_dir)).replace("\\", "/")
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()

            file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
            existing = db.get_document_by_path(rel_path)

            # تجنب إعادة الفهرسة إذا لم يتغير الملف
            if existing and existing.get("file_hash") == file_hash:
                skipped_count += 1
                continue

            if file_path.suffix.lower() == ".html":
                title, chunks = clean_html_to_chunks(content, rel_path)
            else:
                title, chunks = parse_markdown_to_chunks(content, rel_path)

            if chunks:
                db.upsert_document(
                    path=rel_path,
                    title=title,
                    category=category,
                    file_hash=file_hash,
                    chunks=chunks
                )
                indexed_count += 1
                total_chunks += len(chunks)

        except Exception as e:
            print(f"[RAG Indexer] Error processing {file_path.name}: {e}")

    stats = db.get_stats()
    stats["newly_indexed_docs"] = indexed_count
    stats["skipped_unchanged_docs"] = skipped_count
    return stats

# ==============================================================================
# 4. نقطة استعلام موحدة لمساعد الذكاء الاصطناعي (Agent RAG Tool)
# ==============================================================================

def query_rag_knowledge(query: str, top_k: int = 4) -> str:
    """
    استعلام فوري عن معلومات موثقة من صفحات وخدمات ووثائق المشروع عبر RAG الهجين.
    """
    db = SovereignRAGDatabase()
    results = db.hybrid_search(query, top_k=top_k)
    if not results:
        return "لم يتم العثور على مقاطع مطابقة تماماً في ذاكرة المتجهات المحلية للمشروع."

    output = [f"=== نتائج استرجاع المعرفة السيادية (RAG Context) للاستفسار: '{query}' ==="]
    for i, r in enumerate(results, 1):
        output.append(
            f"\n[{i}] العنوان: {r['title']} | المصدر: {r['path']} (درجة التطابق: {r['score']})\n"
            f"المحتوى:\n{r['content'][:400]}..."
        )
    return "\n".join(output)

if __name__ == "__main__":
    print("=" * 70)
    print("S&R CoreSync - بناء وفهرسة ذاكرة المتجهات المحلية (Local Vector DB / RAG)")
    print("=" * 70)
    stats = build_or_update_knowledge_index()
    print("إحصائيات الفهرسة:", stats)
    print("\n--- تجربة استعلام دلالي (Semantic Query Test) ---")
    test_res = query_rag_knowledge("ما هي تفاصيل خدمة التحكيم التجاري الدولي؟", top_k=2)
    print(test_res)
