from django.shortcuts import render, redirect
from .models import *
from django.http import Http404
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    distinct_manufacturers = Manufacturer.objects.values_list('name', flat=True).distinct()
    distinct_engines = ['Gas', 'Diesel', 'Hybrid', 'Electric', 'Hydrogen', 'Other']
    print(distinct_engines)
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
        "distinct_manufacturers": distinct_manufacturers,
        "distinct_engines": distinct_engines,
    })

def car(request, pk):
    try: 
        car = CarMake.objects.get(pk=pk)
    except CarMake.DoesNotExist:
        raise Http404("Car does not exist")
    return render(request, template_name="car.html", context    ={
        "car": car,
    })

@login_required
def create(request):
    return render(request, template_name="create", context={
        
    })

def register(request):
    if request.POST:
        form = RegisterForm(request.POST)
        if not form.is_valid():
            return render(request, template_name="registration/register.html", context=
                {
                    "form":form
                })
        else:
            try:
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('username')
                user = User(username=username, password=password)
                user.save()
                login(request, user)
                return redirect('/')
            except Exception as e:
                print(e)
    form = RegisterForm()
    return render(request, template_name="registration/register.html", context=
    {"form":form})