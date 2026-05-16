from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    """
    Custom user registration form extending the built-in UserCreationForm.
    Adds an email field to the registration process.
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class UserUpdateForm(forms.ModelForm):
    """Form to update User model fields (username, email)"""
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    """Form to update Profile model fields (image, bio)"""
    class Meta:
        model = Profile
        fields = ['image', 'bio']
