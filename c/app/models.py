from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    origin_demonym = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} from {self.origin}"

class CarSeries(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="series")
    name = models.CharField(max_length=100)
    car_class = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.manufacturer.name} {self.name}" 

class CarMake(models.Model):
    series = models.ForeignKey(CarSeries, on_delete=models.CASCADE, related_name="makes")
    year_manufactured = models.PositiveIntegerField(verbose_name='years_manufactued', 
        validators=[MinValueValidator(1900), MaxValueValidator(2024)])
    mileage = models.PositiveIntegerField()
    price = models.FloatField(validators=[MinValueValidator(0.0)],)
    # User will go here 

    def __str__(self):
        return f"{self.series.__str__()} {self.year_manufactured} \n Mileage: {self.mileage} \n Price: {self.price}$"