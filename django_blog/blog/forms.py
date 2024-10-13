from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from taggit.forms import TagField, TagWidget
from django.forms import widgets

from .models import Profile, Post, Comment


class CustomerUserCreationForm(UserCreationForm):
    """
       A form that extends the default UserCreationForm to include an email field.
       Attributes:
           email (EmailField): Mandatory email field to capture the user's email during registration.
       """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        """
            Extends the save method to handle the email field explicitly.
            commit (bool): If True, saves the user to the database immediately. Defaults to True.
            Returns:
                User: The user instance with email set.
            The email is extracted from the cleaned_data dictionary before saving the User instance.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    """
    A form for editing basic User model fields.

    Allows editing of 'username' and 'email'.
    """

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileEditForm(forms.ModelForm):
    """
    A form for editing the additional fields in the Profile model.

    Allows editing of 'bio' and 'profile_picture'.
    """

    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']


class PostCreateEditForm(forms.ModelForm):
    """
        using modelForm to create a Form to either create or Update a Post using the Post model
        allowed field to edit are title and content as the author is automatically set to the logged in user
        and published_date are auto now add which is auto created upon post creation
    """
    tags = TagField(widget=TagWidget())

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
