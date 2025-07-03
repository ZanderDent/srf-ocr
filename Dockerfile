# Dockerfile
FROM python:3.10-slim

# Install Poppler for PDF→image conversion
RUN apt-get update && \
    apt-get install -y poppler-utils && \
    rm -rf /var/lib/apt/lists/*

# Copy your app
WORKDIR /app
COPY . /app

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (for local dev, ignored by Vercel)
EXPOSE 5002

# Start the Flask server
CMD ["python", "app.py"]
