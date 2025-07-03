"""
SRF OCR Tool Flask Backend

This Flask app serves a frontend for OCR file uploads and provides a mock OCR API endpoint.
It uses Flask-CORS to allow cross-origin requests (useful for development).
"""

import logging
import time
import os
import base64
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
from pdf2image import convert_from_bytes

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")

# Initialize the Flask application
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS) for all routes
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")

SYSTEM_PROMPT = (
    "You are an OCR assistant. Extract and return *only* the text from the provided image. "
    "Do not include any explanations, markdown, or extra characters."
)

@app.route('/')
def index():
    """
    Serve the main HTML page.
    This renders the index.html template located in the 'templates' directory.
    """
    return render_template('index.html')

@app.route('/api/ocr', methods=['POST'])
def ocr():
    """
    OCR API endpoint using TrOCR for handwritten images and MarkItDown for other files.
    Accepts a POST request with a file and returns Markdown or plain text as JSON.
    """
    logs = []
    def log(msg):
        logging.info(msg)
        logs.append(msg)

    file = request.files.get('file')
    if not file:
        return jsonify(error="No file uploaded", logs=logs), 400

    name = file.filename.lower()
    content = file.read()
    images = []

    # PDF support: convert each page to an image
    if name.endswith('.pdf'):
        log(f"Converting PDF ({len(content)} bytes) to images…")
        pages = convert_from_bytes(content)
        for i, page in enumerate(pages, start=1):
            buf = page.convert('RGB')
            images.append(buf)
            log(f"Page {i}/{len(pages)} rendered to image")
    else:
        # single static image
        from PIL import Image
        from io import BytesIO
        images.append(Image.open(BytesIO(content)))
        log("Loaded single image for OCR")

    all_text = []
    # Send each page/image to OpenAI
    for idx, img in enumerate(images, start=1):
        # encode as data URL
        from io import BytesIO
        buf = BytesIO()
        img.save(buf, format='PNG')
        data_url = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

        log(f"Sending image page {idx}/{len(images)} to OpenAI…")
        resp = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system",  "content": SYSTEM_PROMPT},
                {"role": "user",    "content": [{"type":"image_url","image_url":{"url":data_url}}]}
            ],
            max_tokens=1024
        )
        page_text = resp.choices[0].message.content.strip()
        log(f"Received text for page {idx}: {page_text[:50]}…")
        all_text.append(page_text)
        # rate-limit backoff
        time.sleep(0.2)

    # Combine pages and return
    full_text = "\n\n".join(all_text)
    return jsonify(description=full_text, logs=logs)

if __name__ == '__main__':
    # Run the Flask development server with debug mode enabled
    app.run(host="0.0.0.0", port=5002)
