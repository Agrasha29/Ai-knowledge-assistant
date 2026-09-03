import os
import io
import json
import cgi
import PyPDF2
from http.server import BaseHTTPRequestHandler
from openai import OpenAI

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        # 1. Parse Environment Variables
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "GROQ_API_KEY environment variable is missing on Vercel."}).encode('utf-8'))
            return

        # 2. Parse Multipart Form Data (File + Question)
        try:
            content_type = self.headers.get('Content-Type')
            if not content_type or 'multipart/form-data' not in content_type:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Content-Type must be multipart/form-data"}).encode('utf-8'))
                return

            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers['Content-Type'],
                }
            )

            file_item = form['file'] if 'file' in form else None
            question_item = form['question'] if 'question' in form else None

            if not file_item or not file_item.file:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No file uploaded"}).encode('utf-8'))
                return

            question = question_item.value if question_item else ""
            if not question.strip():
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Question is required"}).encode('utf-8'))
                return

            # 3. Extract PDF Text in RAM
            pdf_bytes = file_item.file.read()
            pdf_stream = io.BytesIO(pdf_bytes)
            reader = PyPDF2.PdfReader(pdf_stream)

            extracted_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"

            if not extracted_text.strip():
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No readable text found in PDF"}).encode('utf-8'))
                return

            # 4. Call Groq API via OpenAI SDK
            client = OpenAI(
                api_key=groq_api_key,
                base_url="https://api.groq.com/openai/v1"
            )

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"Document content:\n{extracted_text}"},
                    {"role": "user", "content": question}
                ],
                max_tokens=300
            )

            answer = response.choices[0].message.content

            # 5. Send Success Response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"answer": answer}).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
