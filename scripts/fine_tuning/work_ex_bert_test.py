from transformers import BertTokenizer, BertForSequenceClassification
import torch
import json

# Load model and tokenizer
model_path = "./bert-match-model"  # Or wherever you saved the model
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)
model.eval()

# Optional label map (based on your training data)
label_map = {0: "negative", 1: "positive"}

# Example inputs
job_description = "Requires Java and Python"
work_experience = "Worked on php, c++"
data = json.load(open("../../data/cleaned/all_job_descriptions.json"))

for i in data:
    # Tokenize as a sequence pair
    inputs = tokenizer(
        job_description,
        work_experience,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=512
    )

    # Predict
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        prediction = torch.argmax(logits, dim=1).item()

    print(f"Prediction: {label_map[prediction]}")
