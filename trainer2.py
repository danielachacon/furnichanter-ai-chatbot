from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch

# Load the tokenizer and the trained model
tokenizer = AutoTokenizer.from_pretrained("ner_model_output")
model = AutoModelForTokenClassification.from_pretrained("ner_model_output")

# Define the label list
label_list = ["type", "color", "style", "material"]

# Example text
text = "I would like a modern wooden dining table in oak color."

# Tokenize input
inputs = tokenizer(text, return_tensors="pt")

# Perform inference
with torch.no_grad():
    outputs = model(**inputs)

# Extract predictions
logits = outputs.logits
predictions = torch.argmax(logits, dim=2)

# Convert predictions to labels
tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
predicted_labels = [label_list[p] for p in predictions[0].numpy()]

# Print results
for token, label in zip(tokens, predicted_labels):
    print(f"{token}: {label}")
