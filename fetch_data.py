import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

cities = ['Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Chennai']
API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    try:
        import streamlit as st
        API_KEY = st.secrets["OPENWEATHER_API_KEY"]
    except:
        pass

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