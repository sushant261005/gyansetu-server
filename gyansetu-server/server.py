from flask import Flask, request, jsonify
import os
import requests
import google.generativeai as genai
from openai import OpenAI

app = Flask(__name__)

# =========================
# API KEYS (ENV VARIABLES)
# =========================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

# =========================
# GEMINI SETUP
# =========================
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# =========================
# OPENAI SETUP
# =========================
openai_client = None
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return "GyanSetu AI Server is running 🚀"

@app.route("/ask")
def ask():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Query is required"}), 400

    # 1️⃣ GEMINI (FREE – PRIMARY)
    if GEMINI_API_KEY:
        try:
            model = genai.GenerativeModel("gemini-pro")
            res = model.generate_content(query)
            return jsonify({
                "provider": "Gemini",
                "answer": res.text
            })
        except Exception as e:
            print("Gemini failed:", e)

    # 2️⃣ GROQ (FREE – FAST)
    if GROQ_API_KEY:
        try:
            r = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-8b-8192",
                    "messages": [{"role": "user", "content": query}]
                },
                timeout=20
            )
            data = r.json()
            return jsonify({
                "provider": "Groq (LLaMA)",
                "answer": data["choices"][0]["message"]["content"]
            })
        except Exception as e:
            print("Groq failed:", e)

    # 3️⃣ OPENAI (PAID – READY)
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
            print("OpenAI failed:", e)

    # 4️⃣ HUGGINGFACE (FREE – BACKUP)
    if HF_API_KEY:
        try:
            r = requests.post(
                "https://api-inference.huggingface.co/models/google/flan-t5-large",
                headers={"Authorization": f"Bearer {HF_API_KEY}"},
                json={"inputs": query},
                timeout=20
            )
            data = r.json()
            return jsonify({
                "provider": "HuggingFace",
                "answer": data[0]["generated_text"]
            })
        except Exception as e:
            print("HF failed:", e)

    return jsonify({
        "error": "All AI services are currently unavailable"
    }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
