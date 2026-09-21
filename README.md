# 🤖 AI-Powered Knowledge Assistant

An intelligent **PDF Question Answering System** that allows users to upload documents and ask questions in natural language. The system extracts text from uploaded PDFs and uses an AI model through the **Groq API** to generate context-aware answers.

---

## 🚀 Overview

The **AI-Powered Knowledge Assistant** is designed to make information retrieval from large PDF documents faster and easier.

Instead of manually searching through lengthy documents, users can simply:

1. 📄 Upload a PDF
2. 💬 Enter a question
3. 🧠 Let the AI analyze the document context
4. ⚡ Receive an AI-generated answer

The project combines **Python, Flask, PDF processing, REST APIs, and Large Language Models (LLMs)** into a simple web application.

---

## ✨ Features

* 📄 **PDF Upload** — Upload PDF documents through the web interface.
* 🔍 **PDF Text Extraction** — Extract textual content using PyPDF2.
* 💬 **Natural Language Questions** — Ask questions about the uploaded document.
* 🧠 **AI-Powered Answers** — Generate answers using an LLM through the Groq API.
* 🌐 **Web Interface** — Simple frontend for document upload and question answering.
* 🔐 **Environment-Based API Key** — API credentials are managed using environment variables.
* ⚠️ **Input Validation** — Handles missing files, empty filenames, and missing questions.
* 🛡️ **Error Handling** — Handles PDF-processing and API-related errors.
* ⚡ **REST API Architecture** — Frontend communicates with the Flask backend through HTTP requests.

---

## 🏗️ System Architecture

```text
                👤 User
                  │
                  ▼
          🌐 Web Interface
                  │
                  │ PDF + Question
                  ▼
          🐍 Flask Backend
                  │
          ┌───────┴────────┐
          ▼                ▼
     📄 PyPDF2          📝 Query
          │                │
          └───────┬────────┘
                  ▼
          📚 Document Context
                  │
                  ▼
             🤖 Groq API
                  │
                  ▼
          🧠 AI-Generated Answer
                  │
                  ▼
             🌐 Frontend
                  │
                  ▼
                👤 User
```

---

## 🔄 Application Workflow

### Step 1 — Upload PDF

The user selects a PDF document from the web interface.

### Step 2 — File Validation

The Flask backend checks whether a file has been provided and whether a valid filename exists.

### Step 3 — Save Document

The uploaded PDF is saved in the project's upload directory using a secure filename.

### Step 4 — Extract Text

PyPDF2 reads the PDF and extracts text from each available page.

### Step 5 — Process Question

The user's question is received together with the extracted document content.

### Step 6 — AI Processing

The document context and question are sent to the Groq API using an LLM.

### Step 7 — Generate Answer

The AI model generates a natural-language response based on the provided document context.

### Step 8 — Display Result

The generated answer is returned as JSON and displayed to the user through the frontend.

---

## 🧠 RAG Concept

The project is designed around the concept of **Retrieval-Augmented Generation (RAG)**.

In a complete RAG architecture:

```text
PDF
 │
 ▼
Text Extraction
 │
 ▼
Chunking
 │
 ▼
Embeddings
 │
 ▼
Vector Database
 │
 ▼
Relevant Chunks
 │
 ▼
LLM
 │
 ▼
Answer
```

### Current Implementation

The current version performs document-grounded question answering by extracting PDF text and providing the document content as context to the AI model.

A full RAG pipeline with **chunking, embeddings, and vector database retrieval** can be added as a future enhancement.

---

## 🛠️ Tech Stack

| Technology       | Purpose                                       |
| ---------------- | --------------------------------------------- |
| 🐍 Python        | Core programming language                     |
| 🌐 Flask         | Backend and REST API                          |
| 📄 PyPDF2        | PDF text extraction                           |
| 🤖 Groq API      | AI response generation                        |
| 🧠 LLM           | Natural-language understanding and generation |
| 🌐 HTML          | Frontend structure                            |
| 🎨 CSS           | Frontend styling                              |
| ⚡ JavaScript     | Frontend interaction                          |
| 🔐 python-dotenv | Environment variable management               |
| 🔀 Flask-CORS    | Frontend-backend communication                |

---

## 📁 Project Structure

```text
AI SUMMARIZER/
│
├── Backend/
│   ├── app.py
│   ├── .env
│   └── uploads/
│
├── Frontend/
│   └── index.html
│
├── Data/
│
├── Models/
│
├── Utils/
│
├── uploads/
│
├── venv/
│
├── README.md
├── test_upload.html
└── Process Readme.txt
```

---

## 🔌 API

### Upload PDF and Ask Question

**Endpoint**

```text
POST /upload_and_ask
```

### Request

The request uses `multipart/form-data` containing:

```text
file      → PDF document
question  → User's question
```

### Response

```json
{
  "answer": "AI-generated answer based on the document."
}
```

---

## 🔐 Environment Setup

Create a `.env` file inside the `Backend` folder:

```text
GROQ_API_KEY=your_groq_api_key
```

⚠️ **Never upload your `.env` file or API key to GitHub.**

Add the following to `.gitignore`:

```text
.env
venv/
__pycache__/
*.pyc
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI-SUMMARIZER
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

**Windows:**

```powershell
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install flask flask-cors PyPDF2 groq python-dotenv
```

### 5. Configure API key

Create:

```text
Backend/.env
```

Add:

```text
GROQ_API_KEY=your_groq_api_key
```

---

## ▶️ Run the Application

Navigate to the backend:

```powershell
cd Backend
```

Start Flask:

```powershell
python app.py
```

The application will run at:

```text
http://127.0.0.1:5000
```

Open the URL in your browser.

---

## 🖥️ User Interface

### 🏠 Home Page

The home page provides the interface for uploading a PDF and entering a question.

> 📸 Add your homepage screenshot here.

### 📄 PDF Upload

Users can select and upload their PDF document.

> 📸 Add your PDF upload screenshot here.

### 💬 Question & Answer

The user enters a question and receives an AI-generated response based on the uploaded document.

> 📸 Add your question-answer screenshot here.

---

## 🧪 Example

### Input

**Document:**
Database Management System notes

**Question:**

```text
What is a DBMS?
```

### Processing

```text
PDF
 ↓
Text Extraction
 ↓
Document Context
 ↓
Question + Context
 ↓
Groq LLM
```

### Output

```text
A Database Management System (DBMS) is software
used to create, manage, store, and retrieve data
from databases.
```

---

## 🛡️ Error Handling

The backend handles several common errors:

### No File

```json
{
  "error": "No file uploaded"
}
```

### No Question

```json
{
  "error": "Question is required"
}
```

### API Failure

The application catches AI API exceptions and returns an appropriate error response instead of terminating the application.

---

## ⚠️ Current Limitations

* Large PDFs may require significant processing time.
* Scanned/image-based PDFs may not produce usable text through standard text extraction.
* The current version does not use a persistent database.
* Document text is currently handled in memory during application execution.
* A complete vector-based RAG pipeline is not yet implemented.
* AI responses depend on the availability and behavior of the external AI API.

---

## 🔮 Future Enhancements

* 🧩 Implement document chunking
* 🔢 Generate text embeddings
* 🗄️ Integrate a vector database such as FAISS or Chroma
* 📚 Support multiple documents
* 🔎 Retrieve only relevant document sections
* 🖼️ Add OCR for scanned PDFs
* 👤 Add user authentication
* 💾 Store conversation history
* 🌍 Add multilingual support
* ☁️ Deploy the application to the cloud
* 🎙️ Add voice-based questions
* 📊 Add document summarization

---

## 🎯 Objectives

* Develop an intelligent document-based question-answering system.
* Reduce the time required to manually search through documents.
* Improve information retrieval using AI.
* Provide a simple and user-friendly interface.
* Automate document-based question answering.
* Create a foundation for a scalable RAG-based application.

---

## 📈 Learning Outcomes

Through this project, the following concepts were explored:

* Python backend development
* Flask REST APIs
* PDF processing
* Frontend-backend integration
* API integration
* Large Language Models
* Prompt engineering
* Environment variable management
* Error handling
* Document-based AI systems
* RAG architecture concepts

---

## 👩‍💻 Author

**Agrasha Patel**

🎓 B.Tech Computer Science & Engineering — AI & Machine Learning

🔗 GitHub: https://github.com/Agrasha29

---

## ⭐ Acknowledgements

* Python
* Flask
* PyPDF2
* Groq
* HTML, CSS & JavaScript

---

## 📄 License

This project is developed for **educational and academic purposes**.
