import os
from flask import Flask, flash, request, redirect, url_for, session, jsonify, url_for, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['POST'])
def conversation():
    data = request.get_json()
    prompt = data.get('prompt')
    print(f"Received prompt: {prompt}")
    return jsonify({"message": "Data received successfully", "prompt": prompt})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5500, debug=True)