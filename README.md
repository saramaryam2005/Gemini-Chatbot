# 🤖 Gemini AI Chatbot using Flask

A web-based AI chatbot built using **Python, Flask, Google Gemini API, HTML, CSS, Jinja2, and SQLite**.

Users can chat with Google's Gemini model through a clean web interface. Chat history is stored permanently using SQLite, so conversations remain available even after restarting the application.

---

## 🚀 Features

- AI-powered chatbot using Gemini API
- Clean chat interface with chat bubbles
- User messages displayed on the right
- Gemini responses displayed on the left
- Chat history stored in SQLite database
- Persistent conversations after restarting the application
- Environment variable support for API security
- Beginner-friendly Flask project structure

---

## 🛠️ Technologies Used

### Backend
- Python
- Flask
- Google Generative AI (Gemini API)
- SQLite3

### Frontend
- HTML
- CSS
- Jinja2 Templates

### Security
- Python Dotenv
- Environment Variables (.env)

---

## 📂 Project Structure

```text
GEMINI_CHATBOT/
│
├── app.py
├── chat.db
├── .env
├── .gitignore
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
└── venv/
```

---

## ⚙️ Installation


## Open browser:

```text
http://127.0.0.1:5000
```

---

## 🗄️ Database

The project uses SQLite.

Database file:

```text
chat.db
```

Table:

```sql
messages
```

Structure:

| Column | Type |
|----------|--------|
| id | INTEGER |
| sender | TEXT |
| text | TEXT |

---

## 🔄 Application Workflow

```text
User
 │
 ▼
HTML Form
 │
 ▼
Flask Backend
 │
 ▼
Gemini API
 │
 ▼
Gemini Response
 │
 ▼
SQLite Database
 │
 ▼
Jinja Template
 │
 ▼
Chat Interface
```

---

## 📸 Current Version

### Version 1
- Gemini API Integration
- Basic Chat Functionality

### Version 2
- Chat History
- Chat Bubble UI
- Improved Styling

### Version 3
- SQLite Database Integration
- Persistent Chat Storage

---


## 🎯 Future Improvements

- Multiple chat sessions
- New Chat button
- User authentication
- Dark mode
- File upload support
- PDF Question Answering (RAG)

---

## 👩‍💻 Author

Sara Maryam

B.Tech Electrical Engineering Student

Built as a learning project to understand:
- Flask
- APIs
- Databases
- Frontend Development
- Generative AI Integration

---
