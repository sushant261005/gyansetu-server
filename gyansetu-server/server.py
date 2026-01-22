from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from openai import OpenAI

app = Flask(__name__)

# Load API keys from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# OpenAI client
openai_client = None
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)


@app.route("/", methods=["GET"])
def home():
    return "GyanSetu AI Server is running 🚀"


@app.route("/ask", methods=["GET", "POST"])
def ask_ai():
    # Get query from GET or POST
    if request.method == "POST":
        data = request.json
        query = data.get("query")
    else:
        query = request.args.get("query")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    # First try Gemini
    if GEMINI_API_KEY:
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(query)
            return jsonify({
                "reply": response.text,
                "model": "gemini"
            })
        except Exception as e:
            print("Gemini error:", e)

    # Fallback to OpenAI
    if OPENAI_API_KEY:
        try:
            completion = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Reply in the same language as the user."},
                    {"role": "user", "content": query}
                ]
            )

            return jsonify({
                "reply": completion.choices[0].message.content,
                "model": "openai"
            })
        except Exception as e:
            print("OpenAI error:", e)

    return jsonify({"error": "No AI service available"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
