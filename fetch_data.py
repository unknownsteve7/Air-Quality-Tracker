import requests
import json

cities = ['Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Chennai']
API_KEY = "c1abcda61cc3e80dd2daab4791befa08"

def fetch_data(city):
    api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(api)
    data = response.json()
    return json.dumps(data, indent=4)

for city in cities:
    data = fetch_data(city)
    print(f"Weather data for {city}:\n{data}\n")

def get_city_coordinates(city):
    api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(api)
    data = response.json()
    return data['coord']['lat'], data['coord']['lon']

def pollution_check(city):
    latitude, longitude = get_city_coordinates(city)
    api = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={API_KEY}"
    response = requests.get(api)
    data = response.json()
    return json.dumps(data, indent=4)

for city in cities:
    data = pollution_check(city)
    print(f"Pollution data for {city}:\n{data}\n")