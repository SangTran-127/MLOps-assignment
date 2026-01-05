# Dockerfile for MLOps Flask Application
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  build-essential \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY data_generator.py .
COPY train.py .
COPY run_experiments.py .
COPY verify_model.py .
COPY templates/ templates/
COPY start_all.sh .

# Create mlruns directory (models will be trained on startup if needed)
RUN mkdir -p mlruns && chmod +x start_all.sh

# Expose ports: 5000 for MLflow UI, 5001 for Flask app
EXPOSE 5000 5001

# Set environment variables
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:5001/health || exit 1

# Run both MLflow UI and Flask app
CMD ["./start_all.sh"]
