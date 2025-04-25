# nlp-resume-builder

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
