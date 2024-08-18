from django import forms
from django.contrib.auth.models import User
from .models import Book

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

        def save(self, commit=True):
            user = super().save(commit=True)
            user.set_password(self.cleaned_data['password'])
            if commit:
                user.save()
            return user
        

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']