"""
Data generation module for classification experiments.
Supports sklearn make_classification and MNIST datasets.
"""

import numpy as np
from sklearn.datasets import make_classification, fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd


def generate_synthetic_data(n_samples=1000, n_features=20, n_informative=15, 
                           n_redundant=5, n_classes=3, random_state=42):
    """
    Generate synthetic classification data using sklearn.
    
    Args:
        n_samples: Number of samples
        n_features: Total number of features
        n_informative: Number of informative features
        n_redundant: Number of redundant features
        n_classes: Number of classes
        random_state: Random seed
    
    Returns:
        X_train, X_test, y_train, y_test, scaler
    """
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=n_informative,
        n_redundant=n_redundant,
        n_classes=n_classes,
        n_clusters_per_class=2,
        random_state=random_state,
        flip_y=0.1  # Add some noise
    )
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state, stratify=y
    )
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler


def load_mnist_data(subset_size=None, random_state=42):
    """
    Load MNIST dataset for classification.
    
    Args:
        subset_size: If specified, use only a subset of data for faster experiments
        random_state: Random seed
    
    Returns:
        X_train, X_test, y_train, y_test, scaler
    """
    print("Loading MNIST dataset...")
    mnist = fetch_openml('mnist_784', version=1, parser='auto')
    X, y = mnist.data.to_numpy(), mnist.target.to_numpy().astype(int)
    
    # Use a subset if specified
    if subset_size:
        indices = np.random.RandomState(random_state).choice(
            len(X), subset_size, replace=False
        )
        X, y = X[indices], y[indices]
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state, stratify=y
    )
    
    # Scale the features (normalize to 0-1)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler


def get_data_info(X_train, X_test, y_train, y_test):
    """
    Print information about the dataset.
    """
    print(f"Training samples: {X_train.shape[0]}")
    print(f"Test samples: {X_test.shape[0]}")
    print(f"Number of features: {X_train.shape[1]}")
    print(f"Number of classes: {len(np.unique(y_train))}")
    print(f"Class distribution (train): {np.bincount(y_train)}")
    print(f"Class distribution (test): {np.bincount(y_test)}")
