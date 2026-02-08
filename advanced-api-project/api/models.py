from django.db import models

# Create your models here.

class Author(models.Model):
    """
    The Author model represents a writer of books.
    
    Attributes:
        name (str): The name of the author.
    """
    name = models.CharField(max_length=200, help_text="The name of the author.")

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    The Book model represents a book written by an author.
    
    Attributes:
        title (str): The title of the book.
        publication_year (int): The year the book was published.
        author (Author): A foreign key linking to the Author who wrote the book.
                         This establishes a one-to-many relationship: One author can write many books.
                         Default related_name 'books' allows accessing books from an author instance.
    """
    title = models.CharField(max_length=200, help_text="The title of the book.")
    publication_year = models.IntegerField(help_text="The year the book was published.")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books', help_text="The author of the book.")

    def __str__(self):
        return self.title
