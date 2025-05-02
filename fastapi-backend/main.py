from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from score_resumes import ResumeScore  # Assuming the code you provided is saved as ResumeScore.py
from fastapi.middleware.cors import CORSMiddleware
import requests
import config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get("/bot/ping")
def ping_bot():
    return requests.get(config.BOT_PING_URL).ok


@app.post("/bot/chat")
def chat_with_bot(sender: str, message: str):
    response = requests.post(config.BOT_CHAT_URL, json={"sender": sender, "message": message})
    if response.ok:
        return JSONResponse(response.json())
    else:
        raise HTTPException(status_code=500, detail="Could not reach BOT server.")

# To run the server, use: uvicorn filename:app --reload
