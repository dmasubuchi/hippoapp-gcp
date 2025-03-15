FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for service account key
RUN mkdir -p /app/credentials

# Set environment variables
ENV PORT=8080
# Note: GOOGLE_APPLICATION_CREDENTIALS should be set at runtime
# ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/service-account-key.json

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
