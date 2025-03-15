FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for service account key
RUN mkdir -p /app/credentials

# Create a mock service account key for testing
RUN echo '{"type":"service_account","project_id":"lucid-inquiry-453823-b0","private_key_id":"mock-key-id","private_key":"-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCxlGlLH1vxQJKO\nMOCKDC0uQrBQkjlK6WpfHJgcjjQXYlPS8gqV9HVhvPD5QYUYwAIqLEYtAFrktopE\nKA5H8YgZZL+0zdQHYFVlUmJzwqrYaZwVz+ohZmzfKKD0Xft9c8K+xJjRsXTEHBs+\nDzXpBZHYXj3aLnZI1Vx/J/JDyCB9I9BXcr9xcFRv8qBOyQEJxpHBLMlbLDMwJJZ/\nYd0hnuP9iyxwOxVVO/Al7oBLrXjEiRwJJ9rHoGZ9YMkUJ9UXVYD5z6l8QqlEiwWH\nHs/yZMxqFKTe3a3yxATsS5E0Oc5EXXaKRPM8wUYwmQhwgQYhIfSdj7fKQvjrfwrO\nPmEQ3KVvAgMBAAECggEABQwfpaoYWpUQMmRlKK5QzYQnpnCBF8fOWZqDXKYFOFV0\nJXV8wVxbzm1wmbCKRpzHQbHmEVFWXE9YYAfZSCyGdH3I+IEHeZ5gHFQJHLzqILNv\nVxlQRFTGG9uf9HxJeONLHVZvwUy5yW5i1CjYrDzaOyWZlH1a2m2U4oW5NzBQXcv/\nROQIHFbBmxnwmfypTu3XvOxAUXR2GYo4cQ5NeKwKw9TfdFMuTKxsqRiPPEOHEIAF\nEAKLR5wKh0ILBIoQ2k4vB3JjkZYhGTcWy+h+/Yp7zUOGFMJOsQfQmJFHBaDIvjrP\nBOkGnKNBQwwXt5xKVQlTZ8BKgUVjGIZj8dYMvNjQAQKBgQDrEQ9iau7hjQQNh8VM\nMOCKDC0uQrBQkjlK6WpfHJgcjjQXYlPS8gqV9HVhvPD5QYUYwAIqLEYtAFrktopE\nKA5H8YgZZL+0zdQHYFVlUmJzwqrYaZwVz+ohZmzfKKD0Xft9c8K+xJjRsXTEHBs+\nDzXpBZHYXj3aLnZI1Vx/J/JDyCB9I9BXcr9xcFRv8qBOyQEJxpHBLMlbLDMwJJZ/\n-----END PRIVATE KEY-----","client_email":"hippoapp-service@lucid-inquiry-453823-b0.iam.gserviceaccount.com","client_id":"mock-client-id","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/hippoapp-service%40lucid-inquiry-453823-b0.iam.gserviceaccount.com"}' > /app/credentials/service-account-key.json

# Set environment variables
ENV PORT=8080
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/service-account-key.json

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
