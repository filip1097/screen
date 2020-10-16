import datetime
import time


class TaskList:
  def __init__(self, id):
    self.id = id
    self.tasks = []

  def update(self, service):
    results = service.tasks().list(tasklist = self.id, showCompleted = False, dueMax = rfc3339_today_midnight()).execute()
    items = results.get('items')
    self.tasks = []

    if not items: # empty list do nothing
      pass
    
    else:
      for item in items:
        self.tasks.append(item['title'])


def rfc3339_today_midnight(): 
  now = datetime.datetime.now()
  dt = datetime.datetime(now.year, now.month, now.day, 23, 59, 59, 0).isoformat()

  timezone = int(time.timezone / 3600.0)
  if timezone < 0:
    dt = dt + '-'
  if abs(timezone) < 10:
    dt = dt + '0' + str( abs(timezone) ) + ':00'
  else:
    dt = dt + str( abs(timezone) ) + ':00'

  return dt

