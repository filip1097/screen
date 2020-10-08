#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
icondir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'icons')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'fonts')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
  sys.path.append(libdir)

import logging
import schedule
import time
from waveshare_epd import epd4in2
from PIL import Image,ImageDraw,ImageFont

# my files
import DateAndTime
from weather import get_weather_dict
from tasks import get_all_task_titles

def update_screen(dt, logging):
  # Get weather information
  weather = get_weather_dict()

  # Update time
  dt.update()

  try:
    logging.info("Update Screen")

    # init the screen
    epd = epd4in2.EPD()
    logging.info("Init Screen")
    epd.init()

    # Drawing on the Horizontal image
    logging.info("Drawing on the Horizontal image...")
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)

    # Draw lines
    logging.info("Drawing lines")
    draw_horizontal_line(draw)
    draw_vertical_line(draw)

    # Time section
    draw_date_and_time(draw)

    # Weather section
    paste_weather_icon(Himage, weather)
    draw_temperature(draw, weather)
    draw_weather_desc(draw, weather)

    # Task Section
    draw_todo(draw)
    draw_tasks(draw)

    # Displaying image on screen
    logging.info("Displaying image")
    epd.display(epd.getbuffer(Himage))
    
  except IOError as e:
    logging.info(e)
    
  except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd4in2.epdconfig.module_exit()
    exit()  


def draw_date_and_time(draw):
  logging.info("Drawing date and time")
  draw.text((12, 0), dt.get_time_string(), font = font68, fill = 0)
  draw.text((32, 80), dt.get_date_string(), font = font24, fill = 0)


def draw_vertical_line(draw):
  draw.line((199, 0, 199, 300), fill=0)
  draw.line((200, 0, 200, 300), fill=0)
  draw.line((201, 0, 201, 300), fill=0)


def draw_horizontal_line(draw):
  draw.line((0, 129, 200, 129), fill = 0) 
  draw.line((0, 130, 200, 130), fill = 0)
  draw.line((0, 131, 200, 131), fill = 0)


def draw_tasks(draw):
  logging.info("API call for tasks")
  tasks = get_all_task_titles()

  logging.info("Drawing tasks")

  height = 60
  for task in tasks:
    draw.text((220, height), '-' + task, font = font18, fill = 0)
    height = height + 25


def draw_temperature(draw, weather):
  logging.info("Drawing temperature")
  # print temperature
  draw.text((30, 125), str( round(weather['temp']) ), font = font68, fill = 0)
  # print degree sign
  draw.text((107, 130), 'o', font = font24, fill = 0)
  # print celsius C
  draw.text((120, 125), 'C', font = font68, fill = 0)


def draw_todo(draw):
  logging.info("Drawing TODO")
  draw.text((220, 10), "TODO:", font = font35, fill = 0)


def draw_weather_desc(draw, weather):
  logging.info("Drawing weather description")
  draw.text((30, 270), weather['description'], font = font18, fill = 0)


def paste_weather_icon(image, weather):
  logging.info("Pasting weather icon")
  icon_path = os.path.join(icondir, weather['icon_file_name'])
  weather_icon = Image.open(icon_path)
  image.paste(weather_icon, (50, 180))


if __name__ == "__main__":
  # init logging
  logging.basicConfig(level=logging.DEBUG)
  logging.info("Start Screen Program")

  # init date and time 
  dt = DateAndTime.DateAndTime()

  # init the fonts
  font18 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 18)
  font24 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 24)
  font35 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 35)
  font68 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 68)

  schedule.every(1).minutes.do(update_screen, dt = dt, logging = logging)

  update_screen(dt, logging)

  while True:
    schedule.run_pending()
    time.sleep(1)
 
