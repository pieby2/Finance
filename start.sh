#!/bin/bash

# Run migrations automatically
python manage.py migrate

# Automatically create a default admin user if one doesn't exist
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Default admin user created: admin / admin')
"

# Start the gunicorn web server
gunicorn finance_backend.wsgi --log-file -
