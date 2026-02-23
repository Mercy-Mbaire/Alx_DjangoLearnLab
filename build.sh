#!/usr/bin/env bash
# exit on error
set -o errexit

# install dependencies
pip install -r social_media_api/requirements.txt

# move into Django project folder
cd social_media_api

# collect static files
python manage.py collectstatic --noinput

# run migrations
python manage.py migrate