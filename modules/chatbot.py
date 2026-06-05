import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chat_with_coach(user_message, history, resume_text, job_role):
    system_prompt = f"""You are an expert AI Career Coach.
You have already read the candidate's resume and know their background.

CANDIDATE RESUME:
{resume_text}

TARGET JOB ROLE: {job_role}

Your job is to:
- Answer career questions based on their actual resume
- Give specific, personalised advice
- Suggest resources, courses, and projects
- Help them prepare for interviews
- Be encouraging but honest

Always refer to their actual skills and experience from the resume.
Keep answers concise and practical."""

    messages = [{"role": "system", "content": system_prompt}]

    # Gradio 6.x history is list of dicts: {"role": "user"/"assistant", "content": "..."}
    for turn in history:
        if isinstance(turn, dict):
            if turn.get("role") in ("user", "assistant") and turn.get("content"):
                messages.append({"role": turn["role"], "content": turn["content"]})

    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content