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

        model = genai.GenerativeModel("gemini-pro")

        response = model.generate_content(
            f"User journal: {entry}\nGive professional personal development advice."
        )

        if hasattr(response, "text"):
            print("✅ AI Response generated successfully")
            return jsonify({"advice": response.text})
        else:
            print("❌ Unexpected response structure:", response)
            return jsonify({"error": "Invalid response from Gemini"}), 500

    except Exception as e:
        print("❌ Error during AI generation:", repr(e))
        return jsonify({"error": "AI service failed"}), 500

if __name__ == "__main__":
    app.run(debug=True)
