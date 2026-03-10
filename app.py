from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import subprocess
from dotenv import load_dotenv

# Flask app
app = Flask(__name__)

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("gemini_api_key"))

# Gemini instruction
instruction = """
Give very short answers in plain text.
Do not use symbols, stars, bullet points, or formatting.
"""

# Gemini model
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction=instruction
)

# Home page
@app.route("/")
def index():
    return render_template("index.html")


# AI endpoint
@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()
    command = data.get("message").lower()

    # OPEN NOTEPAD
    if "open notepad" in command:
        subprocess.Popen("notepad.exe")
        return jsonify({"reply": "Opening Notepad"})

    try:
        result = model.generate_content(command)

        if result and result.text:
            answer = result.text.strip()
        else:
            answer = "Sorry I could not generate a response."

    except Exception as e:
        print(e)
        answer = "AI service is not responding."

    return jsonify({"reply": answer})


# Run server
if __name__ == "__main__":
    app.run(debug=True)