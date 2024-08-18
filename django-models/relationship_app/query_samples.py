from django.db.models import Prefetch
from .models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return None

# 2. List all books in a library
def list_all_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)  # Now matches the required syntax
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return None

# 3. Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)  # Now matches the required syntax
        librarian = Librarian.objects.get(library=library)
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None



from relationship_app.query_samples import get_books_by_author, list_all_books_in_library, get_librarian_for_library

# Example usage
books_by_author = get_books_by_author('Author Name')
all_books_in_library = list_all_books_in_library('Library Name')
librarian = get_librarian_for_library('Library Name')

print(books_by_author)
print(all_books_in_library)
print(librarian)
