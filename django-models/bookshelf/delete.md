# Import the Book model
from bookshelf.models import Book

# Retrieve the Book instance you want to delete
book = Book.objects.get(title="Nineteen Eighty-Four", author="George Orwell", publication_year=1949)

# Delete the Book instance
book.delete() from bookshelf.models import Book

# Confirm the deletion by attempting to retrieve all books
all_books = Book.objects.all()
print("All Books:", list(all_books))


All Books: []
