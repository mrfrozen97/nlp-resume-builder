# nlp-resume-builder

---
# Resume Scoring UI Setup
## Instructions to Run

1. cd resume-builder-ui (move to the directory)
2. Install the dependency `npm install`
3. Start a development server `npm run dev`
4. Open your browser and visit [http://localhost:3000](http://localhost:3000) to see OpenResume live

---
# Resume Scoring FastAPI Backend

This is a lightweight FastAPI service that scores a resume against a job description based on skill matching using TF-IDF weights.


## 🛠 Setup Instructions

1. **Install required packages**:

```bash
pip install fastapi uvicorn scikit-learn pandas spacy joblib
python -m spacy download en_core_web_sm
```

---

## 🚀 Running the API Server

Inside the `fastapi-backend` folder, run:

```bash
uvicorn main:app --reload
```

- Server will start at: `http://127.0.0.1:8000`
- You can access automatic API docs at: `http://127.0.0.1:8000/docs`

## 📨 Usage

### Endpoint: `/score_resume`

- **Method**: POST
- **Request Body** (JSON):

```json
{
  "resume_text": "<Paste your resume text here>",
  "job_description": "<Paste your job description text here>"
}
```

- **Response** (JSON):

```json
{
  "normalized_score": 0.85,
  "matched_skills": {
    "java": 0.6,
    "javascript": 0.25
  },
  "missing_skills": {}
}
```

### Endpoint: `/bot/ping`

- **Method**: GET

- **Response** (text):

```json
true
```

### Endpoint: `/bot/chat`

- **Method**: POST
- **Request Body** (JSON):

```json
{
  "sender": "<User id>",
  "message": "<Paste your prompt here>"
}
```

- **Response** (JSON):

```json
{
  "recipient_id": "<User id>",
  "text": "<Bot response>"
}
```
---

# 📄 Resume Scorer

This script scores a candidate's **resume** against a **job description (JD)** based on a predefined list of Computer Science skills using **TF-IDF weighting**.
### Location: src/score_resumes.py
## 🚀 What It Does

- Uses NLP library spaCy to extract relevant skills from both JD and resume.
- Trains and loads a TF-IDF model based on job descriptions to weigh skill importance.
- Compares resume skills with JD-required skills.
- Uses a predetermined vocabulary list of CS related job skills.
- Calculates:
  - 🎯 A **normalized match score** (0 to 1).
  - ✅ A **list of matched skills** with weights (sorted by importance).
  - ❌ A **list of missing but important skills** (also sorted).

## 📦 Output Example

```python
🎯 Score: 0.52
✅ Matched Skills (with weights): {'python': 0.26, 'sql': 0.34}
❌ Missing Skills (with weights): {'kubernetes': 0.90, 'r': 0.0}
```
