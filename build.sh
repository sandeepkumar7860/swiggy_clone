#!/bin/bash

# Exit on error
set -o errexit

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate
