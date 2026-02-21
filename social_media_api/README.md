## Deployment

This project is configured for deployment on **Render**.

### Steps to Deploy

1.  **Create a PostgreSQL Database** on Render.
    - Copy the **Internal Database URL**.
2.  **Create a Web Service** on Render.
    - Connect your GitHub repository.
    - Set **Runtime** to `Python 3`.
    - Set **Build Command** to `./build.sh`.
    - Set **Start Command** to `gunicorn social_media_api.wsgi`.
3.  **Environment Variables**:
    - Add the following environment variables in the Render Dashboard:
      - `SECRET_KEY`: Your Django secret key.
      - `DATABASE_URL`: The Internal Database URL from your Render PostgreSQL.
      - `ALLOWED_HOSTS`: `your-app-name.onrender.com` (or `*`).
      - `DEBUG`: `False`.
      - `PYTHON_VERSION`: `3.14.0` (or as specified in `runtime.txt`).

### Production Security

The following security settings are enabled when `DEBUG=False`:
- `SECURE_BROWSER_XSS_FILTER = True`
- `X_FRAME_OPTIONS = 'DENY'`
- `SECURE_CONTENT_TYPE_NOSNIFF = True`
- `SECURE_SSL_REDIRECT = True`

A Django-based social media API with user authentication.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd social_media_api
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install django djangorestframework pillow
    ```

4.  **Run migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Start the server:**
    ```bash
    python manage.py runserver
    ```

## API Endpoints

### Authentication

-   **Register:** `POST /api/accounts/register/`
    -   Payload: `{"username": "...", "password": "...", "email": "...", "bio": "..."}`
    -   Response: `{"token": "..."}`

-   **Login:** `POST /api/accounts/login/`
    -   Payload: `{"username": "...", "password": "..."}`
    -   Response: `{"token": "..."}`

-   **Profile:** `GET /api/accounts/profile/`
    -   Headers: `Authorization: Token <token>`
    -   Response: User details including bio and followers.

### Posts and Comments

-   **Posts:** `/api/posts/`
    -   `GET`: List all posts (Pagination: ?page=1). Filter by title/content: `?search=keyword`.
    -   `POST`: Create a new post.
    -   `PUT/DELETE`: Update/Delete post (Author only).

-   **Comments:** `/api/comments/`
    -   `GET`: List all comments.
    -   `POST`: Create a new comment.
    -   `PUT/DELETE`: Update/Delete comment (Author only).

### Follows and Feed

-   **Follow User:** `POST /api/accounts/follow/<user_id>/`
-   **Unfollow User:** `POST /api/accounts/unfollow/<user_id>/`
-   **Feed:** `GET /api/feed/`
    -   Returns posts from users the current user follows, ordered by newest first.

## Deployment

This project is configured for deployment on platforms like Heroku.

### Prerequisites

-   `gunicorn`
-   `whitenoise`
-   `dj-database-url`
-   `psycopg2-binary`

### Configuration

The project uses environment variables for configuration. Ensure the following variables are set in your production environment:

-   `DEBUG`: Set to `False`.
-   `SECRET_KEY`: Your production secret key.
-   `ALLOWED_HOSTS`: Comma-separated list of allowed hosts (e.g., `myapp.herokuapp.com`).
-   `DATABASE_URL`: Connection string for your production database (e.g., PostgreSQL).

### Run Command

The `Procfile` is set up to run the application using Gunicorn:

```
web: gunicorn social_media_api.wsgi --log-file -
```

## Models

### CustomUser

Extends `AbstractUser` with:
-   `bio`: TextField
-   `profile_picture`: ImageField
-   `followers`: ManyToManyField to self (symmetrical=False)

### Post
-   `author`: ForeignKey to CustomUser
-   `title`: CharField
-   `content`: TextField
-   `created_at`, `updated_at`: DateTimeField

### Comment
-   `post`: ForeignKey to Post
-   `author`: ForeignKey to CustomUser
-   `content`: TextField
-   `created_at`, `updated_at`: DateTimeField
