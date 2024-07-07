#!/bin/bash

echo "Starting build process..."

# Check Python version
python --version || { echo 'Python is not available'; exit 1; }

# Install dependencies using a lightweight method
python -m ensurepip --upgrade || { echo 'Failed to upgrade ensurepip'; exit 1; }

# Upgrade pip to the latest version
python -m pip install --upgrade pip || { echo 'Failed to upgrade pip'; exit 1; }

# Install only the required dependencies
python -m pip install --no-cache-dir -r requirements.txt || { echo 'Failed to install dependencies'; exit 1; }

# Apply migrations (if using Django)
python manage.py migrate || { echo 'Failed to apply migrations'; exit 1; }


echo "Build process completed successfully."
