#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install dependencies
pip install -r requirements.txt

# 2. Collect static files
python manage.py collectstatic --no-input

# 3. Apply database migrations
python manage.py migrate

# 4. Restore your data from the JSON file
# IMPORTANT: Delete the line below after your first successful deploy!
python manage.py loaddata data.json