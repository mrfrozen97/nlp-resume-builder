from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from score_resumes import ResumeScore  # Assuming the code you provided is saved as ResumeScore.py
import requests
import config

app = FastAPI()
app.state.data = {}

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
