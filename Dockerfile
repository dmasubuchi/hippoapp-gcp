# Use the official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements files
COPY agentspace-app/requirements.txt requirements.txt
COPY data-ingestion/requirements.txt data-ingestion-requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt -r data-ingestion-requirements.txt

# Copy application code
COPY agentspace-app/ .
COPY data-ingestion/scripts/ ./data-ingestion/scripts/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Run the application
CMD ["python", "-m", "app.main"]