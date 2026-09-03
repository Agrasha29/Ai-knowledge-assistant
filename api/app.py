import os
import tempfile
import PyPDF2

from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI


# -----------------------------
# Groq API Client
# -----------------------------
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


# -----------------------------
# Flask Setup
# -----------------------------
app = Flask(__name__)
CORS(app)


# -----------------------------
# Extract text from PDF
# -----------------------------
def extract_text_from_pdf(filepath):
    text = ""

    with open(filepath, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        for i, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

            except Exception as e:
                print(f"Warning: failed to extract page {i}: {e}")

    return text


# -----------------------------
# Upload PDF + Ask Question
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
        # Create temporary PDF file
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            file.save(temp_file.name)
            filepath = temp_file.name

        # Extract PDF text
        text = extract_text_from_pdf(filepath)

        # Delete temporary file
        os.remove(filepath)

        # Ask Groq AI
        response = client.responses.create(
            model="openai/gpt-oss-20b",
            input=f"Document:\n{text}\n\nQuestion: {question}",
            max_output_tokens=300,
        )

        answer = response.output_text.strip()

        return jsonify({"answer": answer})

    except Exception as e:

        print("Error:", e)

        return jsonify({
            "error": str(e)
        }), 500


# Vercel uses this Flask app
if __name__ == "__main__":
    app.run()
