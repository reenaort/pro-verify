#!/bin/bash
# ProVerify startup script
# Run this once to start the server

echo "=== ProVerify Backend ==="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 not found. Please install Python 3.10+"
    exit 1
fi

# Install dependencies if needed
echo "Installing dependencies..."
pip install -r requirements.txt --quiet

# Run migrations
echo "Running migrations..."
python3 manage.py migrate

# Start server
echo ""
echo "Starting server at http://127.0.0.1:8000"
echo ""
echo "  Verify page:      http://127.0.0.1:8000/verify/"
echo "  Admin Login:      http://127.0.0.1:8000/admin-login/"
echo "  Admin Dashboard:  http://127.0.0.1:8000/admin-dashboard/"
echo "  Admin Upload:     http://127.0.0.1:8000/admin-upload/"
echo "  Admin Codes:      http://127.0.0.1:8000/admin-codes/"
echo "  Django Admin:     http://127.0.0.1:8000/django-admin/"
echo ""
python3 manage.py runserver
