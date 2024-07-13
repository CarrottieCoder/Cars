from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden, HttpResponse
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    distinct_manufacturers = Manufacturer.objects.values_list('name', flat=True).distinct()
    distinct_manufacturer_origin = Manufacturer.objects.values_list('origin', flat=True).distinct()
    distinct_engines = ['Gas', 'Diesel', 'Hybrid', 'Electric', 'Hydrogen', 'Other']
    # Enable filters 
    queryset = CarMake.objects.all()
    f = False
    
    # Get GET parameters 
    accident_free = request.GET.get('accident_free')
    engines = request.GET.getlist('engines')
    manufacturers = request.GET.getlist('manufacturers')
    distance_unit = request.GET.get('distance_unit', request.COOKIES.get('distance_unit', "Miles"))
    manufacturer_origin = request.GET.getlist('manufacturer_origin')

    if not len(request.GET) == 0:
        if not len(request.GET) == 1 and distance_unit:
            f = True

        if accident_free != None:
            queryset = queryset.filter(accident_free=True)

        if engines:
            engine_filter = Q()
            for engine in engines:
                engine_filter |= Q(engine=engine)
            queryset = queryset.filter(engine_filter)
        
        if manufacturers:
            man_filter = Q()
            for man in manufacturers:
                man_filter |= Q(series__manufacturer__name=man)
            queryset = queryset.filter(man_filter)
        
        if manufacturer_origin:
            print('MO: ')
            print(manufacturer_origin)

            man_o_filter = Q()
            for man_o in manufacturer_origin:
                man_o_filter |= Q(series__manufacturer__origin=man_o)
            queryset = queryset.filter(man_o_filter)

        if distance_unit != "Miles":
            distance_unit = "Kilometers"
    
    print(accident_free)
    response = HttpResponse()
    response =  render(request, template_name='index.html', context={
        "cars": queryset,
        "distinct_manufacturers": distinct_manufacturers,
        "distinct_manufacturer_origin": distinct_manufacturer_origin,
        "distinct_engines": distinct_engines,
        "f": f,
        "accident_free": accident_free,
        "engines": engines,
        "manufacturers": manufacturers,
        "manufacturer_origin": manufacturer_origin,
        "distance_unit": distance_unit

    })
    # Cookies 
    response.set_cookie(key='distance_unit', value=distance_unit, max_age=10000)
    return response


def car(request, pk):
    try: 
        car = CarMake.objects.get(pk=pk)
    except CarMake.DoesNotExist:
        raise Http404("Car does not exist")
    print(car.owner == request.user)
    unit = request.COOKIES.get('distance_unit', "Miles")
    return render(request, template_name="car.html", context    ={
        "car": car,
        "unit": unit,
    })

@login_required
def delete_make(request, pk):
    try:
        car = CarMake.objects.get(pk=pk)
    except CarMake.DoesNotExist:
        return redirect('/')
    
    if car.owner == request.user:
        car.delete()
        return redirect('/')
    else:
        return HttpResponseForbidden("That is NOT yours")

@login_required
def edit_make(request, pk):
    try:
        car = CarMake.objects.get(pk=pk)
    except CarMake.DoesNotExist:
        return redirect('/')
    if car.owner == request.user:
        if request.method == "POST":
            form = CarMakeForm(request.POST, instance=car)
            if form.is_valid():
                form.save()
                car.save()
                return redirect('car', car.id)
            else:
               return render(request, template_name="edit.html", context={
                "form": form,
                "car": car
            }) 
        else:
            form = CarMakeForm(instance=car)
            return render(request, template_name="edit.html", context={
                "form": form,
                "car": car
            })
    else: 
        return HttpResponseForbidden("That is NOT yours")

@login_required
def create_make(request):
    if request.POST:
        form = CreateCarMakeForm(request.POST)
        if not form.is_valid():
            return render(request, template_name="create.html", context={
                "form": form
            })
        else:
            try:
                series = form.cleaned_data.get('series')
                year_manufactured = form.cleaned_data.get('year_manufactured')
                mileage = form.cleaned_data.get('mileage')
                price = form.cleaned_data.get('price')
                engine = form.cleaned_data.get('engine')
                accident_free = form.cleaned_data.get('accident_free')
                origin_country = form.cleaned_data.get('origin_country')
                other_data = form.cleaned_data.get('other_data', "")
                owner = request.user

                make = CarMake(series=series, year_manufactured=year_manufactured, mileage=mileage, price=price, engine=engine, accident_free=accident_free, origin_country=origin_country, other_data=other_data, owner=owner)
                make.save()
                return redirect(f"cars/{make.id}")
            except Exception as e:
                print(e)
    form = CreateCarMakeForm()
    return render(request, template_name="create.html", context={
        "form": form
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