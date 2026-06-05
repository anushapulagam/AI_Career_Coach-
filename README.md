---
title: AI Career Coach
emoji: 🎯
colorFrom: purple
colorTo: green
sdk: gradio
sdk_version: "6.15.2"
python_version: "3.11"
app_file: app.py
pinned: false
---

# 🎯 AI Career Coach

> An AI-powered career counsellor that reads your resume, finds skill gaps, generates a personalised 30-day learning roadmap, and lets you practice mock interviews — all in one web app.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Gradio](https://img.shields.io/badge/Gradio-6.x-orange?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-Llama3.3-green?style=flat-square)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-purple?style=flat-square)

---

## 🌐 Live Demo

👉 **[Click here to try the app](https://huggingface.co/spaces/anushapulagam/AI_Career_Coach)**

---

## 📸 Screenshots

### 📊 Tab 1 — Career Analysis

<img src="Screenshots/03_analysis_result.png" width="800"/>

### 💬 Tab 2 — Chat with Coach

<img src="Screenshots/04_chatbot.png" width="800"/>

### 🎤 Tab 3 — Mock Interview

<img src="Screenshots/05_mock_interview.png" width="800"/>

### 🏠 Home Page

<img src="Screenshots/01_home.png" width="800"/>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 Resume Parser | Reads any PDF resume and extracts all text automatically |
| 🔍 Semantic Job Matching | Uses FAISS and sentence transformers to find the most relevant job description |
| 🎯 ATS Score | Calculates real ATS compatibility score with keyword-level breakdown |
| ✅ Skill Gap Analysis | Compares resume against job description to find matching and missing skills |
| 📅 30-Day Roadmap | Generates a personalised week-by-week learning plan with free resources |
| 💬 Multi-turn Chatbot | Conversational AI coach that remembers your resume throughout the session |
| 🎤 Mock Interview | AI interviewer asks role-specific questions and evaluates your answers |
| 🛡️ Error Handling | Friendly error messages for all edge cases — app never crashes |

---

## 🏗️ Project Architecture

```
User uploads Resume PDF
        ↓
resume_parser.py  →  Extracts and cleans all text
        ↓
vector_store.py   →  FAISS semantic search  →  Finds best matching Job Description
        ↓
skill_gap.py      →  Groq LLM API  →  Generates Analysis
        ↓
app.py            →  Gradio UI  →  Displays results in browser
```

---

## 🛠️ Tech Stack

| Technology | Purpose | Why This |
|------------|---------|----------|
| Python 3.11 | Core language | Industry standard for AI/ML |
| Gradio 6.x | Web UI framework | Fastest way to build AI demos |
| Groq API Llama 3.3 70B | LLM for AI analysis | 100% free, fastest inference speed |
| FAISS | Vector similarity search | Built by Meta, lightning fast |
| Sentence Transformers | Text embeddings | Captures meaning not just keywords |
| PyPDF2 | PDF text extraction | Lightweight, handles multi-page PDFs |
| python-dotenv | Secret management | Industry standard for API key security |

---

## 📁 Folder Structure

```
ai_career_coach/
├── modules/
│   ├── __init__.py
│   ├── resume_parser.py
│   ├── vector_store.py
│   ├── skill_gap.py
│   ├── chatbot.py
│   └── mock_interview.py
├── data/
│   └── job_descriptions.json
├── Screenshots/
├── app.py
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run Locally

**Step 1 — Clone the repository**
```bash
git clone https://github.com/anushapulagam/AI_Career_Coach-.git
cd AI_Career_Coach-
```

**Step 2 — Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

**Step 3 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4 — Create .env file**
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free key at https://console.groq.com

**Step 5 — Run the app**
```bash
python app.py
```

Open browser at http://127.0.0.1:7860

---

## 💡 How to Use

**Tab 1 — Career Analysis**
- Upload your resume as PDF
- Type your target job role
- Click Analyse My Resume
- Get ATS score, skill gap and 30-day roadmap

**Tab 2 — Chat with Coach**
- Ask anything about your resume, skills or career
- AI remembers your resume throughout the conversation

**Tab 3 — Mock Interview**
- Click Start Mock Interview
- Answer questions honestly
- Get feedback and next question

---

## 🧠 How RAG Works in This Project

This project uses RAG — Retrieval Augmented Generation:

1. **Retrieve** — FAISS searches job descriptions database using semantic similarity
2. **Augment** — Retrieved job description is combined with resume text into a prompt
3. **Generate** — Groq Llama 3.3 70B generates personalised career analysis

---

## 👩‍💻 About

Built by **Anusha** as part of the **Generative AI with LLMs** internship at **SkillDzire Technologies Private Limited**.

This project demonstrates:
- RAG architecture implementation
- Semantic search with vector embeddings
- LLM prompt engineering
- Conversational AI with memory
- Production-ready error handling
- Full-stack AI application deployment

---

## 🔮 Future Scope

- Live job description fetching via Jsearch API
- Resume PDF download with improvements applied
- LinkedIn profile analysis
- Interview performance tracking over time

---

⭐ If you found this project helpful please give it a star on GitHub!