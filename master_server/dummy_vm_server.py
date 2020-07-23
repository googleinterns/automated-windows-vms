"""This is a dummy VM server.
  It is built to test the master server.
"""
import sys
import os
import threading
from datetime import datetime
import timeit
import multiprocessing
import time
import requests
from flask import request
from flask import Flask
from flask import send_file
import Request_pb2

class MyFlaskApp(Flask):
  """This class configures the flask app and executes function
     pre_task before starting flask server.
  """
  def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
    if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
      with self.app_context():
        pre_task()
    super(MyFlaskApp, self).run(
        host=host, port=int(sys.argv[1]), debug=debug,
        load_dotenv=load_dotenv, **options)

APP = MyFlaskApp(__name__)

flag = False
MASTER_SERVER = 'http://127.0.0.1:5000'
VM_ADDRESS = 'http://127.0.0.1:'
request_id = ''
task_request = Request_pb2.TaskRequest()
task_status_response = Request_pb2.TaskStatusResponse()

def task_done():
  """It prints time and then sleep for some time
     and then again print time.
  """
  global flag
  global task_status_response
  now = datetime.now()
  current_time = now.strftime('%H:%M:%S')
  print('Started Task id is '+str(request_id)+' VM is '+str(VM_ADDRESS))
  print('Current Time =', current_time)
  start = timeit.default_timer()
  process = multiprocessing.Process(target=execute_task)
  process.start()
  process.join(int(task_request.timeout))
  if process.is_alive():
    task_status_response.task_response.status = Request_pb2.TaskResponse.FAILURE
    task_status_response.task_response.time_taken = 0.0
    process.terminate()
    process.join()
  else:
    stop = timeit.default_timer()
    time_taken = stop-start
    task_status_response.task_response.time_taken = time_taken
    task_status_response.task_response.status = Request_pb2.TaskResponse.SUCCESS
  now = datetime.now()
  current_time = now.strftime('%H:%M:%S')
  print('Current Time =', current_time)
  print('Ended Task id is '+str(request_id)+' VM is '+str(VM_ADDRESS))
  process = threading.Thread(target = task_completed)
  process.start()
  flag = False
  register_vm_address()

def execute_task():
  time.sleep(10)

def task_completed():
  """Notify the master server after task is completed."""
  read = task_status_response.SerializeToString()
  response = requests.post(url='http://127.0.0.1:5000/success', files=
      {'task_response': read, 'request_id': ('', str(task_request.request_id))})
  print(response.status_code)

@APP.route('/assign_task', methods=['GET', 'POST'])
def hello_world():
  """This function receives files from master server.
     And executes some task to make the VM busy.
  """
  global flag
  global request_id
  global task_request
  global task_status_response
  input_file = request.files['task_request']
  task_request.ParseFromString(input_file.read())
  print(task_request)
  request_id = task_request.request_id
  flag = True
  process = threading.Thread(target=task_done)
  process.start()
  task_status_response.current_task_id = task_request.request_id
  task_status_response.status = Request_pb2.TaskStatusResponse.ACCEPTED
  return task_status_response.SerializeToString()

@APP.route('/active', methods=['GET', 'POST'])
def is_active():
  """Master can check here if VM is active or not."""
  return {'hello': 'world'}

@APP.route('/status', methods=['GET', 'POST'])
def flag_status():
  """Returns the state of VM."""
  return {'status': flag}
  
@APP.route('/get_status', methods=['GET', 'POST'])
def get_status_of_request():
  """Return the current status of the executing request."""
  input_file = request.files['task_request']
  task_status_request = Request_pb2.TaskStatusRequest()
  task_status_request.ParseFromString(input_files.read())
  if task_status_response.current_task_id == task_status_request.request_id:
    return task_status_response.SeralizeToString()
  else:
    task = Request_pb2.TaskStatusResponse()
    task.status = Request_pb2.TaskStatusResponse.INVALID_ID
    return task.SeralizeToString()
  
def register_vm_address():
  """This functions tells the master server that VM is healhty."""
  data = 'http://127.0.0.1:' + str(sys.argv[1])
  try:
    req = requests.get(MASTER_SERVER + str('/register'), data=data)
  except:
    print('can''t connect to master server')

def pre_task():
  """This function performs tasks before the start of flask server."""
  global VM_ADDRESS
  if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], 'INPUT_PORT')
    sys.exit(-1)
  VM_ADDRESS = 'http://127.0.0.1:' + sys.argv[1]
  file = open('listfile.txt', 'a')
  file.write(VM_ADDRESS + '\n')
  register_vm_address()

if __name__ == '__main__':
  APP.run()
