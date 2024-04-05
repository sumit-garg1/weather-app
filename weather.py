from tkinter import *
from tkinter import messagebox
from datetime import datetime
from configparser import ConfigParser
import requests
url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']
app = Tk()


def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        # print(result.content)
        json = result.json()
        City = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        temp_fahrenheit = (temp_kelvin-273.15) * 9/5 + 32
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        final = (City, country, temp_celsius, temp_fahrenheit, icon, weather)
        return final

    else:
        return None


def search():
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        location_lb['text'] = '{}, {}'.format(weather[0], weather[1])
        tem_lb['text'] = '{:.2f}°C, {:.2f}°F'.format(weather[2], weather[3])
        weather_lb['text'] = weather[5]
        current_time = datetime.now().strftime('%H:%M:%S')
        time_lb['text'] = 'Current Time: {}'.format(current_time)
    else:
        messagebox.showerror('Error', 'The city was not found: {}'.format(city))


app.title("Weather App")
app.geometry("700x600")

city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()

src_btn = Button(app, text="search", width=12, command=search)
src_btn.pack()

location_lb = Label(app, text="location", font=("Times New Roman", 20, "bold"))
location_lb.pack()

image_lb = Label(app, bitmap='')
image_lb.pack()

tem_lb = Label(app, text="")
tem_lb.pack()

weather_lb = Label(app, text="")
weather_lb.pack()

time_lb = Label(app, text="")
time_lb.pack()
app.mainloop()
