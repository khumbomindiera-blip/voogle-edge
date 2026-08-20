from flask import Flask, render_template, request, jsonify
import requests
import json
from knowledge_loader import load_knowledge

app = Flask(__name__)

# ==================================
# PRELOAD KNOWLEDGE ON STARTUP
# ==================================

print("Preloading English knowledge...")
load_knowledge("English")

print("Preloading Chichewa knowledge...")
load_knowledge("Chichewa")

print("Knowledge base ready.")

# ==================================
# AI FUNCTION
# ==================================

def ask_voogle(question, language):

    knowledge = load_knowledge(language)

    prompt = f"""
You are Voogle Edge.

You are an agricultural AI assistant.

Respond in the same language selected by the user.

Use ONLY the agricultural knowledge below.

If the answer is not contained in the knowledge, say:

"I do not have that information in my local agricultural database."

AGRICULTURAL KNOWLEDGE:

{knowledge}

QUESTION:

{question}

ANSWER:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma3:4b",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data["response"]

# ==================================
# HOME PAGE
# ==================================

@app.route("/")
def home():
    return render_template("index.html")

# ==================================
# ASK AI
# ==================================

@app.route("/ask", methods=["POST"])
def ask():

    question = request.json["question"]
    language = request.json["language"]

    answer = ask_voogle(question, language)

    return jsonify({
        "answer": answer
    })

# ==================================
# COMMUNITY REPORTING
# ==================================

@app.route("/report", methods=["POST"])
def report():

    location = request.json["location"]
    category = request.json["category"]
    report_text = request.json["report"]

    try:

        with open("reports.json", "r") as f:
            reports = json.load(f)

    except:
        reports = []

    reports.append({

        "location": location,
        "category": category,
        "report": report_text

    })

    with open("reports.json", "w") as f:

        json.dump(reports, f, indent=4)

    return jsonify({
        "message": "Report submitted successfully"
    })

# ==================================
# ADMIN DASHBOARD
# ==================================

@app.route("/admin")
def admin():

    try:

        with open("reports.json", "r") as f:
            reports = json.load(f)

    except:
        reports = []

    return render_template(
        "admin.html",
        reports=reports
    )

# ==================================
# RUN APP
# ==================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )