import os
import json
import requests

# ─────────────────────────────────────────────────────────────────────────────
# Constants and Configuration
# ─────────────────────────────────────────────────────────────────────────────
# Default to Ollama's generate API endpoint
OLLAMA_URL = os.getenv(
    "OLLAMA_API_URL",
    "http://localhost:11434/api/generate"
)
MODEL_NAME  = "deepseek-r1:7b"
TEMPERATURE = 0.2
MAX_TOKENS  = 2048

# ─────────────────────────────────────────────────────────────────────────────
# Prompt Templates
# ─────────────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are an expert resume optimization assistant. Follow these rules EXACTLY and do NOT reveal your reasoning:

1. Preserve all original headings, section order, and bullet styles—do NOT add or remove sections, except:
   • Replace the current job title in the header with the title that best matches the target job description.
2. Start each existing bullet with a strong action verb (past tense for past roles, present for ongoing).
3. Quantify achievements only if the original bullet already contains numbers; do NOT fabricate any metrics.
4. Integrate these keywords naturally—only when they fit the context:  
   Data, Python, Software, Team, Cloud, Machine Learning, Support, Engineering, SQL, Development.
5. In **Technical Skills**, you may add a few logically implied technologies (e.g., add “NumPy” if “Pandas” is listed), but do NOT introduce unrelated skills.
6. Output ONLY the revised resume text. No new sections, no explanations, no commentary.
""".strip()

USER_PROMPT_TEMPLATE = """
Original Resume:
{resume}

Job Description:
{job_description}

Relevant ATS Keywords:
{keywords}

Optimize the resume according to the SYSTEM instructions above and output ONLY the updated resume text.
""".strip()


# ─────────────────────────────────────────────────────────────────────────────
# Utility: Load Pre-Extracted Data
# ─────────────────────────────────────────────────────────────────────────────
def load_extracted_data(json_path: str) -> dict:
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# ─────────────────────────────────────────────────────────────────────────────
# Step 1: Bucket Selection
# ─────────────────────────────────────────────────────────────────────────────
def select_bucket(job_desc: str, extracted: dict) -> str:
    jd = job_desc.lower()
    best_key, best_score = None, -1
    for key, info in extracted.items():
        score = sum(jd.count(kw.lower()) for kw in info.get("ats_keywords", []))
        if score > best_score:
            best_key, best_score = key, score
    return best_key

# ─────────────────────────────────────────────────────────────────────────────
# Utility: Retrieve RAG Hints
# ─────────────────────────────────────────────────────────────────────────────
def retrieve_rag_hints(resume: str, job_desc: str, keywords: list) -> str:
    return ", ".join(keywords)

# ─────────────────────────────────────────────────────────────────────────────
# Guardrails & Fallbacks
# ─────────────────────────────────────────────────────────────────────────────
def apply_guardrails(text: str) -> str:
    # Placeholder: enforce length and repetition checks
    return text

# ─────────────────────────────────────────────────────────────────────────────
# Core: Optimize Resume via Ollama Generate
# ─────────────────────────────────────────────────────────────────────────────
def optimize_resume(resume: str, job_desc: str, hints: str) -> str:
    prompt = SYSTEM_PROMPT + "\n\n" + USER_PROMPT_TEMPLATE.format(
        resume=resume,
        job_description=job_desc,
        keywords=hints
    )
    payload = {
        "model":       MODEL_NAME,
        "prompt":      prompt,
        "temperature": TEMPERATURE,
        "max_tokens":  MAX_TOKENS,
        "stream":      False
    }
    resp = requests.post(OLLAMA_URL, json=payload)
    resp.raise_for_status()
    data = resp.json()
    optimized = data.get("response", "").strip()
    return apply_guardrails(optimized)

# ─────────────────────────────────────────────────────────────────────────────
# CLI Entry Point
# ─────────────────────────────────────────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Optimize resumes locally with Ollama LLM"
    )
    parser.add_argument("--resume",    required=True, help="Path to candidate's resume text file")
    parser.add_argument("--job_desc",  required=True, help="Path to job description text file")
    parser.add_argument("--extracted", required=True, help="Path to pre-extracted keywords JSON")
    parser.add_argument("--output",    required=True, help="Path to write optimized resume")
    args = parser.parse_args()

    resume   = open(args.resume,    encoding='utf-8').read()
    job_desc = open(args.job_desc,  encoding='utf-8').read()
    extracted = load_extracted_data(args.extracted)

    bucket = select_bucket(job_desc, extracted)
    if not bucket:
        raise ValueError("Couldn't match job description to any category")
    print(f"Selected bucket: {bucket}")

    keywords = extracted[bucket].get("ats_keywords", [])
    hints = retrieve_rag_hints(resume, job_desc, keywords)

    optimized = optimize_resume(resume, job_desc, hints)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(optimized)
    print(f"Optimized resume written to {args.output}")

if __name__ == "__main__":
    main()
