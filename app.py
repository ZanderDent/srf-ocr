"""
SRF OCR Tool Flask Backend

This Flask app serves a frontend for OCR file uploads and provides a mock OCR API endpoint.
It uses Flask-CORS to allow cross-origin requests (useful for development).
"""

from flask import Flask, request, jsonify, render_template  # Import Flask modules for web server, JSON, and templates
from flask_cors import CORS  # Import CORS to allow cross-origin requests

# Initialize the Flask application
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS) for all routes
CORS(app)

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
    Mock OCR API endpoint.
    Accepts a POST request (with or without a file) and returns a mock OCR result as JSON.
    """
    # In a real implementation, you would process the uploaded file here.
    # For now, we return a static list of lines as a mock OCR result.
    mock_text = [
        "This is a mock OCR line 1.",
        "This is a mock OCR line 2.",
        "Another line from the document.",
        "End of mock OCR output."
    ]
    # Return the mock OCR lines as a JSON response
    return jsonify({"lines": mock_text})

if __name__ == '__main__':
    # Run the Flask development server with debug mode enabled
    app.run(debug=True)