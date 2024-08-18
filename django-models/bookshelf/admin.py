from django.contrib import admin

# Register your models here.

from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('title', 'author', 'publication_year')

    # Add filters for easier navigation
    list_filter = ('publication_year', 'author')

    # Enable search functionality on these fields
    search_fields = ('title', 'author')

    # Optional: Add pagination (default is 100)
    list_per_page = 20