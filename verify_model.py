"""
Simple verification script to test model loading and prediction.
"""

import mlflow
import mlflow.sklearn
import numpy as np

print("="*60)
print("VERIFYING MLFLOW MODEL")
print("="*60)

# Load the best model
try:
    experiment = mlflow.get_experiment_by_name("Classification_Experiments")
    runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
    runs = runs.sort_values('metrics.test_f1_score', ascending=False)
    
    best_run = runs.iloc[0]
    best_run_id = best_run['run_id']
    
    print(f"\nBest Run ID: {best_run_id}")
    print(f"Model: {best_run['tags.mlflow.runName']}")
    print(f"Test Accuracy: {best_run['metrics.test_accuracy']:.4f}")
    print(f"Test F1 Score: {best_run['metrics.test_f1_score']:.4f}")
    
    # Load the model
    model_uri = f"runs:/{best_run_id}/model"
    model = mlflow.sklearn.load_model(model_uri)
    print(f"\n✓ Model loaded successfully!")
    print(f"Model type: {type(model).__name__}")
    
    # Test prediction
    print("\n" + "="*60)
    print("TESTING PREDICTION")
    print("="*60)
    
    # Generate random test data
    test_features = np.random.randn(5, 20)
    predictions = model.predict(test_features)
    
    print(f"\nGenerated {len(test_features)} test samples")
    print(f"Predictions: {predictions}")
    
    # Try to get probabilities
    try:
        probabilities = model.predict_proba(test_features)
        print(f"\nProbabilities for first sample:")
        for i, prob in enumerate(probabilities[0]):
            print(f"  Class {i}: {prob:.4f}")
    except:
        print("\nProbabilities not available for this model type")
    
    print("\n" + "="*60)
    print("✓ MODEL VERIFICATION COMPLETE!")
    print("="*60)
    print("\nThe Flask app is ready to serve predictions.")
    print("Start it with: python3 app.py")
    print("Then visit: http://localhost:5001")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
