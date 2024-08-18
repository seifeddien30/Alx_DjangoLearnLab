# Import the Book model
from bookshelf.models import Book

# Retrieve the Book instance you want to update
book = Book.objects.get(title="1984", author="George Orwell", publication_year=1949)

# Update the title
book.title = "Nineteen Eighty-Four"

# Save the changes to the database
book.save()

# Verify that the title was updated
updated_book = Book.objects.get(author="George Orwell", publication_year=1949)
print("Updated Title:", updated_book.title)


Updated Title: Nineteen Eighty-Four
