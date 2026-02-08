from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    """
    View to list all books.
    accesible to all users (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # Or AllowAny if completely public, but prompt asked for IsAuthenticatedOrReadOnly logic implicitly for list/detail vs others? 
    # Prompt says: "restrict CreateView, UpdateView, and DeleteView to authenticated users only, while allowing read-only access to unauthenticated users for ListView and DetailView."
    # IsAuthenticatedOrReadOnly does exactly that for standard method based differentiation, but if we split views, we can use specific permissions.
    # For ListView (GET only usually), AllowAny or IsAuthenticatedOrReadOnly works. Let's use IsAuthenticatedOrReadOnly to be safe/consistent.

class BookDetailView(generics.RetrieveAPIView):
    """
    View to retrieve a single book by ID.
    Accessible to all users (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookCreateView(generics.CreateAPIView):
    """
    View to create a new book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Custom behavior during creation can be added here
        # For now, just save.
        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    """
    View to update an existing book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # Custom behavior during update can be added here
        serializer.save()

class BookDeleteView(generics.DestroyAPIView):
    """
    View to delete a book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
