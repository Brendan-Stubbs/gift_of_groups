from django import forms
from .models import GiftGroup, Profile


class GiftGroupForm(forms.ModelForm):
    class Meta:
        model = GiftGroup
        fields = ["name"]

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "The Gift Crew"}
        )
    )
