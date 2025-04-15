
from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://shebins298.github.io"])


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/analyze", methods=["POST"])
def analyze_entry():
    data = request.get_json()
    entry = data.get("entry", "")
    email = data.get("email", "anonymous")
    print(f"Received entry from {email}: {entry}")

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"User journal: {entry}\nGive professional personal development advice.")
        print("Generated advice:", response.text)
        return jsonify({"advice": response.text})
    except Exception as e:
        print("Error during AI generation:", e)
        return jsonify({"error": "AI service failed"}), 500
