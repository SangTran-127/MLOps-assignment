# Dockerfile for MLOps Flask Application
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY data_generator.py .
COPY train.py .
COPY verify_model.py .
COPY templates/ templates/

# Copy MLflow artifacts (if needed)
# Note: In production, you'd load models from MLflow server
COPY mlruns/ mlruns/

# Expose Flask port
EXPOSE 5001

# Set environment variables
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:5001/health')" || exit 1

# Run Flask application
CMD ["python", "app.py"]
