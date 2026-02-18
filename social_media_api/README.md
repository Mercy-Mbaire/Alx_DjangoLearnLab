# Social Media API

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
