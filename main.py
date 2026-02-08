from fastapi import FastAPI, UploadFile, File
from models.schemas import InterviewSetup, EvaluationRequest, InterviewResult
from services.groq_service import generate_question, evaluate_answer
from services.speech_service import speech_to_text
from utils.scoring import calculate_percentage, grade_from_percentage

app = FastAPI(title="AI Interview Backend")

scores_store = [] 

@app.post("/interview/setup")
def interview_setup(data: InterviewSetup):
    try:
        question = generate_question(
            role=data.role,
            experience=data.experience,
            difficulty=data.difficulty,
            tech_skills=data.tech_skills,
            target_company=data.target_company
        )
        return {"question": question}
    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}


@app.post("/interview/speech-to-text")
async def transcribe_audio(audio: UploadFile = File(...)):
    audio_bytes = await audio.read()
    transcript = speech_to_text(audio_bytes)
    return {"transcript": transcript}

@app.post("/interview/evaluate")
def evaluate(data: EvaluationRequest):
    result = evaluate_answer(data.question, data.answer)

    print("TYPE OF RESULT:", type(result))
    print("RESULT VALUE:", result)

    return result


@app.get("/interview/result")
def final_result():
    if not scores_store:
        return {
            "message": "No evaluations completed yet",
            "total_questions": 0,
            "percentage": 0,
            "grade": "N/A"
        }

    percentage = calculate_percentage(scores_store)
    grade = grade_from_percentage(percentage)

    return {
        "total_questions": len(scores_store),
        "total_score": sum(scores_store),
        "percentage": percentage,
        "grade": grade
    }

