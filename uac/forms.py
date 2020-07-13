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
            attrs={"class": "form-control", "placeholder": "test@test.com"}
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Tester"})
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Tester"})
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

