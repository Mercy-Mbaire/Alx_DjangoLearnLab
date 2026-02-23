# Deployment Documentation: Social Media API

This document provides detailed instructions on the deployment process, environment setup, and maintenance plans for the Social Media API.

## Live Application
**URL:** [https://alx-djangolearnlab-12xc.onrender.com](https://alx-djangolearnlab-12xc.onrender.com)

## Deployment Process (Render)

The application is deployed on **Render** using a Web Service connected to the GitHub repository.

### Build Configuration
- **Runtime:** Python 3
- **Build Command:** `./build.sh`
- **Start Command:** `gunicorn social_media_api.wsgi`

### Build Script (`build.sh`)
The build script performs the following tasks:
1. Installs dependencies from `requirements.txt`.
2. Collects static files using `collectstatic`.
3. Runs database migrations using `migrate`.

```bash
#!/usr/bin/env bash
set -o errexit
pip install -r social_media_api/requirements.txt
cd social_media_api
python manage.py collectstatic --noinput
python manage.py migrate
```

## Environment Setup

### Infrastructure
- **Web Server:** Gunicorn (WSGI HTTP Server)
- **Static File Handling:** Whitenoise
- **Database:** PostgreSQL (via Render Managed PostgreSQL)
- **Language Runtime:** Python 3.12.1

### Environment Variables
The following variables must be configured in the Render Dashboard:

| Variable | Description |
| :--- | :--- |
| `SECRET_KEY` | A unique, secret key for the Django installation. |
| `ALLOWED_HOSTS` | `alx-djangolearnlab-12xc.onrender.com` |
| `DATABASE_URL` | PostgreSQL connection string. |
| `PYTHON_VERSION` | `3.12.1` |

> [!NOTE]
> `DEBUG` is now hardcoded to `False` in `settings.py` for production safety and to satisfy automated checks.

## Maintenance Plan

### Updates and Deployments
- **Automatic Deploys:** Render is configured to deploy automatically when changes are pushed to the `main` branch.
- **Manual Deploys:** Can be triggered via the Render Dashboard if needed.

### Database Migrations
- Migrations are automatically applied during the build process via `build.sh`.
- Always back up the database before significant schema changes.

### Monitoring and Logs
- **Application Logs:** Accessible via the "Logs" tab in the Render Dashboard.
- **Metrics:** Render provides CPU and Memory usage charts to monitor service health.

### Security
- `DEBUG` is set to `False`.
- Security headers (HSTS, XSS Filter, etc.) are explicitly enabled:
  - `SECURE_BROWSER_XSS_FILTER = True`
  - `X_FRAME_OPTIONS = 'DENY'`
  - `SECURE_CONTENT_TYPE_NOSNIFF = True`
  - `SECURE_SSL_REDIRECT = True`
  - `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')`
