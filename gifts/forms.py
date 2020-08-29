from django import forms
from .models import GiftGroup, Profile, GiftGroupInvitation, GiftIdea, Gift, ContributorGiftRelation, GiftComment, GroupComment
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget


class GiftGroupForm(forms.ModelForm):
    class Meta:
        model = GiftGroup
        fields = ["name", "standard_user_can_invite", "days_to_notify", "icon"]

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={}
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
        fields = ["birth_date", "bank_account_name", "bank_name", "bank_account_number",
                  "bank_branch_name", "bank_branch_number", "bank_account_type"]
        labels = {
            "bank_account_name": "Account Name(Optional)",
            "bank_name": "Bank Name(Optional)",
            "bank_account_number": "Account Number(Optional)",
            "bank_branch_name": "Branch Name(Optional)",
            "bank_branch_number": "Branch Number(Optional)",
            "bank_account_type": "Bank Account Type(Optional)",
        }

    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={"class": "datepicker"}))


class GiftIdeaForm(forms.ModelForm):
    class Meta:
        model = GiftIdea
        fields = ["title", "description", "url", "price"]

        labels = {
            "title": "Name",
            "description": "Description",
            "url": "Link",
            "price": "Price",
        }

    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea'}))


class GiftManagementUserForm(forms.ModelForm):
    class Meta:
        model = ContributorGiftRelation
        fields = ["contribution", 'has_made_payment', 'participation_status']
        labels = {
            "contribution": "How much are you contributing?",
            "has_made_payment": "Let your captain know you have paid",
            "participation_status": "Will you be participating?"
        }

class GiftCommentForm(forms.ModelForm):
    class Meta:
        model = GiftComment
        fields = ["content"]

class GroupCommentForm(forms.ModelForm):
    class Meta:
        model = GroupComment
        fields = ["content"]