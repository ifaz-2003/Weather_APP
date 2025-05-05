from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
#custom signup form that extends Django's built-in UserCreationForm
class SignupForm(UserCreationForm):
    # Adds an email field as required and links the form to the CustomUser model

    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        # defines fields in form

        fields = ["username", "email", "password1", "password2"]

class LoginForm(AuthenticationForm):
    pass
