# LibraryProject - Advanced Features and Security

This project demonstrates advanced Django features, including a custom user model and a permission-based access control system.

## Setup Instructions

1. **Environment**: It is recommended to use a virtual environment.
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. **Install Dependencies**:
   ```bash
   pip install django Pillow
   ```
3. **Database Setup**:
   ```bash
   python manage.py makemigrations bookshelf relationship_app
   python manage.py migrate
   ```
4. **Group Setup**: Run the custom management command to create groups and permissions.
   ```bash
   python manage.py setup_groups
   ```

## Security Best Practices (Task 3)
- **CSRF Protection**: All forms in templates use `{% csrf_token %}`.
- **Safe Input Handling**: `BookForm` and `ExampleForm` in `forms.py` sanitize and validate inputs.
- **Safe Searching**: The `book_search` view uses Django's ORM filtering to parameterized queries and prevent SQL Injection.
- **Content Security Policy**: CSRF and CSP headers are enforced via middleware.

## Key Features

### 1. Custom User Model
Located in `bookshelf/models.py`.
- **`CustomUser`**: Extends `AbstractUser`.
- **Additional Fields**: `date_of_birth`, `profile_photo`.
- **Custom Manager**: `CustomUserManager` handles user and superuser creation, ensuring required fields are populated.
- **Config**: `AUTH_USER_MODEL` is set to `bookshelf.CustomUser` in `settings.py`.

### 2. Permissions and Groups
Located in `bookshelf/models.py` and `bookshelf/views.py`.
- **Custom Permissions**: Added to the `Book` model (`can_view`, `can_create`, `can_edit`, `can_delete`).
- **Groups**:
    - **Viewers**: Can view books (`can_view`).
    - **Editors**: Can view, create, and edit books (`can_view`, `can_create`, `can_edit`).
    - **Admins**: Full CRUD permissions.
- **Enforcement**: Views in `bookshelf/views.py` are protected using the `@permission_required` decorator.

## Verification
- **Automated Tests**: Run tests with `python manage.py test`.
- **Manual Verification**: Create test users, assign them to groups, and verify access to protected views in the `bookshelf` app.

## Task 3: Security Best Practices
- **Secure Settings**: `DEBUG` is set to `False`, and CSRF/Session cookies are secured.
- **Security Headers**: XSS filter, No-Sniff, and X-Frame-Options are configured.
- **SSL/HTTPS**: `SECURE_SSL_REDIRECT` and HSTS settings are enabled for production safety.
- **CSP**: Content Security Policy is implemented using `django-csp`.
- **Form Safety**: All user inputs are validated via Django forms in `bookshelf/forms.py`.
- **Safe Queries**: All database access uses Django's ORM to prevent SQL injection.
