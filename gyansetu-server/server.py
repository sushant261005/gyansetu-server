from flask import Flask, request, jsonify
import os
from google import genai

app = Flask(__name__)

# Load API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)

@app.route("/")
def home():
    return "GyanSetu AI Server is running 🚀"

@app.route("/ask")
def ask():
    query = request.args.get("query")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    if not client:
        return jsonify({"error": "Gemini API key missing"}), 500

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=query
        )

        return jsonify({
            "provider": "Gemini",
            "answer": response.text
        })

    except Exception as e:
        print("Gemini error:", e)
        return jsonify({
            "error": "AI service temporarily unavailable"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
