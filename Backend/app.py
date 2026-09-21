import os
import io
import PyPDF2

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv


# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


# -----------------------------
# Flask setup
# -----------------------------
app = Flask(__name__)
CORS(app)


# -----------------------------
# Folder paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FRONTEND_FOLDER = os.path.join(BASE_DIR, "Frontend")


# -----------------------------
# Extract text directly from PDF
# -----------------------------
def extract_text_from_pdf(file):
    text = ""

    reader = PyPDF2.PdfReader(file)

    for i, page in enumerate(reader.pages):
        try:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        except Exception as e:
            print(f"Warning: failed to extract page {i}: {e}")
            continue

    return text


# -----------------------------
# Upload PDF + Ask Question
# -----------------------------
@app.route("/upload_and_ask", methods=["POST"])
def upload_and_ask():

    # Check file
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Check question
    question = request.form.get("question")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    try:

        # -----------------------------
        # Read PDF directly into memory
        # -----------------------------
        pdf_bytes = io.BytesIO(file.read())

        # -----------------------------
        # Extract PDF text
        # -----------------------------
        text = extract_text_from_pdf(pdf_bytes)

        if not text.strip():
            return jsonify({
                "error": "Could not extract text from the PDF."
            }), 400

        # -----------------------------
        # Send document + question to Groq
        # -----------------------------
        response = client.responses.create(
            model="openai/gpt-oss-20b",
            input=f"""
You are an AI Knowledge Assistant.

Answer the user's question using the provided document.

Document:
{text}

Question:
{question}
""",
            max_output_tokens=300,
        )

        answer = response.output_text.strip()

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        print("Error:", e)

        return jsonify({
            "error": str(e)
        }), 500


# -----------------------------
# Serve Frontend
# -----------------------------
@app.route("/")
def index():
    return send_from_directory(
        FRONTEND_FOLDER,
        "index.html"
    )


# -----------------------------
# Run locally
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)