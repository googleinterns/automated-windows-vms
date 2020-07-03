
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
task_response = Request_pb2.TaskResponse()
task_request = Request_pb2.TaskRequest()

def task_done():
  """It prints time and then sleep for some time
     and then again print time.
  """
  global flag
  global task_response
  now = datetime.now()
  current_time = now.strftime('%H:%M:%S')
  print('Current Time =', current_time)
  task_response.status = Request_pb2.TaskResponse.BUSY
  start = timeit.default_timer()
  t = multiprocessing.Process(target=execute_task)
  t.start()
  t.join(int(task_request.timeout))
  if t.is_alive():
    task_response.status = Request_pb2.TaskResponse.FAILURE
    task_response.time_taken = 0.0
    t.terminate()
    t.join()
  else:
    stop = timeit.default_timer()
    time_taken = stop-start
    task_response.time_taken = time_taken
    task_response.status = Request_pb2.TaskResponse.SUCCESS
  now = datetime.now()
#  print(task_response)
  current_time = now.strftime('%H:%M:%S')
  print('Current Time =', current_time)
  task_completed()
  flag = False
  register_vm_address()

def execute_task():
  time.sleep(10)

def task_completed():
#  Notify the master server after task is completed.
  
  read = task_response.SerializeToString()
  response = requests.post(url='http://127.0.0.1:5000/success', files=
      {'task_response': read, 'request_id': ('', str(task_request.request_id))})

@APP.route('/', methods=['GET', 'POST'])
def hello_world():
  """This function receives files from master server.
     And executes some task to make the VM busy.
  """
  global flag
  global request_id
  global task_request
  input_file = request.files['task_request']
  task_request.ParseFromString(input_file.read())
  print(task_request)
  request_id = task_request.request_id
  flag = True
  t = threading.Thread(target=task_done)
  t.start()
  return 'success'

@APP.route('/active', methods=['GET', 'POST'])
def is_active():
#  Master can check here if VM is active or not.
  return {'hello': 'world'}

@APP.route('/status', methods=['GET', 'POST'])
def flag_status():
#  Returns the state of VM
  return {'status': flag}

def register_vm_address():
#  This functions tells the master server that VM is healhty.
  data = 'http://127.0.0.1:' + str(sys.argv[1])
  try:
    req = requests.get(MASTER_SERVER + str('/register'), data=data)
  except:
    print('can''t connect to master server')

def pre_task():
#  This function performs tasks before the start of flask server.
  if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], 'INPUT_PORT')
    sys.exit(-1)
  VM_ADDRESS = 'http://127.0.0.1:' + sys.argv[1]
  register_vm_address()

if __name__ == '__main__':
  APP.run()