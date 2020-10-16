from __future__ import print_function
import datetime
import time
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import TaskList

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']

# Paths
CREDS_JSON = os.path.join( os.path.dirname( os.path.realpath(__file__) ), "client_secret.json")
TOCKEN_PICKLE = os.path.join( os.path.dirname( os.path.realpath(__file__) ), "token.pickle")

class Tasks:
  def __init__(self):
    self.task_lists = []

    # -1 refers to that task_list_ids should be updated, the rest the index of the task list in task_list_ids
    self.update_index = -1 

    self.update_all()

  def update(self, n):
    '''Makes n update requests.'''
    
    service = connect_to_service()

    for _ in range(n):
      if self.update_index >= len( self.task_lists ):
        self.update_index = -1

      if self.update_index == -1:
        self.update_tasks_lists(service)
      else:
        self.task_lists[ self.update_index ].update(service)

      self.update_index += 1

  def update_all(self):
    service = connect_to_service()
    self.update_tasks_lists(service)

    for task_list in self.task_lists: 
      task_list.update(service)

  def update_tasks_lists(self, service):
    # Call the Tasks API
    results = service.tasklists().list().execute()
    items = results.get('items', [])
    
    task_list_ids = []
    for item in items:
      task_list_ids.append( item['id'] )

    # remove deleted lists:
    for task_list in self.task_lists:
      if task_list.id not in task_list_ids:
        self.task_lists.remove( task_list )

    # add new task lists:
    for task_list_id in task_list_ids:
      existing_task_list_ids = [ task_list.id for task_list in self.task_lists ]

      if task_list_id not in existing_task_list_ids:
        self.task_lists.append( TaskList.TaskList( task_list_id ) )

  def get_all_tasks(self):
    tasks = []
    for task_list in self.task_lists:
      tasks = tasks + task_list.tasks

    return tasks

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


if __name__ == '__main__':
  tasks = Tasks()

  for task in tasks.get_all_tasks():
    print("- {}".format(task))
  
  


  
