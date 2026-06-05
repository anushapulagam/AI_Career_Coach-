import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def start_interview(resume_text, job_role):
    prompt = f"""You are a strict but fair technical interviewer at a top tech company.
The candidate is applying for: {job_role}

Their resume:
{resume_text}

Start the mock interview. Ask the FIRST interview question only.
Make it a real technical question relevant to {job_role} and their background.
Do NOT give the answer. Just ask the question clearly.
Format: just the question, nothing else."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300
    )
    return response.choices[0].message.content

def evaluate_answer(question, user_answer, job_role, history):
    system = f"""You are a technical interviewer for a {job_role} position.
Evaluate the candidate's answer honestly:
- Tell them what was GOOD in their answer
- Tell them what was MISSING or could be better
- Then ask the NEXT interview question

Keep it like a real interview conversation. Be encouraging but honest."""

    messages = [{"role": "system", "content": system}]

    # history is list of dicts in Gradio 6.x
    for turn in history:
        if isinstance(turn, dict):
            if turn.get("role") in ("user", "assistant") and turn.get("content"):
                messages.append({"role": turn["role"], "content": turn["content"]})

    messages.append({"role": "user", "content": f"My answer: {user_answer}"})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=600
    )
    return response.choices[0].message.content