from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    error_css_class = "red-text"

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password1", "password2"]

    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"autofocus": ""}
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={})
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={})
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={})
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={})
    )
