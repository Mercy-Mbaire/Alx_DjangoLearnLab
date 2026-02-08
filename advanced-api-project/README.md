# Advanced API Project

## Overview
This project is a Django-based API for managing books and authors, built using Django REST Framework (DRF). It includes custom models, serializers with validation, and a set of Generic Views for CRUD operations.

## Features
- **Data Models**: `Author` and `Book` models with a one-to-many relationship.
- **Serializers**: Custom serializers with nested relationships and validation (e.g., prohibiting future publication years).
- **Views**: Generic Class-Based Views (CBVs) for standard API operations.
- **Permissions**: configured to allow read-only access to unauthenticated users, while restricting modification actions to authenticated users.

## API Endpoints

The following endpoints are available under the `/api/` prefix:

| Endpoint | HTTP Method | View | Description | Permissions |
| :--- | :--- | :--- | :--- | :--- |
| `/books/` | GET | `BookListView` | List all books. | AllowAny (Read-Only) |
| `/books/<id>/` | GET | `BookDetailView` | Retrieve a specific book by ID. | AllowAny (Read-Only) |
| `/books/create/` | POST | `BookCreateView` | Create a new book. | IsAuthenticated |
| `/books/update/<id>/` | PUT/PATCH | `BookUpdateView` | Update an existing book. | IsAuthenticated |
| `/books/delete/<id>/` | DELETE | `BookDeleteView` | Delete a book. | IsAuthenticated |

## Configuration
- **Views**: implemented in `api/views.py` using `generics.ListAPIView`, `generics.RetrieveAPIView`, etc.
- **URLs**: defined in `api/urls.py` and included in the main project URLs.
- **Permissions**: 
    - `IsAuthenticatedOrReadOnly`: Used for List and Detail views to allow public read access.
    - `IsAuthenticated`: Used for Create, Update, and Delete views to ensure only logged-in users can modify data.

## Advanced Query Features
The `BookListView` endpoint (`/api/books/`) supports the following query parameters:

### Filtering
Filter books by exact matches:
- `?title=...`
- `?author=...`
- `?publication_year=...`

### Searching
Search `title` and `author` (by name) using the `search` parameter:
- `?search=Harry` (Matches "Harry Potter")

### Ordering
Order results using the `ordering` parameter:
- `?ordering=title` (Ascending by title)
- `?ordering=-publication_year` (Descending by year)

## Testing
To run the view verification script:
```bash
python3 test_views.py
```
(Ensure you have `testserver` in `ALLOWED_HOSTS` if running via `APIClient` in a standalone script).
