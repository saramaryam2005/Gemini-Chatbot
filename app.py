from flask import Flask, render_template, request
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form["message"]
    response = model.generate_content(user_message)
    return response.text
if __name__ == "__main__":
    app.run(debug=True)
