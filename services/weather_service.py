import requests

# Replace with your OpenWeather API Key

API_KEY = "6c8b18cc4f1c9fb2fd5a9be6ab41ae3d"

def get_weather(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}"
        f"&appid={API_KEY}"
        f"&units=metric"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return "Normal", 25

    data = response.json()
    temperature = data["main"]["temp"]

    if temperature > 30:
        weather_type = "Hot"
    elif temperature < 20:
        weather_type = "Cold"
    else:
        weather_type = "Normal"

    return weather_type, temperature

