#!/bin/bash
# Blood Donation App - Virtual Environment Activation Script

echo "Activating Blood Donation App Virtual Environment..."
source venv/bin/activate

echo "Virtual environment activated!"
echo "Current Python: $(which python)"
echo "Python version: $(python --version)"
echo "Django version: $(python -c 'import django; print(django.get_version())')"

echo ""
echo "To deactivate, run: deactivate"
echo "To run the server: python manage.py runserver"
echo "To install packages: pip install <package_name>"
