from modules.vector_store import load_job_descriptions, build_vector_store, search_job

# Step 1: Load job descriptions from JSON
jobs = load_job_descriptions("data/job_descriptions.json")
print(f"✅ Loaded {len(jobs)} job descriptions")

# Step 2: Build the FAISS vector store
print("⏳ Building vector store... (takes 30 seconds first time)")
index, descriptions, jobs = build_vector_store(jobs)
print("✅ Vector store built successfully!")

# Step 3: Test search with different queries
test_queries = [
    "Python developer with Django",
    "Machine learning and deep learning",
    "AI chatbot with LLMs"
]

print("\n--- Search Results ---")
for query in test_queries:
    result = search_job(query, index, jobs)
    print(f"\nQuery : {query}")
    print(f"Match : {result['role']}")
