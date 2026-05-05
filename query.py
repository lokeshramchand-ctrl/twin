from rag import load_index, rag_query

index, chunks = load_index()

print("✅ Index loaded. Ready for queries.")

while True:
    q = input("\nAsk: ")
    print(rag_query(q, index, chunks))