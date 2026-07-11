# 🤖 HobbyFi Copilot

HobbyFi Copilot is an AI-powered chatbot built with **FastAPI** that performs CRUD (Create, Read, Update, Delete) operations on a SQLite database using natural language requests. It leverages function/tool calling to translate user queries into database actions.

---

## 🚀 Features

- 🤖 AI-powered chatbot
- ➕ Create records
- 🔍 Read records
- ✏️ Update records
- 🗑️ Delete records
- ⚡ FastAPI REST API
- 🗄️ SQLite + SQLAlchemy ORM
- 📖 Swagger UI support

---

## 🛠️ Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn
- LangChain
- LangGraph
- Streamlit
- LlM
  
---

## 📂 Project Structure

```
backend/
├── api.py
├── config.py
├── copilot.py
├── crud.py
├── database.py
├── dependencies.py
├── models.py
├── prompts.py
├── schemas.py
├── services.py
├── tools.py
├── routers/
└── requirements.txt
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/hobbyfi-copilot.git
cd hobbyfi-copilot/backend
```

Create and activate a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
uvicorn api:app --reload
```

Server:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

## 💬 Example Commands

- "Create a new hobby called Photography."
- "Show all hobbies."
- "Update the hobby with ID 3."
- "Delete the membership with ID 5."

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Vansh Mittal**

B.Tech CSE (Data Science) | AI/ML Enthusiast | Python Developer
