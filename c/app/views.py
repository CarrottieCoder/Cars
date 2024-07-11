from django.shortcuts import render
from .models import *
from django.http import Http404
# Create your views here.
def index(request):
    # Enable filters
    if request.GET and "f" in request.GET:
        origin_country = request.GET.get('origin_country')
        accident_free = request.GET.get('accident_free')
        engine = request.GET.get('engine')
        cars = CarMake.objects.filter(
            origin_country=origin_country,
            accident_free=accident_free,
            engine=engine,
            )
        
    else:
        cars = CarMake.objects.all()

    return render(request, template_name='index.html', context={
        "cars": cars,
    })

def car(request, pk):
    try: 
        car = CarMake.objects.get(pk=pk)
    except CarMake.DoesNotExist:
        raise Http404("Car does not exist")
    return render(request, template_name="car.html", context    ={
        "car": car,
    })