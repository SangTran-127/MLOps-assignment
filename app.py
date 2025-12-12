"""
Flask web application for classification using the best MLflow model.
"""

from flask import Flask, request, render_template, jsonify
import mlflow
import mlflow.sklearn
import numpy as np
import os

app = Flask(__name__)

# Load the best model from MLflow Model Registry
MODEL_NAME = "BestClassifier"
MODEL_STAGE = "Production"

# Try to load the model
try:
    model_uri = f"models:/{MODEL_NAME}/{MODEL_STAGE}"
    model = mlflow.sklearn.load_model(model_uri)
    print(f"Model loaded successfully from Model Registry: {model_uri}")
except Exception as e:
    print(f"Could not load from Model Registry: {e}")
    print("Attempting to load latest model from runs...")
    try:
        # Fallback: Load the latest model from runs
        experiment = mlflow.get_experiment_by_name("Classification_Experiments")
        runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
        runs = runs.sort_values('metrics.test_f1_score', ascending=False)
        best_run_id = runs.iloc[0]['run_id']
        model_uri = f"runs:/{best_run_id}/model"
        model = mlflow.sklearn.load_model(model_uri)
        print(f"Model loaded from run: {best_run_id}")
    except Exception as e2:
        print(f"Error loading model: {e2}")
        model = None


@app.route('/')
def home():
    """
    Home page with input form for classification.
    """
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict endpoint for classification.
    """
    if model is None:
        return jsonify({
            'error': 'Model not loaded. Please run experiments first.'
        }), 500
    
    try:
        # Get input data from form
        if request.is_json:
            data = request.get_json()
            features = data.get('features', [])
        else:
            # Get features from form (comma-separated)
            features_str = request.form.get('features', '')
            features = [float(x.strip()) for x in features_str.split(',')]
        
        # Validate input
        if not features:
            return jsonify({'error': 'No features provided'}), 400
        
        # Convert to numpy array and reshape
        X = np.array(features).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(X)[0]
        
        # Get prediction probabilities if available
        try:
            probabilities = model.predict_proba(X)[0]
            prob_dict = {f"Class {i}": float(prob) for i, prob in enumerate(probabilities)}
        except:
            prob_dict = None
        
        # Prepare response
        result = {
            'prediction': int(prediction),
            'prediction_label': f"Class {prediction}",
            'input_features': features,
            'num_features': len(features)
        }
        
        if prob_dict:
            result['probabilities'] = prob_dict
        
        return jsonify(result)
    
    except ValueError as e:
        return jsonify({'error': f'Invalid input format: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500


@app.route('/info')
def model_info():
    """
    Get information about the loaded model.
    """
    if model is None:
        return jsonify({
            'error': 'Model not loaded. Please run experiments first.'
        }), 500
    
    info = {
        'model_type': type(model).__name__,
        'model_name': MODEL_NAME,
        'model_stage': MODEL_STAGE,
    }
    
    # Add model-specific info
    if hasattr(model, 'n_features_in_'):
        info['n_features'] = int(model.n_features_in_)
    if hasattr(model, 'classes_'):
        info['classes'] = [int(c) for c in model.classes_]
        info['n_classes'] = len(model.classes_)
    
    return jsonify(info)


@app.route('/health')
def health():
    """
    Health check endpoint.
    """
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
