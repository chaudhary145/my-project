import os
from groq import Groq
from dotenv import load_dotenv
import json
import re
import random
import time

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
) 

FORBIDDEN_KEYWORDS = [
    "implement",
    "write code",
    "code",
    "program",
    "syntax",
    "Design",
    "pseudocode",
    "develop",
    "coding",
    "example code"
]
def is_valid_verbal_question(question: str) -> bool:
    question_lower = question.lower()
    return not any(keyword in question_lower for keyword in FORBIDDEN_KEYWORDS)

def _generate_from_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        top_p=0.95
    )
    return response.choices[0].message.content.strip()


def generate_question(role, experience, difficulty, tech_skills=None, target_company=None, interview_type="technical"):

    
    # ---------- BASE PROMPT (ALWAYS INITIALIZED) ----------
    prompt = f"""
You are an AI interviewer conducting a {interview_type.upper()} interview.

Role: {role}
Experience level: {experience}
Difficulty: {difficulty}
"""

    # ---------- TECHNICAL vs BEHAVIORAL VARIATION ----------
    if interview_type == "technical":
        if tech_skills:
            skills_text = ", ".join(tech_skills)
            prompt += f"\nBase the question on these technical skills: {skills_text} that can be answered verbally"

    elif interview_type == "behavioral":

        prompt += f"""
    
Generate 3 COMPLETELY DIFFERENT behavioral interview questions.

Each question must:
- Focus on a DIFFERENT workplace scenario
- Be unique from common textbook questions
- Avoid generic phrases like:
    - "Tell me about a time..."
    - "Describe a challenge..."
    - "Describe a conflict..."

Role: {role}
Experience: {experience}

Do NOT repeat standard interview questions.
Be creative and realistic.
"""
    # Add tech skills ONLY if provided
    if tech_skills:
        skills_text = ", ".join(tech_skills)
        prompt += f"\nBase the question on these technical skills: {skills_text}"

    # ---------- COMPANY CONTEXT (UNCHANGED FUNCTIONALITY) ----------
    if target_company:
        prompt += f"\nKeep the question aligned with {target_company}'s interview style."

    # ---------- DIFFICULTY AFFECTS QUESTION STYLE ----------
    difficulty_styles = {
        "easy": "Ask a simple, conceptual question suitable for beginners.",
        "medium": "Ask a practical question that requires reasoning and trade-offs.",
        "hard": "Ask a deep, system-design or advanced problem-solving question."
    }

    prompt += f"\n{difficulty_styles.get(difficulty.lower(), 'Ask a balanced technical question.')}"

    # ---------- ASK FOR 3 DIFFERENT QUESTIONS ----------
    prompt += """
Generate 3 DIFFERENT concise interview questions.
Number them as:
1)
2)
3)
"""
    for _ in range(5):
        response = _generate_from_llm(prompt)

        # Ensure response contains 3 questions
    questions = [
    q.strip()
    for q in response.split("\n")
    if q.strip() and q.strip()[0].isdigit()
     ]

    valid_questions = [
    q.split(")", 1)[-1].strip()
    for q in questions
    if is_valid_verbal_question(q)
    ]

    if len(valid_questions) >= 3:
            return {
                "q1": valid_questions[0],
                "q2": valid_questions[1],
                "q3": valid_questions[2]
            }

    # ---------- SAFE FALLBACK (IF LLM FAILS) ----------
    return {
        "q1": "Explain a core concept related to your role and experience.",
        "q2": "Describe a technical challenge you faced and how you solved it.",
        "q3": "What is the most important concept in your field and why?"
}

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






 