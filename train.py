"""
Training module with MLflow tracking for classification experiments.
Supports SVM, Logistic Regression, and Neural Network models.
"""

import mlflow
import mlflow.sklearn
import numpy as np
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import os


def log_metrics(y_true, y_pred, prefix=""):
    """
    Calculate and log metrics to MLflow.
    """
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
    
    mlflow.log_metric(f"{prefix}accuracy", accuracy)
    mlflow.log_metric(f"{prefix}precision", precision)
    mlflow.log_metric(f"{prefix}recall", recall)
    mlflow.log_metric(f"{prefix}f1_score", f1)
    
    return accuracy, precision, recall, f1


def plot_confusion_matrix(y_true, y_pred, run_name):
    """
    Create and log confusion matrix plot.
    """
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix - {run_name}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    
    # Save and log to MLflow
    plot_path = f"confusion_matrix_{run_name}.png"
    plt.savefig(plot_path)
    mlflow.log_artifact(plot_path)
    plt.close()
    os.remove(plot_path)


def train_svm(X_train, X_test, y_train, y_test, C=1.0, kernel='rbf', 
              gamma='scale', run_name="SVM", description=""):
    """
    Train SVM classifier with MLflow tracking.
    
    Args:
        C: Regularization parameter
        kernel: Kernel type ('linear', 'poly', 'rbf', 'sigmoid')
        gamma: Kernel coefficient
        run_name: Name for the MLflow run
        description: Description of the experiment
    """
    with mlflow.start_run(run_name=run_name):
        # Log parameters
        mlflow.log_param("model_type", "SVM")
        mlflow.log_param("C", C)
        mlflow.log_param("kernel", kernel)
        mlflow.log_param("gamma", gamma)
        mlflow.log_param("n_features", X_train.shape[1])
        mlflow.log_param("n_samples", X_train.shape[0])
        mlflow.log_param("n_classes", len(np.unique(y_train)))
        
        if description:
            mlflow.set_tag("description", description)
        
        # Train model
        print(f"\nTraining {run_name}...")
        model = SVC(C=C, kernel=kernel, gamma=gamma, random_state=42)
        model.fit(X_train, y_train)
        
        # Make predictions
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
        
        # Log metrics
        train_acc, train_prec, train_rec, train_f1 = log_metrics(y_train, y_train_pred, "train_")
        test_acc, test_prec, test_rec, test_f1 = log_metrics(y_test, y_test_pred, "test_")
        
        # Log confusion matrix
        plot_confusion_matrix(y_test, y_test_pred, run_name)
        
        # Log model
        mlflow.sklearn.log_model(model, "model")
        
        print(f"Test Accuracy: {test_acc:.4f}")
        print(f"Test F1 Score: {test_f1:.4f}")
        
        return model, test_acc, test_f1


def train_logistic_regression(X_train, X_test, y_train, y_test, C=1.0, 
                              max_iter=1000, solver='lbfgs', run_name="LogisticRegression",
                              description=""):
    """
    Train Logistic Regression classifier with MLflow tracking.
    
    Args:
        C: Inverse of regularization strength
        max_iter: Maximum number of iterations
        solver: Algorithm to use ('lbfgs', 'liblinear', 'saga')
        run_name: Name for the MLflow run
        description: Description of the experiment
    """
    with mlflow.start_run(run_name=run_name):
        # Log parameters
        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_param("C", C)
        mlflow.log_param("max_iter", max_iter)
        mlflow.log_param("solver", solver)
        mlflow.log_param("n_features", X_train.shape[1])
        mlflow.log_param("n_samples", X_train.shape[0])
        mlflow.log_param("n_classes", len(np.unique(y_train)))
        
        if description:
            mlflow.set_tag("description", description)
        
        # Train model
        print(f"\nTraining {run_name}...")
        model = LogisticRegression(C=C, max_iter=max_iter, solver=solver, 
                                  random_state=42, multi_class='auto')
        model.fit(X_train, y_train)
        
        # Make predictions
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
        
        # Log metrics
        train_acc, train_prec, train_rec, train_f1 = log_metrics(y_train, y_train_pred, "train_")
        test_acc, test_prec, test_rec, test_f1 = log_metrics(y_test, y_test_pred, "test_")
        
        # Log confusion matrix
        plot_confusion_matrix(y_test, y_test_pred, run_name)
        
        # Log model
        mlflow.sklearn.log_model(model, "model")
        
        print(f"Test Accuracy: {test_acc:.4f}")
        print(f"Test F1 Score: {test_f1:.4f}")
        
        return model, test_acc, test_f1


def train_neural_network(X_train, X_test, y_train, y_test, 
                        hidden_layers=(100,), alpha=0.0001, learning_rate_init=0.001,
                        run_name="NeuralNetwork", description=""):
    """
    Train Neural Network (MLP) classifier with MLflow tracking.
    
    Args:
        hidden_layers: Tuple of hidden layer sizes
        alpha: L2 penalty parameter
        learning_rate_init: Initial learning rate
        run_name: Name for the MLflow run
        description: Description of the experiment
    """
    with mlflow.start_run(run_name=run_name):
        # Log parameters
        mlflow.log_param("model_type", "NeuralNetwork")
        mlflow.log_param("hidden_layers", str(hidden_layers))
        mlflow.log_param("alpha", alpha)
        mlflow.log_param("learning_rate_init", learning_rate_init)
        mlflow.log_param("n_features", X_train.shape[1])
        mlflow.log_param("n_samples", X_train.shape[0])
        mlflow.log_param("n_classes", len(np.unique(y_train)))
        
        if description:
            mlflow.set_tag("description", description)
        
        # Train model
        print(f"\nTraining {run_name}...")
        model = MLPClassifier(
            hidden_layer_sizes=hidden_layers,
            alpha=alpha,
            learning_rate_init=learning_rate_init,
            max_iter=500,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1
        )
        model.fit(X_train, y_train)
        
        # Make predictions
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
        
        # Log metrics
        train_acc, train_prec, train_rec, train_f1 = log_metrics(y_train, y_train_pred, "train_")
        test_acc, test_prec, test_rec, test_f1 = log_metrics(y_test, y_test_pred, "test_")
        
        # Log confusion matrix
        plot_confusion_matrix(y_test, y_test_pred, run_name)
        
        # Log model
        mlflow.sklearn.log_model(model, "model")
        
        print(f"Test Accuracy: {test_acc:.4f}")
        print(f"Test F1 Score: {test_f1:.4f}")
        
        return model, test_acc, test_f1
