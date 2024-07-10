from django.contrib import admin
from .models import CarSeries, CarMake, Manufacturer
# Register your models here.

admin.site.register(CarMake)
admin.site.register(CarSeries)
admin.site.register(Manufacturer)
