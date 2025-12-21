"""
Unit tests for the MLOps project.
Tests data generation, training, and model validation.
"""

import pytest
import numpy as np
from data_generator import generate_synthetic_data
from train import train_svm, train_logistic_regression, train_neural_network
import mlflow


class TestDataGeneration:
    """Test data generation functionality."""
    
    def test_generate_synthetic_data_shape(self):
        """Test that generated data has correct shape."""
        X_train, X_test, y_train, y_test, scaler = generate_synthetic_data(
            n_samples=100,
            n_features=10,
            n_classes=2,
            random_state=42
        )
        
        assert X_train.shape[1] == 10, "Training features should have 10 columns"
        assert X_test.shape[1] == 10, "Test features should have 10 columns"
        assert len(X_train) == 80, "Training set should have 80 samples (80% of 100)"
        assert len(X_test) == 20, "Test set should have 20 samples (20% of 100)"
    
    def test_generate_synthetic_data_classes(self):
        """Test that generated data has correct number of classes."""
        X_train, X_test, y_train, y_test, scaler = generate_synthetic_data(
            n_samples=100,
            n_features=10,
            n_classes=3,
            random_state=42
        )
        
        assert len(np.unique(y_train)) == 3, "Should have 3 classes in training set"
        assert len(np.unique(y_test)) <= 3, "Should have at most 3 classes in test set"
    
    def test_data_scaling(self):
        """Test that data is properly scaled."""
        X_train, X_test, y_train, y_test, scaler = generate_synthetic_data(
            n_samples=100,
            n_features=10,
            random_state=42
        )
        
        # Check that mean is close to 0 and std is close to 1
        mean = np.mean(X_train, axis=0)
        std = np.std(X_train, axis=0)
        
        assert np.allclose(mean, 0, atol=0.1), "Mean should be close to 0"
        assert np.allclose(std, 1, atol=0.2), "Std should be close to 1"


class TestModelTraining:
    """Test model training functionality."""
    
    @pytest.fixture
    def sample_data(self):
        """Generate sample data for testing."""
        return generate_synthetic_data(
            n_samples=100,
            n_features=10,
            n_classes=2,
            random_state=42
        )
    
    def test_svm_training(self, sample_data):
        """Test SVM model training."""
        X_train, X_test, y_train, y_test, scaler = sample_data
        
        mlflow.set_experiment("test_experiment")
        model, acc, f1 = train_svm(
            X_train, X_test, y_train, y_test,
            C=1.0,
            kernel='rbf',
            run_name="test_svm"
        )
        
        assert model is not None, "Model should be trained"
        assert 0 <= acc <= 1, "Accuracy should be between 0 and 1"
        assert 0 <= f1 <= 1, "F1 score should be between 0 and 1"
    
    def test_logistic_regression_training(self, sample_data):
        """Test Logistic Regression model training."""
        X_train, X_test, y_train, y_test, scaler = sample_data
        
        mlflow.set_experiment("test_experiment")
        model, acc, f1 = train_logistic_regression(
            X_train, X_test, y_train, y_test,
            C=1.0,
            run_name="test_logreg"
        )
        
        assert model is not None, "Model should be trained"
        assert 0 <= acc <= 1, "Accuracy should be between 0 and 1"
        assert 0 <= f1 <= 1, "F1 score should be between 0 and 1"
    
    def test_neural_network_training(self, sample_data):
        """Test Neural Network model training."""
        X_train, X_test, y_train, y_test, scaler = sample_data
        
        mlflow.set_experiment("test_experiment")
        model, acc, f1 = train_neural_network(
            X_train, X_test, y_train, y_test,
            hidden_layers=(50,),
            run_name="test_nn"
        )
        
        assert model is not None, "Model should be trained"
        assert 0 <= acc <= 1, "Accuracy should be between 0 and 1"
        assert 0 <= f1 <= 1, "F1 score should be between 0 and 1"


class TestModelPrediction:
    """Test model prediction functionality."""
    
    def test_svm_prediction_shape(self):
        """Test that SVM predictions have correct shape."""
        X_train, X_test, y_train, y_test, scaler = generate_synthetic_data(
            n_samples=100,
            n_features=10,
            n_classes=2,
            random_state=42
        )
        
        mlflow.set_experiment("test_experiment")
        model, _, _ = train_svm(
            X_train, X_test, y_train, y_test,
            run_name="test_prediction"
        )
        
        predictions = model.predict(X_test)
        assert len(predictions) == len(X_test), "Should have one prediction per sample"
        assert all(p in [0, 1] for p in predictions), "Predictions should be valid class labels"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
