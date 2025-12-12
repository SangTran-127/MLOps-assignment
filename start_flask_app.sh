#!/bin/bash
# Script to start Flask Web Application

echo "Starting Flask Web Application..."
echo "Access at: http://localhost:5001"
echo "Press Ctrl+C to stop"
echo ""

cd "$(dirname "$0")"
python3 app.py
