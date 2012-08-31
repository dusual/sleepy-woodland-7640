from django import forms
from gitapp.models import GithubUser




class UserForm(forms.ModelForm):
    """Form for creating a new user."""
    class Meta:
        model = GithubUser
        exclude = ('public_repo_count', 'email','name')
