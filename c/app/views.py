from django.shortcuts import render
from .models import *
from django.http import Http404
# Create your views here.
def index(request):
    cars = CarMake.objects.all()
    return render(request, template_name='index.html', context={
        "cars": cars
    })

def car(request, pk):
    try: 
        car = Car.objects.get(pk=pk)
    except Car.DoesNotExist:
        raise Http404("Car does not exist")
    return render(request, template_name="car.html", content={
        "car": car,
    })