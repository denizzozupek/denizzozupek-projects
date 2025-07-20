import requests
from datetime import datetime

base_url = "https://api.openweathermap.org/data/2.5/weather?"
appid = "bc2eb23296420510646a3cb37e942553"
lat = "38.37101007312297"
lon = "27.12192809794194"



url = f"{base_url}lat={lat}&lon={lon}&appid={appid}&units=metric"

response = requests.get(url)
data = response.json()



if data["cod"] != 404:
    sky = str.capitalize(data["weather"][0]["description"])

    weather = data["main"]
    temp = weather["temp"]
    feels_like_temp = weather["feels_like"]
    humidity = weather["humidity"]
    name = data["name"]
    timestamp = data["dt"]
    date_time = datetime.fromtimestamp(timestamp)

    print(f"City Name={name}"
          f"\nDate/Time={date_time}"
          f"\nTemperature= {temp} "
          f"\nFeeling Temperature= {feels_like_temp}"
          f"\nHumidity = {humidity}"
          f"\nWeather = {sky}")

else:
    print("City Not Found")

