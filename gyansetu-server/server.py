from flask import Flask, request, jsonify
import os
import requests
import google.generativeai as genai

app = Flask(__name__)

# ================= API KEYS =================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ================ GEMINI ====================
gemini_model = None
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# ================ GROQ ======================
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# ============== TOGETHER ===================
TOGETHER_URL = "https://api.together.xyz/v1/chat/completions"

# ============ OPENROUTER ===================
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


@app.route("/")
def home():
    return "GyanSetu AI Server is running 🚀 (Multi-Free AI Engine)"


@app.route("/ask", methods=["GET"])
def ask():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Query is required"}), 400

    # ===== 1) Gemini =====
    if gemini_model:
        try:
            res = gemini_model.generate_content(query)
            return jsonify({"provider": "Gemini", "answer": res.text})
        except Exception as e:
            print("Gemini error:", e)

    # ===== 2) Groq =====
    if GROQ_API_KEY:
        try:
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama3-70b-8192",
                "messages": [{"role": "user", "content": query}]
            }
            r = requests.post(GROQ_URL, headers=headers, json=payload)
            data = r.json()
            return jsonify({"provider": "Groq", "answer": data["choices"][0]["message"]["content"]})
        except Exception as e:
            print("Groq error:", e)

    # ===== 3) Together AI =====
    if TOGETHER_API_KEY:
        try:
            headers = {
                "Authorization": f"Bearer {TOGETHER_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "meta-llama/Llama-3-70b-chat-hf",
                "messages": [{"role": "user", "content": query}]
            }
            r = requests.post(TOGETHER_URL, headers=headers, json=payload)
            data = r.json()
            return jsonify({"provider": "TogetherAI", "answer": data["choices"][0]["message"]["content"]})
        except Exception as e:
            print("Together error:", e)

    # ===== 4) OpenRouter (free models) =====
    if OPENROUTER_API_KEY:
        try:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://gyansetu.app",
                "X-Title": "GyanSetu"
            }
            payload = {
                "model": "mistralai/mistral-7b-instruct:free",
                "messages": [{"role": "user", "content": query}]
            }
            r = requests.post(OPENROUTER_URL, headers=headers, json=payload)
            data = r.json()
            return jsonify({"provider": "OpenRouter", "answer": data["choices"][0]["message"]["content"]})
        except Exception as e:
            print("OpenRouter error:", e)

    return jsonify({"error": "All AI services are currently unavailable"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
