
import spacy
from spacy.training import Example
import json

# Load the base model
nlp = spacy.load("en_core_web_sm")

# Load the data
with open("ner_dataset_extended.json", "r") as file:
    data = json.load(file)

# Convert to spaCy training format
TRAINING_DATA = []
for item in data:
    text = item["content"]
    entities = [(ann["start"], ann["end"], ann["tag_name"]) for ann in item["annotations"]]
    TRAINING_DATA.append((text, {"entities": entities}))

def check_overlaps(annotations):
    seen = set()
    for start, end, tag in annotations:
        for i in range(start, end):
            if i in seen:
                print(f"Overlap found: ({start}, {end}, '{tag}')")
            seen.add(i)

# Call this function for each item's annotations
for item in data:
    check_overlaps([(ann["start"], ann["end"], ann["tag_name"]) for ann in item["annotations"]])


# Create the pipeline and add the NER component
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")
else:
    ner = nlp.get_pipe("ner")

# Add the labels
for _, annotations in TRAINING_DATA:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])

# Disable other pipes to train only NER
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):
    optimizer = nlp.begin_training()
    for i in range(10):  # Number of iterations
        losses = {}
        for text, annotations in TRAINING_DATA:
            example = Example.from_dict(nlp.make_doc(text), annotations)
            nlp.update([example], drop=0.35, losses=losses)
        print(f"Iteration {i}: Losses - {losses}")

# Save the trained model
nlp.to_disk("custom_ner_model")
