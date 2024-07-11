from django import forms
from django.core import validators

class RegisterForm(forms.Form):
    username = forms.CharField(validators=[
        validators.MinLengthValidator(2, "Username must have at least 3 chars"), 
        validators.ProhibitNullCharactersValidator,
        validators.validate_unicode_slug],)
    password = forms.PasswordInput()