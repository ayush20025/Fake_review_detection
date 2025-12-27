#!/bin/bash

# Deployment script for Fake Review Detection System

echo "Starting deployment of Fake Review Detection System..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is required but not installed. Please install pip3."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Download NLTK data
echo "Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('vader_lexicon', quiet=True)"

# Create necessary directories
echo "Creating directories..."
mkdir -p temp_uploads
mkdir -p logs
mkdir -p backups

# Set permissions
echo "Setting permissions..."
chmod +x deploy.sh
chmod 755 app.py

# Run tests (if available)
if [ -f "test_app.py" ]; then
    echo "Running tests..."
    python test_app.py
fi

echo "Deployment completed successfully!"
echo ""
echo "To run the application:"
echo "1. Development mode: python app.py"
echo "2. Production mode: gunicorn app:app"
echo ""
echo "Access the application at: http://localhost:5000"
