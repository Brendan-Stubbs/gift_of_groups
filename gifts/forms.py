from django import forms
from .models import GiftGroup, Profile, GiftGroupInvitation
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget



class GiftGroupForm(forms.ModelForm):
    class Meta:
        model = GiftGroup
        fields = ["name", "standard_user_can_invite"]

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "The Gift Crew"}
        )
    )

    standard_user_can_invite = forms.CheckboxInput()


class GiftGroupInvitationForm(forms.ModelForm):

    class Meta:
        model = GiftGroupInvitation
        fields = ["invitee_email"]

    invitee_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control"}
        )
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["birth_date"]

    birth_date = forms.DateField(widget=forms.DateInput(attrs={"class":"datepicker"}))
