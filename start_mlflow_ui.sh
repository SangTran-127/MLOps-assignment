#!/bin/bash
# Script to start MLflow UI

echo "Starting MLflow UI..."
echo "Access at: http://localhost:5000"
echo "Press Ctrl+C to stop"
echo ""

cd "$(dirname "$0")"
python3 -m mlflow ui
