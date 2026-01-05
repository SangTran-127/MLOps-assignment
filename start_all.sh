#!/bin/bash
# Script to start both MLflow UI and Flask app

set -e

# Function to cleanup on exit
cleanup() {
    echo "Shutting down services..."
    kill $MLFLOW_PID 2>/dev/null || true
    kill $FLASK_PID 2>/dev/null || true
    exit 0
}

trap cleanup SIGTERM SIGINT

echo "=========================================="
echo "Starting MLOps Services"
echo "=========================================="

# Check if mlruns directory exists and has experiments
if [ ! -d "mlruns" ] || [ -z "$(ls -A mlruns 2>/dev/null)" ]; then
    echo "No MLflow experiments found. Training models..."
    export MPLCONFIGDIR=/tmp/matplotlib
    python run_experiments.py
    echo "Model training completed!"
fi

# Start MLflow UI in background
echo ""
echo "Starting MLflow UI on port 5000..."
mlflow ui --host 0.0.0.0 --port 5000 &
MLFLOW_PID=$!

# Wait a bit for MLflow to start
sleep 5

# Check if MLflow started successfully
if ! kill -0 $MLFLOW_PID 2>/dev/null; then
    echo "Error: MLflow UI failed to start"
    exit 1
fi

# Start Flask app in background
echo "Starting Flask app on port 5001..."
python app.py &
FLASK_PID=$!

# Wait a bit for Flask to start
sleep 3

echo ""
echo "=========================================="
echo "Services Started Successfully!"
echo "=========================================="
echo "MLflow UI:  http://localhost:5000"
echo "Flask App:  http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop all services"
echo "=========================================="

# Wait for processes
wait $MLFLOW_PID $FLASK_PID
