"""
SRF OCR Tool Flask Backend

This Flask app serves a frontend for OCR file uploads and provides an OCR API endpoint.
It uses Flask-CORS to allow cross-origin requests and PyMuPDF (fitz) for PDF→image conversion.
"""

import logging
import time
import os
import base64
from io import BytesIO
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
from PIL import Image
import fitz  # PyMuPDF

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")

# Initialize Flask
app = Flask(__name__)
CORS(app)

# OpenAI credentials
openai.api_key      = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")

SYSTEM_PROMPT = (
    "You are an OCR assistant. Extract and return *only* the text from the provided image. "
    "Do not include any explanations, markdown, or extra characters."
)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/ocr', methods=['POST'])
def ocr():
    logs = []
    def log(msg):
        logging.info(msg)
        logs.append(msg)

    uploaded = request.files.get('file')
    if not uploaded:
        return jsonify(error="No file uploaded", logs=logs), 400

    name = uploaded.filename.lower()
    data = uploaded.read()
    images = []

    # --- PDF support via PyMuPDF ---
    if name.endswith('.pdf'):
        log(f"Opening PDF ({len(data)} bytes) with PyMuPDF…")
        pdf = fitz.open(stream=data, filetype="pdf")
        for i, page in enumerate(pdf, start=1):
            pix = page.get_pixmap()                     # render page
            img = Image.open(BytesIO(pix.tobytes("png")))
            images.append(img)
            log(f"Rendered page {i}/{len(pdf)} to image")
    else:
        # single static image
        img = Image.open(BytesIO(data))
        images.append(img)
        log("Loaded single image for OCR")

    # --- Send each image to OpenAI ---
    all_text = []
    for idx, img in enumerate(images, start=1):
        buf = BytesIO()
        img.save(buf, format='PNG')
        data_url = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

        log(f"Sending page {idx}/{len(images)} to OpenAI…")
        resp = openai.chat.completions.create(
            model="gpt-4o",  # or whatever vision-enabled model you choose
            messages=[
                {"role": "system",  "content": SYSTEM_PROMPT},
                {"role": "user",    "content": [{"type":"image_url","image_url":{"url":data_url}}]}
            ],
            max_tokens=1024
        )
        page_text = resp.choices[0].message.content.strip()
        log(f"Received text for page {idx}: {page_text[:50]}…")
        all_text.append(page_text)
        time.sleep(0.2)  # avoid hitting RPM/TPM limits

    full_text = "\n\n".join(all_text)
    return jsonify(description=full_text, logs=logs)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002)
