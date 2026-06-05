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

👉 **[Try it here](https://huggingface.co/spaces/anushapulagam/AI_Career_Coach)**

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 **Resume Parser** | Reads any PDF resume and extracts all text automatically |
| 🔍 **Semantic Job Matching** | Uses FAISS + sentence transformers to find the most relevant job description |
| 🎯 **ATS Score** | Calculates real ATS compatibility score with keyword-level breakdown |
| ✅ **Skill Gap Analysis** | Compares your resume against the job description to find matching and missing skills |
| 📅 **30-Day Roadmap** | Generates a personalised week-by-week learning plan with free resources |
| 💬 **Multi-turn Chatbot** | Conversational AI coach that remembers your resume throughout the session |
| 🎤 **Mock Interview** | AI interviewer asks role-specific questions and evaluates your answers |
| 🛡️ **Error Handling** | Friendly error messages for all edge cases — app never crashes |

---

## 🏗️ Project Architecture

```
User uploads Resume PDF
        ↓
resume_parser.py → Extracts and cleans text
        ↓
vector_store.py → FAISS semantic search → Finds best matching Job Description
        ↓
skill_gap.py → Groq LLM API → Generates Analysis
        ↓
app.py → Gradio UI → Displays results in browser
```

---

## 🛠️ Tech Stack

| Technology | Purpose | Why This? |
|------------|---------|-----------|
| **Python 3.11** | Core language | Industry standard for AI/ML |
| **Gradio 6.x** | Web UI framework | Fastest way to build AI demos |
| **Groq API (Llama 3.3 70B)** | LLM for AI analysis | 100% free, fastest inference speed |
| **FAISS** | Vector similarity search | Built by Meta, lightning fast |
| **Sentence Transformers** | Text embeddings | Captures meaning not just keywords |
| **PyPDF2** | PDF text extraction | Lightweight, handles multi-page PDFs |

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
├── app.py
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/anushapulagam/AI_Career_Coach-.git
cd AI_Career_Coach-
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

Run:
```bash
python app.py
```

---

## 👩‍💻 About

Built by **Anusha** as part of the **Generative AI with LLMs** internship at **SkillDzire Technologies Private Limited**.

---

⭐ If you found this project helpful, please give it a star!