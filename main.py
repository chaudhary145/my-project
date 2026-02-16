from fastapi import FastAPI, UploadFile, File
from models.schemas import InterviewSetup, EvaluationRequest, InterviewResult
from services.groq_service import generate_question, evaluate_answer
from services.speech_service import speech_to_text
from utils.scoring import calculate_percentage, grade_from_percentage


from fastapi.middleware.cors import CORSMiddleware
from routes import interview
import re


import uuid


app = FastAPI(title="AI Interview Backend")
app.include_router(interview.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, OPTIONS, etc.
    allow_headers=["*"],
)




scores_store = [] 

def extract_score_from_text(text: str) -> int:
    """
    Extracts score like '8/10' from Groq feedback
    """
    match = re.search(r'(\d+)\s*/\s*10', text)
    if match:
        return int(match.group(1))
    return 0

question_store = {}  # temporarily holds 3 questions
current_index = {}    # tracks which question we are on


@app.post("/interview/setup")
def interview_setup(data: InterviewSetup):
    print("insideeee")
    try:
        questions = generate_question(
            role=data.role,
            experience=data.experience,
            difficulty=data.difficulty,
            tech_skills=data.tech_skills,
            target_company=data.target_company,
            interview_type=data.interview_type
        )

        print("GENERATED QUESTION:", question)
        return {"question": question}


        # Generate a simple session ID (you can later replace with real user ID)
        session_id = str(uuid.uuid4())


        # Store questions for THIS user only
        question_store[session_id] = [
            questions["q1"],
            questions["q2"],
            questions["q3"],
        ]
        current_index[session_id] = 0

        # Return first question + session_id
        return {
            "session_id": session_id,
            "question": question_store[session_id][0]
        }


    except Exception as e:
        print("ufffff")
        print("ERROR:", str(e))
        return {"error": str(e)}


@app.post("/interview/next-question")
def next_question(session_id: str):
    if session_id not in question_store:
        return {"error": "Invalid session or interview not started"}

    current_index[session_id] += 1

    if current_index[session_id] < len(question_store[session_id]):
        return {
            "question": question_store[session_id][current_index[session_id]]
        }

    return {"message": "Interview completed"}



@app.post("/interview/speech-to-text")
async def transcribe_audio(audio: UploadFile = File(...)):
    audio_bytes = await audio.read()
    transcript = speech_to_text(audio_bytes)
    return {"transcript": transcript}

@app.post("/interview/evaluate")
def evaluate(data: EvaluationRequest):
    if not data.answer or not data.answer.strip():
        return {
            "score": 0,
            "feedback": "No answer provided."
        }
    
    score, feedback = evaluate_answer(data.question, data.answer)
    return {
        "score": score,
        "feedback": feedback
    }

<<<<<<< HEAD
    print("TYPE OF RESULT:", type(result))
    print("RESULT VALUE:", result)

    # 👇 NEW: score extract karo
    score = extract_score_from_text(result)
    scores_store.append(score)

    print("EXTRACTED SCORE:", score)
    print("SCORES STORE:", scores_store)

    return {
        "score": score,
        "feedback": result
    }
=======
>>>>>>> 722cd08672dbfb17ef8bda55987aa32f3d8ae8e3


@app.get("/interview/result")
def final_result():
    if not scores_store:
        return {
            "percentage": 0,
            "grade": "N/A"
        }

    percentage = calculate_percentage(scores_store)
    grade = grade_from_percentage(percentage)

    return {
        "percentage": percentage,
        "grade": grade
    }

