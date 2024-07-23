#!/bin/bash

echo "Starting build process..."


# Install only the required dependencies
python3.9 -m pip install -r requirements.txt || { echo 'Failed to install dependencies'; exit 1; }

# Make migrations (if using Django)
python3.9 manage.py makemigrations || { echo 'Failed to make migrations'; exit 1; }

# Apply migrations (if using Django)
python3.9 manage.py migrate || { echo 'Failed to apply migrations'; exit 1; }

echo "Build process completed successfully."
