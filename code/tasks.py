from __future__ import print_function
import datetime
import time
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']

# Paths
CREDS_JSON = os.path.join( os.path.dirname( os.path.realpath(__file__) ), "client_secret.json")
TOCKEN_PICKLE = os.path.join( os.path.dirname( os.path.realpath(__file__) ), "token.pickle")


def connect_to_service():
  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists(TOCKEN_PICKLE):
    with open(TOCKEN_PICKLE, 'rb') as token:
      creds = pickle.load(token)

  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
  else:
    flow = InstalledAppFlow.from_client_secrets_file(CREDS_JSON, SCOPES)
    creds = flow.run_local_server(port = 0)
    # Save the credentials for the next run
    with open(TOCKEN_PICKLE, 'wb') as token:
      pickle.dump(creds, token)

  service = build('tasks', 'v1', credentials=creds)
  return service


def get_tasklist_ids(service):
  # Call the Tasks API
  results = service.tasklists().list().execute()
  items = results.get('items', [])

  tasklist_ids = []

  for item in items:
    tasklist_ids.append(item['id'])

  return tasklist_ids


def get_all_task_titles():
  service = connect_to_service()
  tasklist_ids = get_tasklist_ids(service)

  all_task_titles = []
  if not tasklist_ids:
    print('No task lists found.')
  else:
    for id in tasklist_ids:
      all_task_titles = all_task_titles + get_task_titles(service, id)

  return all_task_titles


def get_task_titles(service, tasklist_id):
  results = service.tasks().list(tasklist = tasklist_id, showCompleted = False, dueMax = rfc3339_today_midnight()).execute()
  items = results.get('items')
  task_titles = []

  if not items:
    return task_titles

  for item in items:
    task_titles.append(item['title'])

  return task_titles


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


if __name__ == '__main__':
  tasks = get_all_task_titles()

  for task in tasks:
    print("- {}".format(task))
  
  


  
