#!/usr/bin/env bash
set -o errexit

# install dependencies
pip install -r social_media_api/requirements.txt

# move into project folder
cd social_media_api

# collect static files
python manage.py collectstatic --noinput || echo "collectstatic failed, skipping"

# run migrations
python manage.py migrate

# create superuser only if env vars exist
if [[ -n "$DJANGO_SUPERUSER_USERNAME" ]] && [[ -n "$DJANGO_SUPERUSER_PASSWORD" ]]; then
  python << END
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
END
else
  echo "Superuser env vars not set, skipping superuser creation"
fi