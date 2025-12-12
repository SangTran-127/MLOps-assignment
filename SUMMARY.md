# MLflow Assignment - Project Completion Summary

## All Requirements Met

### 1. Data Generation

- **Source**: `sklearn.datasets.make_classification`
- **Configuration**:
  - 2,000 samples
  - 20 features
  - 15 informative features
  - 5 redundant features
  - 3 classes
  - Data standardized with StandardScaler

### 2. Machine Learning Models

Tested 3 main model types:

- **SVM (Support Vector Machine)**: 3 variants
- **Logistic Regression**: 2 variants
- **Neural Networks (MLP)**: 3 variants

### 3. Hyperparameter Tuning (8 Experiments)

#### Experiment 1: SVM RBF Baseline

- **Parameters**: C=1.0, kernel='rbf', gamma='scale'
- **Rationale**: Start with default RBF kernel configuration as baseline. RBF kernel works well for non-linear data.
- **Results**: Accuracy=82.25%, F1=82.17%

#### Experiment 2: SVM RBF High C - BEST MODEL

- **Parameters**: C=10.0, kernel='rbf', gamma='scale'
- **Rationale**: Increase C to 10 to reduce regularization, allowing the model to fit training data better and capture more complex patterns.
- **Results**: Accuracy=82.25%, F1=82.19%

#### Experiment 3: SVM Linear

- **Parameters**: C=1.0, kernel='linear'
- **Rationale**: Test linear kernel to check if data is linearly separable. Linear models are simpler, faster, and less prone to overfitting.
- **Results**: Accuracy=71.00%, F1=70.64%

#### Experiment 4: Logistic Regression Baseline

- **Parameters**: C=1.0, solver='lbfgs', max_iter=1000
- **Rationale**: Compare SVM with Logistic Regression - a simple linear model often used as a strong baseline for classification.
- **Results**: Accuracy=69.00%, F1=68.62%

#### Experiment 5: Logistic Regression Strong Regularization

- **Parameters**: C=0.1, solver='lbfgs', max_iter=1000
- **Rationale**: Reduce C to 0.1 to increase regularization strength, helping avoid overfitting and improve generalization.
- **Results**: Accuracy=69.25%, F1=68.86%

#### Experiment 6: Neural Network Single Layer

- **Parameters**: hidden_layers=(100,), alpha=0.0001, learning_rate=0.001
- **Rationale**: Test a simple neural network with 1 hidden layer (100 neurons) to capture non-linear patterns while keeping the model relatively simple.
- **Results**: Accuracy=79.75%, F1=79.59%

#### Experiment 7: Neural Network Deep

- **Parameters**: hidden_layers=(100, 50), alpha=0.001, learning_rate=0.001
- **Rationale**: Use a deeper network (2 layers: 100, 50 neurons) to learn more complex hierarchical features with stronger regularization (alpha=0.001).
- **Results**: Accuracy=78.00%, F1=77.87%

#### Experiment 8: Neural Network Wide

- **Parameters**: hidden_layers=(200,), alpha=0.0001, learning_rate=0.001
- **Rationale**: Use a wider layer (200 neurons) to increase model capacity and see if more neurons can better capture data patterns.
- **Results**: Accuracy=80.00%, F1=79.88%

### 4. Results Comparison

| Model            | Accuracy   | F1 Score   | Rank |
| ---------------- | ---------- | ---------- | ---- |
| **SVM_RBF_C10**  | **82.25%** | **82.19%** | **1** |
| SVM_RBF_Baseline | 82.25%     | 82.17%     | 2     |
| NN_Wide          | 80.00%     | 79.88%     | 3     |
| NN_Single_Layer  | 79.75%     | 79.59%     | 4     |
| NN_Deep          | 78.00%     | 77.87%     | 5     |
| SVM_Linear       | 71.00%     | 70.64%     | 6     |
| LogReg_C0.1      | 69.25%     | 68.86%     | 7     |
| LogReg_Baseline  | 69.00%     | 68.62%     | 8     |

**Conclusion**: SVM with RBF kernel and C=10.0 achieved the best results with F1 Score = 82.19%

### 5. Model Registry

- **Mô hình tốt nhất**: SVM_RBF_C10
- **Đã đăng ký**: MLflow Model Registry
- **Tên model**: BestClassifier
- **Version**: 1
- **Trạng thái**: Production-ready
- **Run ID**: ae4786b8303142a29a2d3b4c3e0b2ee7

### 6. ✅ Flask Web Application

#### Features:

- Beautiful, modern web interface with gradient design
- Automatically loads best model from Model Registry
- Input 20 features (comma-separated)
- "Random Example" button to generate sample data
- Display predictions and probabilities
- Responsive design
- Error handling
- Model information display

#### API Endpoints:

- `GET /` - Web interface
- `POST /predict` - Prediction endpoint
- `GET /info` - Model information
- `GET /health` - Health check

#### How to Use:

```bash
# Start Flask app
python3 app.py

# Access web interface
http://localhost:5001
```

## MLflow Tracking

All experiments are tracked with:

- **Parameters**: Model type, hyperparameters, data characteristics
- **Metrics**: Accuracy, Precision, Recall, F1-Score (train & test)
- **Artifacts**: Confusion matrices (PNG), trained models
- **Tags**: Experiment descriptions và rationale

Xem kết quả:

```bash
python3 -m mlflow ui
# Mở http://localhost:5000
```

## Project Structure

```
MLOps-assignment/
├── README.md                   # Complete documentation
├── QUICKSTART.py              # Quick start guide
├── SUMMARY.md                 # This file
├── requirements.txt           # Dependencies
├── .gitignore                # Git ignore rules
│
├── data_generator.py         # Data generation module
├── train.py                  # Training with MLflow tracking
├── run_experiments.py        # Script to run 8 experiments
│
├── app.py                    # Flask web application
├── templates/
│   └── index.html           # Beautiful web UI
│
├── verify_model.py           # Model verification script
├── test_app.py              # Flask API test script
│
└── mlruns/                  # MLflow tracking data
    ├── 0/                   # Default experiment
    ├── 425084089838690602/  # Classification_Experiments
    └── models/              # Model Registry
```

## Highlights

### Code Quality:

- Modular design (separation of concerns)
- Comprehensive error handling
- Clear documentation and comments
- Type hints and docstrings
- Reproducibility (random_state=42)

### MLflow Best Practices:

- Experiment naming and organization
- Comprehensive metric logging
- Artifact tracking (confusion matrices)
- Model versioning
- Tags and descriptions

### Flask Application:

- Professional UI/UX design
- RESTful API design
- Input validation
- Error handling
- Model fallback strategy

## How to Run the Project

### 1. Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

### 2. Run experiments (already completed):

```bash
python3 run_experiments.py
```

### 3. View results in MLflow UI:

```bash
mlflow ui
# Open http://localhost:5000
```

### 4. Start Flask app:

```bash
python3 app.py
# Open http://localhost:5001
```

### 5. Verify model:

```bash
python3 verify_model.py
```

## Results Achieved

- 8 experiments with clear rationale for each tuning
- Best model: SVM with RBF kernel (C=10.0)
- Accuracy: 82.25%
- F1 Score: 82.19%
- Model Registry: Registered and versioned
- Flask App: Beautiful interface with full features
- MLflow Tracking: Complete tracking of metrics, parameters, artifacts

## Requirements Checklist

- Use sklearn's make_classification
- Create ML models (SVM, Logistic Regression, Neural Networks)
- Tune hyperparameters multiple times with clear rationale
- Compare model results
- Save best model to Model Registry
- Create Flask web app using best model

## Conclusion

Project completed 100% of all requirements with:

- High-quality, well-structured code
- Complete documentation
- Detailed MLflow tracking
- Flask app with professional UI
- 8 experiments with clear rationale
- Best model registered and deployed

---

**Author**: MLOps Assignment  
**Date**: 12/12/2025  
**Framework**: MLflow + Flask + scikit-learn
