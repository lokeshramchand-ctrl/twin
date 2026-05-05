from rag import load_documents, build_index, save_index

# IMPORTANT: Use V1 only
docs = load_documents("project/data/v1")

index, chunks = build_index(docs)

save_index(index, chunks)

print("✅ Index built and saved from V1 dataset.")