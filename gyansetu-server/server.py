from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from openai import OpenAI

app = Flask(__name__)

# Load API keys from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setup Gemini
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-pro")

# Setup OpenAI
openai_client = OpenAI(api_key=OPENAI_API_KEY)

@app.route("/")
def home():
    return "GyanSetu AI Server is running 🚀"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question")

    try:
        # Try Gemini first
        response = gemini_model.generate_content(question)
        answer = response.text
    except:
        # Fallback to OpenAI
        chat = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": question}]
        )
        answer = chat.choices[0].message.content

    return jsonify({"answer": answer})

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=8080)
    # Render redeploy trigger
print("Gyansetu cloud server starting...")
