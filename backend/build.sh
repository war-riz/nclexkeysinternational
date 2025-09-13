#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.production.txt

# Apply database migrations
python manage.py migrate
