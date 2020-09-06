import datetime

class DateAndTime:
  def __init__(self):
    self.dt = datetime.datetime.now()

  def get_time_string(self):  
    return self.dt.strftime("%H:%M")
  
  def get_date_string(self):
    return self.dt.strftime("20%y-%m-%d")

  def update(self):
    self.dt = datetime.datetime.now()

  def new_minute(self):
    old_min = self.dt.minute
    self.update()
    return old_min != self.dt.minute

if __name__ == "__main__":
  dt = DateAndTime()
  print(dt.get_time_string())
  print(dt.get_date_string())
  print(dt.new_minute())
