from ingest.scraper import load_all_docs
from ingest.pipeline import build_vector_store

print("=== Phase 2: RAG Ingestion ===\n")

# 1. Scrape docs
docs = load_all_docs()
print(f"\nLoaded {len(docs)} documents\n")

# 2. Chunk, embed, store
vector_store = build_vector_store(docs)

# 3. Quick sanity check — run a test query
print("\n--- Test query ---")
results = vector_store.similarity_search(
    "How do I detect ANR in Android?",
    k=3  # Return top 3 matching chunks
)

for i, chunk in enumerate(results):
    print(f"\nResult {i+1} [{chunk.metadata['platform']} - {chunk.metadata['topic']}]")
    print(chunk.page_content[:300])  # Print first 300 chars of each chunk
    print("...")
