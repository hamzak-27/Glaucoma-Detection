#!/bin/bash

# Install Python dependencies
python3 -m pip install -r requirements.txt

# Run migrations
python3 manage.py migrate

# Collect static files
python3 manage.py collectstatic --noinput

# Create superuser if not exists (optional, remove if not needed)
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python3 manage.py shell 