"""
Judicial Document RAG Upload & Search Verification Test
=======================================================
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from sr_rag_engine import index_custom_document, query_rag_knowledge, SovereignRAGDatabase


def main():
    claim_path = os.path.join(os.path.dirname(__file__), "..", "uploads", "sample_arbitration_claim_arb0418.txt")
    with open(claim_path, "r", encoding="utf-8") as f:
        doc_text = f.read()

    print("📄 1. Indexing judicial brief into Sovereign RAG Engine...")
    result = index_custom_document(
        title="مذكرة دعوى تحكيم تجاري ARB-2026-0418",
        text_content=doc_text,
        source_identifier="uploads/sample_arbitration_claim_arb0418.txt",
        category="legal_arbitration_claim",
    )
    print(f"  ✅ Result: {result}")

    print("\n🔍 2. Performing hybrid RAG retrieval for Rotterdam & ARB-2026-0418...")
    rag_context = query_rag_knowledge("Rotterdam Logistics ARB-2026-0418 EVD-2026-901", top_k=3)
    print(f"  ✅ RAG Context Length: {len(rag_context)} chars")
    print(f"  Snippet Preview:\n{rag_context[:350]}...")

    db = SovereignRAGDatabase()
    raw_matches = db.hybrid_search("Rotterdam Logistics ARB-2026-0418 EVD-2026-901", top_k=3)
    print(f"\n  ✅ Raw Search Matches retrieved: {len(raw_matches)}")
    for i, m in enumerate(raw_matches):
        print(f"  [{i+1}] Title: {m.get('title')} | Source: {m.get('source')} | Score: {m.get('score', 0):.3f}")

    print("\n📊 3. Checking RAG Database Stats...")
    db = SovereignRAGDatabase()
    stats = db.get_stats()
    print(f"  ✅ Total documents in RAG: {stats.get('total_documents')}")
    print(f"  ✅ Total chunks in RAG:    {stats.get('total_chunks')}")


if __name__ == "__main__":
    main()
