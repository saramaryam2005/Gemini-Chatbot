from flask import Flask, render_template, request
import google.generativeai as genai
import os
import sqlite3
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
messages = []


def init_db():

    conn = sqlite3.connect("chat.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_sessions(

        id INTEGER PRIMARY KEY AUTOINCREMENT

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        session_id INTEGER,

        sender TEXT,

        text TEXT)""")

    conn.commit()
    conn.close()

init_db()
def create_chat_session():

    conn = sqlite3.connect("chat.db")

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chat_sessions DEFAULT VALUES"
    )

    conn.commit()

    session_id = cursor.lastrowid

    conn.close()

    return session_id

def get_chat_sessions():

    conn = sqlite3.connect("chat.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM chat_sessions ORDER BY id DESC"
    )

    sessions = cursor.fetchall()

    conn.close()

    return sessions
def get_messages():

    conn = sqlite3.connect("chat.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT sender, text FROM messages"
    )

    rows = cursor.fetchall()

    conn.close()

    messages = []

    for row in rows:

        messages.append(
            {
                "sender": row[0],
                "text": row[1]
            }
        )

    return messages

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")
@app.route("/")
def home():

    return render_template(
        "index.html",
        messages=get_messages())
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form["message"]

    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute(
    "INSERT INTO messages (sender, text) VALUES (?, ?)",
    ("user", user_message))
    conn.commit()

    conn.close()

    messages.append(
    {"sender": "user",
    "text": user_message})

    try:
        response = model.generate_content(user_message)
        bot_reply = response.text

    except Exception as e:
        bot_reply = f"Error: {str(e)}"

    conn = sqlite3.connect("chat.db")

    cursor = conn.cursor()

    cursor.execute("INSERT INTO messages (sender, text) VALUES (?, ?)",("bot", bot_reply))

    conn.commit()

    conn.close()
    messages.append(
{
    "sender": "bot",
    "text": bot_reply
})
    
    return render_template(
    "index.html",
    messages=get_messages())
if __name__ == "__main__":
    app.run(debug=True)
