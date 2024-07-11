from django.shortcuts import render
from .models import *
# Create your views here.
def index(request):
    cars = CarMake.objects.all()
    return render(request, template_name='index.html', context={
        "cars": cars
    })