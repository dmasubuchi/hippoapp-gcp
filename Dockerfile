FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY agentspace-app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY agentspace-app/ .

# Create directory for service account key
RUN mkdir -p /app/credentials

# Set environment variables
ENV PORT=8080
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/service-account-key.json

# Create a mock service account key for deployment
# This will be replaced by the actual key during deployment
RUN echo '{"type":"service_account","project_id":"lucid-inquiry-453823-b0"}' > /app/credentials/service-account-key.json

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
