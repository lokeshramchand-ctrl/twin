import json
import time
from rag import load_index, rag_query

# =========================
# CONFIG
# =========================
QUERY_FILE = "queries.json"
RESULT_FILE = "run_1.json"

# =========================
# LOAD DATA
# =========================
with open(QUERY_FILE, "r") as f:
    queries = json.load(f)

# Load index (batch or event system)
index, chunks = load_index()

results = []

correct_count = 0
total = len(queries)

# =========================
# RUN EVALUATION
# =========================
for q in queries:
    question = q["question"]
    expected = q["v2"]   # change to v1 for baseline if needed

    start_time = time.time()

    answer = rag_query(question, index, chunks)

    end_time = time.time()
    latency = end_time - start_time

    # simple correctness check (case-insensitive match)
    is_correct = expected.lower() in answer.lower()

    if is_correct:
        correct_count += 1

    results.append({
        "question": question,
        "expected": expected,
        "answer": answer,
        "correct": is_correct,
        "latency": latency
    })

# =========================
# METRICS
# =========================
hallucination_rate = 1 - (correct_count / total)
avg_latency = sum(r["latency"] for r in results) / total

summary = {
    "total_queries": total,
    "correct": correct_count,
    "hallucination_rate": hallucination_rate,
    "avg_latency": avg_latency
}

# =========================
# SAVE RESULTS
# =========================
output = {
    "summary": summary,
    "details": results
}

with open(RESULT_FILE, "w") as f:
    json.dump(output, f, indent=2)

# =========================
# PRINT SUMMARY
# =========================
print("\n===== RESULTS =====")
print(f"Total Queries: {total}")
print(f"Correct: {correct_count}")
print(f"Hallucination Rate: {hallucination_rate:.2f}")
print(f"Avg Latency: {avg_latency:.3f} sec")