"""
SRF OCR Tool Flask Backend

This Flask app serves a frontend for OCR file uploads and provides a mock OCR API endpoint.
It uses Flask-CORS to allow cross-origin requests (useful for development).
"""

from flask import Flask, request, jsonify, render_template  # Import Flask modules for web server, JSON, and templates
from flask_cors import CORS  # Import CORS to allow cross-origin requests
from markitdown import MarkItDown
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import io
import torch

# Initialize the Flask application
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS) for all routes
CORS(app)

# Load TrOCR model and processor once at startup
trocr_processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
trocr_model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

def is_image(filename):
    ext = filename.lower().rsplit('.', 1)[-1]
    return ext in ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff']

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
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    filename = file.filename

    if is_image(filename):
        # Use TrOCR for handwritten images
        try:
            image = Image.open(file.stream).convert("RGB")
            pixel_values = trocr_processor(image, return_tensors="pt").pixel_values
            with torch.no_grad():
                generated_ids = trocr_model.generate(pixel_values)
            text = trocr_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            lines = text.splitlines()
            return jsonify({"lines": lines})
        except Exception as e:
            return jsonify({"error": f"TrOCR failed: {str(e)}"}), 500
    else:
        # Use MarkItDown for other file types
        try:
            file_stream = io.BytesIO(file.read())
            md = MarkItDown()
            result = md.convert_stream(file_stream, filename=filename)
            lines = result.text_content.splitlines()
            return jsonify({"lines": lines})
        except Exception as e:
            return jsonify({"error": f"MarkItDown failed: {str(e)}"}), 500

if __name__ == '__main__':
    # Run the Flask development server with debug mode enabled
    app.run(debug=True)