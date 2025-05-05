"""
Resume Optimizer using RAG with open-source models

This script implements a RAG (Retrieval-Augmented Generation) system
to optimize resumes for ATS (Applicant Tracking Systems) using free/open-source models.
"""

import json
import os
from typing import List, Dict, Any, Optional
import re
import requests
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


class ResumeOptimizer:
    """Resume optimization using RAG with open-source models."""

    def __init__(self,
                 job_data_path: str,
                 huggingface_token: Optional[str] = None):
        """
        Initialize the Resume Optimizer.

        Args:
            job_data_path: Path to the JSON file containing scraped job data
            huggingface_token: Optional HuggingFace API token for better rate limits
        """
        self.job_data_path = job_data_path
        self.huggingface_token = huggingface_token or os.environ.get("HUGGINGFACE_API_TOKEN")

        # Load job data
        self.job_data = self._load_job_data()

        # Initialize the sentence transformer model for embeddings
        # This will download the model on first use
        print("Loading embedding model (this may take a moment the first time)...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

        # Create job description embeddings
        self._create_job_embeddings()

        # Initialize TF-IDF vectorizer for keyword extraction
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words='english',
            ngram_range=(1, 2)
        )

    def _load_job_data(self) -> List[Dict[str, Any]]:
        """Load and process job data from JSON file."""
        with open(self.job_data_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        # Process the job data based on the format provided by scraper
        processed_data = []

        # Handle different possible formats from the scraper
        if isinstance(raw_data, dict):  # Format like {id1: job1, id2: job2, ...}
            for key, job in raw_data.items():
                if isinstance(job, dict):  # Ensuring it's a valid job entry
                    processed_data.append({
                        "id": job.get("id", key),
                        "company": job.get("Company", ""),
                        "title": job.get("title", ""),
                        "description": job.get("description", ""),
                        "location": job.get("location", "")
                    })
        elif isinstance(raw_data, list):  # Format like [job1, job2, ...]
            for job in raw_data:
                if isinstance(job, dict):
                    processed_data.append({
                        "id": job.get("id", ""),
                        "company": job.get("Company", job.get("company", "")),
                        "title": job.get("title", ""),
                        "description": job.get("description", ""),
                        "location": job.get("location", "")
                    })

        print(f"Loaded {len(processed_data)} job postings from {self.job_data_path}")
        return processed_data

    def _create_job_embeddings(self):
        """Create embeddings for job descriptions."""
        print("Creating job embeddings...")
        job_texts = [
            f"Job: {job['title']} at {job['company']}. {job['description'][:1000]}"
            for job in self.job_data
        ]

        # Get embeddings using SentenceTransformer
        self.job_embeddings = self.embedding_model.encode(job_texts)
        print(f"Created embeddings for {len(job_texts)} job postings")

    def find_relevant_jobs(self, resume_text: str, job_type: Optional[str] = None, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Find the most relevant job postings for a resume using vector similarity.

        Args:
            resume_text: The text content of the resume
            job_type: Optional filter for job type/title
            top_k: Number of relevant jobs to return

        Returns:
            List of most relevant job postings
        """
        # Get resume embedding
        resume_embedding = self.embedding_model.encode([resume_text])[0]

        # Calculate similarity scores
        similarities = cosine_similarity([resume_embedding], self.job_embeddings)[0]

        # Create a list of (index, similarity) tuples
        job_similarities = list(enumerate(similarities))

        # Filter by job type if provided
        if job_type:
            job_type_lower = job_type.lower()
            filtered_jobs = []

            for idx, sim in job_similarities:
                if job_type_lower in self.job_data[idx]["title"].lower():
                    filtered_jobs.append((idx, sim))

            if filtered_jobs:
                job_similarities = filtered_jobs

        # Sort by similarity (highest first)
        job_similarities.sort(key=lambda x: x[1], reverse=True)

        # Get top_k jobs
        relevant_jobs = []
        for idx, _ in job_similarities[:top_k]:
            relevant_jobs.append(self.job_data[idx])

        return relevant_jobs

    def extract_keywords(self, job_postings: List[Dict[str, Any]], resume_text: str) -> Dict[str, Any]:
        """
        Extract important keywords from job postings using TF-IDF.

        Args:
            job_postings: List of relevant job postings
            resume_text: The text content of the resume

        Returns:
            Dictionary with keyword analysis
        """
        # Combine job descriptions
        job_desc_text = [
            f"{job['title']} {job['description']}"
            for job in job_postings
        ]

        # Fit TF-IDF on job descriptions
        job_tfidf_matrix = self.tfidf_vectorizer.fit_transform(job_desc_text)

        # Get feature names (keywords)
        feature_names = self.tfidf_vectorizer.get_feature_names_out()

        # Calculate the average TF-IDF score for each keyword
        avg_tfidf_scores = job_tfidf_matrix.mean(axis=0).A1

        # Sort keywords by importance
        keyword_scores = list(zip(feature_names, avg_tfidf_scores))
        keyword_scores.sort(key=lambda x: x[1], reverse=True)

        # Get top keywords (limiting to 30 for now)
        top_keywords = [keyword for keyword, _ in keyword_scores[:30]]

        # Check which keywords are in the resume
        resume_lower = resume_text.lower()

        present_keywords = []
        missing_keywords = []

        for keyword in top_keywords:
            if keyword.lower() in resume_lower or self._check_keyword_variant(keyword.lower(), resume_lower):
                present_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)

        return {
            "all_keywords": top_keywords,
            "present_keywords": present_keywords,
            "missing_keywords": missing_keywords
        }

    def _check_keyword_variant(self, keyword: str, text: str) -> bool:
        """Check if a close variant of the keyword exists in the text."""
        # Check for plural/singular variants
        if keyword.endswith('s') and keyword[:-1] in text:
            return True
        if keyword + 's' in text:
            return True

        # Check for hyphenated variants
        if '-' in keyword and keyword.replace('-', ' ') in text:
            return True
        if ' ' in keyword and keyword.replace(' ', '-') in text:
            return True

        return False

    # Find this function in resume_optimizer_free.py and replace it with this improved version

    def get_llm_suggestion(self, prompt: str) -> str:
        """
        Get suggestions from HuggingFace Inference API using a more capable model.

        Args:
            prompt: The prompt for the LLM

        Returns:
            LLM generated text
        """
        # Use Mistral-7B which is more capable than OPT-1.3B
        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        headers = {"Authorization": f"Bearer {self.huggingface_token}"} if self.huggingface_token else {}

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 1000,
                "temperature": 0.7,
                "top_p": 0.95,
                "repetition_penalty": 1.15,
                "do_sample": True
            }
        }

        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            result = response.json()

            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "").strip()
            return "Error: Unexpected response format from the model."

        except Exception as e:
            print(f"Error getting LLM suggestion: {e}")

            # Try a backup model if the first one fails
            try:
                backup_api_url = "https://api-inference.huggingface.co/models/google/flan-t5-xl"
                backup_response = requests.post(backup_api_url, headers=headers, json=payload)
                backup_response.raise_for_status()
                backup_result = backup_response.json()

                if isinstance(backup_result, list) and len(backup_result) > 0:
                    return backup_result[0].get("generated_text", "").strip()
            except:
                pass

            # If all API calls fail, use the rule-based backup
            return self._backup_suggestion_generation(prompt)

    def generate_optimized_resume(self, resume_text: str, job_type: Optional[str] = None) -> str:
        """
        Generate an optimized version of the resume text for better ATS matching.

        Args:
            resume_text: The original text content of the resume
            job_type: Optional job type filter (e.g., "data engineer")

        Returns:
            String containing the optimized resume text
        """
        # Find relevant job postings
        relevant_jobs = self.find_relevant_jobs(resume_text, job_type)

        if not relevant_jobs:
            return resume_text  # Return original if no relevant jobs found

        # Extract keywords
        keyword_analysis = self.extract_keywords(relevant_jobs, resume_text)
        missing_keywords = keyword_analysis["missing_keywords"]

        # Create a dictionary of specific improvements based on resume context
        data_engineering_improvements = {
            # Skills improvements
            "Python": "Python (Pandas, NumPy, PySpark)",
            "Database": "SQL (PostgreSQL, MySQL, Oracle)",
            "Data Structures": "Data Structures, ETL Pipelines",
            "Algorithms": "Algorithms, Data Modeling",

            # Weak verb replacements
            "Created": "Engineered",
            "Made": "Developed",
            "Used": "Leveraged",
            "Provided": "Delivered",
            "Worked": "Collaborated",
            "Helped": "Supported",
            "Assisted": "Facilitated",

            # Context-specific additions
            "weather patterns": "weather patterns using data engineering techniques",
            "database schema": "database schema with SQL optimization",
            "using HTML": "using HTML, CSS, and JavaScript with backend data pipelines",
            "public APIs": "public APIs with automated ETL processes",
            "coding assignments": "coding assignments focused on data processing",
            "coding challenges": "coding challenges and data engineering hackathons",
        }

        # Split the resume into sections and lines
        sections = []
        current_section = []
        current_section_name = "HEADER"

        for line in resume_text.split('\n'):
            # Detect if this is a section header
            if line.strip().upper() == line.strip() and len(line.strip()) > 2:
                if current_section:
                    sections.append((current_section_name, current_section))
                current_section = []
                current_section_name = line.strip()
            current_section.append(line)

        # Add the last section
        if current_section:
            sections.append((current_section_name, current_section))

        # Process each section appropriately
        optimized_sections = []

        for section_name, section_lines in sections:
            optimized_section = []

            # Handle the header section specially
            if section_name == "HEADER":
                for i, line in enumerate(section_lines):
                    if i == 0:  # Name line
                        optimized_section.append(line)
                    elif i == 1:  # Title line
                        if job_type:
                            optimized_section.append(job_type.title())
                        else:
                            optimized_section.append("Data Engineer")  # Default if no job type specified
                    else:
                        optimized_section.append(line)

            # Handle the skills section
            elif "SKILL" in section_name:
                for line in section_lines:
                    if ":" in line:
                        # Split into label and skills list
                        label, skills_text = line.split(":", 1)
                        skills = [s.strip() for s in skills_text.split(",")]

                        # Enhance existing skills with more specific versions
                        enhanced_skills = []
                        for skill in skills:
                            if skill in data_engineering_improvements:
                                enhanced_skills.append(data_engineering_improvements[skill])
                            else:
                                enhanced_skills.append(skill)

                        # Add missing relevant skills (up to 3)
                        relevant_missing = [
                            "SQL", "ETL", "Data Pipelines", "Data Modeling",
                            "Data Engineering", "Database Design"
                        ]

                        added = 0
                        for skill in relevant_missing:
                            if added >= 3:
                                break
                            if not any(skill.lower() in s.lower() for s in enhanced_skills):
                                enhanced_skills.append(skill)
                                added += 1

                        optimized_section.append(f"{label}: {', '.join(enhanced_skills)}")
                    else:
                        optimized_section.append(line)

            # Handle projects and experience
            elif any(keyword in section_name for keyword in ["PROJECT", "EXPERIENCE"]):
                current_project = None

                for line in section_lines:
                    # Check if this is a project title line
                    if "(" in line and ")" in line and "-" not in line:
                        current_project = line
                        # Don't add "Data Engineer" to every project - it looks artificial
                        optimized_section.append(line)

                    # Check if this is a bullet point
                    elif line.strip().startswith("-"):
                        # Apply targeted improvements based on context
                        improved_line = line

                        # Replace weak verbs with stronger alternatives
                        for weak, strong in [(k, v) for k, v in data_engineering_improvements.items()
                                             if len(k.split()) == 1]:  # Only single words
                            if weak in improved_line:
                                improved_line = improved_line.replace(weak, strong)

                        # Add context-specific enhancements
                        for context, enhancement in [(k, v) for k, v in data_engineering_improvements.items()
                                                     if len(k.split()) > 1]:  # Only phrases
                            if context in improved_line.lower():
                                improved_line = improved_line.lower().replace(context, enhancement)
                                # Restore capitalization if needed
                                if line[0].isupper():
                                    improved_line = improved_line[0].upper() + improved_line[1:]

                        # If no improvements were made, consider adding a relevant keyword
                        if improved_line == line:
                            # Look for opportunities to add specificity
                            if "database" in line.lower() and not any(
                                    kw in line.lower() for kw in ["sql", "postgres", "mysql"]):
                                improved_line = line.rstrip() + " using SQL and database optimization techniques"
                            elif "python" in line.lower() and not any(
                                    kw in line.lower() for kw in ["pandas", "numpy", "pyspark"]):
                                improved_line = line.rstrip() + " with Pandas for efficient data processing"
                            elif "data" in line.lower() and not any(
                                    kw in line.lower() for kw in ["etl", "pipeline", "transform"]):
                                improved_line = line.rstrip() + " implementing ETL best practices"

                        optimized_section.append(improved_line)
                    else:
                        optimized_section.append(line)

            # Other sections - keep as is
            else:
                optimized_section.extend(section_lines)

            # Add the processed section
            optimized_sections.append((section_name, optimized_section))

        # Combine all sections back into a resume
        optimized_lines = []
        for section_name, section_lines in optimized_sections:
            optimized_lines.extend(section_lines)

        return '\n'.join(optimized_lines)

    def _fallback_resume_optimization(self, resume_text: str, keyword_analysis: Dict) -> str:
        """Conservative fallback method to optimize the resume when the LLM approach fails."""
        lines = resume_text.split('\n')
        optimized_lines = []

        # Get important missing keywords
        missing_keywords = keyword_analysis["missing_keywords"][:10]

        # Track which sections we've modified to distribute keywords
        modified_skills = False
        modified_exp_lines = 0

        # Process the resume line by line
        for line in lines:
            # Skip empty lines
            if not line.strip():
                optimized_lines.append(line)
                continue

            # Look for job title/role near the top
            if len(optimized_lines) < 5 and any(w in line.lower() for w in ["developer", "engineer", "analyst"]):
                # Find the most relevant title from keywords
                relevant_titles = [kw for kw in missing_keywords if
                                   any(t in kw.lower() for t in ["engineer", "developer", "analyst"])]
                if relevant_titles:
                    optimized_lines.append(relevant_titles[0].title())  # Use the first relevant title
                    continue

            # Check if this is a skills line that could be enhanced
            if (not modified_skills and
                    any(keyword in line.lower() for keyword in
                        ["skills", "technical", "technologies", "proficiencies"])):

                modified_skills = True
                # Get missing keywords related to skills/technologies
                tech_keywords = [kw for kw in missing_keywords
                                 if kw.lower() not in line.lower()]

                if tech_keywords and ":" in line:
                    # Add relevant missing tech keywords to skills line
                    prefix, skills = line.split(":", 1)
                    current_skills = [s.strip() for s in skills.split(",")]

                    # Add up to 3 new relevant keywords
                    new_skills = current_skills.copy()
                    for kw in tech_keywords[:3]:
                        if not any(kw.lower() in skill.lower() for skill in current_skills):
                            new_skills.append(kw)

                    optimized_lines.append(f"{prefix}: {', '.join(new_skills)}")
                    continue

            # Enhance action verbs in experience bullet points (limit to 3 modifications)
            if (modified_exp_lines < 3 and
                    (line.strip().startswith("-") or line.strip().startswith("•"))):

                modified_exp_lines += 1

                # Replace weak verbs with stronger ones
                weak_verbs = ["worked", "helped", "did", "made", "used", "was responsible for"]
                strong_verbs = ["developed", "implemented", "engineered", "optimized", "designed", "analyzed",
                                "created", "built", "managed", "led", "coordinated", "executed"]

                line_lower = line.lower()
                modified = False

                # Replace weak verbs with stronger ones
                for weak_verb in weak_verbs:
                    if weak_verb in line_lower:
                        # Randomly select a stronger verb
                        import random
                        strong_verb = random.choice(strong_verbs)

                        # Replace the weak verb with the strong one (preserve capitalization)
                        if weak_verb[0].isupper():
                            strong_verb = strong_verb.capitalize()

                        line = line.replace(weak_verb, strong_verb)
                        modified = True
                        break

                # Try to add one missing keyword if we haven't already modified the line
                if not modified and missing_keywords:
                    for keyword in missing_keywords:
                        if keyword.lower() not in line.lower():
                            # Add keyword to the end if it doesn't make the line too long
                            if len(line.split()) < 15:
                                if line.strip().endswith("."):
                                    line = line[:-1] + f", utilizing {keyword}."
                                else:
                                    line = line + f", utilizing {keyword}"
                            break

            # Add the processed line to the result
            optimized_lines.append(line)

        return '\n'.join(optimized_lines)

    def _backup_suggestion_generation(self, prompt: str) -> str:
        """Generate suggestions using a rule-based approach as backup."""
        # Extract the missing keywords from the prompt
        missing_keywords_match = re.search(r"Missing Keywords: (.*?)(?:\n|$)", prompt)
        missing_keywords = []

        if missing_keywords_match:
            missing_keywords = [kw.strip() for kw in missing_keywords_match.group(1).split(",")]

        # Generate rule-based suggestions
        suggestions = [
            "### Resume ATS Optimization Suggestions",

            "#### 1. Add Missing Keywords",
            "Your resume is missing some important keywords that appear in relevant job descriptions:",
            ", ".join(missing_keywords[:10]),
            "Consider naturally incorporating these terms into your experience and skills sections.",

            "#### 2. Structure Recommendations",
            "For optimal ATS parsing, use these standard section headers:",
            "- Professional Summary",
            "- Skills",
            "- Experience",
            "- Education",
            "- Projects",

            "#### 3. Skills Section Optimization",
            "Create a dedicated skills section with bullet points or a clean list that includes both technical and soft skills relevant to the position.",

            "#### 4. Quantify Accomplishments",
            "Add specific metrics and numbers to quantify your achievements. Instead of 'Improved website performance', say 'Improved website load time by 40%'.",

            "#### 5. Use Action Verbs",
            "Start your experience bullet points with strong action verbs such as 'Developed', 'Implemented', 'Engineered', 'Designed', etc."
        ]

        return "\n\n".join(suggestions)

    def optimize_resume(self, resume_text: str, job_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Optimize a resume for ATS using RAG.

        Args:
            resume_text: The text content of the resume
            job_type: Optional job type filter (e.g., "software engineer")

        Returns:
            Dictionary with optimization results
        """
        # Find relevant job postings
        relevant_jobs = self.find_relevant_jobs(resume_text, job_type)

        if not relevant_jobs:
            return {
                "error": "No relevant job postings found. Try a different job type or add more job data."
            }

        # Extract keywords
        keyword_analysis = self.extract_keywords(relevant_jobs, resume_text)

        # Prepare job descriptions text
        job_descriptions = "\n\n".join([
            f"JOB {i+1}: {job['title']} at {job['company']}\n{job['description'][:500]}..."  # Truncate for brevity
            for i, job in enumerate(relevant_jobs[:3])  # Limit to top 3 for prompt length
        ])

        # Format missing keywords
        missing_keywords = ", ".join(keyword_analysis["missing_keywords"])
        present_keywords = ", ".join(keyword_analysis["present_keywords"])

        # Create prompt for LLM
        prompt = f"""
        # Resume Optimization Task
        
        You are an expert in optimizing resumes for ATS (Applicant Tracking Systems).
        
        ## Resume:
        {resume_text}
        
        ## Relevant Job Descriptions:
        {job_descriptions}
        
        ## Keyword Analysis:
        Present Keywords: {present_keywords}
        Missing Keywords: {missing_keywords}
        
        ## Task:
        Provide 5-7 specific, actionable suggestions to improve this resume for ATS optimization.
        Focus on:
        
        1. Including missing keywords naturally
        2. Improving structure for better ATS parsing
        3. Enhancing phrasing with action verbs
        4. Quantifying achievements when possible
        5. Overall format recommendations
        
        ## Output Format:
        Provide suggestions as a list with clear explanations and examples.
        """

        # Get LLM suggestions
        print("Generating optimization suggestions...")
        suggestions = self.get_llm_suggestion(prompt)

        return {
            "relevant_jobs": [
                {
                    "title": job["title"],
                    "company": job["company"],
                    "location": job["location"]
                }
                for job in relevant_jobs
            ],
            "keyword_analysis": keyword_analysis,
            "optimization_suggestions": suggestions
        }


if __name__ == "__main__":
    # Example usage (for testing)
    optimizer = ResumeOptimizer(
        job_data_path="data/job_data/software_intern_data.json",
    )

    # Example resume
    sample_resume = """
    JANE DOE
    jdoe@email.com | (555) 123-4567 | github.com/janedoe
    
    EDUCATION
    University of Technology
    Bachelor of Science in Computer Science, GPA: 3.8/4.0
    Relevant Coursework: Data Structures, Algorithms, Database Systems, Web Development
    
    SKILLS
    Programming: Java, Python, HTML/CSS
    Tools: Git, VS Code
    
    PROJECTS
    Personal Website (2023)
    - Created a personal portfolio website using HTML and CSS
    - Hosted on GitHub Pages
    
    Inventory Management System (2022)
    - Developed a Java application to track inventory
    - Implemented database connectivity using SQL
    
    EXPERIENCE
    Tech Solutions Inc., IT Intern (Summer 2022)
    - Assisted with troubleshooting hardware and software issues
    - Helped maintain company website
    - Participated in weekly team meetings
    """

    # Test the optimizer
    results = optimizer.optimize_resume(sample_resume, job_type="software intern")

    # Print results
    print("\n" + "="*80)
    print("RESUME OPTIMIZATION RESULTS")
    print("="*80 + "\n")

    print("RELEVANT JOBS:")
    for i, job in enumerate(results["relevant_jobs"]):
        print(f"{i+1}. {job['title']} at {job['company']} ({job['location']})")

    print("\nKEYWORD ANALYSIS:")
    print("Present Keywords:", ", ".join(results["keyword_analysis"]["present_keywords"][:10]))
    print("Missing Keywords:", ", ".join(results["keyword_analysis"]["missing_keywords"][:10]))

    print("\nOPTIMIZATION SUGGESTIONS:")
    print(results["optimization_suggestions"])