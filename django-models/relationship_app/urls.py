# myapp/urls.py
from django.urls import path
from . import views
from .views import list_books, LibraryDetailView
from django.urls import path
from .views import admin_view, librarian_view, member_view


urlpatterns = [
    path('', views.book_list_view, name='home'),
    path('', views.LibraryDetails_view, name='home'),
    "LogoutView.as_view(template_name="logut.html, 
    "LoginView.as_view(template_name="login.html"
    "views.register"
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('admin/', admin_view, name='admin_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('member/', member_view, name='member_view')
]