from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://shebins298.github.io"])  # Limit CORS to your GitHub Pages site

# Check if API key is set
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY not set in environment variables!")
else:
    print("✅ GEMINI_API_KEY is present.")

# Configure Gemini
try:
    genai.configure(api_key=api_key)
except Exception as config_err:
    print("❌ Error configuring Gemini:", config_err)

@app.route("/", methods=["GET"])
def home():
    return "✅ Gemini backend is live!", 200

@app.route("/analyze", methods=["POST"])
def analyze_entry():
    try:
        data = request.get_json()
        if not data:
            print("❌ No JSON data received")
            return jsonify({"error": "No input data provided"}), 400

        entry = data.get("entry", "").strip()
        email = data.get("email", "anonymous")
        print(f"📩 Received entry from {email}: {entry}")

        if not entry:
            print("⚠️ Empty journal entry received")
            return jsonify({"error": "Journal entry cannot be empty"}), 400

        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            f"User journal: {entry}\nYou are a cognitive behavioral therapy (CBT) expert.

  Based on the user's journal entry before this and identified negative patterns, suggest alternative, more balanced thoughts to challenge and reframe those patterns.
  Return an array of suggested restructured thoughts."
        )

        if hasattr(response, "text"):
            print("✅ AI Response generated successfully")
            return jsonify({"advice": response.text})
        else:
            print("❌ Unexpected response structure:", response)
            return jsonify({"error": "Invalid response from Gemini"}), 500



    except Exception as e:
        error_message = repr(e)  # Shows full error detail
        print("❌ Error during AI generation:", error_message)
        return jsonify({"error": error_message}), 500  # Return full error (DEV ONLY)


if __name__ == "__main__":
    app.run(debug=True)
