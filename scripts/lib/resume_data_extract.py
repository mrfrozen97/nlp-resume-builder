import pandas as pd
import re
from extract_skills import SkillsExtractor
import json

resume_df = pd.read_csv("../../data/resumes/UpdatedResumeDataSet.csv")



def extract_email_from_resume(text):
    email = None

    # Use regex pattern to find a potential email address
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    if match:
        email = match.group()

    return email



if __name__ == '__main__':
    text = open("../../optimized_resumes/data_engineer_resume.txt", "r").read()
    email = extract_email_from_resume(text)

    skills = SkillsExtractor.extract_skills_from_resume(text)
    print(skills)
    data = json.load(open("../../data/script/linkedin/data/software_intern_data.json", "r"))["1"]["description"]
    print(SkillsExtractor.extract_skills_from_resume(data))
    print(SkillsExtractor.extract_skills_from_resume(json.load(open("sample.json", "r"))["content"]))
    if email:
        print("Email:", email)
    else:
        print("Email not found")

