from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from score_resumes import ResumeScore  # Assuming the code you provided is saved as ResumeScore.py

app = FastAPI()

# Initialize ResumeScore once when the API starts
resume_scorer = ResumeScore()

class ResumeRequest(BaseModel):
    resume_text: str
    job_description: str

class ResumeResponse(BaseModel):
    normalized_score: float
    matched_skills: dict
    missing_skills: dict

@app.post("/score_resume", response_model=ResumeResponse)
def score_resume_endpoint(request: ResumeRequest):
    try:
        normalized_score, matched_skills, missing_skills = resume_scorer.score_resume(
            request.job_description, request.resume_text
        )
        return ResumeResponse(
            normalized_score=normalized_score,
            matched_skills=matched_skills,
            missing_skills=missing_skills
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run the server, use: uvicorn filename:app --reload
