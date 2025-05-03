from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from score_resumes import ResumeScore
from fastapi.middleware.cors import CORSMiddleware
from lib.workex.score_workex import WorkEX
from lib.projectex.score_projectex import ProjectEX
import requests
import config
import spacy

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

class ChatRequest(BaseModel):
    sender: str
    message: str


class ResumeRequest(BaseModel):
    resume_text: str
    job_description: str


class WorkExRequest(BaseModel):
    workex_text: str
    job_description: str

class ProjectRequest(BaseModel):
    project_text: str
    job_description: str

class WorkExResponse(BaseModel):
    feedback_text: str
    score: bool
    matched_skills: dict
    missing_skills: dict

class ProjectResponse(BaseModel):
    feedback_text: str
    score: bool
    matched_skills: dict
    missing_skills: dict

class ResumeResponse(BaseModel):
    normalized_score: float
    matched_skills: dict
    missing_skills: dict


@app.post("/workex_feedback", response_model=WorkExResponse)
def get_workex_feedback_endpoint(request: WorkExRequest):
    try:
        obj = WorkEX()
        feedback_text = obj.get_workex_feedback(request.job_description, request.workex_text)
        score, matched_skills, missing_skills = resume_scorer.score_resume(
            request.job_description, request.workex_text
        )
        return WorkExResponse(
            feedback_text = feedback_text,
            score=score,
            matched_skills=matched_skills,
            missing_skills=missing_skills
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/projectex_feedback", response_model=ProjectResponse)
def get_project_feedback_endpoint(request: ProjectRequest):
    try:
        obj = ProjectEX()
        feedback_text = obj.get_project_feedback(request.job_description, request.project_text)

        score, matched_skills, missing_skills = resume_scorer.score_resume(
            request.job_description, request.project_text
        )

        return ProjectResponse(
            feedback_text=feedback_text,
            score=score,
            matched_skills=matched_skills,
            missing_skills=missing_skills
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
def chat_with_bot(chat_request: ChatRequest):
    # Extract sender and message from the parsed ChatRequest model
    sender = chat_request.sender
    message = chat_request.message

    try:
        response = requests.post(config.BOT_CHAT_URL, json={"sender": sender, "message": message})
        if response.ok:
            return response.json()  # Forward the response from the bot server
        else:
            raise HTTPException(status_code=500, detail="Could not reach BOT server.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# To run the server, use: uvicorn filename:app --reload
