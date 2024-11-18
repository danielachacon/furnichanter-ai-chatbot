import base64
import vertexai
from vertexai.preview.generative_models import GenerativeModel, SafetySetting, Part, Tool
from vertexai.preview.generative_models import grounding
import os 

def generate_content(prompt):
    
    vertexai.init(project="forward-vector-439602-v4", location="us-east1")
    tools = [
        Tool.from_google_search_retrieval(
            google_search_retrieval=grounding.GoogleSearchRetrieval()
        ),
    ]
    model = GenerativeModel(
        "gemini-1.5-flash-002",
    )

    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 1,
        "top_p": 0.95,
    }

    safety_settings = [
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
    ]

    
    response = model.generate_content(
    contents = f"""
    Use your knowledge and the information provided to classify the intent of the sentence delimited by `.
    
    The sentence must be classifed as 1 of the following intents.
    Furniture Search (example: I am looking for a brown chair)
    Furniture-Related Query (example: How can I mix modern and vintage furniture styles in one room?)
    Greetings (example: hello, goodbye)
    Affirmation (example: Yes, that's right)
    Negation (example: No)
    Other

    Respond with one of either "Furniture Search", "Furniture-Related Query",  "Greetings", "Other", "Affirmation", "Negation".
    `f{prompt}`)""",
    safety_settings= safety_settings,
    generation_config= generation_config)
    
    return response.candidates[0].content.parts[0].text
    
    