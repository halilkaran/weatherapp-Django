# PRECLASS SETUP

```bash
# CREATING VIRTUAL ENVIRONMENT
# windows
py -m venv env
# windows other option
python -m venv env
# linux / Mac OS
python3 -m venv env

# ACTIVATING ENVIRONMENT
# windows
.\env\Scripts\activate
# linux / Mac OS
source env/bin/activate

# PACKAGE INSTALLATION
# if pip does not work try pip3 in linux/Mac OS
pip install django
# alternatively python -m pip install django

python -m django --version
django-admin startproject weather .

pip install python-decouple
pip freeze > requirements.txt
```
add a gitignore file at same level as env folder

create a new file and name as .env at same level as env folder

copy your SECRET_KEY from settings.py into this .env file. Don't forget to remove quotation marks from SECRET_KEY

```
SECRET_KEY = django-insecure-)=b-%-w+0_^slb(exmy*mfiaj&wz6_fb4m&s=az-zs!#1^ui7j
```

go to settings.py, make amendments below

```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
```

go to terminal

```bash
py manage.py migrate
py manage.py runserver
```

click the link with CTRL key pressed in the terminal and see django rocket.

go to terminal, stop project, add app

```
py manage.py startapp weatherapp
```

go to settings.py and add 'weatherapp' app to installed apps and add below lines

go to createsuperuser
and runserver


index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>Weather App</h1>
</body>
</html>
```

go to weatherapp/views.py

```python
from django.shortcuts import render

def index(request):
    return render(request, 'weatherapp/index.html')

```
go to weather/urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('weatherapp.urls')),
]
```

go to weatherapp/urls.py

```python
from django.urls import path
from .views import index

urlpatterns = [
    path('', index, name='home'),
]
```

------------------------------------------------------------- Setup completed


go to https://openweathermap.org/current#geocoding and talk about apı document

go to https://home.openweathermap.org/api_keys and copy your apı key and paste in .env file

```.env file:
API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```


go to terminal
```bash
pip install requests
``` 

views.py
```python
from django.shortcuts import render
import requests
from decouple import config
from pprint import pprint

def index(request):
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"
    city = "Berlin"
    response = requests.get(url.format(city, config("API_KEY")))
    content = response.json()  # convert to dictionary
    pprint(content)
    pprint(type(content))
    return render(request, 'weatherapp/index.html')

```

runserver, request from browser and see results in terminal


models.py
```Python
from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name

```

```bash
py manage.py makemigrations
py manage.py migrate
```

admin.py
```Python
from django.contrib import admin
from .models import City

admin.site.register(City)
```

add city objects from admin site

views.py
```python
from django.shortcuts import render
import requests
from decouple import config
from pprint import pprint
from .models import City

def index(request):
    cities = City.objects.all()
    # url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"
    # response = requests.get(url.format(city, config("API_KEY")))
    # content = response.json()  # convert to dictionary
    # pprint(content)
    # pprint(type(content))
    
    for city in cities:
        print(city)
    
    return render(request, 'weatherapp/index.html')

```

runserver, request from browser and see results in terminal

views.py
```python
from django.shortcuts import render
import requests
from decouple import config
from pprint import pprint
from .models import City

def index(request):
    cities = City.objects.all()
    city_data = []
    for city in cities:
        url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"
        response = requests.get(url.format(city, config("API_KEY")))
        content = response.json()  # convert to dictionary
        # pprint(content)
        data = {
            "city" : city.name,
            "temp" : content["main"]["temp"],
            "desc" : content["weather"][0]["description"],
            "icon" : content["weather"][0]["icon"]
        }
        pprint(data)
        city_data.append(data)
    
    context = {
        "city_data" : city_data
    }
    
    return render(request, 'weatherapp/index.html', context)

```

runserver, request from browser and see results in terminal


index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>Weather App</h1>

    {% for city in city_data  %}
        {{city.city}} <br>
        {{city.temp}} <br>
        {{city.desc}} <br>
        <hr>
    {% endfor %}
    
</body>
</html>

```

runserver, request from browser and see results in browser


weather API url for icons : https://openweathermap.org/weather-conditions 
endpoint : http://openweathermap.org/img/wn/{{}}.png

update index.html 
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>Weather App</h1>

    {% for city in city_data  %}
        {{city.city}} <br>
        {{city.temp}} <br>  <!-- <p>{{city.temp}}&#8451;</p> <br> -->
        <img src="http://openweathermap.org/img/wn/{{ city.icon }}.png" alt="icon">
        {{city.desc}} <br>
        <hr>
    {% endfor %}
    
</body>
</html>

```

------------------------------------------------------------------------
# Take City From User

Add form in index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>Weather App</h1>

    <form action="">
        <input type="text" name="name">
        <input type="submit" value="Add">
    </form>
    <br>

    {% for city in city_data  %}
        {{city.city}} <br>
        {{city.temp}} <br>  <!-- <p>{{city.temp}}&#8451;</p> <br> -->
        <img src="http://openweathermap.org/img/wn/{{ city.icon }}.png" alt="icon">
        {{city.desc}} <br>
        <hr>
    {% endfor %}
    
</body>
</html>

```

update views.py file:
views.py
```python
from django.shortcuts import render
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
            "city" : city.name,
            "temp" : content["main"]["temp"],
            "desc" : content["weather"][0]["description"],
            "icon" : content["weather"][0]["icon"]
        }
        pprint(data)
        city_data.append(data)
    
    context = {
        "city_data" : city_data
    }
    
    return render(request, 'weatherapp/index.html', context)

```

```html
    {% if messages %}
        
        {% for message in  messages%}
            {{message}}
        {% endfor %}
            
    {% endif %}
    <br>
```


add delete city feature

views.py
```Python

def city_delete(request, id):
    city = get_object_or_404(City, id=id)
    city.delete()
    messages.success(request, "City deleted.")
    return redirect("home")
```

urls.py
```python
from django.urls import path
from .views import index, city_delete

urlpatterns = [
    path('', index, name='home'),
    path('delete/<int:id>', city_delete, name='delete'),
]
```

index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>

    
    {% if messages %}
        
        {% for message in  messages%}
            {{message}}
        {% endfor %}
            
    {% endif %}
    <br>

    <h1>Weather App</h1>

    <form action="">
        <input type="text" name="name">
        <input type="submit" value="Add">
    </form>
    <br>

    {% for i in city_data  %}
        {{i.city.name}} <br>
        <p>{{i.temp}}&#8451;</p> <br>
        <img src="http://openweathermap.org/img/wn/{{ i.icon }}.png" alt="icon">
        {{i.desc}} <br>
        <button><a href="{% url 'delete' i.city.id %}">Delete</a></button>
        <hr>
    {% endfor %}

</body>
</html>
```

Note : change city in data:
```python
        data = {
            "city" : city,
            "temp" : content["main"]["temp"],
            "desc" : content["weather"][0]["description"],
            "icon" : content["weather"][0]["icon"]
        }
```
go to browser and try new changes

-------------------------------------------------------------
change template to index2.html 

