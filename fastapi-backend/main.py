import logging
import os
import requests
import sys

from fastapi import FastAPI, HTTPException, status
from fastapi import UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

import config
from lib.projectex.score_projectex import ProjectEX
from lib.workex.score_workex import WorkEX
from score_impact import ImpactScore
from score_resumes import ResumeScore

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from scripts.llm.resume_optimizer_v2 import (
        load_extracted_data,
        select_bucket,
        retrieve_rag_hints,
        optimize_resume,
        )

UPLOAD_DIR = "../resume_bot/file"
os.makedirs(UPLOAD_DIR, exist_ok=True)


log = logging.getLogger("uvicorn")
log.setLevel(logging.DEBUG)
app = FastAPI()
app.state.data = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ResumeScore once when the API starts
resume_scorer = ResumeScore()


# Init scorer (global reuse for performance)
impact_scorer = ImpactScore()

class ActionWordRequest(BaseModel):
    resume_text: str

class ActionWordResponse(BaseModel):
    score: float

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
    score: float
    matched_skills: dict
    missing_skills: dict


class ProjectResponse(BaseModel):
    feedback_text: str
    score: float
    matched_skills: dict
    missing_skills: dict


class ResumeResponse(BaseModel):
    normalized_score: float
    matched_skills: dict
    missing_skills: dict

class TextPayload(BaseModel):
    text: str


@app.post("/optimize_resume")
async def optimize_resume_endpoint(request: ResumeRequest) -> str:
    try:
        extracted = load_extracted_data("../extracted_data.json")

        bucket = select_bucket(request.job_description, extracted)
        if not bucket:
            raise ValueError("Couldn't match job description to any category")
        print(f"Selected bucket: {bucket}")

        keywords = extracted[bucket].get("ats_keywords", [])
        hints = retrieve_rag_hints(request.resume_text, request.job_description, keywords)

        optimized = optimize_resume(request.resume_text, request.job_description, hints)

        if "<think>" in optimized and "</think>" in optimized:
            start_think = optimized.find("<think>")
            end_think = optimized.find("</think>") + len("</think>")
            optimized = optimized[:start_think] + optimized[end_think:]
        parts = optimized.split('---')
        if len(parts) >= 3:
            optimized = parts[1].strip()
        else:
            raise ValueError("Could not find content between --- markers.")
        with open('../optimized.txt', 'w', encoding='utf-8') as f:
            f.write(optimized)
        print(f"Optimized resume written to ../optimized.txt")
        return optimized
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/save-text")
async def save_text(payload: TextPayload):
    filename = f"jd.txt"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(payload.text)

    return {"message": "Text saved successfully", "filename": filename}


@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_path = os.path.join(UPLOAD_DIR, "user1.pdf")

    with open(file_path, "wb") as f:
        contents = await file.read()
        f.write(contents)
    return {"filename": file.filename, "status": "Uploaded successfully"}


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
        print("Debug message: "+e, flush=True)
        raise HTTPException(status_code=500, detail=str(e)) from e


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
        raise HTTPException(status_code=500, detail=str(e)) from e


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
      raise HTTPException(status_code=500, detail=str(e)) from e     


@app.post("/score_impact", response_model=ActionWordResponse)
def score_impact_endpoint(request: ActionWordRequest):
    try:
        score, _matched, _missing = impact_scorer.score_impact(request.resume_text)
        return ActionWordResponse(score=float(score))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error scoring impact: {str(e)}")


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
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}") from e


@app.get("/bot/webhooks/state")
def bot_webhook_current_state(sender_id: str):
    return app.state.data.get(sender_id, {})


@app.post("/bot/webhooks/state")
def bot_webhook_current_state_update(sender_id: str, state: dict):
    app.state.data[sender_id] = state
    return Response(status_code=status.HTTP_201_CREATED)


@app.post("/bot/webhooks/job_title")
def bot_webhook_job_title(sender: str, message: str):
    response = requests.post(config.BOT_CHAT_URL, json={"sender": sender, "message": message})
    if response.ok:
        return JSONResponse(response.json())
    else:
        raise HTTPException(status_code=500, detail="Could not reach BOT server.")

# To run the server, use: uvicorn filename:app --reload
