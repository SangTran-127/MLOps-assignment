"""
Main experiment script to run multiple MLflow experiments with different hyperparameters.
Compares models and registers the best one to MLflow Model Registry.
"""

import mlflow
import mlflow.sklearn
from data_generator import generate_synthetic_data, get_data_info
from train import train_svm, train_logistic_regression, train_neural_network
import numpy as np


def run_all_experiments():
    """
    Run multiple experiments with different hyperparameters and compare results.
    """
    # Set MLflow experiment name
    mlflow.set_experiment("Classification_Experiments")
    
    print("="*80)
    print("GENERATING DATA")
    print("="*80)
    
    # Generate synthetic data
    X_train, X_test, y_train, y_test, scaler = generate_synthetic_data(
        n_samples=2000,
        n_features=20,
        n_informative=15,
        n_redundant=5,
        n_classes=3,
        random_state=42
    )
    
    get_data_info(X_train, X_test, y_train, y_test)
    
    print("\n" + "="*80)
    print("EXPERIMENT 1: Baseline SVM with RBF kernel")
    print("="*80)
    print("Rationale: Start with default RBF kernel (C=1.0) as baseline.")
    print("RBF kernel works well for non-linear data.")
    
    model1, acc1, f1_1 = train_svm(
        X_train, X_test, y_train, y_test,
        C=1.0,
        kernel='rbf',
        gamma='scale',
        run_name="SVM_RBF_Baseline",
        description="Baseline SVM with RBF kernel and default C=1.0"
    )
    
    print("\n" + "="*80)
    print("EXPERIMENT 2: SVM with higher regularization")
    print("="*80)
    print("Rationale: Increase C to 10 to reduce regularization and allow")
    print("the model to fit training data more closely, potentially capturing")
    print("more complex patterns.")
    
    model2, acc2, f1_2 = train_svm(
        X_train, X_test, y_train, y_test,
        C=10.0,
        kernel='rbf',
        gamma='scale',
        run_name="SVM_RBF_C10",
        description="SVM with higher C=10 to reduce regularization"
    )
    
    print("\n" + "="*80)
    print("EXPERIMENT 3: SVM with Linear kernel")
    print("="*80)
    print("Rationale: Try linear kernel to see if the data has linear separability.")
    print("Linear models are simpler, faster, and less prone to overfitting.")
    
    model3, acc3, f1_3 = train_svm(
        X_train, X_test, y_train, y_test,
        C=1.0,
        kernel='linear',
        gamma='scale',
        run_name="SVM_Linear",
        description="SVM with linear kernel for simpler decision boundary"
    )
    
    print("\n" + "="*80)
    print("EXPERIMENT 4: Logistic Regression baseline")
    print("="*80)
    print("Rationale: Compare SVM with Logistic Regression, which is a simpler")
    print("linear model often used as a strong baseline for classification.")
    
    model4, acc4, f1_4 = train_logistic_regression(
        X_train, X_test, y_train, y_test,
        C=1.0,
        max_iter=1000,
        solver='lbfgs',
        run_name="LogReg_Baseline",
        description="Baseline Logistic Regression with C=1.0"
    )
    
    print("\n" + "="*80)
    print("EXPERIMENT 5: Logistic Regression with stronger regularization")
    print("="*80)
    print("Rationale: Reduce C to 0.1 to increase regularization strength,")
    print("which can help prevent overfitting and improve generalization.")
    
    model5, acc5, f1_5 = train_logistic_regression(
        X_train, X_test, y_train, y_test,
        C=0.1,
        max_iter=1000,
        solver='lbfgs',
        run_name="LogReg_C0.1",
        description="Logistic Regression with stronger regularization C=0.1"
    )
    
    print("\n" + "="*80)
    print("EXPERIMENT 6: Neural Network with single hidden layer")
    print("="*80)
    print("Rationale: Try a simple neural network with one hidden layer (100 neurons)")
    print("to capture non-linear patterns while keeping the model relatively simple.")
    
    model6, acc6, f1_6 = train_neural_network(
        X_train, X_test, y_train, y_test,
        hidden_layers=(100,),
        alpha=0.0001,
        learning_rate_init=0.001,
        run_name="NN_Single_Layer",
        description="Neural Network with single hidden layer (100 neurons)"
    )
    
    print("\n" + "="*80)
    print("EXPERIMENT 7: Neural Network with deeper architecture")
    print("="*80)
    print("Rationale: Use deeper network (100, 50 neurons) to potentially learn")
    print("more complex hierarchical features, with stronger regularization (alpha=0.001).")
    
    model7, acc7, f1_7 = train_neural_network(
        X_train, X_test, y_train, y_test,
        hidden_layers=(100, 50),
        alpha=0.001,
        learning_rate_init=0.001,
        run_name="NN_Deep",
        description="Deeper Neural Network with 2 hidden layers and stronger regularization"
    )
    
    print("\n" + "="*80)
    print("EXPERIMENT 8: Neural Network with wider architecture")
    print("="*80)
    print("Rationale: Use wider single layer (200 neurons) to increase model capacity")
    print("and see if more neurons can better represent the data patterns.")
    
    model8, acc8, f1_8 = train_neural_network(
        X_train, X_test, y_train, y_test,
        hidden_layers=(200,),
        alpha=0.0001,
        learning_rate_init=0.001,
        run_name="NN_Wide",
        description="Wider Neural Network with 200 neurons in hidden layer"
    )
    
    # Compare all results
    print("\n" + "="*80)
    print("EXPERIMENT RESULTS SUMMARY")
    print("="*80)
    
    results = [
        ("SVM_RBF_Baseline", acc1, f1_1),
        ("SVM_RBF_C10", acc2, f1_2),
        ("SVM_Linear", acc3, f1_3),
        ("LogReg_Baseline", acc4, f1_4),
        ("LogReg_C0.1", acc5, f1_5),
        ("NN_Single_Layer", acc6, f1_6),
        ("NN_Deep", acc7, f1_7),
        ("NN_Wide", acc8, f1_8),
    ]
    
    print(f"\n{'Model':<25} {'Accuracy':<15} {'F1 Score':<15}")
    print("-" * 55)
    for name, acc, f1 in results:
        print(f"{name:<25} {acc:<15.4f} {f1:<15.4f}")
    
    # Find best model based on F1 score
    best_idx = np.argmax([r[2] for r in results])
    best_name, best_acc, best_f1 = results[best_idx]
    
    print("\n" + "="*80)
    print(f"BEST MODEL: {best_name}")
    print(f"Test Accuracy: {best_acc:.4f}")
    print(f"Test F1 Score: {best_f1:.4f}")
    print("="*80)
    
    return results, best_name, best_idx


def register_best_model(best_model_name):
    """
    Register the best model to MLflow Model Registry.
    """
    print("\n" + "="*80)
    print("REGISTERING BEST MODEL TO MODEL REGISTRY")
    print("="*80)
    
    # Get the best run
    experiment = mlflow.get_experiment_by_name("Classification_Experiments")
    runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
    
    # Find the run with the best model name
    best_run = runs[runs['tags.mlflow.runName'] == best_model_name].iloc[0]
    best_run_id = best_run['run_id']
    
    print(f"Best Run ID: {best_run_id}")
    print(f"Model Name: {best_model_name}")
    
    # Register the model
    model_uri = f"runs:/{best_run_id}/model"
    model_name = "BestClassifier"
    
    try:
        # Register the model
        model_version = mlflow.register_model(model_uri, model_name)
        print(f"\nModel registered successfully!")
        print(f"Model Name: {model_name}")
        print(f"Version: {model_version.version}")
        
        # Transition to Production
        client = mlflow.tracking.MlflowClient()
        client.transition_model_version_stage(
            name=model_name,
            version=model_version.version,
            stage="Production"
        )
        print(f"Model transitioned to Production stage!")
        
    except Exception as e:
        print(f"Error registering model: {e}")
        print("Note: Model registry might require MLflow tracking server.")


if __name__ == "__main__":
    # Run all experiments
    results, best_name, best_idx = run_all_experiments()
    
    # Register the best model
    register_best_model(best_name)
    
    print("\n" + "="*80)
    print("ALL EXPERIMENTS COMPLETED!")
    print("="*80)
    print("\nTo view results in MLflow UI, run:")
    print("  python3 -m mlflow ui")
    print("\nThen open http://localhost:5000 in your browser.")
