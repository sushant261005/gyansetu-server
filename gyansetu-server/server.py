from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from openai import OpenAI

app = Flask(__name__)

# ==============================
# Load API Keys from Environment
# ==============================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ==============================
# Setup Gemini
# ==============================
gemini_model = None
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("models/gemini-1.5-flash")

# ==============================
# Setup OpenAI
# ==============================
openai_client = None
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)


# ==============================
# Home Route
# ==============================
@app.route("/", methods=["GET"])
def home():
    return "GyanSetu AI Server is running 🚀"


# ==============================
# Ask Route (GET + POST)
# ==============================
@app.route("/ask", methods=["GET", "POST"])
def ask():
    if request.method == "GET":
        query = request.args.get("query")
    else:
        data = request.get_json()
        query = data.get("query") if data else None

    if not query:
        return jsonify({"error": "Query is required"}), 400

    # Try Gemini First
    if gemini_model:
        try:
            res = gemini_model.generate_content(query)
            return jsonify({
                "provider": "Gemini",
                "answer": res.text.strip()
            })
        except Exception as e:
            print("Gemini error:", e)

    # Fallback to OpenAI
    if openai_client:
        try:
            completion = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": query}]
            )
            return jsonify({
                "provider": "OpenAI",
                "answer": completion.choices[0].message.content.strip()
            })
        except Exception as e:
            print("OpenAI error:", e)

    return jsonify({"error": "No AI service available"}), 500


# ==============================
# Run Server
# ==============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

