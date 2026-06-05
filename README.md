# 🎯 AI Career Coach

> An AI-powered career counsellor that reads your resume, finds skill gaps, generates a personalised 30-day learning roadmap, and lets you practice mock interviews — all in one web app.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Gradio](https://img.shields.io/badge/Gradio-6.x-orange?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-Llama3.3-green?style=flat-square)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-purple?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 🌐 Live Demo

👉 **[Try it here](https://huggingface.co/spaces/username/ai-career-coach)**

> Replace the link above with your actual HuggingFace Spaces URL after deployment.

---

## 📸 Screenshots

### 📊 Career Analysis Tab
Upload your resume and get instant AI-powered analysis with ATS score, skill gap, and 30-day roadmap.

![Career Analysis](Screenshots/03_resume_analysis.png)

### 💬 Chat with Coach Tab
Ask anything about your resume, skills, or career path. The AI remembers your resume throughout the conversation.

![Chat with Coach](Screenshots/04_chatbot.png)

### 🎤 Mock Interview Tab
Practice real interview questions tailored to your resume and target role. Get honest feedback after each answer.

![Mock Interview](Screenshots/05_mock_interview.png)

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
| **Gradio 6.x** | Web UI framework | Fastest way to build AI demos, used by HuggingFace |
| **Groq API (Llama 3.3 70B)** | LLM for AI analysis | 100% free, fastest inference speed, high quality |
| **FAISS** | Vector similarity search | Built by Meta, lightning fast semantic search |
| **Sentence Transformers** | Text embeddings | Captures meaning not just keywords |
| **PyPDF2** | PDF text extraction | Lightweight, handles multi-page PDFs |
| **python-dotenv** | Secret management | Industry standard for API key security |

---

## 📁 Folder Structure

```
ai_career_coach/
├── modules/
│   ├── __init__.py          # Makes modules importable
│   ├── resume_parser.py     # PDF text extraction
│   ├── vector_store.py      # FAISS semantic search
│   ├── skill_gap.py         # AI analysis via Groq
│   ├── chatbot.py           # Multi-turn conversation
│   └── mock_interview.py    # Mock interview logic
├── data/
│   └── job_descriptions.json  # Job descriptions database
├── screenshots/             # App screenshots
├── app.py                   # Main Gradio UI entry point
├── requirements.txt         # Project dependencies
├── .gitignore               # Files excluded from Git
└── README.md                # This file
```

---

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/anushapulagam/ai-career-coach.git
cd ai-career-coach
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your API key
Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free API key at [console.groq.com](https://console.groq.com)

### 5. Run the app
```bash
python app.py
```

Open your browser at `http://127.0.0.1:7860`

---

## 💡 How to Use

1. **Tab 1 — Career Analysis**
   - Upload your resume as a PDF
   - Type your target job role (e.g. "Python Developer")
   - Click **Analyse My Resume**
   - Get your ATS score, skill gap, and 30-day roadmap

2. **Tab 2 — Chat with Coach**
   - After analysing, come here to ask follow-up questions
   - The AI remembers your resume and gives personalised answers
   - Ask anything — resources, projects, salary, cover letter

3. **Tab 3 — Mock Interview**
   - Click **Start Mock Interview**
   - Answer questions in the text box
   - Get honest feedback and the next question

---

## 🧠 How It Works (RAG Pipeline)

This project implements a **RAG (Retrieval Augmented Generation)** architecture:

1. **Retrieval** — FAISS searches the job descriptions database using semantic similarity to find the most relevant JD for the user's target role
2. **Augmentation** — The retrieved JD is combined with the resume text into a structured prompt
3. **Generation** — Groq's Llama 3.3 70B model generates the personalised career analysis based on the augmented context

This approach ensures the AI gives **specific, relevant advice** based on real job requirements rather than generic suggestions.

---

## 📊 ATS Score Calculation

The ATS score is calculated in two steps:

1. **Keyword extraction** — Python extracts 40+ tech keywords from the job description and checks which ones appear in the resume
2. **Overlap scoring** — Calculates the ratio of JD keywords found in the resume and converts to a 0-100 score
3. **AI explanation** — Groq LLM explains the score with specific reasons based on the actual resume content

---

## 🔮 Future Scope

- [ ] Live job description fetching via Jsearch API
- [ ] Resume PDF download with improvements applied
- [ ] LinkedIn profile analysis
- [ ] Multiple resume comparison
- [ ] Interview performance tracking over time
- [ ] Support for multiple languages

---

## 👩‍💻 About

Built by **Anusha** as part of the **Generative AI with LLMs** internship at **SkillDzire Technologies Private Limited**.

This project demonstrates practical implementation of:
- RAG (Retrieval Augmented Generation) architecture
- Semantic search with vector embeddings
- LLM prompt engineering
- Conversational AI with memory
- Production-ready error handling
- Full-stack AI application deployment

---

## 📄 License

This project is licensed under the MIT License.

---

⭐ **If you found this project helpful, please give it a star on GitHub!**