from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import requests
from decouple import config
from pprint import pprint
from .models import City
 


def index(request):
    cities = City.objects.all()
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"
    
    user_city = request.GET.get("name") # if does not exists doesnt give error, returns None
    if user_city:
        response = requests.get(url.format(user_city, config("API_KEY")))
        print(response.status_code)
        if response.status_code == 200:
            content = response.json()
            response_city = content["name"]
            if City.objects.filter(name=response_city):
                messages.warning(request, "city already exists.")
            else:
                City.objects.create(name=response_city)
                messages.success(request, "City successfully created.")
        else:
            messages.warning(request, "city not found.")
    
    city_data = []
    for city in cities:
        url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"
        response = requests.get(url.format(city, config("API_KEY")))
        content = response.json()  # convert to dictionary
        # pprint(content)
        data = {
            "city" : city,
            "temp" : content["main"]["temp"],
            "desc" : content["weather"][0]["description"],
            "icon" : content["weather"][0]["icon"]
        }
        pprint(data)
        city_data.append(data)
    
    context = {
        "city_data" : city_data
    }
    
    return render(request, 'weatherapp/index2.html', context)

def city_delete(request, id):
    city = get_object_or_404(City, id=id)
    city.delete()
    messages.success(request, "City succesfully deleted.")
    return redirect("home")