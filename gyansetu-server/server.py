from flask import Flask, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)

# Load Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

gemini_model = None

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("models/gemini-1.5-flash")

@app.route("/")
def home():
    return "GyanSetu AI Server is running 🚀"

@app.route("/ask", methods=["GET"])
def ask():
    query = request.args.get("query")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    if not gemini_model:
        return jsonify({"error": "Gemini API key not configured"}), 500

    try:
        response = gemini_model.generate_content(query)
        return jsonify({
            "provider": "Gemini",
            "answer": response.text
        })
    except Exception as e:
        print("Gemini error:", e)
        return jsonify({"error": "AI service temporarily unavailable"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
