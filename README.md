# MLOps Assignment - MLflow Classification Project

This project demonstrates a complete MLOps workflow using MLflow for experiment tracking, model registry, and deployment.

## Project Overview

This project includes:

- **Data Generation**: Synthetic classification data using sklearn's `make_classification`
- **Model Training**: Multiple machine learning models (SVM, Logistic Regression, Neural Networks)
- **Hyperparameter Tuning**: 8 different experiments with reasoned hyperparameter choices
- **MLflow Tracking**: Track all experiments, metrics, parameters, and artifacts
- **Model Registry**: Register and version the best performing model
- **Flask Web App**: Web interface for making predictions with the best model

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Docker & Docker Compose (optional, for containerized deployment)
- Git (for version control)

### Installation

1. Install required packages:

```bash
pip install -r requirements.txt
```

## Running Experiments

### Step 1: Run All Experiments

Execute the main experiment script to train and compare multiple models:

```bash
python run_experiments.py
```

This will:

- Generate synthetic classification data (2000 samples, 20 features, 3 classes)
- Train 8 different models with various hyperparameters:
  1. **SVM RBF Baseline** (C=1.0)
  2. **SVM RBF High C** (C=10.0) - Less regularization
  3. **SVM Linear** - Simpler decision boundary
  4. **Logistic Regression Baseline** (C=1.0)
  5. **Logistic Regression Strong Regularization** (C=0.1)
  6. **Neural Network Single Layer** (100 neurons)
  7. **Neural Network Deep** (100, 50 neurons) - Hierarchical features
  8. **Neural Network Wide** (200 neurons) - Higher capacity
- Log all metrics, parameters, and artifacts to MLflow
- Compare all models and identify the best one
- Register the best model to MLflow Model Registry

### Step 2: View Experiment Results

Launch the MLflow UI to explore results:

```bash
python3 -m mlflow ui
```

> **Note**: If `mlflow` command is not found, use `python3 -m mlflow ui` instead.

Then open [http://localhost:5000](http://localhost:5000) in your browser.

In the MLflow UI, you can:

- Compare metrics across all runs
- View confusion matrices
- Analyze parameters and their impact
- See the registered models

## CI/CD & Deployment

### GitHub Actions Pipeline

The project includes automated CI/CD pipeline that runs on every push:

- Automated testing and validation
- Code quality checks (flake8)
- Full experiment runs
- Artifact uploads
- Build and package

View pipeline status: [GitHub Actions](https://github.com/SangTran-127/MLOps-assignment/actions)

### Docker Deployment

#### Quick Start with Docker Compose

```bash
docker-compose up -d
```

This starts both MLflow UI (port 5000) and Flask app (port 5001).

#### Build Docker Image Only

```bash
docker build -t mlops-app .
docker run -d -p 5001:5001 mlops-app
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment guide.

---

## Flask Web Application

### Launch the Web App

After running the experiments, start the Flask application:

```bash
python app.py
```

The web app will be available at [http://localhost:5001](http://localhost:5001)

### Using the Web Interface

1. **Enter Features**: Input 20 comma-separated numerical values (e.g., standardized features between -3 and 3)
2. **Random Example**: Click to generate random sample data
3. **Predict**: Get classification result with probability distribution
4. **Model Info**: View information about the loaded model

### API Endpoints

- `GET /` - Web interface
- `POST /predict` - Make predictions
  ```bash
  curl -X POST http://localhost:5001/predict \
    -H "Content-Type: application/json" \
    -d '{"features": [1.5, -0.3, 2.1, 0.8, -1.2, 0.5, 1.1, -0.9, 0.4, 1.7, -0.6, 0.2, 1.3, -0.4, 0.9, 1.0, -0.7, 0.3, 1.4, -0.5]}'
  ```
- `GET /info` - Get model information
- `GET /health` - Health check

## Experiment Rationale

### Experiment 1: SVM RBF Baseline (C=1.0)

**Rationale**: Start with default RBF kernel as baseline. RBF works well for non-linear data.

### Experiment 2: SVM RBF High C (C=10.0)

**Rationale**: Reduce regularization to allow the model to fit training data more closely and capture complex patterns.

### Experiment 3: SVM Linear

**Rationale**: Test if data has linear separability. Linear models are simpler, faster, and less prone to overfitting.

### Experiment 4: Logistic Regression Baseline (C=1.0)

**Rationale**: Compare SVM with a simpler linear model often used as strong baseline for classification.

### Experiment 5: Logistic Regression Strong Regularization (C=0.1)

**Rationale**: Increase regularization strength to prevent overfitting and improve generalization.

### Experiment 6: Neural Network Single Layer (100 neurons)

**Rationale**: Try neural network with one hidden layer to capture non-linear patterns while keeping model simple.

### Experiment 7: Neural Network Deep (100, 50 neurons, alpha=0.001)

**Rationale**: Use deeper network to learn hierarchical features with stronger regularization.

### Experiment 8: Neural Network Wide (200 neurons)

**Rationale**: Increase model capacity with more neurons to better represent data patterns.

## Project Structure

```
MLOps-assignment/
├── README.md                      # This file
├── SUMMARY.md                     # Project summary (Vietnamese)
├── DEPLOYMENT.md                  # Deployment guide
├── CI_CD_GUIDE.md                # CI/CD guide (Vietnamese)
│
├── requirements.txt               # Python dependencies
├── .gitignore                    # Git ignore rules
├── .dockerignore                 # Docker ignore rules
│
├── Dockerfile                    # Docker image definition
├── docker-compose.yml            # Multi-container setup
│
├── .github/
│   └── workflows/
│       └── mlops-pipeline.yml   # GitHub Actions CI/CD
│
├── data_generator.py             # Data generation
├── train.py                      # Model training with MLflow
├── run_experiments.py            # Main experiment script
├── test_models.py                # Unit tests
│
├── app.py                        # Flask web application
├── verify_model.py               # Model verification
├── templates/
│   └── index.html               # Web interface
│
├── start_mlflow_ui.sh           # Quick start MLflow UI
├── start_flask_app.sh           # Quick start Flask app
│
└── mlruns/                       # MLflow tracking data (auto-generated)
```

## Metrics Tracked

For each experiment, MLflow tracks:

- **Parameters**: Model hyperparameters, data characteristics
- **Metrics**: Accuracy, Precision, Recall, F1-Score (train & test)
- **Artifacts**: Confusion matrices, model files
- **Tags**: Model descriptions and experiment rationale

## Model Selection

The best model is automatically selected based on **Test F1 Score**, which balances precision and recall. The selected model is:

1. Registered in MLflow Model Registry
2. Transitioned to "Production" stage
3. Loaded by the Flask app for serving predictions

## Customization

### Use Different Data

You can modify the data generation in `run_experiments.py`:

```python
# Use MNIST instead
from data_generator import load_mnist_data
X_train, X_test, y_train, y_test, scaler = load_mnist_data(subset_size=5000)
```

### Add More Experiments

Add new experiments to `run_experiments.py`:

```python
model_new, acc_new, f1_new = train_svm(
    X_train, X_test, y_train, y_test,
    C=5.0,
    kernel='poly',
    gamma='auto',
    run_name="SVM_Poly",
    description="Your rationale here"
)
```

## Testing

The project includes comprehensive unit tests:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest test_models.py -v

# Run with coverage
pytest test_models.py --cov=. --cov-report=html
```

Tests cover:
- Data generation and validation
- Model training for all model types
- Prediction functionality

---

## Notes

- All experiments use `random_state=42` for reproducibility
- Models are automatically scaled using StandardScaler
- Neural networks use early stopping to prevent overfitting
- The Flask app loads the model from "Production" stage in Model Registry
- CI/CD pipeline automatically runs tests on every push

## Assignment Requirements Checklist

- Use sklearn's make_classification for data generation
- ✅ Create multiple ML models (SVM, Logistic Regression, Neural Networks)
- ✅ Tune hyperparameters with clear rationale for each experiment (8 experiments)
- ✅ Compare model results with metrics and visualizations
- ✅ Register best model to MLflow Model Registry
- ✅ Create Flask web application that uses the best model

## Troubleshooting

### Model Not Loading in Flask App

If the Flask app can't load the model:

1. Make sure you've run `python run_experiments.py` first
2. Check that MLflow tracking data exists in `mlruns/` directory
3. The app will fallback to loading from latest run if Model Registry fails

### MLflow UI Not Starting

Make sure port 5000 is available, or specify a different port:

```bash
python3 -m mlflow ui --port 5002
```

### Flask App Port Conflict

Change the port in `app.py` or run:

```bash
python app.py
# Then manually access http://localhost:5001
```

---

**Author**: MLOps Assignment  
**Date**: December 2025  
**Framework**: MLflow + Flask + scikit-learn
