from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from openai import OpenAI

app = Flask(__name__)

# Load API keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setup Gemini
gemini_model = None
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-pro")

# Setup OpenAI
openai_client = None
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)


@app.route("/")
def home():
    return "GyanSetu AI Server is running 🚀"


@app.route("/ask", methods=["GET"])
def ask():
    query = request.args.get("query")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    # Try Gemini
    if gemini_model:
        try:
            res = gemini_model.generate_content(query)
            return jsonify({
                "provider": "Gemini",
                "answer": res.text
            })
        except Exception as e:
            print("Gemini error:", e)

    # Try OpenAI
    if openai_client:
        try:
            completion = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": query}]
            )
            return jsonify({
                "provider": "OpenAI",
                "answer": completion.choices[0].message.content
            })
        except Exception as e:
            print("OpenAI error:", e)

    return jsonify({"error": "No AI service available"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
