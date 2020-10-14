import requests
import json
import os

API_KEY_FILE_PATH = os.path.join( os.path.dirname( os.path.realpath(__file__) ), "api_key.txt")
API_URL = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"
CITY_NAME = "Malmoe"

class Weather:
  def __init__(self):
    self.weather_dict = {}
    self.update_weather_dict()

  def update_weather_dict(self):
    weather_request = get_weather_request()

    if weather_request.status_code == 200: # HTTP code for success
      weather_json = weather_request.json()

      new_weather_dict = {}
      new_weather_dict['description'] = weather_json['weather'][0]['description']
      new_weather_dict['temp'] = weather_json['main']['temp']
      new_weather_dict['icon_file_name'] = "{}_2x.bmp".format( weather_json['weather'][0]['icon'] )

      self.weather_dict = new_weather_dict


def get_weather_request():
  '''Gets the Open Weather API request.'''

  api_key_file = open(API_KEY_FILE_PATH, "r")
  api_key = api_key_file.read()
  return requests.get(API_URL.format(CITY_NAME, api_key))


if __name__ == "__main__":
  weather = Weather().weather_dict
  print("Weather description: {}.".format(weather['description']))
  print("Temperature {} degree C.".format(weather['temp']))
  print("Icon file name = {}.".format(weather['icon_file_name']))

