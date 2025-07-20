import customtkinter
import requests
from datetime import datetime
from PIL import Image
from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkImage

KEY_API = "bc2eb23296420510646a3cb37e942553"
app = customtkinter.CTk()
app.title("Weather App")
app.resizable(False, False)
app.geometry("600x500")
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")
app.iconbitmap("weather.ico")
app.container_icons = [None]*5

#frames
header_frame = CTkFrame(app, fg_color="#00bfff")
header_frame.place(relx=0, rely=0, relwidth=1, relheight=0.65)

bottom_frame = CTkFrame(app, fg_color="#0085b2")
bottom_frame.place(relx =0, rely=0.65, relwidth=1, relheight=0.35)

#labels
cityLabel = CTkLabel(header_frame, text="Izmir", font=("Arial Black", 25), anchor="w", width=100)
cityLabel.pack(padx=60, pady=(25,2), anchor="w")

dateLabel = CTkLabel(header_frame, text="", font=("Arial Black", 18), anchor="w", width=100)
dateLabel.pack(padx=60, pady=(0,5), anchor="w")

tempLabel = CTkLabel(header_frame, text="", font=("Arial Black", 48))
tempLabel.pack(padx=60, pady=(0,10), anchor="w")

forecastLabel = CTkLabel(header_frame, text="", font=('Arial', 18), justify="left")
forecastLabel.pack(padx=60, pady=(0, 10), anchor="w")

watchLabel= CTkLabel(header_frame, text="", font=("Arial Black", 25), width=100)
watchLabel.place(x=470, y=25)

weather_imageLabel = CTkLabel(header_frame, text="", image=None)
weather_imageLabel.place(x=80, y=190)

# containers
containers = []
for i in range(5):
    label = CTkLabel(
        bottom_frame,
        text="",
        compound="bottom",
        font=("Arial", 14, "bold"),
        text_color="black",
        width=100,
        height=150,
        fg_color="#ecf4fb",
        corner_radius=20
    )
    label.grid(row=0, column=i, padx=10, pady=10)
    containers.append(label)

search_entry = CTkEntry(
    master=header_frame,
    placeholder_text="Enter City",
    width=250,
    height=50,
    fg_color="#404040",
    border_width=0,
    corner_radius=25,
    font=("Arial", 17),
    text_color="white"
)
search_entry.place(x=310, y=110)
search_entry.bind("<Return>", lambda event: get_weather(city_name=search_entry.get()))

def search_city():
    city = search_entry.get()
    get_weather(city_name=city)

buton = CTkButton(header_frame, text="Search", width=100, height=30, border_width=0,
                  corner_radius=10, font=("Arial", 14), text_color="black", command=search_city)
buton.place(x=450, y=165)

def add_watch():
    watch = datetime.now().strftime("%H:%M")
    watchLabel.configure(text=watch)
    watchLabel.after(1000, add_watch)

def filter_day(data):
    day = {}
    for item in data["list"]:
        date = item["dt_txt"].split(" ")[0]
        if date not in day:
            day[date] = []
        day[date].append(item)
    return day

def filter_temp(dates):
    result = {}
    for key, values in dates.items():
        temps = [value["main"]["temp"] for value in values]
        result[key] = {"min": min(temps), "max": max(temps)}
    return result

def get_weather(city_name = "İzmir"):
    cityLabel.configure(text=city_name.title())

    GEOCODING_BASE_URL = "http://api.openweathermap.org/geo/1.0/direct?"
    geocoding_url = f"{GEOCODING_BASE_URL}q={city_name}&appid={KEY_API}"
    geo_response = requests.get(geocoding_url)
    geo_data = geo_response.json()
    if not geo_data:
        dateLabel.configure(text="City not found.")
        tempLabel.configure(text="")
        forecastLabel.configure(text="")
        return
    lat = geo_data[0]["lat"]
    lon = geo_data[0]["lon"]

    WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/forecast?"
    url = f"{WEATHER_BASE_URL}lat={lat}&lon={lon}&appid={KEY_API}&units=metric"
    response = requests.get(url)
    data = response.json()

    dates = filter_day(data)
    daily_temps = filter_temp(dates)

    today_dt = datetime.now()
    today_day = today_dt.strftime("%a")
    dateLabel.configure(text=today_day)

    temps_today = dates[list(dates.keys())[0]]
    noon_temp = None
    for entry in temps_today:
        if "12:00:00" in entry["dt_txt"]:
            noon_temp = entry["main"]["temp"]
            break
    if noon_temp is None:
        noon_temp = temps_today[0]["main"]["temp"]
    tempLabel.configure(text=f"{noon_temp:.1f}°C")

    #add daily temps in containers and add icon for temps
    for i, key in enumerate(list(daily_temps.keys())[:5]):
        day_dt = datetime.strptime(key, "%Y-%m-%d")
        day_name = day_dt.strftime("%a")
        max_temp = daily_temps[key]["max"]
        min_temp = daily_temps[key]["min"]

        noon_entry = None
        for entry in dates[key]:
            if "12:00:00" in entry["dt_txt"]:
                noon_entry = entry
                break
        if noon_entry is None:
            noon_entry = dates[key][0]

        desc = noon_entry["weather"][0]["description"].lower()
        temp = noon_entry["main"]["temp"]

        if temp > 28:
            image_path = "icons/sun.png"
        elif temp < 10:
            image_path = "icons/snow.png"
        elif "rain" in desc:
            image_path = "icons/rainy-day.png"
        elif "cloud" in desc:
            image_path = "icons/clouds.png"
        elif "thunder" in desc or "storm" in desc:
            image_path = "icons/storm.png"
        else:
            image_path = "icons/default.png"

        app.container_icons[i] = CTkImage(Image.open(image_path), size=(50,50))
        containers[i].configure(text=f"{day_name}\n{max_temp:.0f}° / {min_temp:.0f}°",
            image=app.container_icons[i],
            compound="bottom")
        header_icon = CTkImage(Image.open(image_path), size=(100,100))
        weather_imageLabel.configure(image=header_icon)

add_watch()
get_weather()
app.mainloop()