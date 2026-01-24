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
