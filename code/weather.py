import requests
import json
import os

def get_weather_json():
  api_key_file_path = os.path.join( os.path.dirname( os.path.realpath(__file__) ), "api_key.txt")
  api_key_file = open(api_key_file_path, "r")

  city_name = "Malmoe"
  api_key = api_key_file.read()
  api_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"

  return requests.get(api_url.format(city_name, api_key))


def get_weather_dict():
  weather_json = get_weather_json().json()
  weather_dict = {}
  weather_dict['description'] = weather_json['weather'][0]['description']
  weather_dict['temp'] = weather_json['main']['temp']
  weather_dict['icon_file_name'] = "{}_2x.bmp".format( weather_json['weather'][0]['icon'] )
  return weather_dict


if __name__ == "__main__":
  weather = get_weather_dict()
  print("Weather description: {}.".format(weather['description']))
  print("Temperature {} degree C.".format(weather['temp']))
  print("Icon file name = {}.".format(weather['icon_file_name']))

