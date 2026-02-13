import os
from groq import Groq
from dotenv import load_dotenv
import json
import re

load_dotenv()
client = Groq()  
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print("🔑 GROQ_API_KEY:", api_key)

if not api_key:
    raise RuntimeError("GROQ_API_KEY not found in environment")

FORBIDDEN_KEYWORDS = [
    "implement",
    "write code",
    "code",
    "program",
    "syntax",
    "pseudocode",
    "develop",
    "coding",
    "example code"
]
def is_valid_verbal_question(question: str) -> bool:
    question_lower = question.lower()
    return not any(keyword in question_lower for keyword in FORBIDDEN_KEYWORDS)

def _generate_from_llm(prompt: str) -> str:
    try:
        print("🧠 Sending prompt to Groq...")
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        print("✅ Groq response received")
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("❌ GROQ ERROR:", repr(e))
        raise


def generate_question(role, experience, difficulty, tech_skills=None, target_company=None):
    prompt = f"""
You are an AI interviewer conducting a VERBAL technical interview.

Role: {role}
Experience level: {experience}
Difficulty: {difficulty}
"""

    # Add tech skills ONLY if provided
    if tech_skills:
        skills_text = ", ".join(tech_skills)
        prompt += f"\nBase the question on these technical skills: {skills_text}"

    # Add company context ONLY if provided
    if target_company:
         prompt += f"\nKeep the question aligned with {target_company}'s interview style."

    prompt += """
Ask ONE concise interview question that tests understanding and reasoning.
"""

    for _ in range(3):
        question = _generate_from_llm(prompt)
        if is_valid_verbal_question(question):
            return question

    # Fallback (guaranteed safe)
    return "Explain a core concept related to your role and experience."

def evaluate_answer(question, answer):
    prompt = f"""
    Interview Question:
    {question}

    Candidate Answer:
    {answer}

    Evaluate on:
    - Clarity
    - Technical accuracy
    - Completeness

    Respond in this format:
    Score: 0-10,
    Feedback: <short feedback>
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
