import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import spacy



class ImpactScore:
    def __init__(self,
                 resume_csv_path="../data/resumes/UpdatedResumeDataSet.csv",
                 vectorizer_path="../data/cache/impact_tfidf_vectorizer.pkl",
                 action_word_file="../data/impact/action_words.txt"):

        # Load Action Words
        self.action_words = self._load_action_words(action_word_file)
        self.vectorizer_path = vectorizer_path
        self.action_set = set(word.lower().strip() for word in self.action_words)

        # Load Resumes (CSV with 'Resume' column)
        self.resume_df = pd.read_csv(resume_csv_path)
        if "Resume" not in self.resume_df.columns:
            raise ValueError("CSV must contain a 'Resume' column.")

        # SpaCy Tokenizer
        self.nlp = spacy.load("en_core_web_sm")

    def _load_action_words(self, path):
        with open(path, 'r') as f:
            return [line.strip() for line in f if line.strip()]

    def calculate_quantitative_impact(self, text):
        nlp = spacy.load("en_core_web_sm")
        IMPACT_ENTITY_LABELS = [
                "CARDINAL",    # e.g., 20 million records
                "PERCENT",     # e.g., 50% optimized
                "MONEY",       # e.g., saved $10,000
                "QUANTITY",    # e.g., 500 GB processed
                "TIME",        # e.g., in 2 hours
            ]
        score = 0
        used_types = set()
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in IMPACT_ENTITY_LABELS:
                score += 5
                used_types.add(ent.label_)
        # Bonus if multiple types are present
        score += len(used_types) * 5
        score = min((score/100), 1)

        return score

    def extract_relevant_verbs(self, text):
        doc = self.nlp(text.lower())
        tokens = [token.lemma_ for token in doc
                  if token.pos_ == "VERB" and not token.is_stop and not token.is_punct]
        return set(token for token in tokens if token in self.action_set)

    def extract_relevant_verbs_without_tokens(self, text):
        text_lower = text.lower()
        return {word for word in self.action_set if word in text_lower}

    def extract_all_relevant_verbs(self, text):
        return self.extract_relevant_verbs(text).union(self.extract_relevant_verbs_without_tokens(text))

    def train(self):
        resumes = self.resume_df["Resume"].fillna("").astype(str).tolist()
        preprocessed = [" ".join(self.extract_all_relevant_verbs(resume)) for resume in resumes]

        vectorizer = TfidfVectorizer(vocabulary=sorted(self.action_set))
        X = vectorizer.fit_transform(preprocessed)

        # Save vectorizer
        joblib.dump(vectorizer, self.vectorizer_path)

        # Optionally save weights to CSV
        tfidf_df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
        tfidf_df.to_csv("../data/cache/impact_tfidf_weights.csv", index=False)

        print("TF-IDF vectorizer trained on action words from resumes!")

    def score_impact(self, resume_text):
        vectorizer = joblib.load(self.vectorizer_path)

        tfidf_vector = vectorizer.transform([" ".join(self.extract_all_relevant_verbs(resume_text))])
        tfidf_weights = pd.DataFrame(tfidf_vector.toarray(), columns=vectorizer.get_feature_names_out())

        verbs_in_resume = set(self.extract_all_relevant_verbs(resume_text))

        matched = [verb for verb in tfidf_weights.columns if verb in verbs_in_resume]
        score = tfidf_weights[matched].sum(axis=1).values[0]
        max_possible = tfidf_weights.sum(axis=1).values[0]

        normalized_score = score / max_possible if max_possible else 0

        quant_score = self.calculate_quantitative_impact(resume_text)

        combined_score = (0.5 * normalized_score) + (0.5 * quant_score)

        sorted_matched = dict(
            sorted(
                {verb: tfidf_weights[verb].values[0] for verb in matched if tfidf_weights[verb].values[0] != 0}.items(),
                key=lambda item: item[1],
                reverse=True
            )
        )

        missing = [verb for verb in tfidf_weights.columns if verb not in verbs_in_resume]
        sorted_missing = dict(
            sorted(
                {verb: tfidf_weights[verb].values[0] for verb in missing if tfidf_weights[verb].values[0] != 0}.items(),
                key=lambda item: item[1],
                reverse=True
            )
        )

        return combined_score, sorted_matched, sorted_missing

if __name__ == "__main__":
    scorer = ImpactScore(
    )

    # Train on resumes
    # scorer.train()

    # Score a new resume
    new_resume = open("../optimized_resumes/data_engineer_resume.txt").read()
    score, matched, missing = scorer.score_impact(new_resume)
    print(scorer.calculate_quantitative_impact(new_resume))
    print(f"Impact Score: {score:.2f}")
    print(f"Matched Verbs: {matched}")
    print(f"Missing Verbs: {missing}")
