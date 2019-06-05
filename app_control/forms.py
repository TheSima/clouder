from django import forms
from .models import validate_user_unique_email_login


class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"autofocus": ""}),
                             validators=[validate_user_unique_email_login])


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autofocus": ""}))


class UserForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"autofocus": ""}))
    last_name = forms.CharField(max_length=100)
    file = forms.FileField
