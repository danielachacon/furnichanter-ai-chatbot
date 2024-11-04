from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForTokenClassification, TrainingArguments, Trainer
from transformers import DataCollatorForTokenClassification
import numpy as np

# Load the dataset and split it into train and validation sets
dataset = load_dataset("json", data_files="ner_dataset_extended.json")
dataset = dataset["train"].train_test_split(test_size=0.2)

# Define the labels
label_list = ["type", "color", "style", "material"]  # Define your labels here

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
model = AutoModelForTokenClassification.from_pretrained("bert-base-cased", num_labels=len(label_list))

# Preprocessing function
def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(examples["content"], truncation=True)
    labels = []
    
    for i, annotation_list in enumerate(examples["annotations"]):
        label_ids = [-100] * len(tokenized_inputs["input_ids"][i])  # Initialize labels with -100

        word_ids = tokenized_inputs.word_ids(batch_index=i)  # Get word_ids for each token

        for annotation in annotation_list:
            start, end = annotation["start"], annotation["end"]
            label = label_list.index(annotation["tag_name"])

            # Assign labels based on word_ids
            for idx, word_id in enumerate(word_ids):
                if word_id is not None and start <= word_id < end:
                    label_ids[idx] = label

        labels.append(label_ids)
    
    tokenized_inputs["labels"] = labels
    return tokenized_inputs

# Apply preprocessing
tokenized_dataset = dataset.map(tokenize_and_align_labels, batched=True)

# Set up training arguments
training_args = TrainingArguments(
    output_dir="ner_model_output",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Set up data collator for token classification
data_collator = DataCollatorForTokenClassification(tokenizer)

# Trainer setup
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],  # Use the test split created from train_test_split
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# Training
trainer.train()
trainer.save_model("ner_model_output")
# Testing
predictions = trainer.predict(tokenized_dataset["test"])
print(predictions)
