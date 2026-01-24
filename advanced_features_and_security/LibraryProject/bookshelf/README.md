# Documentation: Permissions and Groups Setup

## Custom Permissions
Custom permissions have been added to the `Book` model in `bookshelf/models.py`:
- `can_view`: Allows viewing the list of books.
- `can_create`: Allows adding new books.
- `can_edit`: Allows editing existing books.
- `can_delete`: Allows deleting books.

## Groups
Three groups have been established to manage these permissions:
1. **Viewers**: Assigned `can_view` permission.
2. **Editors**: Assigned `can_view`, `can_create`, and `can_edit` permissions.
3. **Admins**: Assigned all permissions (`can_view`, `can_create`, `can_edit`, `can_delete`).

## Enforcement
Permissions are enforced in `bookshelf/views.py` using the `@permission_required` decorator with `raise_exception=True`. This ensures that users without the required permissions receive a 403 Forbidden error.

## Setup
To set up the groups and permissions automatically, run the custom management command:
```bash
python manage.py setup_groups
```
