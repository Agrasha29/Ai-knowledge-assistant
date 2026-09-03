import os
import io
import PyPDF2
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

# -----------------------------
# Groq API Client Setup
# -----------------------------
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# -----------------------------
# Flask App Setup
# -----------------------------
app = Flask(__name__)
CORS(app)

# -----------------------------
# PDF Processing (In-Memory)
# -----------------------------
def extract_text_from_pdf_stream(file_bytes):
    text = ""
    try:
        # Load directly from RAM buffer without disk write permissions
        pdf_stream = io.BytesIO(file_bytes)
        reader = PyPDF2.PdfReader(pdf_stream)
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print(f"Error parsing PDF memory stream: {e}")
    return text

# -----------------------------
# Upload PDF + Ask Question Endpoint
# -----------------------------
@app.route("/api/upload_and_ask", methods=["POST"])
def upload_and_ask():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    question = request.form.get("question")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    try:
        # Extract PDF text entirely in memory
        file_bytes = file.read()
        text = extract_text_from_pdf_stream(file_bytes)

        if not text.strip():
            return jsonify({"error": "Could not extract text from the provided PDF."}), 400

        # Query Groq API via standard OpenAI Chat Completions SDK
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful AI assistant. Use the following PDF content to answer the user question:\n\n{text}"
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            max_tokens=300
        )

        answer = response.choices[0].message.content.strip()
        return jsonify({"answer": answer})

    except Exception as e:
        print("Serverless Invocation Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
