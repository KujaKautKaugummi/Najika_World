#!/bin/bash
# Najika World - Backend Start Script

echo "========================================="
echo "🚀 Starting Najika World Backend"
echo "========================================="

# Navigate to project root
cd "$(dirname "$0")"

# Check Python version
echo "Checking Python version..."
python3 --version

# Start FastAPI server
echo ""
echo "Starting FastAPI on http://localhost:8000"
echo "API Docs will be available at: http://localhost:8000/docs"
echo "========================================="
echo ""

cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
