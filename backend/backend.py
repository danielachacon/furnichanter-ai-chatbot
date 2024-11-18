import os
from flask import Flask, flash, request, redirect, url_for, session, jsonify, url_for, render_template
from flask_cors import CORS, cross_origin
import intent_classification
import greeting
import furniture_related_query
import ner
import recommendation

required_keys = ['STYLE', 'MATERIAL', 'TYPE', 'COLOR']

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.secret_key = os.urandom(24)

@app.before_request
def ensure_session():
    session.modified = True

@app.route("/", methods=['POST'])
def conversation():
    data = request.get_json()
    prompt = data.get('prompt')
    print(f"Received prompt: {prompt}")

    conversation_state = session.get('conversation_state', None)
    
    print(f"Conversation State: {conversation_state}")
    
    if conversation_state == "furniture_search":
        keys = session.get('keys', [])
    intent = intent_classification.generate_content(prompt).strip()
    print(f"Intent detected: {intent}")
        
    if intent == "Furniture Search" and conversation_state is None:
        session['conversation_state'] = 'furniture_search'
        parameters = ner.ner(prompt)
        session['search_parameters'] = parameters
        print(parameters)
            
        missing_keys = [key for key in required_keys if key not in parameters]        
        response = "Confirming that you are looking for:\n"
        key_value_dict = {}
        
        response_parts = []
        for key in required_keys:
            if key in parameters:
                # If multiple values exist, join them into a string
                values = ', '.join(parameters[key])
                response_parts.append(f"{key}: {values}")
                key_value_dict[key] = values
                
        response += '\n'.join(response_parts)
        
        session['keys'] = key_value_dict
        print(session['keys'])
    elif intent == "Affirmation" and conversation_state == "furniture_search":
        parameters_dict = session.get('keys', [])
        print(parameters_dict)
        parameters_string = ' '.join(str(value) for value in parameters_dict.values())
        response = recommendation.give_recommendation(parameters_string)
    elif intent == "Negation" and conversation_state == "furniture_search":
        response = "Let's try again, what are you looking for?"
        session.pop('conversation_state', None)
        session.pop('missing_keys', None)
            
    elif intent == "Furniture-Related Query":
        response = furniture_related_query.generate_content(prompt)
        
    elif intent == "Greetings":
        response = greeting.generate_content(prompt)
        
    else:
        response = "Sorry, I don't understand. Please try again."
    conversation_state = session.get('conversation_state', None)
    print(f"Conversation State: {conversation_state}")
    return jsonify({"response": response, "prompt": prompt})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5500, use_reloader=False)