# SRF OCR Tool

**DEMO VIDEO:**  
[![Watch the demo](https://i.ytimg.com/vi/9CDuV0Dphu4/maxresdefault.jpg?sqp=-oaymwEmCIAKENAF8quKqQMa8AEB-AH-CYAChgWKAgwIABABGBMgRih_MA8=&rs=AOn4CLC8LYwUN-jTUu69CM8788MsgKl8zg)](https://youtu.be/9CDuV0Dphu4)

**SRF OCR Tool** is a modern, enterprise-grade web application for extracting text from PDFs and images using advanced OCR models. It features a drag-and-drop interface, camera capture, and export to Excel, CSV, and Word. The backend leverages Microsoft’s TrOCR for handwritten images and MarkItDown for document conversion.

---
## Features

- Drag-and-drop PDF upload
- Camera capture for handwritten notes and images
- Handwriting OCR with Microsoft TrOCR
- Document conversion with MarkItDown (PDF, Office, images, audio, and more)
- Export results as Excel, CSV, or Word
- Responsive, accessible UI
- Modular Python/Flask backend

---

## Repository Structure

```
srf-ocr/
│
├── app.py                  # Flask backend, OCR API, TrOCR & MarkItDown integration
├── requirements.txt        # Python dependencies
│
├── static/
│   ├── styles.css          # Main CSS for frontend
│   └── favicon.ico         # App favicon
│
├── templates/
│   └── index.html          # Main frontend HTML
│
├── README.md               # Project documentation
```

---

## Frontend Overview

- **index.html**:  
  - Drag-and-drop area for PDFs
  - Camera capture for images
  - Results container with loading bar and placeholder
  - Export buttons for Excel, CSV, Word

- **styles.css**:  
  - Modern, accessible, and responsive design
  - Centered results container and loading bar
  - Consistent branding and color palette

---

## Backend Overview

- **app.py**:
  - `/api/ocr` endpoint accepts file uploads
  - Uses TrOCR for handwritten images (JPG, PNG, etc.)
  - Uses MarkItDown for PDFs and other supported documents
  - Returns extracted text as a list of lines (JSON)

- **Dependencies**:
  - `flask`, `flask-cors`: Web server and CORS
  - `transformers`, `torch`, `pillow`: TrOCR OCR pipeline
  - `markitdown[all]`: Document conversion and OCR

---

## API Reference

### `POST /api/ocr`

- **Request:**  
  `multipart/form-data` with a `file` field

- **Response:**  
  ```json
  { "lines": ["Extracted text line 1", "Extracted text line 2", ...] }
  ```

- **Error Handling:**  
  - Returns `400` if no file is uploaded  
  - Returns `500` on processing error
