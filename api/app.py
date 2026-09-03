import os
import io
import PyPDF2
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Fetch key from environment or use dummy key to prevent top-level import crash
groq_key = os.getenv("GROQ_API_KEY") or "dummy_key_for_initialization"

client = OpenAI(
    api_key=groq_key,
    base_url="https://api.groq.com/openai/v1"
)

@app.route("/api/upload_and_ask", methods=["POST"])
def upload_and_ask():
    # Verify the real key exists at runtime
    if not os.getenv("GROQ_API_KEY"):
        return jsonify({
            "error": "GROQ_API_KEY environment variable is not configured on Vercel."
        }), 500

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    question = request.form.get("question", "")

    try:
        pdf_stream = io.BytesIO(file.read())
        reader = PyPDF2.PdfReader(pdf_stream)

        extracted_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"

        if not extracted_text.strip():
            return jsonify({"error": "No readable text found in PDF"}), 400

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

if __name__ == "__main__":
    app.run()
