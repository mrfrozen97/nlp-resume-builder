import os
os.environ["TRANSFORMERS_NO_TF"] = "1"
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset, load_from_disk
import torch
import os
import json

# ---------- CONFIG ----------
MODEL_DIR = "./bert-match-model"
EPOCHS = 3
BATCH_SIZE = 8

# ---------- Load List of JSON ----------
with open("../label_dataset/formatted_workex.json", "r", encoding="utf-8") as f:
    data = json.load(f)["data"]
    for i in range(len(data)):
        data[i]["label"] = 1 if data[i]["label"] == "positive" else 0
        print(data[i]["label"])

# ---------- Convert to HF Dataset ----------
dataset = Dataset.from_list(data)

# ---------- Tokenization ----------
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

def tokenize(example):
    return tokenizer(
        example["job_description"],
        example["work_experience"],
        truncation=True,
        padding="max_length",
        max_length=512
    )

dataset = dataset.map(tokenize, batched=True)

# ---------- Format for PyTorch ----------
dataset = dataset.train_test_split(test_size=0.1, seed=42)
dataset.set_format(type="torch", columns=["input_ids", "token_type_ids", "attention_mask", "label"])

# ---------- Load Model ----------
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

# ---------- Training ----------
training_args = TrainingArguments(
    output_dir=MODEL_DIR,
    per_device_train_batch_size=BATCH_SIZE,
    num_train_epochs=EPOCHS,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_dir=f"{MODEL_DIR}/logs",
    load_best_model_at_end=True,
    learning_rate=0.0001
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer
)

trainer.train()
model.save_pretrained(MODEL_DIR)
tokenizer.save_pretrained(MODEL_DIR)
print(f"✅ Model saved to: {MODEL_DIR}")

# ---------- Load Model & Predict Function ----------
def load_model_and_tokenizer(model_path=MODEL_DIR):
    model = BertForSequenceClassification.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)
    return model.eval(), tokenizer

def predict_match(job_description, work_experience, model=None, tokenizer=None):
    if model is None or tokenizer is None:
        model, tokenizer = load_model_and_tokenizer()

    inputs = tokenizer(
        job_description,
        work_experience,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=512
    )
    #input["labels"] = label2id[example["label"]]  # Convert string label to int

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)
        prediction = torch.argmax(probs, dim=1).item()
        confidence = probs[0][prediction].item()

    label = "Match" if prediction == 1 else "No Match"
    return {"label": label, "confidence": round(confidence, 3)}

# ---------- Example ----------
example = predict_match(
    "Seeking Python backend developer for cloud services...",
    "Worked on AWS Lambda functions with Python backend..."
)
print("🔍 Prediction:", example)
