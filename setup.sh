#!/bin/bash

# Setup script for Customer Purchase Prediction Pipeline
# This script sets up the complete environment and initializes the project

echo "========================================="
echo "Customer Purchase Prediction Pipeline"
echo "Automated Setup Script"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # macOS/Linux
    source venv/bin/activate
fi

echo "✓ Virtual environment created and activated"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✓ Dependencies installed"

# Initialize Git (if not already initialized)
if [ ! -d ".git" ]; then
    echo ""
    echo "Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: ML pipeline setup"
    echo "✓ Git repository initialized"
else
    echo "✓ Git repository already exists"
fi

# Initialize DVC
echo ""
echo "Initializing DVC..."
dvc init

echo "✓ DVC initialized"

# Create necessary directories
echo ""
echo "Creating directory structure..."
mkdir -p data/raw
mkdir -p data/processed
mkdir -p models

echo "✓ Directory structure created"

echo ""
echo "========================================="
echo "✅ Setup completed successfully!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment (if not already active):"
echo "   - Windows: venv\\Scripts\\activate"
echo "   - macOS/Linux: source venv/bin/activate"
echo ""
echo "2. Run the complete pipeline:"
echo "   dvc repro"
echo ""
echo "3. View MLflow tracking:"
echo "   mlflow ui"
echo ""
echo "4. Check pipeline status:"
echo "   dvc status"
echo ""
echo "For more information, see README.md"
echo ""
