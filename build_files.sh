#!/bin/bash

echo "Starting build process..."

# Install dependencies
pip install --no-cache-dir -r requirements.txt || { echo 'Failed to install dependencies'; exit 1; }

# Apply migrations (if using Django)
python manage.py migrate || { echo 'Failed to apply migrations'; exit 1; }

echo "Build process completed successfully."
