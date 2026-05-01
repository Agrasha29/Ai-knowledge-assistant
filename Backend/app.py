import os
import PyPDF2
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()  # .env file should contain GROQ_API_KEY=your_key_here
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
# In-memory storage for uploaded PDF text
# -----------------------------
documents = {}

# -----------------------------
# Folder paths
# -----------------------------
UPLOAD_FOLDER = "../uploads"      # PDFs go here
FRONTEND_FOLDER = "../Frontend"   # HTML goes here
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
                continue
    return text

# -----------------------------
# Upload PDF + Ask question endpoint
# -----------------------------
@app.route("/upload_and_ask", methods=["POST"])
def upload_and_ask():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    question = request.form.get("question")
    if not question:
        return jsonify({"error": "Question is required"}), 400

    # Save PDF
    filepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(filepath)

    # Extract text
    text = extract_text_from_pdf(filepath)
    documents[file.filename] = text

    try:
        # -----------------------------
        # Correct Groq API call
        # -----------------------------
        response = client.responses.create(
            model="openai/gpt-oss-20b",  # ✅ replace with a supported Groq model
            input=f"Document:\n{text}\n\nQuestion: {question}",
            max_output_tokens=300,
        )
        answer = response.output_text.strip()
    except Exception as e:
        print("Groq API error:", e)
        return jsonify({"error": f"Groq API error: {str(e)}"}), 500

    return jsonify({"answer": answer})

# -----------------------------
# Serve HTML frontend
# -----------------------------
@app.route("/")
def index():
    return send_from_directory(FRONTEND_FOLDER, "index.html")

# -----------------------------
# Run Flask
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
