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

## Models

### CustomUser

Extends `AbstractUser` with:
-   `bio`: TextField
-   `profile_picture`: ImageField
-   `followers`: ManyToManyField to self (symmetrical=False)
