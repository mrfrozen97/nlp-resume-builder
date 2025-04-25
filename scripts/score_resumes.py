import json
import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from lib.extract_skills import CS_Generic_List, CS_Comprehensive_List


class ResumeScore:
    def __init__(self, jd_json_path="../data/script/linkedin/data/software_intern_data.json",
                 vectorizer_path="../data/cache/tfidf_vectorizer.pkl"):

        # -------------------------------
        # Your predefined CS skills list
        # -------------------------------
        self.skills_list = CS_Generic_List + CS_Comprehensive_List
        self.vectorizer_path = vectorizer_path

        # Normalize skill list
        self.skills_set = set(skill.lower().strip() for skill in self.skills_list)

        # -------------------------------
        # Step 1: Job Descriptions
        # -------------------------------
        file_data = json.load(open(jd_json_path, "r"))
        self.job_descriptions = [file_data[i]["description"] for i in file_data if file_data[i] is not None]

        # -------------------------------
        # Step 2: spaCy Tokenizer
        # -------------------------------
        self.nlp = spacy.load("en_core_web_sm")

    def extract_relevant_skills_without_tokens(self, text):
        text_lower = text.lower()
        return [skill for skill in self.skills_set if skill in text_lower]


    def extract_relevant_skills(self, text):
        doc = self.nlp(text.lower())
        tokens = [token.lemma_ for token in doc
                  if not token.is_stop and not token.is_punct and not token.like_num]
        return set([token for token in tokens if token in self.skills_set]
                    + self.extract_relevant_skills_without_tokens(text))

    def train(self):
        # Join filtered skills for TF-IDF
        preprocessed_jds = [" ".join(self.extract_relevant_skills(jd)) for jd in self.job_descriptions]

        # -------------------------------
        # Step 3: Train TF-IDF Vectorizer (on skill tokens only)
        # -------------------------------
        vectorizer = TfidfVectorizer(vocabulary=sorted(self.skills_set))  # restrict to predefined skills
        X = vectorizer.fit_transform(preprocessed_jds)

        # Save TF-IDF weights
        tfidf_df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
        tfidf_df.to_csv("../data/cache/tfidf_weights.csv", index=False)

        # Save vectorizer
        joblib.dump(vectorizer, self.vectorizer_path)

        print("✅ TF-IDF vectorizer trained with predefined skills only!\n")

    # -------------------------------
    # Step 4: Score a Resume Against New JD
    # -------------------------------

    def score_resume(self, new_jd, resume_text):

        # Load vectorizer
        vectorizer = joblib.load(self.vectorizer_path)
        jd_vector = vectorizer.transform([" ".join(self.extract_relevant_skills(new_jd))])
        jd_weights = pd.DataFrame(jd_vector.toarray(), columns=vectorizer.get_feature_names_out())

        resume_tokens = set(self.extract_relevant_skills(resume_text))

        matched_skills = [token for token in jd_weights.columns if token in resume_tokens]
        score = jd_weights[matched_skills].sum(axis=1).values[0]
        max_possible = jd_weights.sum(axis=1).values[0]

        normalized_score = score / max_possible if max_possible else 0
        resume_skills = self.extract_relevant_skills(resume_text)
        jd_skills = self.extract_relevant_skills(new_jd)
        # Skills present in both JD and resume
        present_skills = [skill for skill in jd_weights.columns if skill in resume_skills and skill in jd_skills]

        # Skills present in JD but missing from resume
        missing_skills = [skill for skill in jd_weights.columns if skill in jd_skills and skill not in resume_skills]
        # Sorted dictionary for matched skills
        sorted_matched = dict(
            sorted(
                {skill: jd_weights[skill].values[0] for skill in present_skills}.items(),
                key=lambda item: item[1],
                reverse=True
            )
        )

        # Sorted dictionary for missing skills
        sorted_missing = dict(
            sorted(
                {skill: jd_weights[skill].values[0] for skill in missing_skills}.items(),
                key=lambda item: item[1],
                reverse=True
            )
        )

        return normalized_score, sorted_matched, sorted_missing


if __name__ == "__main__":
    # Score JDS, Sample Run
    jds = json.load(open("../data/script/linkedin/data/software_intern_data.json", "r"))
    for i in jds:
        new_jd = jds[i]["description"]
        resume = open("../optimized_resumes/data_engineer_resume.txt").read()

        obj = ResumeScore(jd_json_path="../data/cleaned/all_job_descriptions.json")
        # Uncooment below line to train against new jds
        #obj.train()
        score, present_skills, missing_skills = obj.score_resume(new_jd, resume)
        print(f"🎯 Score: {score:.2f}")
        print(f"✅ Matched Skills: {present_skills}")
        print(f"X Missing Skills: {missing_skills}")
