# Import the Book model
from bookshelf.models import Book

# Retrieve the Book instance you created
book = Book.objects.get(title="1984", author="George Orwell", publication_year=1949)

# Display all attributes of the Book instance
print("Title:", book.title)
print("Author:", book.author)
print("Publication Year:", book.publication_year)

Title: 1984
Author: George Orwell
Publication Year: 1949
