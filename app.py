import gradio as gr
import os
from modules.resume_parser import get_resume_text
from modules.vector_store import load_job_descriptions, build_vector_store, search_job
from modules.skill_gap import analyze_resume
from modules.chatbot import chat_with_coach
from modules.mock_interview import start_interview, evaluate_answer

# ── Load once at startup ─────────────────────────────────────
print("⏳ Loading job descriptions...")
jobs = load_job_descriptions("data/job_descriptions.json")
index, descriptions, jobs_list = build_vector_store(jobs)
print("✅ Ready!")

# Global state
resume_store = {"text": "", "job_role": ""}

# ── Tab 1: Analysis ──────────────────────────────────────────
def run_analysis(pdf_file, job_role):
    # Check 1: No file uploaded
    if pdf_file is None:
        return "❌ **No resume uploaded!**\n\nPlease click the upload box and select your resume PDF file."

    # Check 2: Not a PDF
    if not pdf_file.name.lower().endswith(".pdf"):
        return "❌ **Wrong file type!**\n\nPlease upload a PDF file only. If your resume is in Word format, open it and save as PDF first."

    # Check 3: No job role entered
    if not job_role or not job_role.strip():
        return "❌ **No job role entered!**\n\nPlease type your target job role in the text box. Example: Python Developer, AI Engineer, Data Analyst"

    # Check 4: Job role too short
    if len(job_role.strip()) < 3:
        return "❌ **Job role too short!**\n\nPlease enter a complete job role. Example: Python Developer"

    try:
        # Parse resume
        resume_text, parse_error = get_resume_text(pdf_file.name)
        if parse_error:
            return parse_error

        # Search for matching job
        matched_job = search_job(job_role.strip(), index, jobs_list)

        # Run AI analysis
        result = analyze_resume(resume_text, matched_job["role"], matched_job["description"])

        # Save for chatbot
        resume_store["text"] = resume_text
        resume_store["job_role"] = matched_job["role"]

        return result

    except RuntimeError as e:
        return f"❌ **Search Error**\n\n{str(e)}"
    except ConnectionError:
        return "❌ **No Internet Connection!**\n\nThe AI analysis requires internet to connect to Groq API. Please check your connection and try again."
    except Exception as e:
        error_msg = str(e)
        if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
            return "❌ **Invalid API Key!**\n\nYour Groq API key is missing or incorrect. Please check your .env file."
        elif "rate_limit" in error_msg.lower():
            return "❌ **Rate Limit Reached!**\n\nToo many requests to the AI. Please wait 30 seconds and try again."
        elif "timeout" in error_msg.lower():
            return "❌ **Request Timed Out!**\n\nThe AI took too long to respond. Please try again."
        else:
            return f"❌ **Something went wrong**\n\n{error_msg}\n\nPlease try again or contact support."

# ── Tab 2: Chat ──────────────────────────────────────────────
def respond(user_message, history):
    if not user_message.strip():
        return history, ""

    if not resume_store["text"]:
        history = history + [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": "⚠️ Please go to the **Career Analysis** tab first, upload your resume and click Analyse. Then come back here to chat!"}
        ]
        return history, ""

    try:
        ai_reply = chat_with_coach(
            user_message, history,
            resume_store["text"], resume_store["job_role"]
        )
    except Exception as e:
        error_msg = str(e)
        if "rate_limit" in error_msg.lower():
            ai_reply = "⚠️ Rate limit reached. Please wait 30 seconds and try again."
        elif "timeout" in error_msg.lower():
            ai_reply = "⚠️ The AI took too long to respond. Please try again."
        else:
            ai_reply = f"⚠️ Something went wrong: {error_msg}. Please try again."

    history = history + [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": ai_reply}
    ]
    return history, ""

# ── Tab 3: Mock Interview ────────────────────────────────────
def begin_interview(history):
    if not resume_store["text"]:
        history = history + [
            {"role": "assistant", "content": "⚠️ Please go to the **Career Analysis** tab first and analyse your resume before starting the interview!"}
        ]
        return history, gr.update(interactive=False)

    try:
        first_question = start_interview(resume_store["text"], resume_store["job_role"])
        opening = (
            "🎤 **Mock Interview Started!**\n\n"
            "I am your interviewer today. Answer each question as you would in a real interview.\n\n"
            "---\n\n**Question 1:**\n\n" + first_question
        )
        history = history + [{"role": "assistant", "content": opening}]
        return history, gr.update(interactive=True)

    except Exception as e:
        history = history + [
            {"role": "assistant", "content": f"⚠️ Could not start interview: {str(e)}. Please try again."}
        ]
        return history, gr.update(interactive=False)

def answer_question(user_answer, history):
    if not user_answer.strip():
        return history, ""

    try:
        feedback = evaluate_answer("", user_answer, resume_store["job_role"], history)
    except Exception as e:
        feedback = f"⚠️ Could not evaluate answer: {str(e)}. Please try again."

    history = history + [
        {"role": "user", "content": user_answer},
        {"role": "assistant", "content": feedback}
    ]
    return history, ""

# ── Custom CSS — NO WHITE ────────────────────────────────────
custom_css = """
body, .gradio-container {
    background-color: #0f0e2a !important;
    color: #e8e6ff !important;
    font-family: 'Segoe UI', sans-serif !important;
    max-width: 1100px !important;
    margin: auto !important;
}
.block, .form, .gap, .panel, .gradio-container .block {
    background-color: #1a1840 !important;
    border-color: #534AB7 !important;
    color: #e8e6ff !important;
}
label, .label-wrap span, span, p, li, h1, h2, h3, h4 {
    color: #e8e6ff !important;
}
input, textarea, .scroll-hide {
    background-color: #2a2650 !important;
    color: #e8e6ff !important;
    border: 1px solid #534AB7 !important;
    border-radius: 8px !important;
}
input::placeholder, textarea::placeholder {
    color: #9b97cc !important;
}
.tab-nav button {
    background-color: #1a1840 !important;
    color: #9b97cc !important;
    border: 1px solid #534AB7 !important;
    border-radius: 8px 8px 0 0 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}
.tab-nav button.selected {
    background-color: #534AB7 !important;
    color: #e8e6ff !important;
}
button.primary {
    background: linear-gradient(135deg, #534AB7, #1D9E75) !important;
    color: #e8e6ff !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
}
.prose, .prose p, .prose li, .prose h1,
.prose h2, .prose h3, .markdown-body,
.markdown-body p, .markdown-body li,
.markdown-body h1, .markdown-body h2,
.markdown-body h3 {
    color: #e8e6ff !important;
    background: transparent !important;
}
.message-wrap { background-color: #1a1840 !important; }
.message.user div, .user div {
    background-color: #534AB7 !important;
    color: #e8e6ff !important;
    border-radius: 16px 16px 4px 16px !important;
}
.message.bot div, .bot div, .message.assistant div {
    background-color: #2a2650 !important;
    color: #e8e6ff !important;
    border-radius: 16px 16px 16px 4px !important;
}
.upload-button, .file-preview {
    background-color: #2a2650 !important;
    color: #e8e6ff !important;
    border: 2px dashed #534AB7 !important;
    border-radius: 10px !important;
}
.examples-holder, .examples table, .examples td {
    background-color: #1a1840 !important;
    color: #e8e6ff !important;
    border-color: #534AB7 !important;
}
.examples td:hover { background-color: #534AB7 !important; }
"""

# ── Build UI ─────────────────────────────────────────────────
with gr.Blocks(title="AI Career Coach") as demo:

    gr.HTML("""
    <div style="background:linear-gradient(135deg,#534AB7 0%,#1D9E75 100%);
    border-radius:16px;padding:30px 32px;margin-bottom:14px;text-align:center">
        <h1 style="font-size:2.2rem;font-weight:700;margin:0 0 8px 0;color:#ffffff">
            🎯 AI Career Coach
        </h1>
        <p style="font-size:1rem;margin:0;color:#e0ffe8">
            Upload your resume · Get AI-powered skill gap analysis ·
            Practice mock interviews · Land your dream job
        </p>
    </div>
    """)

    with gr.Tabs():

        # ── TAB 1 ────────────────────────────────────────────
        with gr.Tab("📊 Career Analysis"):
            gr.HTML("""
            <div style="background:#1a1840;border-left:4px solid #534AB7;
            border-radius:8px;padding:12px 16px;margin-bottom:12px">
                <span style="color:#b8b4ff;font-size:13px">
                📌 <strong style="color:#e8e6ff">How to use:</strong>
                Upload resume PDF → Enter job role → Click Analyse
                </span>
            </div>
            """)
            with gr.Row(equal_height=True):
                with gr.Column(scale=1, min_width=260):
                    pdf_input = gr.File(
                        label="📄 Upload Your Resume (PDF only)",
                        file_types=[".pdf"]
                    )
                    job_input = gr.Textbox(
                        label="🎯 Target Job Role",
                        placeholder="e.g. Python Developer, AI Engineer, Data Analyst"
                    )
                    analyse_btn = gr.Button(
                        "🚀 Analyse My Resume",
                        variant="primary", size="lg"
                    )
                    gr.HTML("""
                    <div style="margin-top:12px;padding:12px;
                    background:#0d3321;border-radius:10px;border:1px solid #1D9E75">
                        <p style="color:#6effc1;font-size:12.5px;margin:0">
                        ✅ After analysis → go to <strong style="color:#a8ffd8">
                        Chat with Coach</strong> for questions<br><br>
                        ✅ Go to <strong style="color:#a8ffd8">Mock Interview</strong>
                        to practise
                        </p>
                    </div>
                    """)
                with gr.Column(scale=2):
                    gr.HTML("""
                    <div style="background:#1a1840;border:1px solid #534AB7;
                    border-radius:12px;padding:24px;min-height:260px">
                        <h3 style="color:#b8b4ff;margin:0 0 14px 0">👋 Welcome!</h3>
                        <p style="color:#c8c4f0;font-size:14px;line-height:1.8;margin:0 0 14px 0">
                        Upload your resume and enter a job role to get your personalised career analysis.
                        </p>
                        <ul style="color:#c8c4f0;font-size:13.5px;line-height:2;padding-left:18px;margin:0">
                            <li>🎯 <strong style="color:#b8b4ff">ATS Score</strong> with keyword analysis</li>
                            <li>✅ <strong style="color:#6effc1">Matching Skills</strong></li>
                            <li>❌ <strong style="color:#ff9b9b">Missing Skills</strong></li>
                            <li>📅 <strong style="color:#ffd96e">30-Day Roadmap</strong></li>
                            <li>💡 <strong style="color:#b8b4ff">Resume Tips</strong></li>
                            <li>🚀 <strong style="color:#6effc1">Overall Recommendation</strong></li>
                        </ul>
                    </div>
                    """)
                    output_box = gr.Markdown(value="")
            analyse_btn.click(
                fn=run_analysis,
                inputs=[pdf_input, job_input],
                outputs=output_box
            )

        # ── TAB 2 ────────────────────────────────────────────
        with gr.Tab("💬 Chat with Coach"):
            gr.HTML("""
            <div style="background:#1a1840;border-left:4px solid #1D9E75;
            border-radius:8px;padding:12px 16px;margin-bottom:12px">
                <span style="color:#6effc1;font-size:13px">
                💬 <strong style="color:#a8ffd8">Your personal AI career advisor</strong>
                — Ask anything about your resume, skills or interview prep.
                Analyse your resume in Tab 1 first!
                </span>
            </div>
            """)
            chatbot = gr.Chatbot(height=420, label="AI Career Coach", show_label=False)
            with gr.Row():
                chat_input = gr.Textbox(
                    placeholder="Ask me anything about your career...",
                    label="", scale=5, container=False
                )
                send_btn = gr.Button("Send 📨", variant="primary", scale=1, min_width=100)
            gr.Examples(
                label="💡 Click any question to try:",
                examples=[
                    "What skills should I learn first based on my resume?",
                    "Suggest free YouTube courses for my missing skills",
                    "What projects should I build to get hired faster?",
                    "How should I rewrite my resume summary?",
                    "What salary can I expect for this role in India?",
                    "Compare Python Developer vs AI Engineer for my profile",
                    "Write a cover letter for me for this job role",
                ],
                inputs=chat_input
            )
            send_btn.click(fn=respond, inputs=[chat_input, chatbot], outputs=[chatbot, chat_input])
            chat_input.submit(fn=respond, inputs=[chat_input, chatbot], outputs=[chatbot, chat_input])

        # ── TAB 3 ────────────────────────────────────────────
        with gr.Tab("🎤 Mock Interview"):
            gr.HTML("""
            <div style="background:#1a1840;border-left:4px solid #ffd96e;
            border-radius:8px;padding:12px 16px;margin-bottom:12px">
                <span style="color:#ffd96e;font-size:13px">
                🎤 <strong style="color:#ffe9a0">Practice makes perfect!</strong>
                — AI asks real interview questions and evaluates your answers.
                Analyse your resume in Tab 1 first!
                </span>
            </div>
            """)
            interview_chat = gr.Chatbot(height=420, label="Interviewer", show_label=False)
            start_btn = gr.Button("🚀 Start New Mock Interview", variant="primary", size="lg")
            with gr.Row():
                interview_input = gr.Textbox(
                    placeholder="Type your answer here...",
                    label="", scale=5, interactive=False, container=False
                )
                submit_btn = gr.Button("Submit Answer ✅", variant="primary", scale=1, min_width=140)
            gr.HTML("""
            <div style="margin-top:10px;padding:12px;background:#2a1f00;
            border-radius:10px;border:1px solid #ffd96e">
                <p style="color:#ffd96e;font-size:12.5px;margin:0">
                💡 <strong>Tips:</strong> Answer in full sentences ·
                Use specific examples · Use technical terms ·
                Be honest about what you don't know
                </p>
            </div>
            """)
            start_btn.click(fn=begin_interview, inputs=[interview_chat], outputs=[interview_chat, interview_input])
            submit_btn.click(fn=answer_question, inputs=[interview_input, interview_chat], outputs=[interview_chat, interview_input])
            interview_input.submit(fn=answer_question, inputs=[interview_input, interview_chat], outputs=[interview_chat, interview_input])

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Base(), css=custom_css)