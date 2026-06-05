from modules.resume_parser import get_resume_text
from modules.vector_store import load_job_descriptions, build_vector_store, search_job
from modules.skill_gap import analyze_resume

# Step 1: Read your resume
print("📄 Reading resume...")
resume_text = get_resume_text("resume.pdf")

# Step 2: Load and build vector store
print("🔍 Loading job descriptions...")
jobs = load_job_descriptions("data/job_descriptions.json")
index, descriptions, jobs = build_vector_store(jobs)

# Step 3: Search for best matching job
job_role = "Python Developer"  # change this to test different roles
print(f"🎯 Searching best JD match for: {job_role}")
matched_job = search_job(job_role, index, jobs)
print(f"✅ Matched with: {matched_job['role']}")
# Step 4: Run AI analysis
print("🤖 Analyzing resume with AI... (takes 10-15 seconds)")
result = analyze_resume(resume_text, matched_job["role"], matched_job["description"])

# Step 5: Print the result
print("\n" + "="*60)
print("AI CAREER ANALYSIS RESULT")
print("="*60)
print(result)
print("="*60)