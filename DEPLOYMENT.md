# 🚀 Deployment & CI/CD Guide

This document covers deployment options and CI/CD pipeline for the MLOps project.

## 📋 Table of Contents

- [GitHub Actions CI/CD](#github-actions-cicd)
- [Docker Deployment](#docker-deployment)
- [Local Development](#local-development)
- [Testing](#testing)

---

## 🔄 GitHub Actions CI/CD

The project includes automated CI/CD pipeline using GitHub Actions.

### Pipeline Overview

The pipeline consists of two main jobs:

#### 1. Test & Validate Job

Runs on every push to `main` or `develop` branch:

- ✅ Checkout code
- ✅ Set up Python 3.9
- ✅ Install dependencies
- ✅ Run linting (flake8)
- ✅ Validate data generation
- ✅ Validate model training
- ✅ Run full experiments
- ✅ Upload MLflow artifacts
- ✅ Generate experiment report

#### 2. Build & Package Job

Runs after successful tests:

- ✅ Package application
- ✅ Create release artifacts
- ✅ Upload build artifacts

### Viewing Pipeline Results

1. Go to your GitHub repository
2. Click on **Actions** tab
3. Select the latest workflow run
4. View logs and artifacts

### Pipeline Configuration

The pipeline is defined in `.github/workflows/mlops-pipeline.yml`

---

## 🐳 Docker Deployment

### Option 1: Using Docker Compose (Recommended)

Run both MLflow server and Flask app together:

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Access:

- **MLflow UI**: http://localhost:5000
- **Flask App**: http://localhost:5001

### Option 2: Using Dockerfile Only

Build and run Flask app only:

```bash
# Build image
docker build -t mlops-app .

# Run container
docker run -d -p 5001:5001 --name mlops-flask mlops-app

# View logs
docker logs -f mlops-flask

# Stop container
docker stop mlops-flask
docker rm mlops-flask
```

### Docker Image Details

**Base Image**: `python:3.9-slim`
**Exposed Port**: `5001`
**Health Check**: `GET /health`

---

## 💻 Local Development

### Prerequisites

- Python 3.9+
- pip
- virtualenv (optional)

### Setup

1. **Clone repository**:

```bash
git clone git@github.com:SangTran-127/MLOps-assignment.git
cd MLOps-assignment
```

2. **Create virtual environment** (optional):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Run experiments**:

```bash
python3 run_experiments.py
```

5. **Start MLflow UI**:

```bash
python3 -m mlflow ui
# Open http://localhost:5000
```

6. **Start Flask app**:

```bash
python3 app.py
# Open http://localhost:5001
```

### Quick Start Scripts

For convenience, use the provided scripts:

```bash
# Start MLflow UI
./start_mlflow_ui.sh

# Start Flask app
./start_flask_app.sh
```

---

## 🧪 Testing

### Running Tests

The project includes unit tests for data generation and model training.

**Install test dependencies**:

```bash
pip install pytest pytest-cov
```

**Run all tests**:

```bash
pytest test_models.py -v
```

**Run with coverage**:

```bash
pytest test_models.py --cov=. --cov-report=html
```

**Run specific test**:

```bash
pytest test_models.py::TestDataGeneration::test_generate_synthetic_data_shape -v
```

### Test Structure

- `TestDataGeneration`: Tests for data generation
- `TestModelTraining`: Tests for model training
- `TestModelPrediction`: Tests for model predictions

### Continuous Integration

Tests run automatically on every push via GitHub Actions. View results in the Actions tab.

---

## 🔧 Configuration

### Environment Variables

- `MLFLOW_TRACKING_URI`: MLflow server URL (default: local file system)
- `MPLCONFIGDIR`: Matplotlib config directory (set to `/tmp/matplotlib` in CI)

### Ports

- **5000**: MLflow UI
- **5001**: Flask Application

### Customization

Modify these files to customize behavior:

- `run_experiments.py`: Experiment configuration
- `app.py`: Flask app settings
- `docker-compose.yml`: Docker services
- `.github/workflows/mlops-pipeline.yml`: CI/CD pipeline

---

## 📊 Monitoring & Logging

### MLflow Tracking

All experiments are tracked in MLflow with:

- Parameters
- Metrics
- Artifacts (confusion matrices, models)
- Tags

Access tracking data:

- Locally: `mlruns/` directory
- UI: http://localhost:5000

### Application Logs

**Docker logs**:

```bash
docker-compose logs flask-app
docker-compose logs mlflow-server
```

**Local logs**:
Check `*.log` files in project directory

---

## 🚀 Production Deployment

### Recommended Setup

1. **Use external MLflow tracking server**:

   - Set `MLFLOW_TRACKING_URI` environment variable
   - Example: `http://mlflow-server.example.com`

2. **Use external database** for MLflow:

   - PostgreSQL or MySQL recommended
   - Configure via `mlflow server --backend-store-uri`

3. **Use object storage** for artifacts:

   - S3, Azure Blob Storage, or GCS
   - Configure via `mlflow server --default-artifact-root`

4. **Enable authentication**:

   - Add authentication middleware to Flask app
   - Use API keys or OAuth2

5. **Use production WSGI server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5001 app:app
   ```

### Scaling

- Use Kubernetes for container orchestration
- Load balance Flask app with multiple replicas
- Use Redis for caching predictions
- Implement request queuing for batch predictions

---

## 📝 Troubleshooting

### Common Issues

**Issue**: MLflow UI not accessible
**Solution**: Check if port 5000 is available, try different port:

```bash
python3 -m mlflow ui --port 5002
```

**Issue**: Docker container fails to start
**Solution**: Check logs:

```bash
docker-compose logs
```

**Issue**: Models not loading in Flask app
**Solution**: Ensure experiments have been run:

```bash
python3 run_experiments.py
```

**Issue**: GitHub Actions failing
**Solution**: Check workflow logs in Actions tab, common causes:

- Missing dependencies
- Test failures
- Timeout issues

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests locally
5. Push and create a Pull Request

The CI/CD pipeline will automatically run tests on your PR.

---

## 📚 Additional Resources

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

**Last Updated**: December 2025  
**Maintainer**: MLOps Assignment Team
