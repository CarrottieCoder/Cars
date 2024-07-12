from django import forms
from django.core import validators
from .models import CarSeries

class RegisterForm(forms.Form):
    username = forms.CharField(validators=[
        validators.MinLengthValidator(2, "Username must have at least 3 chars"), 
        validators.ProhibitNullCharactersValidator,
        validators.validate_unicode_slug],)
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        fields = ['username', 'password']

class CreateCarForm(forms.Form):
    series = forms.ModelChoiceField(queryset=CarSeries.objects.all(), required=True)
    year_manufactued = forms.IntegerField(validators=[
        validators.MinValueValidator(1900, "That's not a year"),
        validators.MaxValueValidator(2024, "The car can't be newer than 2024")
    ], required=True)
    mileage = forms.IntegerField(validators=[
        validators.MinValueValidator(0)
    ], required=True)
    price = forms.IntegerField(validators=[
        validators.MinValueValidator(0)
    ], required=True)
    engine = forms.ChoiceField(choices=(
        ("GAS", 'Gas'),
        ("DIESEL", 'Diesel'),
        ('HYBRID', 'Hybrid'),
        ('ELECTRIC', 'Electric'),
        ('Hydrogen', 'Hydrogen'),
        ('OTHER', 'Other')
    ), required=True)
    accident_free = forms.BooleanField(required=True)
    origin_country = forms.CharField(validators=[
        validators.MinLengthValidator(3)
    ], required=True)
    other_data = forms.Textarea()
    

    