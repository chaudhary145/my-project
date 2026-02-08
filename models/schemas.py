from pydantic import BaseModel
from typing import Optional, List

class InterviewSetup(BaseModel):
    role: str
    experience: str
    difficulty: str
    tech_skills: Optional[List[str]] = None
    target_company: Optional[str] = None


class EvaluationRequest(BaseModel):
    question: str
    answer: str

class InterviewResult(BaseModel):
    total_questions: int
    scores: list[int]
