from flask import Flask, render_template, request, session, redirect
import google.generativeai as genai
import os
import sqlite3
from dotenv import load_dotenv

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

app = Flask(__name__)
app.secret_key = "secret123"   # Needed for Flask sessions

# -----------------------------
# Gemini Setup
# -----------------------------
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# -----------------------------
# Database Setup
# -----------------------------
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
        text TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()

# -----------------------------
# Create New Chat Session
# -----------------------------
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


# -----------------------------
# Get All Chat Sessions
# -----------------------------
def get_chat_sessions():

    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM chat_sessions ORDER BY id DESC"
    )

    sessions = cursor.fetchall()

    conn.close()

    return sessions


# -----------------------------
# Get Messages For One Session
# -----------------------------
def get_messages(session_id):

    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT sender, text FROM messages WHERE session_id=?",
        (session_id,)
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


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():

    if "session_id" not in session:
        session["session_id"] = create_chat_session()

    return render_template(
        "index.html",
        messages=get_messages(session["session_id"]),
        sessions=get_chat_sessions(),
        active=session["session_id"]
    )


# -----------------------------
# Create New Chat
# -----------------------------
@app.route("/new_chat")
def new_chat():

    session["session_id"] = create_chat_session()

    return redirect("/")


# -----------------------------
# Open Existing Chat
# -----------------------------
@app.route("/chat/<int:chat_id>")
def load_chat(chat_id):

    session["session_id"] = chat_id

    return redirect("/")

# -----------------------------
# delete Existing Chat
# -----------------------------
@app.route("/delete_chat/<int:chat_id>")
def delete_chat(chat_id):

    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()

    # Delete all messages in that chat
    cursor.execute(
        "DELETE FROM messages WHERE session_id=?",
        (chat_id,)
    )

    # Delete the chat session itself
    cursor.execute(
        "DELETE FROM chat_sessions WHERE id=?",
        (chat_id,)
    )

    conn.commit()
    conn.close()

    # If current chat was deleted, create a new one
    if session.get("session_id") == chat_id:
         sessions = get_chat_sessions()

    if sessions:
        session["session_id"] = sessions[0][0]
    else:
        session["session_id"] = create_chat_session()

    return redirect("/")


# -----------------------------
# Send Message
# -----------------------------
@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.form["message"]

    current_chat = session["session_id"]

    # Save User Message
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO messages
        (session_id, sender, text)
        VALUES (?, ?, ?)
        """,
        (current_chat, "user", user_message)
    )

    conn.commit()
    conn.close()

    # Gemini Response
    try:

        response = model.generate_content(user_message)

        bot_reply = response.text

    except Exception as e:

        bot_reply = f"Error: {str(e)}"

    # Save Bot Reply
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO messages
        (session_id, sender, text)
        VALUES (?, ?, ?)
        """,
        (current_chat, "bot", bot_reply)
    )

    conn.commit()
    conn.close()

    return redirect("/")

