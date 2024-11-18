import spacy

nlp_ner = spacy.load("../ner/model-last")

def ner(prompt):
    doc = nlp_ner(prompt)

    # Initialize a dictionary to store the entities by label
    entities_dict = {}

    # Loop through the entities in the document
    for ent in doc.ents:
        label = ent.label_  # Convert the label to lowercase
        text = ent.text.lower()  # Convert the entity's text to lowercase

        # If the label is already in the dictionary, append the text
        if label in entities_dict:
            entities_dict[label].append(text)
        else:
            # Otherwise, create a new entry with a list containing the text
            entities_dict[label] = [text]
    
    return entities_dict
