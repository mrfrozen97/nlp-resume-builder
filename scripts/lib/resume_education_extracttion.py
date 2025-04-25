import re
from typing import List, Dict, Optional
import spacy

nlp = spacy.load("en_core_web_sm")

class ResumeEducation:
    def __init__(self):
        self.school = ""
        self.degree = ""
        self.gpa = ""
        self.date = ""
        self.descriptions = []

def extract_education(resume_text: str) -> Dict[str, List[ResumeEducation]]:
    # Preprocess text to clean it up
    resume_text = re.sub(r'\s+', ' ', resume_text).strip()

    # Split into lines and remove empty lines
    lines = [line.strip() for line in resume_text.split('\n') if line.strip()]

    # Find education section
    education_start = -1
    for i, line in enumerate(lines):
        if "education" in line.lower():
            education_start = i
            break

    if education_start == -1:
        return {"educations": []}

    # Get education section lines (until next section or end)
    education_lines = []
    section_keywords = ["experience", "skills", "projects", "work"]
    for line in lines[education_start + 1:]:
        if any(keyword in line.lower() for keyword in section_keywords):
            break
        education_lines.append(line)

    # Process education entries
    educations = []
    current_edu = ResumeEducation()
    bullet_pattern = re.compile(r'^[•\-*>\s]+\s*(.+)')

    for line in education_lines:
        # Check for school (highest priority)
        if any(school in line for school in ['University', 'College', 'Institute']):
            if current_edu.school:  # If we already have a school, save current and start new
                educations.append(current_edu)
                current_edu = ResumeEducation()
            current_edu.school = line
            continue

        # Check for degree
        if any(degree in line for degree in ['Bachelor', 'Master', 'PhD', 'B.S.', 'M.S.']):
            current_edu.degree = line
            continue

        # Check for GPA
        gpa_match = re.search(r'GPA[:]?\s*([0-4]\.\d{1,2})', line, re.IGNORECASE)
        if gpa_match:
            current_edu.gpa = gpa_match.group(1)
            continue

        # Check for date (year range)
        date_match = re.search(r'(20\d{2}\s*[-–]\s*20\d{2}|20\d{2}\s*[-–]\s*Present)', line)
        if date_match:
            current_edu.date = date_match.group()
            continue

        # Check for bullet points
        bullet_match = bullet_pattern.match(line)
        if bullet_match:
            current_edu.descriptions.append(bullet_match.group(1))

    if current_edu.school:  # Add the last education entry
        educations.append(current_edu)

    # Extract courses from separate section if exists
    courses_section = []
    for i, line in enumerate(lines):
        if "course" in line.lower() and "education" not in line.lower():
            courses_section = lines[i+1:i+4]  # Get next few lines
            break

    if courses_section and educations:
        courses = []
        for line in courses_section:
            # Split by commas/semicolons and clean up
            parts = re.split(r'[,;]', line)
            courses.extend([part.strip() for part in parts if part.strip()])

        if courses:
            educations[0].descriptions.append(f"Courses: {', '.join(courses)}")

    return {"educations": educations}

# Example usage with your problematic text
if __name__ == "__main__":
    resume_text = """
    EDUCATION
    University of California, Berkeley
    Bachelor of Science in Computer Science
    GPA: 3.8
    2015 - 2019
    • Relevant Coursework: Algorithms, Data Structures, Machine Learning
    • Honors: Dean's List
    
    COURSES
    Advanced Machine Learning, Computer Vision, Natural Language Processing
    """

    result = extract_education(resume_text)
    print(result)
    for i, edu in enumerate(result["educations"]):
        print(f"\nEducation #{i + 1}:")
        print(f"School: {edu.school}")
        print(f"Degree: {edu.degree}")
        print(f"GPA: {edu.gpa}")
        print(f"Date: {edu.date}")
        print("Descriptions:")
        for desc in edu.descriptions:
            print(f"- {desc}")
