#!/bin/bash

echo "Building project..."
python3.12 -m pip install -r requirements.txt

echo "Running migrations..."
python3.12 manage.py migrate --noinput

echo "Collecting static files..."
python3.12 manage.py collectstatic --noinput --clear

echo "Creating default superuser..."
python3.12 manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"

echo "Build complete."
