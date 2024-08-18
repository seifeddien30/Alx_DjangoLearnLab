# Import the Book model
from bookshelf.models import Book

# Create a new Book instance and save it to the database
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Verify the creation
print(book)

# 1984 by George Orwell, and publication year 1949.
