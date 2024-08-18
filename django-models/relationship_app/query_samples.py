from relationship_app.models import Book, Library, Author, Librarian


# Query all books by a specific author
author_name = "John Doe"  # Replace with the actual author's name
author = Author.objects.get(name=author_name)
books_by_author = Book.objects.filter(author=author)

# List all books in a specific library
library_name = "Central Library"  # Replace with the actual library name

books = Book.objects.all()
books.all()


# Retrieve the librarian for a specific library
library = Library.objects.get(Library=library_name)
Library.objects.get(name=library_name)

librarian = Librarian.objects.get(library='Central Library')