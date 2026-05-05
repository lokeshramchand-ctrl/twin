from rag import load_index, rag_query

print("✅ Query system running (auto-reloads index)")

while True:
    q = input("\nAsk: ")

    # 🔥 Reload index EVERY time
    index, chunks = load_index()

    print(rag_query(q, index, chunks))