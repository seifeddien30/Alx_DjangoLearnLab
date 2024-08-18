from django.urls import path
from .views import add_book, admin_view, delete_book, edit_book, librarian_view, list_books, LibraryDetailView, member_view, register, user_login, user_logout
from django.contrib.auth.views import LoginView, LogoutView  # Import `book_list` here
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('books/', list_books, name='list_books'),  # Function-based view URL
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # Class-based view URL
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', register, name='register'),
    path('admin/', admin_view, name='admin_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('member/', member_view, name='member_view'),
    path('add_book/', add_book, name='add_book'),
    path('edit_book/<int:pk>/', edit_book, name='edit_book'),
    path('delete_book/<int:pk>/', delete_book, name='delete_book'),
]


