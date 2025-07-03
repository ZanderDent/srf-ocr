# SRF OCR Tool

A Flask-based web application for Optical Character Recognition (OCR) using the OpenAI Vision API (e.g. GPT-4o with vision capabilities). Supports image uploads (PNG, JPG, JPEG, GIF, WebP), camera capture, and multi-page PDF processing. Displays live logs in a dedicated panel and extracts **only** the text. Provides export to Excel, CSV, and Word formats.

---

## Features

* **Image Upload**: Drag & drop or browse to upload image files.
* **Camera Capture**: Snap a photo directly in the browser.
* **PDF Support**: Convert each PDF page to an image and OCR each page—this ensures proper processing for any embedded images within each PDF.
* **Collapsible Logs Panel**: All backend JSON requests and responses (including logs) are shown in a dedicated, toggleable panel on the input page. Logs are **not** shown in the results area.
* **Clean Text Output**: Instructs OpenAI to return *only* extracted text (no markdown or explanations).
* **Export Options**: Download OCR result as Excel (.xlsx), CSV (.csv), or Word (.docx).
* **Do Another Conversion**: Reset UI for multiple uses without page reload.

---

## Prerequisites

1. **Python 3.8+**
2. **Poppler** (for PDF → image conversion):

   * macOS: `brew install poppler`
   * Ubuntu/Debian: `sudo apt-get install poppler-utils`
3. **Node.js** is *not* required—frontend runs as static HTML/JS in the Flask app.

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-org/srf-ocr-tool.git
   cd srf-ocr-tool
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   *`requirements.txt` includes:*

   ```text
   flask
   flask-cors
   openai
   pdf2image
   pillow
   transformers
   torch
   python-dotenv
   ```

---

## Configuration

The app uses environment variables for API credentials and organization context. You can set these in a `.env` file or in your shell profile:

* `OPENAI_API_KEY` — Your OpenAI secret key with `model.request` and `chat.completions.create` scopes.
* `OPENAI_ORGANIZATION` — (Optional) The OpenAI Organization ID if you belong to multiple orgs.

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_ORGANIZATION="org-..."
```

---

## Running the Application

```bash
# Ensure env vars are set
python app.py
```

* The server starts on [http://127.0.0.1:5002](http://127.0.0.1:5002)
* Visit that URL in your browser.

---

## Project Structure

```
├── app.py            # Flask backend
├── templates/
│   └── index.html    # Main front-end template
├── static/
│   ├── styles.css
│   ├── logo.jpg
│   └── favicon.ico
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## How It Works

1. **File / Camera Input** → `handleFile()` in `index.html` JavaScript.
2. **Loading Bar** → Estimates upload/OCR time.
3. **Upload to `/api/ocr`** → Flask endpoint reads file.
4. **PDF Handling**:

   * Uses `pdf2image.convert_from_bytes()` to render each page.
   * Logs page render events.
5. **Image to Data URL** → Base64 in-memory.
6. **OpenAI Vision Call**:

   * System prompt: *"Extract and return only the text..."*
   * User message with image URL.
   * Collects response text per page.
7. **Concatenate & Return**:

   * JSON payload: `{ description: "...", logs: [ ... ] }`.
   * Frontend dumps `logs` in the collapsible logs panel and shows `description` in the results area.

---

## Troubleshooting

* **429 insufficient\_quota**: Ensure your **Organization budget** is not hit. Raise or disable in OpenAI Dashboard → Billing → Usage limits.
* **401 missing scopes**: Regenerate API key with **Full access** or add `model.request` & `chat.completions.create` scopes.
* **pdf2image errors**: Confirm Poppler is installed and on your PATH.

---

## License

MIT © SRF Consulting Inc.
