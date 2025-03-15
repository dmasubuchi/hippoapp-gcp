FROM python:3.9-slim

WORKDIR /app

# Install system dependencies including ffmpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for service account key
RUN mkdir -p /app/credentials

# Set environment variables
ENV PORT=8080
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/service-account-key.json
ENV DEBUG=True

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
