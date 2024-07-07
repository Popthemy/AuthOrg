#!/bin/bash
# Check Python version
python --version

# Upgrade pip to the latest version
python -m ensurepip --upgrade

# Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Apply migrations (if using Django)
python manage.py migrate

