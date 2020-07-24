"""This script works on the asssumption of a certain directory structure.
     It then acts the master server and load balances the incoming
     requests.
     A database is created to store the incoming requests from user.
"""
import argparse
import os
import requests
from flask import Flask
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time
import threading
import Request_pb2

class MyFlaskApp(Flask):
  """This class configures the flask APP and executes function
    pre_task before starting flask server.

  """
  def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
    if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
      with self.app_context():
        pre_tasks()
    super(MyFlaskApp, self).run(
        host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)

APP = MyFlaskApp(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)

working_vm_address_list = []
available_vm_address_list = []
parser = argparse.ArgumentParser()

parser.add_argument('-d', '--debug_mode', help='debugging mode')
args = parser.parse_args()

class Newrequestentry(DB.Model):
  """This class creates a table Newrequestentry
    init function in this class inserts a new row
    the table.
  """
  request_id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
  request_proto_file = DB.Column(DB.BLOB)
  response_proto_file = DB.Column(DB.BLOB)
  request_status = DB.Column(DB.String(50))
  last_vm_assigned = DB.Column(DB.String(100))
  number_of_retries_allowed = DB.Column(DB.Integer)
  number_of_retries_till_now = DB.Column(DB.Integer)
  datetime_of_accepting_request = DB.Column(DB.DateTime, default=datetime.now())

  def __init__(
      self, request_proto_file, request_status, last_vm_assigned,
      number_of_retries_allowed, number_of_retries_till_now):
    self.request_proto_file = request_proto_file
    self.request_status = request_status
    self.last_vm_assigned = last_vm_assigned
    self.number_of_retries_allowed = number_of_retries_allowed
    self.number_of_retries_till_now = number_of_retries_till_now

def create_new_request(
    request_proto_file, request_status, last_vm_assigned,
    number_of_retries_allowed, number_of_retries_till_now):
  """This function adds a new row to database."""
  dessert = Newrequestentry(
      request_proto_file, request_status, last_vm_assigned,
      number_of_retries_allowed, number_of_retries_till_now)
  DB.session.add(dessert)
  DB.session.commit()
  return dessert

def get_request_status_row(request_id):
#  Get status of previous request.
  get_row_data = Newrequestentry.query.get(request_id)
  return get_row_data

def change_state(request_id, input_file):
  """Change request_status of a request."""
  Newrequestentry.query.filter_by(request_id=request_id).\
  update({Newrequestentry.response_proto_file: input_file})
  DB.session.commit()

def change_state_again(request_id, last_vm_assigned,
      number_of_retries_till_now):
  """Change request_status of a request."""
  Newrequestentry.query.filter_by(request_id=request_id).\
  update({Newrequestentry.last_vm_assigned: last_vm_assigned, Newrequestentry.\
      number_of_retries_till_now: number_of_retries_till_now})
  DB.session.commit()

@APP.route('/', methods=['GET', 'POST'])
def hello_world():
  return(' You have reached master server \n')

@APP.route('/register', methods=['GET', 'POST'])
def add_vm_address():
  """Add a VM to working_vm_address_list list."""
  address = request.data.decode('utf-8')
  if address not in working_vm_address_list:
    working_vm_address_list.append(address)
  return {'message': 'success'}

@APP.route('/upload')
def upload_file_webpage():
  """Serve web page"""
  return render_template('upload.html')

@APP.route('/assign_task', methods=['GET', 'POST'])
def upload_file():
  """Accept proto file from user and
     assign it to VM.
  """
  task_status_response = Request_pb2.TaskStatusResponse()
  file_ = request.files['file']
  read = file_.read()
  vm_address = find_working_vm()
  if vm_address == 'NOT':
    task_status_response.status = Request_pb2.TaskStatusResponse.REJECTED
    if args.debug_mode == 'b':
      return task_status_response.SerializeToString()
    else:
      return str(task_status_response)
  else:
    try:
      working_vm_address_list.remove(vm_address)
      task_request = Request_pb2.TaskRequest()
      task_request.ParseFromString(read)
      requ = create_new_request(
          read, 'accepted', vm_address, task_request. number_of_retries, 0)
      task_request.request_id = requ.request_id
      response = requests.post(url=vm_address + '/assign_task', files={'task_request':
          task_request.SerializeToString()})
      task_status_response.ParseFromString(response.content)
      process = threading.Thread(target= retry_after_timeout, args= (task_request.request_id,
          task_request.timeout, task_request.number_of_retries))
      process.start()
      if args.debug_mode == 'b':
        return task_status_response.SerializeToString()
      else:
        return str(task_status_response)
    except Exception as e:
      task_status_response.status = Request_pb2.TaskStatusResponse.REJECTED
      print(e)
      if args.debug_mode == 'b':
        return task_status_response.SerializeToString()
      else:
        return str(task_status_response)

def retry_after_timeout(request_id, timeout, number_of_retries):
  """Retry to check job status after timeout."""
  timer = timeout * (number_of_retries + 4)
  time.sleep(timer)
  task_status_response = Request_pb2.TaskStatusResponse()
  request_row = get_request_status_row(request_id)
  if request_row.response_proto_file is None:
    retry_again(request_id, True)
  else:
    task_status_response.ParseFromString(request_row.response_proto_file)
    if task_status_response.task_response.status == Request_pb2.TaskResponse.FAILURE:
      retry_again(request_id, True)

@APP.route('/get_status',methods=['GET', 'POST'])
def get_status():
  """Check status of a request."""
  task_status_request = Request_pb2.TaskStatusRequest()
  task_status_request.ParseFromString(request.files['file'].read())
  return status_of_request(task_status_request.request_id)

@APP.route('/vm_status', methods=['GET', 'POST'])
def vm_status():
  """Return VM address which are active."""
  return str(working_vm_address_list)

@APP.route('/success', methods=['GET', 'POST'])
def task_completed():
  """Receive response protocol buffer file from vm_server."""
  input_file = request.files['task_response']
  req = request.files['request_id'].read()
  task_status_response = Request_pb2.TaskStatusResponse()
  task_status_response.ParseFromString(input_file.read())
  request_id = int(req.decode('utf-8'))
  change_state(int(request_id), task_status_response.SerializeToString())
  if task_status_response.task_response.status == Request_pb2.TaskResponse.FAILURE:
    time.sleep(1)
    result = retry_again(request_id, False)
  return 'success'

@APP.route('/request_status', methods=['GET', 'POST'])
def request_status():
  """Check status of a request"""
  req_id = request.form['request_id']
  return status_of_request(req_id)

def status_of_request(req_id):
  """Check status of a request."""
  request_row = get_request_status_row(req_id)
  if request_row is None:
    task_status_response = Request_pb2.TaskStatusResponse()
    task_status_response.status = Request_pb2.TaskStatusResponse.INVALID_ID
    if args.debug_mode == 'b':
      return task_status_response.SerializeToString()
    else:
      return str(task_status_response)
  else:
    a = request_row.response_proto_file
    if a is None:
      task_status_response = Request_pb2.TaskStatusResponse()
      task_status_response.status = Request_pb2.TaskStatusResponse.ACCEPTED
      if args.debug_mode == 'b':
        return task_status_response.SerializeToString()
      else:
        return str(task_status_response)
    else:
      task_status_response = Request_pb2.TaskStatusResponse()
      task_status_response.ParseFromString(request_row.response_proto_file)
      task_status_response.status = Request_pb2.TaskStatusResponse.COMPLETED
      if args.debug_mode == 'b':
        return task_status_response.SerializeToString()
      else:
        return str(task_status_response)

def retry_again(request_id, flag):
  """Retry again,if request fails."""
  request_row = get_request_status_row(request_id)  
  if request_row.number_of_retries_allowed > request_row.number_of_retries_till_now or flag:
    vm_address = find_working_vm()
    if vm_address == 'NOT':
      return 'try again later'
    else:
      try:
        task_request = Request_pb2.TaskRequest()
        task_request.ParseFromString(request_row.request_proto_file)
        task_request.request_id = request_id
        working_vm_address_list.remove(vm_address)
        response = requests.post(url=vm_address + '/assign_task', files={'task_request':
             task_request.SerializeToString()})
        change_state_again(request_id, vm_address, request_row.number_of_retries_till_now + 1)
        return 'success'
      except Exception as e:
        print(e)
        return 'try again later'

def is_healthy(node):
  """Check given VM is healthy or not.
     Args:
       node:
  """
  try:
    req = requests.get(node + str('/active'))
    return True
  except:
    return False

def is_engaged(node):
  """Check whether given VM is engaged in any
     task or not.
     Args:
       node:
  """
  if is_healthy(node):
    try:
      req = requests.get(node + str('/status'))
      status = req.json()
      return bool(status['status'])
    except:
      return False
  return False

def find_working_vm():
  """Find working VM address."""
  for address in working_vm_address_list:
    if not is_engaged(address):
      return address
  return 'NOT'

def get_working_vm_address():
  """Append IP addresses of working VMs to a list."""
  for address in available_vm_address_list:
    if is_healthy(address) and not is_engaged(address):
      working_vm_address_list.append(address)

def get_available_vm_address():
  """Append IP addresses of available VMs to a list.
     It assumes IP addresses are present in a text file.
  """
  try:
    with open('listfile.txt', 'r') as filehandle:
      for line in filehandle:
        new_address = line[:-1]
        available_vm_address_list.append(new_address)
    with open('listfile.txt', 'w') as filehandle:
      print('\n')
  except:
    print(' ')

def pre_tasks():
  """Tasks to do before flask server starts."""
  DB.create_all()
  get_available_vm_address()
  get_working_vm_address()

if __name__ == '__main__':
  APP.run()
