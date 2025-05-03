import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

from transformers import LongformerTokenizer, LongformerForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import json
import torch
torch.cuda.empty_cache()

print("GPU available:", torch.cuda.is_available())

# ---------- CONFIG ----------
MODEL_DIR = "./longformer-match-model"
EPOCHS = 3
BATCH_SIZE = 4  # Adjust based on your GPU memory (e.g., 8 or 16 if you have 8GB+)
MAX_LENGTH = 1024  # Can increase if average input is longer
GRAD_ACCUM_STEPS = 2  # Simulates BATCH_SIZE * GRAD_ACCUM_STEPS effective batch size

# ---------- Load JSON ----------
with open("../label_dataset/formatted_workex.json", "r", encoding="utf-8") as f:
    data = json.load(f)["data"]
    for i in range(len(data)):
        data[i]["label"] = 1 if data[i]["label"] == "positive" else 0

# ---------- Dataset ----------
dataset = Dataset.from_list(data)

# ---------- Tokenizer ----------
tokenizer = LongformerTokenizer.from_pretrained("allenai/longformer-base-4096")

def tokenize(example):
    return tokenizer(
        example["job_description"],
        example["work_experience"],
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH
    )

dataset = dataset.map(tokenize, batched=True)

# ---------- Analyze Token Lengths (optional but helpful) ----------
avg_len = sum(len(x["input_ids"]) for x in dataset) / len(dataset)
print(f"📏 Average input length: {avg_len:.2f} tokens")

# ---------- Split & Format ----------
dataset = dataset.train_test_split(test_size=0.1, seed=42)
dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

# ---------- Load Model ----------
model = LongformerForSequenceClassification.from_pretrained(
    "allenai/longformer-base-4096", num_labels=2
)

# ---------- Training Arguments ----------
training_args = TrainingArguments(
    output_dir=MODEL_DIR,
    per_device_train_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=GRAD_ACCUM_STEPS,
    num_train_epochs=EPOCHS,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_dir=f"{MODEL_DIR}/logs",
    load_best_model_at_end=True,
    learning_rate=1e-4,
    fp16 = False,  # Enable only if supported
)

# ---------- Trainer ----------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer
)

trainer.train()

# ---------- Save ----------
model.save_pretrained(MODEL_DIR)
tokenizer.save_pretrained(MODEL_DIR)
print(f"✅ Model saved to: {MODEL_DIR}")
