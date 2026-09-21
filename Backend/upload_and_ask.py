import os
import io
import PyPDF2
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["POST", "GET"])
@app.route("/api/upload_and_ask", methods=["POST", "GET"])
def handler_func():
    if request.method == "GET":
        return jsonify({"status": "API endpoint active"}), 200

    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        return jsonify({
            "error": "GROQ_API_KEY environment variable is missing on Vercel."
        }), 500

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    question = request.form.get("question", "")

    if not question.strip():
        return jsonify({"error": "Question is required"}), 400

    try:
        client = OpenAI(
            api_key=groq_api_key,
            base_url="https://api.groq.com/openai/v1"
        )

        pdf_stream = io.BytesIO(file.read())
        reader = PyPDF2.PdfReader(pdf_stream)

        extracted_text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text + "\n"

        if not extracted_text.strip():
            return jsonify({"error": "No readable text found in PDF."}), 400

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"Document content:\n{extracted_text}"},
                {"role": "user", "content": question}
            ],
            max_tokens=300
        )

        return jsonify({"answer": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel imports 'app' directly for Flask WSGI
