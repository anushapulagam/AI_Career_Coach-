import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def calculate_ats_score(resume_text, job_description):
    # Extract keywords from JD
    jd_words = set(re.findall(r'\b[a-zA-Z][a-zA-Z+#.]{2,}\b', job_description.lower()))
    resume_words = set(re.findall(r'\b[a-zA-Z][a-zA-Z+#.]{2,}\b', resume_text.lower()))

    # Common tech keywords to check specifically
    tech_keywords = [
        "python", "java", "sql", "django", "flask", "fastapi",
        "machine learning", "deep learning", "tensorflow", "pytorch",
        "docker", "kubernetes", "aws", "azure", "git", "github",
        "rest", "api", "html", "css", "javascript", "react", "nodejs",
        "pandas", "numpy", "scikit", "nlp", "llm", "langchain",
        "faiss", "gradio", "streamlit", "linux", "agile", "scrum",
        "mongodb", "mysql", "postgresql", "redis", "spark", "hadoop",
        "transformers", "huggingface", "openai", "groq", "rag"
    ]

    found_keywords = []
    missing_keywords = []

    for kw in tech_keywords:
        if kw in job_description.lower():
            if kw in resume_text.lower():
                found_keywords.append(kw)
            else:
                missing_keywords.append(kw)

    # Calculate base score
    jd_keywords_in_resume = jd_words.intersection(resume_words)
    overlap_ratio = len(jd_keywords_in_resume) / max(len(jd_words), 1)
    base_score = min(int(overlap_ratio * 100) + 30, 95)

    return base_score, found_keywords, missing_keywords

def analyze_resume(resume_text, job_role, job_description):

    # Calculate ATS score locally
    ats_score, found_kw, missing_kw = calculate_ats_score(resume_text, job_description)

    found_str = ", ".join(found_kw) if found_kw else "None detected"
    missing_str = ", ".join(missing_kw) if missing_kw else "None — great match!"

    prompt = f"""You are a senior HR professional and career coach with 15 years of experience.
Carefully analyze the resume below against the job description.

CANDIDATE RESUME:
{resume_text}

TARGET JOB ROLE: {job_role}

JOB DESCRIPTION:
{job_description}

ATS KEYWORD ANALYSIS (already calculated):
- ATS Score: {ats_score}/100
- Keywords found in resume: {found_str}
- Keywords missing from resume: {missing_str}

Give your response in EXACTLY this format:

---

## 🎯 ATS COMPATIBILITY SCORE

**Score: {ats_score}/100**

{"🟢 Strong Match" if ats_score >= 70 else "🟡 Average Match" if ats_score >= 50 else "🔴 Needs Improvement"}

**Keywords found in your resume:** {found_str}

**Important keywords missing:** {missing_str}

**Why this score:** [Write 2-3 specific reasons based on the actual resume and job description]

---

## ✅ MATCHING SKILLS

[List each matching skill starting with ✅]
✅ Skill — brief reason why it matches the JD

---

## ❌ MISSING SKILLS

[List each missing skill starting with ❌]
❌ Skill — why it is important for this role and how hard it is to learn

---

## 📅 30-DAY PERSONALISED LEARNING ROADMAP

**Week 1 — Foundation (Days 1–7)**
- Task 1: [specific task with free resource]
- Task 2: [specific task with free resource]
- Task 3: [specific task with free resource]

**Week 2 — Building (Days 8–14)**
- Task 1: [specific task with project idea]
- Task 2: [specific task with project idea]
- Task 3: [specific task with project idea]

**Week 3 — Practice (Days 15–21)**
- Task 1: [hands-on practice task]
- Task 2: [hands-on practice task]
- Task 3: [hands-on practice task]

**Week 4 — Polish (Days 22–30)**
- Task 1: [portfolio or interview prep task]
- Task 2: [portfolio or interview prep task]
- Task 3: [portfolio or interview prep task]

---

## 💡 TOP 3 RESUME IMPROVEMENT TIPS

**Tip 1:** [Specific actionable tip based on their actual resume]

**Tip 2:** [Specific actionable tip based on their actual resume]

**Tip 3:** [Specific actionable tip based on their actual resume]

---

## 🚀 OVERALL RECOMMENDATION

[2-3 sentences of honest, encouraging advice specific to this candidate]

---

Rules: Be specific using actual resume details. Suggest only free resources. Be honest but encouraging.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a senior HR professional and career coach. Give detailed structured personalised career analysis. Always follow the exact format."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.6,
        max_tokens=2000
    )

    return response.choices[0].message.content