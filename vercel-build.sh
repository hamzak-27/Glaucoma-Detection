#!/bin/bash

# Ensure Python is available
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found. Installing..."
    apt-get update && apt-get install -y python3 python3-pip
fi

# Install dependencies
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# Run migrations
python3 manage.py migrate

# Collect static files
python3 manage.py collectstatic --noinput

# Create superuser if not exists (optional)
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python3 manage.py shell 