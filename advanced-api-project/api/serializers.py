from rest_framework import serializers
from .models import Book, Author
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Validates that the publication_year is not in the future.
    """
    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        """
        Check that the publication year is not in the future.
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    Includes a nested BookSerializer to dynamicallly serialize related books.
    The 'books' field uses the related_name defined in the Book model's ForeignKey.
    """
    # Nested serializer to include books associated with the author.
    # read_only=True ensures that we don't try to create books when creating an author via this serializer,
    # unless we explicitly handle it (which is not required by the prompt, simplifying to read-only for nesting).
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']
