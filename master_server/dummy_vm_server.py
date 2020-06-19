"""
  This is a dummy VM server.
  It is built to test master server.
"""
import sys
import os
import threading
from datetime import datetime
import requests
from flask import Flask
from flask import request
import random


class MyFlaskApp(Flask):
  """
    This class configures the flask app and executes function
    pre_task before starting flask server.
  """
  def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
    if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
      with self.app_context():
        pre_task()
    super(MyFlaskApp, self).run(
        host=host, port=int(sys.argv[1]), debug=debug,
        load_dotenv=load_dotenv, **options)

app = MyFlaskApp(__name__)

flag = False
master_server = 'http://127.0.0.1:5000'
vm_address = 'http://127.0.0.1:'
request_id = ''

def task_done():
  """
    It prints time and then sleep for some time
    and then again print time.
  """
  global flag
  now = datetime.now()
  current_time = now.strftime('%H:%M:%S')
  print('Current Time =', current_time)
  n = random.randint(0,3000)
  os.system('sleep '+str(n))
  now = datetime.now()
  current_time = now.strftime('%H:%M:%S')
  print('Current Time =', current_time)
  task_completed()
  flag = False
  register_vm_address()

def task_completed():
  """Notify the master server after task is completed.
  """
  req = requests.get(master_server+str('/success'), data=request_id)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
  """
    This function receives files from master server.
    And executes some task to make the VM busy.
  """
  global flag
  global request_id
  input_file = request.files['task_request']
  req = request.files['request_id'].read()
  req = req.decode('utf-8')
  request_id = req
  flag = True
  t = threading.Thread(target=task_done)
  t.start()
  return 'success'

@app.route('/active', methods=['GET', 'POST'])
def f():
  """Master can check here if VM is active or not.
  """
  return {'hello': 'world'}

@app.route('/status', methods=['GET', 'POST'])
def g():
  """returns the state of VM
  """
  return {'status': flag}

def register_vm_address():
  """This functions tells the master server that VM is healhty.
  """
  data = 'http://127.0.0.1:'+str(sys.argv[1])
  try:
    req = requests.get(master_server+str('/register'), data=data)
  except:
    print('can''t connect to master server')

def pre_task():
  """This function performs tasks before the start of flask server.
  """
  if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "INPUT_PORT")
    sys.exit(-1)
  vm_address = 'http://127.0.0.1:' + sys.argv[1]
  register_vm_address()

if __name__ == '__main__':
  app.run()
