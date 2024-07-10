from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.
class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    origin_demonym = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class CarSeries(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="series")
    name = models.CharField(max_length=100)
    car_class = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.manufacturer.name} {self.name}" 

    class Meta():
        # Fixes weird plural
        verbose_name = 'Car Series'
        verbose_name_plural = 'Car Series'

class CarMake(models.Model):
    series = models.ForeignKey(CarSeries, on_delete=models.CASCADE, related_name="makes", default=None)
    year_manufactured = models.PositiveIntegerField(verbose_name='year_manufactued', 
        validators=[MinValueValidator(1900), MaxValueValidator(2024)], default=2023)
    mileage = models.PositiveIntegerField()
    price = models.FloatField(validators=[MinValueValidator(0.0)],)
    engine = models.CharField(max_length=1000, choices=(
        ("GAS", 'Gas'),
        ("DIESEL", 'Diesel'),
        ('HYBRID', 'Hybrid'),
        ('ELECTRIC', 'Electric'),
        ('Hydrogen', 'Hydrogen'),
        ('OTHER', 'Other')
    ), default="Gas")
    accident_free = models.BooleanField(default=True)
    origin_country = models.CharField(max_length=1000, default="USA")
    other_data = models.TextField(default="", blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cars", default=1)

    def __str__(self):
        return f"{self.year_manufactured} {self.series.__str__()} ({self.id})"
    
    def mileage_to_kilometers(self):
        return round(self.mileage * 1.60934)