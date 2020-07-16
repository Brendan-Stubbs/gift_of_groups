from django import forms
from .models import GiftGroup, Profile, GiftGroupInvitation
from django.contrib.auth.models import User


class GiftGroupForm(forms.ModelForm):
    class Meta:
        model = GiftGroup
        fields = ["name"]

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "The Gift Crew"}
        )
    )


class GiftGroupInvitationForm(forms.ModelForm):

    class Meta:
        model = GiftGroupInvitation
        fields = ["invitee_email"]

    invitee_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control"}
        )
    )
