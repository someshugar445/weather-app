from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm


def index(request):
    YOUR_APP_KEY = "2a0a71c25e652f0dd035518417583a5d"
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate

    form = CityForm()
    cities = City.objects.all()  # return all the cities in the database
    weather_data = []
    for city in cities:
        city_weather = requests.get(url.format(city.name,YOUR_APP_KEY)).json()  # request the API data and convert the JSON to Python data types

        weather = {
            'city': city.name,
            'Country': city_weather['sys']['country'],
            'wind_speed': city_weather['wind']['speed'],
            'temperature': city_weather['main']['temp'],
            'humidity': city_weather['main']['humidity'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }

        weather_data.append(weather)  # add the data for the current city into our list

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/index.html', context) #returns the index.html template

