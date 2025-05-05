# NLP Resume Optimizer

A tool that helps optimize your resume for specific job applications by analyzing job descriptions and suggesting improvements.

## What it does

- Analyzes your resume against relevant job postings
- Identifies important keywords you're missing
- Suggests ways to improve your resume
- Can generate an optimized version of your resume

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/nlp-resume-builder.git
cd nlp-resume-builder

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Analyze your resume:

```bash
python scripts/test_optimizer.py --resume sample_resumes/your_resume.txt --job-type "data engineer" --job-data "data/job_data/data_engineering_data.json"
```

### Generate an optimized resume:

```bash
python scripts/test_optimizer.py --resume sample_resumes/your_resume.txt --job-type "data engineer" --job-data "data/job_data/data_engineering_data.json" --generate-optimized-resume --optimized-output "optimized_resumes/optimized_resume.txt"
```

## Main Options

- `--resume, -r`: Path to your resume file (txt format)
- `--job-type, -j`: Target job type (e.g., "software engineer")
- `--job-data, -d`: Path to job data file
- `--generate-optimized-resume, -g`: Create an optimized resume
- `--optimized-output, -oo`: Where to save the optimized resume
- `--huggingface-token, -t`: Optional HuggingFace API token for better results

## How It Works

1. Finds jobs similar to your background
2. Extracts important keywords from those jobs
3. Compares your resume to identify missing keywords
4. Suggests improvements or creates an optimized version

## Data Collection

The repository includes a LinkedIn job scraper to collect job posting data:

```bash
cd data/script/linkedin
# Follow README.md instructions to collect job data
```
## Basic overview 
The core functionality is implemented in resume_optimizer.py, which uses a Retrieval-Augmented Generation (RAG) approach with sentence embeddings to match resumes against job descriptions. The system processes job data scraped from LinkedIn (using the script in data/script/linkedin/linkedin-job-scrape.py), extracts relevant keywords using TF-IDF vectorization, and identifies missing keywords in the resume. It then generates optimization suggestions using either a HuggingFace API or a fallback rule-based approach. There's also a React-based UI component (in the resume-builder-ui directory) that appears to be in the early stages of development. The focus of the project, as stated in research.md, is on specificity - helping users tailor their resumes with strategic keyword integration and ATS-friendly formatting.

## License

MIT
